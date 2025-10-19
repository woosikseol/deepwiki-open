"""
LLM 기반 Mermaid 다이어그램 검증 모듈

실제 Mermaid 렌더링을 통해 구문 오류를 감지하고, LLM을 사용하여 수정합니다.
다중 검증 및 재시도 로직을 포함하여 구문 오류를 완벽히 제거합니다.
"""

import logging
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Tuple, List, Optional
import google.generativeai as genai

from config import GEMINI_API_KEY, GEMINI_MODEL

logger = logging.getLogger(__name__)


class LLMMermaidValidator:
    """LLM 기반 Mermaid 다이어그램 구문 검증 및 수정 클래스 (실제 렌더링 기반)"""
    
    def __init__(self, api_key: str = None, model_name: str = None, max_iterations: int = 5):
        """
        Args:
            api_key: Gemini API 키 (None이면 환경변수에서 가져옴)
            model_name: 모델 이름 (기본값: config의 GEMINI_MODEL)
            max_iterations: 최대 검증 반복 횟수
        """
        self.api_key = api_key or GEMINI_API_KEY
        self.model_name = model_name or GEMINI_MODEL
        self.max_iterations = max_iterations
        self.mermaid_cli_available = self._check_mermaid_cli()
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다.")
        
        # Gemini API 설정
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        
        logger.info(f"LLM Mermaid Validator 초기화 완료: {self.model_name} (최대 {max_iterations}회 반복)")
        if self.mermaid_cli_available:
            logger.info("Mermaid CLI 사용 가능 - 실제 렌더링 기반 검증 활성화")
        else:
            logger.warning("Mermaid CLI 없음 - 기본 검증 모드로 동작")
    
    def _check_mermaid_cli(self) -> bool:
        """Mermaid CLI가 설치되어 있는지 확인"""
        try:
            result = subprocess.run(
                ['mmdc', '--version'], 
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def _analyze_parse_error(self, error_message: str) -> str:
        """Parse error를 분석하여 가능한 원인을 제시"""
        analysis = []
        
        # 라인 번호 추출
        if "line" in error_message.lower():
            import re
            line_match = re.search(r'line (\d+)', error_message, re.IGNORECASE)
            if line_match:
                line_num = line_match.group(1)
                analysis.append(f"- Error occurs at line {line_num}")
        
        # 괄호 관련 오류
        if "(" in error_message or ")" in error_message:
            analysis.append("- **LIKELY CAUSE**: Parentheses () in node label without quotes")
            analysis.append("- **FIX**: Wrap the label in quotes: [Text (info)] → [\"Text (info)\"]")
        
        # expecting 오류 분석
        if "Expecting" in error_message:
            analysis.append("- Parse error: Mermaid parser expected different syntax")
            analysis.append("- This usually means a node label has special characters without quotes")
        
        # got 'PS' 오류 (괄호 시작)
        if "got 'PS'" in error_message:
            analysis.append("- **CRITICAL**: Parser encountered '(' which should be inside quotes")
            analysis.append("- **ACTION**: Find all [Text (something)] and change to [\"Text (something)\"]")
        
        if not analysis:
            analysis.append("- Generic parse error - likely special characters need quoting")
        
        return "\n".join(analysis)
    
    def extract_mermaid_blocks(self, content: str) -> List[Tuple[int, str]]:
        """
        Markdown 내용에서 Mermaid 코드 블록을 추출
        
        Args:
            content: Markdown 내용
            
        Returns:
            List[Tuple[int, str]]: (시작 라인 번호, Mermaid 코드) 튜플 리스트
        """
        pattern = r'```mermaid\n(.*?)\n```'
        matches = []
        
        for match in re.finditer(pattern, content, re.DOTALL):
            start_line = content[:match.start()].count('\n') + 1
            mermaid_code = match.group(1)
            matches.append((start_line, mermaid_code))
        
        return matches
    
    def render_mermaid(self, mermaid_code: str) -> Tuple[bool, Optional[str]]:
        """
        실제로 Mermaid 코드를 렌더링하여 오류 확인
        
        Args:
            mermaid_code: Mermaid 코드
            
        Returns:
            Tuple[bool, Optional[str]]: (성공 여부, 오류 메시지)
        """
        if not self.mermaid_cli_available:
            return True, None  # CLI가 없으면 검증 건너뛰기
        
        try:
            # 임시 파일 생성
            with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as f:
                f.write(mermaid_code)
                temp_input = f.name
            
            # 임시 출력 파일 경로
            temp_output = temp_input.replace('.mmd', '.svg')
            
            # Mermaid CLI로 렌더링 시도
            result = subprocess.run(
                ['mmdc', '-i', temp_input, '-o', temp_output],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # 파일 정리
            Path(temp_input).unlink(missing_ok=True)
            Path(temp_output).unlink(missing_ok=True)
            
            if result.returncode == 0:
                return True, None
            else:
                # 실제 오류 메시지 반환
                error_message = result.stderr.strip() or result.stdout.strip()
                return False, error_message
                
        except subprocess.TimeoutExpired:
            Path(temp_input).unlink(missing_ok=True)
            Path(temp_output).unlink(missing_ok=True)
            return False, "Rendering timeout - code may be too complex or have infinite loops"
        except Exception as e:
            return False, f"Rendering error: {str(e)}"
    
    def validate_and_fix_mermaid(self, mermaid_code: str) -> Tuple[str, bool, str]:
        """
        실제 렌더링을 통해 Mermaid 구문을 검증하고 LLM으로 수정 (강화된 재시도)
        
        Args:
            mermaid_code: 원본 Mermaid 코드
            
        Returns:
            Tuple[str, bool, str]: (수정된 코드, 수정 여부, 메시지)
        """
        current_code = mermaid_code
        was_ever_modified = False
        previous_errors = []  # 이전 오류들을 추적
        
        for iteration in range(self.max_iterations):
            # 1. 실제 렌더링으로 오류 확인
            is_valid, error_message = self.render_mermaid(current_code)
            
            if is_valid:
                # 렌더링 성공 - 검증 완료
                if iteration > 0:
                    logger.info(f"✓ 검증 완료: {iteration}회 반복 후 렌더링 성공")
                else:
                    logger.info("✓ 코드가 이미 유효함 - 렌더링 성공")
                
                if was_ever_modified:
                    return current_code, True, f"Fixed after {iteration} iteration(s)"
                else:
                    return current_code, False, "Code is valid"
            
            # 2. 렌더링 실패 - 실제 오류 메시지와 함께 LLM에 수정 요청
            logger.info(f"렌더링 실패 ({iteration + 1}회차)")
            if error_message:
                # 더 자세한 오류 정보 출력
                logger.info(f"오류 상세: {error_message[:300]}")
                previous_errors.append(error_message)
            
            # 3. LLM을 통한 수정 (이전 시도 정보 포함)
            fixed_code = self._call_llm_to_fix_with_error(
                current_code, 
                error_message,
                previous_attempts=iteration,
                previous_errors=previous_errors
            )
            
            if fixed_code.strip() == current_code.strip():
                # LLM이 코드를 변경하지 않음 - 다른 전략 시도
                logger.warning(f"LLM이 코드를 변경하지 않음 (반복 {iteration + 1}회)")
                
                # 마지막 시도가 아니면 계속 진행
                if iteration < self.max_iterations - 1:
                    logger.info("다른 수정 전략으로 재시도...")
                    continue
                else:
                    if was_ever_modified:
                        return current_code, True, f"Partially fixed after {iteration + 1} iteration(s)"
                    else:
                        return current_code, False, f"Could not fix: {error_message}"
            
            # 코드가 변경됨
            current_code = fixed_code
            was_ever_modified = True
            logger.info(f"✓ {iteration + 1}회차 수정 완료 - 재검증 시작")
        
        # 최대 반복 횟수 도달
        logger.warning(f"최대 반복 횟수 도달 ({self.max_iterations}회)")
        if was_ever_modified:
            return current_code, True, f"Partially fixed after {self.max_iterations} iterations"
        else:
            return mermaid_code, False, "Could not fix within iteration limit"
    
    def _call_llm_to_fix_with_error(
        self, 
        mermaid_code: str, 
        error_message: Optional[str] = None,
        previous_attempts: int = 0,
        previous_errors: List[str] = None
    ) -> str:
        """
        실제 렌더링 오류 메시지와 함께 LLM을 호출하여 Mermaid 코드 수정 (강화된 프롬프트)
        
        Args:
            mermaid_code: 수정할 Mermaid 코드
            error_message: 실제 렌더링 오류 메시지
            previous_attempts: 이전 시도 횟수
            previous_errors: 이전 오류 목록
            
        Returns:
            str: 수정된 Mermaid 코드
        """
        error_context = ""
        if error_message:
            # Parse error 상세 분석
            error_analysis = self._analyze_parse_error(error_message)
            
            error_context = f"""
<actual_rendering_error>
The Mermaid CLI returned the following PARSE ERROR when trying to render:

ERROR MESSAGE:
{error_message}

ANALYSIS:
{error_analysis}

This is attempt #{previous_attempts + 1}. Previous attempts failed with similar errors.
You MUST fix this specific parse error completely.
</actual_rendering_error>
"""
        
        # 이전 시도 정보 추가
        retry_context = ""
        if previous_attempts > 0:
            retry_context = f"""
<previous_attempts>
This is retry attempt #{previous_attempts + 1}. Previous fixes did not work.
You must try a DIFFERENT approach this time. Be more aggressive with adding quotes.
</previous_attempts>
"""
        
        prompt = f"""You are a Mermaid diagram syntax expert and validator.

<task>
Fix the following Mermaid diagram code. The code FAILED TO RENDER with a parse error.
</task>
{error_context}{retry_context}
<original_code>
```mermaid
{mermaid_code}
```
</original_code>

<fixing_instructions>
1. **CRITICAL**: Parse errors are usually caused by:
   - Parentheses () inside node labels WITHOUT quotes
   - Example: A[Text (something)] ❌ WRONG
   - Fix: A["Text (something)"] ✅ CORRECT
   
2. **ALWAYS wrap these in quotes**:
   - Any text with parentheses: [Text (info)] → ["Text (info)"]
   - Any text with slashes: [path/file] → ["path/file"]
   - Any Korean text: [한글] → ["한글"]
   - Any text with special chars: [Text: value] → ["Text: value"]

3. Find the problematic line in the error message and fix it

4. When in doubt, ADD QUOTES - it's safer

5. Common patterns to fix:
   - [설정 로드 (config.py)] → ["설정 로드 (config.py)"]
   - [캐시 디렉토리 (.adalflow)] → ["캐시 디렉토리 (.adalflow)"]
   - [LLM 호출 (Gemini API)] → ["LLM 호출 (Gemini API)"]
</fixing_instructions>

<critical_rules>
- **WRAP ALL LABELS WITH PARENTHESES IN QUOTES**: [Text (info)] → ["Text (info)"]
- **WRAP ALL KOREAN TEXT IN QUOTES**: [한글] → ["한글"]
- **WRAP ALL TEXT WITH SPECIAL CHARACTERS IN QUOTES**
- NEVER use reserved keywords as node IDs
- Use clean arrow syntax: --> or -- "label" -->
- Remove all semicolons and comments
- When unsure, ADD QUOTES to node labels
</critical_rules>

<output_format>
Return ONLY the fixed Mermaid code.
- Do NOT include ```mermaid fences
- Do NOT include any explanations or comments
- Do NOT add extra newlines at start or end
- Just return the clean, working Mermaid syntax
- Make sure EVERY label with parentheses has quotes
</output_format>

Fixed Mermaid code:"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.0,
                    max_output_tokens=4096
                )
            )
            
            if not response or not response.text:
                logger.warning("Empty response from LLM")
                return mermaid_code
            
            fixed_code = response.text.strip()
            
            # Remove markdown fences if LLM added them
            fixed_code = re.sub(r'^```mermaid\s*\n?', '', fixed_code)
            fixed_code = re.sub(r'\n?```\s*$', '', fixed_code)
            fixed_code = fixed_code.strip()
            
            return fixed_code
            
        except Exception as e:
            logger.error(f"Error during LLM call: {e}")
            return mermaid_code
    
    def _call_llm_to_fix(self, mermaid_code: str, known_errors: List[str] = None) -> str:
        """
        LLM을 호출하여 Mermaid 코드 수정
        
        Args:
            mermaid_code: 수정할 Mermaid 코드
            known_errors: 알려진 오류 목록 (옵션)
            
        Returns:
            str: 수정된 Mermaid 코드
        """
        error_context = ""
        if known_errors:
            error_context = f"\n<detected_errors>\nThe following errors were detected:\n" + "\n".join(f"- {err}" for err in known_errors) + "\n</detected_errors>\n"
        
        prompt = f"""You are a Mermaid diagram syntax expert and validator.

<task>
Analyze and fix the following Mermaid diagram code. The code may contain syntax errors that prevent it from rendering correctly.
</task>
{error_context}
<original_code>
```mermaid
{mermaid_code}
```
</original_code>

<common_errors_to_fix>
1. **Comments**: Remove all comments (lines starting with // or %%) as they are NOT valid in Mermaid
2. **Node Labels with Special Characters**: 
   - Labels containing special characters like --, //, =>, etc. MUST be wrapped in quotes
   - Example: B["This -- is valid"] not B[This -- is invalid]
3. **Link/Edge Syntax**:
   - Use --> for arrows (not -- alone or -- -->)
   - Link labels must be in quotes: A -- "label text" --> B
   - No spaces in arrow syntax: A-->B or A --> B (not A - -> B)
4. **Korean/Unicode Characters in Labels**:
   - ALL labels with Korean text MUST be wrapped in quotes
   - Example: A["한글 텍스트"] not A[한글 텍스트]
5. **Semicolons**: Remove all semicolons (;) - they are optional and can cause errors
6. **Node IDs - CRITICAL**: 
   - NEVER use Mermaid reserved keywords as node IDs: end, graph, subgraph, style, class, click, etc.
   - If you need to use "end" as a node, use a different ID like: endNode, finish, done, complete
   - Example: endNode(("종료")) not end(("종료"))
   - Node IDs should be simple alphanumeric (A, B, C1, NodeName, startNode, endNode)
7. **Brackets Balance**: Ensure all brackets [], (), {{}} are properly balanced
8. **Subgraph Syntax**: Use proper subgraph syntax with 'end' keyword for closing subgraphs only
</common_errors_to_fix>

<critical_rules>
- NO inline comments (// or %%)
- ALL labels with special characters or Korean text MUST use quotes
- Use clean arrow syntax: --> or -- "label" -->
- Remove all semicolons
- NEVER use reserved keywords (end, graph, subgraph, style, class, click) as node IDs
- Keep node structure simple and clear
- Preserve the diagram type (graph, flowchart, etc.)
- Maintain the logical flow and meaning
</critical_rules>

<output_format>
Return ONLY the fixed Mermaid code.
- Do NOT include ```mermaid fences
- Do NOT include any explanations or comments
- Do NOT add extra newlines at start or end
- Just return the clean, working Mermaid syntax
</output_format>

Fixed Mermaid code:"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.0,  # Temperature 0 for maximum consistency
                    max_output_tokens=4096
                )
            )
            
            if not response or not response.text:
                logger.warning("Empty response from LLM")
                return mermaid_code
            
            fixed_code = response.text.strip()
            
            # Remove markdown fences if LLM added them despite instructions
            fixed_code = re.sub(r'^```mermaid\s*\n?', '', fixed_code)
            fixed_code = re.sub(r'\n?```\s*$', '', fixed_code)
            fixed_code = fixed_code.strip()
            
            return fixed_code
            
        except Exception as e:
            logger.error(f"Error during LLM call: {e}")
            return mermaid_code
    
    def validate_markdown_content(self, content: str) -> Tuple[str, int, int]:
        """
        Markdown 내용의 모든 Mermaid 블록을 검증하고 수정
        
        Args:
            content: Markdown 내용
            
        Returns:
            Tuple[str, int, int]: (수정된 내용, 검증된 블록 수, 수정된 블록 수)
        """
        mermaid_blocks = self.extract_mermaid_blocks(content)
        
        if not mermaid_blocks:
            logger.info("No Mermaid blocks found in content")
            return content, 0, 0
        
        logger.info(f"Found {len(mermaid_blocks)} Mermaid blocks to validate")
        
        validated_count = 0
        fixed_count = 0
        
        # Sort blocks by position (reverse order to maintain positions during replacement)
        sorted_blocks = sorted(mermaid_blocks, key=lambda x: x[0], reverse=True)
        
        # Process each block
        modified_content = content
        for start_line, mermaid_code in sorted_blocks:
            validated_count += 1
            
            logger.info(f"Validating Mermaid block {validated_count}/{len(mermaid_blocks)} (line {start_line})...")
            
            # Validate and fix
            fixed_code, was_fixed, message = self.validate_and_fix_mermaid(mermaid_code)
            
            if was_fixed:
                fixed_count += 1
                # Replace in content
                old_block = f"```mermaid\n{mermaid_code}\n```"
                new_block = f"```mermaid\n{fixed_code}\n```"
                
                # Find and replace the specific occurrence
                # Use a more precise replacement to avoid replacing similar blocks
                pattern = re.escape(old_block)
                modified_content = re.sub(pattern, new_block, modified_content, count=1)
                
                logger.info(f"✓ Fixed Mermaid block at line {start_line}")
            else:
                logger.info(f"✓ Mermaid block at line {start_line} is valid")
        
        logger.info(f"Validation complete: {validated_count} blocks checked, {fixed_count} blocks fixed")
        return modified_content, validated_count, fixed_count


def validate_mermaid_in_file(file_path: str) -> Tuple[bool, int, int]:
    """
    파일의 Mermaid 다이어그램을 검증하고 수정
    
    Args:
        file_path: Markdown 파일 경로
        
    Returns:
        Tuple[bool, int, int]: (수정 여부, 검증된 블록 수, 수정된 블록 수)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        validator = LLMMermaidValidator()
        modified_content, validated_count, fixed_count = validator.validate_markdown_content(original_content)
        
        if fixed_count > 0:
            # Write back modified content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            logger.info(f"Updated file: {file_path} ({fixed_count} blocks fixed)")
            return True, validated_count, fixed_count
        else:
            logger.info(f"No changes needed for: {file_path}")
            return False, validated_count, fixed_count
            
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")
        return False, 0, 0

