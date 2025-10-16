"""
LLM 기반 Mermaid 다이어그램 검증 모듈

기존의 규칙 기반 MermaidValidator 대신 LLM을 사용하여 Mermaid 구문을 검증하고 수정합니다.
다중 검증 및 재시도 로직을 포함하여 구문 오류를 완벽히 제거합니다.
"""

import logging
import re
from typing import Tuple, List
import google.generativeai as genai

from config import GEMINI_API_KEY, GEMINI_MODEL

logger = logging.getLogger(__name__)

# Mermaid 예약어 목록 (노드 ID로 사용 불가)
MERMAID_RESERVED_KEYWORDS = {
    'end', 'graph', 'subgraph', 'style', 'class', 'click', 
    'classDef', 'linkStyle', 'interpolate', 'default',
    'TB', 'BT', 'RL', 'LR', 'TD'
}


class LLMMermaidValidator:
    """LLM 기반 Mermaid 다이어그램 구문 검증 및 수정 클래스 (다중 검증 및 재시도 포함)"""
    
    def __init__(self, api_key: str = None, model_name: str = None, max_iterations: int = 3):
        """
        Args:
            api_key: Gemini API 키 (None이면 환경변수에서 가져옴)
            model_name: 모델 이름 (기본값: config의 GEMINI_MODEL)
            max_iterations: 최대 검증 반복 횟수
        """
        self.api_key = api_key or GEMINI_API_KEY
        self.model_name = model_name or GEMINI_MODEL
        self.max_iterations = max_iterations
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다.")
        
        # Gemini API 설정
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        
        logger.info(f"LLM Mermaid Validator 초기화 완료: {self.model_name} (최대 {max_iterations}회 반복)")
    
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
    
    def check_syntax_errors(self, mermaid_code: str) -> List[str]:
        """
        규칙 기반으로 Mermaid 코드의 구문 오류를 검사
        
        Args:
            mermaid_code: Mermaid 코드
            
        Returns:
            List[str]: 발견된 오류 목록
        """
        errors = []
        
        # 1. 예약어를 노드 ID로 사용했는지 확인
        # 패턴: 노드ID(label) 또는 노드ID[label] 또는 노드ID{label} 등
        node_pattern = r'\b(\w+)(?:\[|\(|\{)'
        for match in re.finditer(node_pattern, mermaid_code):
            node_id = match.group(1)
            if node_id in MERMAID_RESERVED_KEYWORDS:
                errors.append(f"Reserved keyword used as node ID: '{node_id}'")
        
        # 2. 화살표 앞에 예약어가 있는지 확인
        arrow_pattern = r'\b(\w+)\s*(?:-->|---)'
        for match in re.finditer(arrow_pattern, mermaid_code):
            node_id = match.group(1)
            if node_id in MERMAID_RESERVED_KEYWORDS:
                errors.append(f"Reserved keyword used before arrow: '{node_id}'")
        
        # 3. 주석이 있는지 확인
        if '//' in mermaid_code or mermaid_code.strip().startswith('%%'):
            errors.append("Comments found (// or %%)")
        
        # 4. 세미콜론이 있는지 확인
        if ';' in mermaid_code:
            errors.append("Semicolons found")
        
        # 5. 한글이 따옴표 없이 사용되었는지 확인 (간단한 체크)
        korean_pattern = r'\[([^"]*[\uac00-\ud7a3]+[^"]*)\]'
        for match in re.finditer(korean_pattern, mermaid_code):
            text = match.group(1)
            if '"' not in text:
                errors.append(f"Korean text without quotes: '{text}'")
        
        return errors
    
    def validate_and_fix_mermaid(self, mermaid_code: str) -> Tuple[str, bool, str]:
        """
        LLM을 사용하여 Mermaid 구문을 검증하고 수정 (다중 반복)
        
        Args:
            mermaid_code: 원본 Mermaid 코드
            
        Returns:
            Tuple[str, bool, str]: (수정된 코드, 수정 여부, 메시지)
        """
        current_code = mermaid_code
        was_ever_modified = False
        
        for iteration in range(self.max_iterations):
            # 1. 규칙 기반 검사로 먼저 오류 확인
            errors = self.check_syntax_errors(current_code)
            
            if not errors and iteration > 0:
                # 규칙 기반 검사에서 오류가 없고, 이미 한 번 이상 수정했다면 종료
                logger.info(f"✓ 검증 완료: {iteration}회 반복 후 오류 없음")
                break
            
            if errors:
                logger.info(f"발견된 오류 ({iteration + 1}회차): {', '.join(errors[:3])}")
            
            # 2. LLM을 통한 수정
            fixed_code = self._call_llm_to_fix(current_code, errors)
            
            if fixed_code.strip() == current_code.strip():
                # 더 이상 변경사항이 없으면 종료
                if iteration == 0:
                    logger.info("코드가 이미 유효함")
                    return current_code, False, "Code is valid"
                else:
                    break
            
            # 코드가 변경됨
            current_code = fixed_code
            was_ever_modified = True
            logger.info(f"✓ {iteration + 1}회차 수정 완료")
        
        if was_ever_modified:
            return current_code, True, f"Fixed after {iteration + 1} iteration(s)"
        else:
            return mermaid_code, False, "Code is valid"
    
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

