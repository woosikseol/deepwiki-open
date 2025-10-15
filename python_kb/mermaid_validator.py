"""
Mermaid 구문 검증 도구

이 모듈은 Markdown 파일의 Mermaid 다이어그램 구문을 검증하고 수정하는 기능을 제공합니다.
"""

import re
import subprocess
import tempfile
import logging
from pathlib import Path
from typing import List, Tuple, Dict, Any

logger = logging.getLogger(__name__)


class MermaidValidator:
    """Mermaid 다이어그램 구문 검증 및 수정 클래스"""
    
    def __init__(self):
        self.mermaid_cli_available = self._check_mermaid_cli()
    
    def _check_mermaid_cli(self) -> bool:
        """Mermaid CLI가 설치되어 있는지 확인"""
        try:
            result = subprocess.run(['mmdc', '--version'], 
                         capture_output=True, check=True)
            # Chrome 브라우저 의존성 문제로 인해 CLI 사용을 비활성화
            logger.info("Mermaid CLI가 설치되어 있지만 Chrome 의존성 문제로 인해 기본 구문 검사만 사용합니다.")
            return False
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("Mermaid CLI (mmdc)가 설치되지 않았습니다. 기본 구문 검사만 사용합니다.")
            return False
    
    def extract_mermaid_blocks(self, content: str) -> List[Tuple[int, str]]:
        """Markdown 내용에서 Mermaid 코드 블록을 추출"""
        pattern = r'```mermaid\n(.*?)\n```'
        matches = []
        
        for match in re.finditer(pattern, content, re.DOTALL):
            start_line = content[:match.start()].count('\n') + 1
            mermaid_code = match.group(1)
            matches.append((start_line, mermaid_code))
        
        return matches
    
    def validate_mermaid_syntax(self, mermaid_code: str) -> Tuple[bool, str]:
        """Mermaid 구문을 검증하고 오류 메시지를 반환"""
        if not self.mermaid_cli_available:
            # CLI가 없으면 기본적인 구문 검사만 수행
            return self._basic_syntax_check(mermaid_code)
        
        try:
            # 임시 파일 생성
            with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as f:
                f.write(mermaid_code)
                temp_file = f.name
            
            # Mermaid CLI로 구문 검증 (임시 SVG 파일로 출력)
            temp_output = temp_file.replace('.mmd', '.svg')
            result = subprocess.run(
                ['mmdc', '-i', temp_file, '-o', temp_output, '--quiet'],
                capture_output=True,
                text=True
            )
            
            # 임시 출력 파일 삭제
            if Path(temp_output).exists():
                Path(temp_output).unlink()
            
            # 임시 파일 삭제
            Path(temp_file).unlink()
            
            if result.returncode == 0:
                return True, "구문이 올바릅니다"
            else:
                return False, result.stderr
                
        except Exception as e:
            return False, f"검증 중 오류 발생: {str(e)}"
    
    def _basic_syntax_check(self, mermaid_code: str) -> Tuple[bool, str]:
        """기본적인 Mermaid 구문 검사 (CLI 없이)"""
        errors = []
        
        # 주석 검사
        if re.search(r'%.*$', mermaid_code, re.MULTILINE):
            errors.append("Mermaid에서는 % 주석을 사용할 수 없습니다")
        
        # 세미콜론 누락 검사
        lines = mermaid_code.split('\n')
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.startswith('subgraph') and not line.endswith(';') and not line.endswith('{') and not line.endswith('}'):
                if '-->' in line or '--' in line:
                    errors.append(f"라인 {i}: 연결 구문이 세미콜론으로 끝나지 않았습니다")
        
        # 노드 정의 오류 검사 (예: B --> C;{File Discovery})
        if re.search(r';\s*\{[^}]*\}', mermaid_code):
            errors.append("노드 정의와 연결 구문이 잘못 결합되었습니다")
        
        # 중괄호 위치 오류 검사
        if re.search(r'-->\s*\{[^}]*\}', mermaid_code):
            errors.append("연결 구문과 노드 정의 사이에 세미콜론이 누락되었습니다")
        
        if errors:
            return False, "; ".join(errors)
        return True, "기본 구문 검사 통과"
    
    def fix_common_mermaid_errors(self, mermaid_code: str) -> str:
        """일반적인 Mermaid 구문 오류를 자동으로 수정"""
        
        # 주석 제거
        mermaid_code = re.sub(r'%.*$', '', mermaid_code, flags=re.MULTILINE)
        
        # 노드 정의와 연결 구문 분리 (예: B --> C;{File Discovery} -> B --> C; C{File Discovery})
        mermaid_code = re.sub(r'(\w+)\s*-->\s*(\w+);\s*\{([^}]*)\}', r'\1 --> \2;\n    \2{\3}', mermaid_code)
        
        # 연결 구문과 노드 정의 사이 세미콜론 추가 (예: B --> C{File Discovery} -> B --> C; C{File Discovery})
        mermaid_code = re.sub(r'(\w+)\s*-->\s*(\w+)\s*\{([^}]*)\}', r'\1 --> \2;\n    \2{\3}', mermaid_code)
        
        # 더 복잡한 패턴 처리 (예: A --> B;{C} -> A --> B; B{C})
        mermaid_code = re.sub(r'(\w+)\s*-->\s*(\w+);\s*\{([^}]*)\}', r'\1 --> \2;\n    \2{\3}', mermaid_code)
        
        # 괄호와 중괄호가 섞인 패턴 처리
        mermaid_code = re.sub(r'(\w+)\s*-->\s*(\w+);\s*\(([^)]*)\);\s*\{([^}]*)\}', r'\1 --> \2;\n    \2(\3){\4}', mermaid_code)
        
        # 세미콜론 누락 수정 (연결 구문에만)
        mermaid_code = re.sub(r'(\w+)\s*-->\s*(\w+)(?!;)', r'\1 --> \2;', mermaid_code)
        mermaid_code = re.sub(r'(\w+)\s*--\s*([^-]+)\s*-->\s*(\w+)(?!;)', r'\1 -- \2 --> \3;', mermaid_code)
        
        # 중괄호 노드 정의 정리 (예: C{File Discovery} -> C{File Discovery})
        mermaid_code = re.sub(r'(\w+)\s*\{\s*([^}]*)\s*\}', r'\1{\2}', mermaid_code)
        
        # 빈 라인 정리
        mermaid_code = re.sub(r'\n\s*\n\s*\n', '\n\n', mermaid_code)
        
        # 라인 정리 및 들여쓰기
        lines = mermaid_code.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line:  # 빈 라인 제거
                # 노드 정의는 들여쓰기 추가
                if re.match(r'\w+\{[^}]*\}', line):
                    line = '    ' + line
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def validate_markdown_file(self, file_path: str) -> Dict[str, Any]:
        """Markdown 파일의 모든 Mermaid 다이어그램을 검증"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {'error': f"파일 읽기 오류: {str(e)}"}
        
        mermaid_blocks = self.extract_mermaid_blocks(content)
        results = {
            'file_path': file_path,
            'total_blocks': len(mermaid_blocks),
            'valid_blocks': 0,
            'invalid_blocks': 0,
            'blocks': {}
        }
        
        for i, (line_num, mermaid_code) in enumerate(mermaid_blocks):
            is_valid, message = self.validate_mermaid_syntax(mermaid_code)
            
            if is_valid:
                results['valid_blocks'] += 1
            else:
                results['invalid_blocks'] += 1
            
            results['blocks'][f"Block {i+1} (Line {line_num})"] = {
                'valid': is_valid,
                'message': message,
                'code_preview': mermaid_code[:100] + "..." if len(mermaid_code) > 100 else mermaid_code
            }
        
        return results
    
    def fix_markdown_file(self, file_path: str) -> bool:
        """Markdown 파일의 Mermaid 다이어그램 구문 오류를 자동 수정"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"파일 읽기 오류: {str(e)}")
            return False
        
        original_content = content
        mermaid_pattern = r'```mermaid\n(.*?)\n```'
        
        def fix_mermaid_block(match):
            mermaid_code = match.group(1)
            fixed_code = self.fix_common_mermaid_errors(mermaid_code)
            return f"```mermaid\n{fixed_code}\n```"
        
        # Mermaid 블록 수정
        fixed_content = re.sub(mermaid_pattern, fix_mermaid_block, content, flags=re.DOTALL)
        
        if original_content != fixed_content:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                logger.info(f"Mermaid 구문 오류가 수정되었습니다: {file_path}")
                return True
            except Exception as e:
                logger.error(f"파일 쓰기 오류: {str(e)}")
                return False
        
        return False
    
    def validate_directory(self, directory: str) -> Dict[str, Any]:
        """디렉토리의 모든 Markdown 파일에서 Mermaid 다이어그램을 검증"""
        directory_path = Path(directory)
        results = {
            'directory': str(directory_path),
            'total_files': 0,
            'files_with_mermaid': 0,
            'total_blocks': 0,
            'valid_blocks': 0,
            'invalid_blocks': 0,
            'file_results': {}
        }
        
        for md_file in directory_path.rglob("*.md"):
            results['total_files'] += 1
            
            file_result = self.validate_markdown_file(str(md_file))
            if 'error' in file_result:
                continue
            
            if file_result['total_blocks'] > 0:
                results['files_with_mermaid'] += 1
                results['total_blocks'] += file_result['total_blocks']
                results['valid_blocks'] += file_result['valid_blocks']
                results['invalid_blocks'] += file_result['invalid_blocks']
                results['file_results'][str(md_file)] = file_result
        
        return results


