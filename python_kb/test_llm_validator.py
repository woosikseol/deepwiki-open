"""
LLM 기반 Mermaid 검증기 테스트 스크립트
"""

import logging
from llm_mermaid_validator import LLMMermaidValidator

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def test_invalid_mermaid():
    """잘못된 Mermaid 코드 테스트"""
    
    # 문제가 있는 Mermaid 코드 (주석, 잘못된 화살표 등)
    invalid_code = """graph TD
    A[Start] --> B  // Analysis results 
    B --> C[Process]
    C -- --no-cache, --force --> D[End]
    E[한글 텍스트] --> F
    G --> H;"""
    
    logger.info("=== 잘못된 Mermaid 코드 테스트 ===")
    logger.info(f"원본 코드:\n{invalid_code}\n")
    
    validator = LLMMermaidValidator()
    fixed_code, was_fixed, message = validator.validate_and_fix_mermaid(invalid_code)
    
    logger.info(f"수정 여부: {was_fixed}")
    logger.info(f"메시지: {message}")
    logger.info(f"수정된 코드:\n{fixed_code}\n")
    
    return fixed_code, was_fixed


def test_markdown_content():
    """Markdown 내용 전체 테스트"""
    
    markdown_content = """# Test Document

## Component Interaction

```mermaid
graph TD
    A[User Input] --> B[Analyzer]  // This is a comment
    B --> C{Decision}
    C -- yes --> D[Process]
    C -- no --> E[한글 레이블]
    D --> F;
```

## Another Diagram

```mermaid
flowchart LR
    Start --> Process -- --option --> End;
```

Some text here.
"""
    
    logger.info("=== Markdown 내용 전체 테스트 ===")
    logger.info(f"원본 Markdown:\n{markdown_content}\n")
    
    validator = LLMMermaidValidator()
    modified_content, validated_count, fixed_count = validator.validate_markdown_content(markdown_content)
    
    logger.info(f"검증된 블록: {validated_count}개")
    logger.info(f"수정된 블록: {fixed_count}개")
    logger.info(f"수정된 Markdown:\n{modified_content}\n")
    
    return modified_content, validated_count, fixed_count


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("LLM 기반 Mermaid 검증기 테스트")
    print("=" * 70 + "\n")
    
    try:
        # 테스트 1: 잘못된 Mermaid 코드
        print("\n[테스트 1] 잘못된 Mermaid 코드 검증 및 수정")
        print("-" * 70)
        fixed_code, was_fixed = test_invalid_mermaid()
        
        if was_fixed:
            print("✓ 코드가 성공적으로 수정되었습니다!")
        else:
            print("ℹ 코드가 이미 유효합니다.")
        
        # 테스트 2: Markdown 내용 전체
        print("\n[테스트 2] Markdown 내용 전체 검증 및 수정")
        print("-" * 70)
        modified_content, validated_count, fixed_count = test_markdown_content()
        
        print(f"✓ 총 {validated_count}개 블록 중 {fixed_count}개가 수정되었습니다.")
        
        print("\n" + "=" * 70)
        print("테스트 완료")
        print("=" * 70 + "\n")
        
    except Exception as e:
        logger.error(f"테스트 중 오류 발생: {e}", exc_info=True)

