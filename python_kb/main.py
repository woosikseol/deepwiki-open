"""
Python Knowledge Base Generator - 메인 실행 파일

로컬 프로젝트의 구조를 분석하고 Knowledge Base를 생성합니다.

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
from mermaid_validator import MermaidValidator

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

생성된 파일 위치:
  - JSON 캐시: python_kb/.adalflow/wikicache/<project_name>/
  - Markdown 파일: python_kb/.adalflow/wikicache/<project_name>/
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
        '--validate-mermaid',
        action='store_true',
        help='생성된 Markdown 파일의 Mermaid 다이어그램 구문을 검증'
    )
    
    parser.add_argument(
        '--fix-mermaid',
        action='store_true',
        help='Mermaid 구문 오류를 자동으로 수정'
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
        
        # Mermaid 검증 및 수정
        if args.validate_mermaid or args.fix_mermaid:
            logger.info("Mermaid 다이어그램 검증 시작...")
            validator = MermaidValidator()
            cache_dir = Path(summary['cache_dir'])
            
            if args.fix_mermaid:
                # 자동 수정 모드
                fixed_files = []
                for md_file in cache_dir.glob("*.md"):
                    if validator.fix_markdown_file(str(md_file)):
                        fixed_files.append(md_file.name)
                
                if fixed_files:
                    logger.info(f"Mermaid 구문 오류가 수정된 파일: {', '.join(fixed_files)}")
                else:
                    logger.info("수정할 Mermaid 구문 오류가 없습니다")
            
            if args.validate_mermaid:
                # 검증 모드
                validation_result = validator.validate_directory(str(cache_dir))
                
                print("\n" + "=" * 50)
                print("Mermaid 다이어그램 검증 결과")
                print("=" * 50)
                print(f"총 파일: {validation_result['total_files']}")
                print(f"Mermaid 포함 파일: {validation_result['files_with_mermaid']}")
                print(f"총 다이어그램 블록: {validation_result['total_blocks']}")
                print(f"유효한 블록: {validation_result['valid_blocks']}")
                print(f"무효한 블록: {validation_result['invalid_blocks']}")
                
                if validation_result['invalid_blocks'] > 0:
                    print("\n❌ 구문 오류가 있는 파일:")
                    for file_path, file_result in validation_result['file_results'].items():
                        if file_result['invalid_blocks'] > 0:
                            print(f"  📄 {Path(file_path).name}")
                            for block_name, block_info in file_result['blocks'].items():
                                if not block_info['valid']:
                                    print(f"    ❌ {block_name}: {block_info['message']}")
                else:
                    print("\n✅ 모든 Mermaid 다이어그램이 올바른 구문을 가지고 있습니다!")
        
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