def main():
    """CLI 인터페이스"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Mermaid 구문 검증 도구')
    parser.add_argument('path', help='검증할 파일 또는 디렉토리 경로')
    parser.add_argument('--fix', action='store_true', help='구문 오류를 자동으로 수정')
    parser.add_argument('--verbose', '-v', action='store_true', help='상세한 출력')
    
    args = parser.parse_args()
    
    validator = MermaidValidator()
    path = Path(args.path)
    
    if path.is_file():
        if args.fix:
            success = validator.fix_markdown_file(str(path))
            if success:
                print(f"✅ {path} 파일의 Mermaid 구문 오류가 수정되었습니다")
            else:
                print(f"❌ {path} 파일 수정에 실패했습니다")
        else:
            result = validator.validate_markdown_file(str(path))
            if 'error' in result:
                print(f"❌ 오류: {result['error']}")
            else:
                print(f"📄 파일: {result['file_path']}")
                print(f"📊 총 블록: {result['total_blocks']}, 유효: {result['valid_blocks']}, 무효: {result['invalid_blocks']}")
                
                if args.verbose:
                    for block_name, block_info in result['blocks'].items():
                        status = "✅" if block_info['valid'] else "❌"
                        print(f"  {status} {block_name}: {block_info['message']}")
    
    elif path.is_dir():
        result = validator.validate_directory(str(path))
        print(f"📁 디렉토리: {result['directory']}")
        print(f"📄 총 파일: {result['total_files']}, Mermaid 포함: {result['files_with_mermaid']}")
        print(f"📊 총 블록: {result['total_blocks']}, 유효: {result['valid_blocks']}, 무효: {result['invalid_blocks']}")
        
        if args.verbose and result['file_results']:
            for file_path, file_result in result['file_results'].items():
                print(f"\n📄 {file_path}:")
                for block_name, block_info in file_result['blocks'].items():
                    status = "✅" if block_info['valid'] else "❌"
                    print(f"  {status} {block_name}: {block_info['message']}")
    
    else:
        print(f"❌ 경로를 찾을 수 없습니다: {path}")


if __name__ == "__main__":
    main()
