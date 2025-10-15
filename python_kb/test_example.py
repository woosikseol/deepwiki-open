"""
간단한 테스트 스크립트
실제 API 호출 없이 모듈 import를 테스트합니다.
"""

import sys
from pathlib import Path

# 현재 디렉토리를 Python path에 추가
sys.path.insert(0, str(Path(__file__).parent))


def test_imports():
    """모든 모듈이 정상적으로 import되는지 테스트"""
    print("모듈 import 테스트 시작...")
    
    try:
        import config
        print("✓ config 모듈 로드 성공")
        
        import logging_config
        print("✓ logging_config 모듈 로드 성공")
        
        import file_tree_analyzer
        print("✓ file_tree_analyzer 모듈 로드 성공")
        
        import readme_parser
        print("✓ readme_parser 모듈 로드 성공")
        
        # Gemini API 키가 없으면 스킵
        try:
            import gemini_client
            print("✓ gemini_client 모듈 로드 성공")
        except ValueError as e:
            print(f"⚠ gemini_client 모듈 로드 스킵 (API 키 필요): {e}")
        
        import cache_manager
        print("✓ cache_manager 모듈 로드 성공")
        
        import markdown_exporter
        print("✓ markdown_exporter 모듈 로드 성공")
        
        import wiki_generator
        print("✓ wiki_generator 모듈 로드 성공")
        
        print("\n✅ 모든 모듈 import 성공!")
        return True
        
    except Exception as e:
        print(f"\n❌ 모듈 import 실패: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_file_tree_analyzer():
    """FileTreeAnalyzer 기본 기능 테스트"""
    print("\nFileTreeAnalyzer 테스트 시작...")
    
    try:
        from file_tree_analyzer import FileTreeAnalyzer
        
        # 현재 디렉토리 분석
        analyzer = FileTreeAnalyzer('.')
        print("✓ FileTreeAnalyzer 초기화 성공")
        
        structure = analyzer.analyze()
        print(f"✓ 프로젝트 분석 성공: {structure.statistics['total_files']}개 파일")
        
        tree_str = analyzer.generate_tree_string()
        print(f"✓ 파일 트리 생성 성공: {len(tree_str)}자")
        
        print("\n✅ FileTreeAnalyzer 테스트 통과!")
        return True
        
    except Exception as e:
        print(f"\n❌ FileTreeAnalyzer 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_readme_parser():
    """ReadmeParser 기본 기능 테스트"""
    print("\nReadmeParser 테스트 시작...")
    
    try:
        from readme_parser import ReadmeParser
        
        # 현재 디렉토리의 README 파싱
        parser = ReadmeParser('.')
        print("✓ ReadmeParser 초기화 성공")
        
        readme_info = parser.parse()
        print(f"✓ README 파싱 성공")
        print(f"  - 제목: {readme_info.get('title', 'N/A')}")
        print(f"  - 섹션: {len(readme_info.get('sections', []))}개")
        
        print("\n✅ ReadmeParser 테스트 통과!")
        return True
        
    except Exception as e:
        print(f"\n❌ ReadmeParser 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cache_manager():
    """CacheManager 기본 기능 테스트"""
    print("\nCacheManager 테스트 시작...")
    
    try:
        from cache_manager import CacheManager
        
        # 테스트용 캐시 매니저 생성
        cache_mgr = CacheManager('test_project')
        print("✓ CacheManager 초기화 성공")
        
        # 테스트 데이터 저장
        cache_mgr.save_wiki_page(
            page_type='test_page',
            page_title='Test Page',
            content='# Test Content\n\nThis is a test.'
        )
        print("✓ 캐시 저장 성공")
        
        # 테스트 데이터 로드
        cached_data = cache_mgr.load_wiki_page('test_page')
        if cached_data and cached_data['content']:
            print("✓ 캐시 로드 성공")
        
        # 테스트 캐시 정리
        cache_mgr.clear_cache()
        print("✓ 캐시 정리 성공")
        
        print("\n✅ CacheManager 테스트 통과!")
        return True
        
    except Exception as e:
        print(f"\n❌ CacheManager 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """메인 테스트 함수"""
    print("=" * 70)
    print("Python Knowledge Base Generator - 테스트")
    print("=" * 70)
    
    results = []
    
    # 모듈 import 테스트
    results.append(("모듈 Import", test_imports()))
    
    # FileTreeAnalyzer 테스트
    results.append(("FileTreeAnalyzer", test_file_tree_analyzer()))
    
    # ReadmeParser 테스트
    results.append(("ReadmeParser", test_readme_parser()))
    
    # CacheManager 테스트
    results.append(("CacheManager", test_cache_manager()))
    
    # 결과 요약
    print("\n" + "=" * 70)
    print("테스트 결과 요약")
    print("=" * 70)
    
    for name, result in results:
        status = "✅ 통과" if result else "❌ 실패"
        print(f"{name}: {status}")
    
    success_count = sum(1 for _, result in results if result)
    total_count = len(results)
    
    print(f"\n총 {total_count}개 중 {success_count}개 통과")
    
    if success_count == total_count:
        print("\n🎉 모든 테스트 통과!")
        return 0
    else:
        print(f"\n⚠️ {total_count - success_count}개 테스트 실패")
        return 1


if __name__ == "__main__":
    sys.exit(main())

