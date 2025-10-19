"""
Python Knowledge Base Generator - 메인 실행 파일

로컬 프로젝트의 구조를 분석하고 Knowledge Base를 생성합니다.
Mermaid 다이어그램이 발견되면 자동으로 검증 및 수정합니다.

사용법:
    python main.py <project_path> [options]

예시:
    python main.py ./python_chunking/
    python main.py ./python_chunking/ --no-cache
    python main.py ./python_chunking/ --force
"""

import sys
import argparse
import logging
from pathlib import Path

from logging_config import setup_logging
from wiki_generator import WikiGenerator
from config import CACHE_ROOT, GEMINI_API_KEY, OUTPUT_LANGUAGES, DEFAULT_LANGUAGE
from llm_mermaid_validator import LLMMermaidValidator

logger = logging.getLogger(__name__)


def parse_arguments():
    """명령행 인자 파싱"""
    parser = argparse.ArgumentParser(
        description='Python Knowledge Base Generator - 프로젝트 구조를 분석하고 Wiki를 생성합니다.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python main.py ./python_chunking/
  python main.py ./python_chunking/ --no-cache
  python main.py ./python_chunking/ --force
  python main.py ./python_chunking/ --verbose

참고:
  - Mermaid 다이어그램이 발견되면 자동으로 검증 및 수정됩니다
  - 별도의 옵션 없이도 구문 오류가 자동으로 수정됩니다

생성된 파일 위치:
  - JSON 캐시: ./python_kb/.adalflow/wikicache/<project_name>/
  - Markdown 파일: ./python_kb/.adalflow/wikicache/<project_name>/
  * 규칙과 구조는 DeepWiki와 동일하나, 저장 위치는 프로젝트 내부입니다
        """
    )
    
    parser.add_argument(
        'project_path',
        type=str,
        help='분석할 프로젝트의 경로'
    )
    
    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='캐시를 사용하지 않고 새로 생성'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='기존 캐시를 무시하고 강제로 재생성'
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='상세 로그 출력'
    )
    
    parser.add_argument(
        '--cache-only',
        action='store_true',
        help='캐시된 데이터만 사용하여 Markdown 생성 (새로 생성하지 않음)'
    )
    
    
    parser.add_argument(
        '--language',
        '-l',
        choices=list(OUTPUT_LANGUAGES.keys()),
        default=DEFAULT_LANGUAGE,
        help=f'출력 언어 선택 (기본값: {DEFAULT_LANGUAGE})'
    )
    
    return parser.parse_args()


def validate_environment():
    """환경 설정 검증"""
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY가 설정되지 않았습니다.")
        logger.error("1. .env 파일을 생성하세요")
        logger.error("2. GEMINI_API_KEY=your_api_key_here 를 추가하세요")
        return False
    
    logger.info(f"캐시 디렉토리: {CACHE_ROOT}")
    return True


def validate_project_path(project_path: str) -> bool:
    """프로젝트 경로 검증"""
    path = Path(project_path).resolve()
    
    if not path.exists():
        logger.error(f"프로젝트 경로가 존재하지 않습니다: {project_path}")
        return False
    
    if not path.is_dir():
        logger.error(f"프로젝트 경로가 디렉토리가 아닙니다: {project_path}")
        return False
    
    logger.info(f"프로젝트 경로: {path}")
    return True


def auto_validate_mermaid(cache_dir: str) -> dict:
    """자동 Mermaid 검증 및 수정"""
    cache_path = Path(cache_dir)
    
    # Mermaid 블록이 있는지 먼저 확인
    has_mermaid = False
    for md_file in cache_path.glob("*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            if '```mermaid' in content:
                has_mermaid = True
                break
        except:
            continue
    
    if not has_mermaid:
        logger.info("Mermaid 블록이 없어 검증을 건너뜁니다.")
        return None
    
    logger.info("Mermaid 블록을 발견했습니다. 자동 검증을 시작합니다...")
    validator = LLMMermaidValidator()
    
    total_validated = 0
    total_fixed = 0
    processed_files = []
    
    # 모든 마크다운 파일 처리
    for md_file in cache_path.glob("*.md"):
        logger.info(f"처리 중: {md_file.name}")
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Mermaid 블록이 있는 파일만 처리
            if '```mermaid' not in content:
                continue
            
            # LLM으로 검증 및 수정
            modified_content, validated_count, fixed_count = validator.validate_markdown_content(content)
            
            total_validated += validated_count
            total_fixed += fixed_count
            
            if fixed_count > 0:
                # 수정된 내용을 파일에 저장
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(modified_content)
                processed_files.append((md_file.name, validated_count, fixed_count))
                logger.info(f"✓ {md_file.name}: {fixed_count}개 블록 수정됨")
            elif validated_count > 0:
                logger.info(f"✓ {md_file.name}: 모든 블록이 유효함")
        
        except Exception as e:
            logger.error(f"파일 처리 중 오류 ({md_file.name}): {e}")
    
    # 결과 출력
    print("\n" + "=" * 70)
    print("자동 Mermaid 다이어그램 검증 결과")
    print("=" * 70)
    print(f"총 검증된 블록: {total_validated}개")
    print(f"수정된 블록: {total_fixed}개")
    
    if processed_files:
        print(f"\n수정된 파일:")
        for filename, validated, fixed in processed_files:
            print(f"  ✓ {filename}: {fixed}/{validated}개 블록 수정됨")
    else:
        if total_validated > 0:
            print("\n✅ 모든 Mermaid 다이어그램이 이미 올바른 구문을 가지고 있습니다!")
        else:
            print("\n⚠️  Mermaid 블록을 찾을 수 없습니다.")
    
    print("=" * 70)
    
    return {
        'validated': total_validated,
        'fixed': total_fixed,
        'processed_files': processed_files
    }


def print_summary(summary: dict):
    """실행 결과 요약 출력"""
    print("\n" + "=" * 70)
    print("Wiki 생성 완료")
    print("=" * 70)
    print(f"\n프로젝트: {summary['project_name']}")
    print(f"경로: {summary['project_path']}")
    print(f"\n생성된 페이지: {summary['pages_generated']}개")
    
    for page_type in summary['pages']:
        print(f"  - {page_type}")
    
    print(f"\n저장 위치: {summary['cache_dir']}")
    
    export_summary = summary.get('export_summary', {})
    if export_summary and export_summary.get('files'):
        print(f"\nMarkdown 파일:")
        for file_info in export_summary['files']:
            size_kb = file_info['size'] / 1024
            print(f"  - {file_info['name']} ({size_kb:.1f} KB)")
    
    # Mermaid 검증 결과 추가
    mermaid_validation = summary.get('mermaid_validation')
    if mermaid_validation:
        print(f"\nMermaid 검증:")
        print(f"  - 검증된 블록: {mermaid_validation['validated']}개")
        print(f"  - 수정된 블록: {mermaid_validation['fixed']}개")
    
    print("\n" + "=" * 70)


def main():
    """메인 함수"""
    # 명령행 인자 파싱
    args = parse_arguments()
    
    # 로깅 설정
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(log_level)
    
    logger.info("=== Python Knowledge Base Generator ===")
    
    # 환경 검증
    if not validate_environment():
        sys.exit(1)
    
    # 프로젝트 경로 검증
    if not validate_project_path(args.project_path):
        sys.exit(1)
    
    try:
        # Wiki 생성기 초기화 (언어 설정 포함)
        generator = WikiGenerator(args.project_path, language=args.language)
        
        # 캐시 옵션 설정
        use_cache = not args.no_cache
        force_regenerate = args.force
        
        if args.cache_only:
            logger.info("캐시 전용 모드: 캐시된 데이터만 사용하여 Markdown 생성")
            # 캐시에서 페이지 로드
            pages = {}
            from config import WIKI_PAGES
            for page_type in WIKI_PAGES.keys():
                cached_page = generator.cache_manager.load_wiki_page(page_type)
                if cached_page:
                    pages[page_type] = {
                        'title': cached_page['page_title'],
                        'content': cached_page['content']
                    }
            
            if not pages:
                logger.error("캐시된 페이지가 없습니다. --cache-only 없이 실행하세요.")
                sys.exit(1)
            
            # Markdown 파일로 내보내기
            exported_files = generator.export_to_markdown(pages=pages)
            
            summary = {
                'project_name': generator.project_name,
                'project_path': str(generator.project_path),
                'pages_generated': len(pages),
                'pages': list(pages.keys()),
                'cache_dir': str(generator.cache_manager.cache_dir),
                'export_summary': generator.markdown_exporter.get_export_summary()
            }
        else:
            # 전체 프로세스 실행
            summary = generator.generate_all(
                use_cache=use_cache,
                force_regenerate=force_regenerate
            )
        
        # 자동 Mermaid 검증 및 수정
        logger.info("Mermaid 다이어그램 자동 검증 시작...")
        mermaid_validation_result = auto_validate_mermaid(summary['cache_dir'])
        
        if mermaid_validation_result:
            summary['mermaid_validation'] = mermaid_validation_result
        
        # 결과 출력
        print_summary(summary)
        
        logger.info("프로그램 정상 종료")
        
    except KeyboardInterrupt:
        logger.info("\n사용자에 의해 중단되었습니다.")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"오류 발생: {e}", exc_info=args.verbose)
        sys.exit(1)


if __name__ == "__main__":
    main()

