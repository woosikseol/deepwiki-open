"""
Wiki 생성 로직 모듈
프로젝트 분석 결과를 기반으로 Wiki 페이지를 생성합니다.
"""

import logging
from typing import Dict, List
from pathlib import Path

from config import WIKI_PAGES, DEFAULT_LANGUAGE
from file_tree_analyzer import FileTreeAnalyzer
from readme_parser import ReadmeParser
from gemini_client import GeminiClient
from cache_manager import CacheManager
from markdown_exporter import MarkdownExporter

logger = logging.getLogger(__name__)


class WikiGenerator:
    """Wiki 생성기"""
    
    def __init__(self, project_path: str, language: str = DEFAULT_LANGUAGE):
        """
        Args:
            project_path: 프로젝트 경로
            language: 출력 언어 ('ko' 또는 'en')
        """
        self.project_path = Path(project_path).resolve()
        self.project_name = self.project_path.name
        self.language = language
        
        # 컴포넌트 초기화
        self.file_analyzer = FileTreeAnalyzer(str(self.project_path))
        self.readme_parser = ReadmeParser(str(self.project_path))
        self.gemini_client = GeminiClient(language=self.language)
        self.cache_manager = CacheManager(self.project_name, language=self.language)
        self.markdown_exporter = MarkdownExporter(self.project_name)
        
        logger.info(f"Wiki 생성기 초기화: {self.project_name}")
    
    def analyze_project(self) -> Dict:
        """
        프로젝트 분석
        
        Returns:
            Dict: 분석 결과
        """
        logger.info("프로젝트 분석 시작...")
        
        # 파일 구조 분석
        structure = self.file_analyzer.analyze()
        
        # README 파싱
        readme_info = self.readme_parser.parse()
        
        # 파일 트리 문자열 생성
        file_tree_str = self.file_analyzer.generate_tree_string()
        
        analysis_result = {
            'project_name': self.project_name,
            'project_path': str(self.project_path),
            'structure': structure,
            'readme': readme_info,
            'file_tree': file_tree_str,
            'statistics': structure.statistics
        }
        
        # 분석 결과를 메타데이터로 저장
        self.cache_manager.save_project_metadata({
            'project_name': self.project_name,
            'project_path': str(self.project_path),
            'statistics': structure.statistics,
            'readme_title': readme_info.get('title', ''),
            'readme_sections': readme_info.get('sections', [])
        })
        
        logger.info("프로젝트 분석 완료")
        return analysis_result
    
    def generate_wiki_pages(
        self,
        use_cache: bool = True,
        force_regenerate: bool = False
    ) -> Dict[str, Dict]:
        """
        Wiki 페이지 생성
        
        Args:
            use_cache: 캐시 사용 여부
            force_regenerate: 강제 재생성 여부
            
        Returns:
            Dict[str, Dict]: 생성된 페이지들
                {page_type: {'title': ..., 'content': ...}}
        """
        logger.info("Wiki 페이지 생성 시작...")
        
        # 프로젝트 분석
        analysis = self.analyze_project()
        
        # 컨텍스트 준비
        context = {
            'project_name': analysis['project_name'],
            'readme_content': analysis['readme']['content'],
            'file_tree': analysis['file_tree'],
            'statistics': analysis['statistics']
        }
        
        pages = {}
        
        for page_type, page_info in WIKI_PAGES.items():
            page_title = page_info[self.language]['title']
            
            # 캐시 확인
            if use_cache and not force_regenerate:
                cached_page = self.cache_manager.load_wiki_page(page_type)
                if cached_page:
                    logger.info(f"캐시에서 페이지 로드: {page_title}")
                    pages[page_type] = {
                        'title': cached_page['page_title'],
                        'content': cached_page['content']
                    }
                    continue
            
            # 페이지 생성
            try:
                logger.info(f"페이지 생성 중: {page_title}")
                content = self.gemini_client.generate_wiki_page(
                    page_type=page_type,
                    page_title=page_title,
                    context=context
                )
                
                pages[page_type] = {
                    'title': page_title,
                    'content': content
                }
                
                # 캐시에 저장
                self.cache_manager.save_wiki_page(
                    page_type=page_type,
                    page_title=page_title,
                    content=content,
                    metadata={
                        'description': page_info[self.language]['description']
                    }
                )
                
                logger.info(f"페이지 생성 완료: {page_title}")
                
            except Exception as e:
                logger.error(f"페이지 생성 실패 ({page_title}): {e}")
                # 실패한 경우 빈 페이지 생성
                pages[page_type] = {
                    'title': page_title,
                    'content': f"# {page_title}\n\n*Error: Failed to generate content*\n\n{str(e)}"
                }
        
        logger.info(f"Wiki 페이지 생성 완료: {len(pages)}개 페이지")
        return pages
    
    def export_to_markdown(
        self,
        pages: Dict[str, Dict] = None,
        use_cache: bool = True
    ) -> List[Path]:
        """
        Markdown 파일로 내보내기
        
        Args:
            pages: 페이지 딕셔너리 (None이면 새로 생성)
            use_cache: 캐시 사용 여부
            
        Returns:
            List[Path]: 저장된 파일 경로 목록
        """
        logger.info("Markdown 파일 내보내기 시작...")
        
        # 페이지가 제공되지 않으면 생성
        if pages is None:
            pages = self.generate_wiki_pages(use_cache=use_cache)
        
        # Markdown 파일로 내보내기
        exported_files = self.markdown_exporter.export_all_pages(pages)
        
        logger.info(f"Markdown 내보내기 완료: {len(exported_files)}개 파일")
        return exported_files
    
    def generate_all(
        self,
        use_cache: bool = True,
        force_regenerate: bool = False
    ) -> Dict:
        """
        전체 프로세스 실행: 분석 -> Wiki 생성 -> Markdown 내보내기
        
        Args:
            use_cache: 캐시 사용 여부
            force_regenerate: 강제 재생성 여부
            
        Returns:
            Dict: 실행 결과
        """
        logger.info("=== Wiki 생성 프로세스 시작 ===")
        
        # Wiki 페이지 생성
        pages = self.generate_wiki_pages(
            use_cache=use_cache,
            force_regenerate=force_regenerate
        )
        
        # Markdown 파일로 내보내기
        exported_files = self.export_to_markdown(pages=pages)
        
        # 요약 정보
        summary = {
            'project_name': self.project_name,
            'project_path': str(self.project_path),
            'pages_generated': len(pages),
            'pages': list(pages.keys()),
            'exported_files': [str(f) for f in exported_files],
            'cache_dir': str(self.cache_manager.cache_dir),
            'export_summary': self.markdown_exporter.get_export_summary()
        }
        
        logger.info("=== Wiki 생성 프로세스 완료 ===")
        logger.info(f"생성된 페이지: {len(pages)}개")
        logger.info(f"내보낸 파일: {len(exported_files)}개")
        logger.info(f"저장 위치: {self.cache_manager.cache_dir}")
        
        return summary

