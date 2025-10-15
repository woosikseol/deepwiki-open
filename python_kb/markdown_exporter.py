"""
Markdown 내보내기 모듈
Wiki 페이지를 Markdown 파일로 저장합니다.
"""

import logging
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

from config import CACHE_ROOT

logger = logging.getLogger(__name__)


class MarkdownExporter:
    """Markdown 파일 내보내기"""
    
    def __init__(self, project_name: str):
        """
        Args:
            project_name: 프로젝트 이름
        """
        self.project_name = self._sanitize_project_name(project_name)
        self.export_dir = CACHE_ROOT / self.project_name
        self.export_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Markdown 내보내기 초기화: {self.export_dir}")
    
    def _sanitize_project_name(self, name: str) -> str:
        """
        프로젝트 이름을 파일시스템에 안전한 이름으로 변환
        
        Args:
            name: 원본 프로젝트 이름
            
        Returns:
            str: 안전한 이름
        """
        safe_name = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in name)
        return safe_name.lower()
    
    def _get_filename(self, page_type: str, page_title: str) -> str:
        """
        페이지 타입과 제목으로부터 파일명 생성
        
        Args:
            page_type: 페이지 타입
            page_title: 페이지 제목
            
        Returns:
            str: 파일명
        """
        # 페이지 타입을 파일명으로 사용
        safe_title = self._sanitize_project_name(page_type)
        return f"{safe_title}.md"
    
    def export_page(
        self,
        page_type: str,
        page_title: str,
        content: str,
        add_metadata: bool = True
    ) -> Path:
        """
        Wiki 페이지를 Markdown 파일로 내보내기
        
        Args:
            page_type: 페이지 타입
            page_title: 페이지 제목
            content: 페이지 내용 (Markdown)
            add_metadata: 메타데이터 추가 여부
            
        Returns:
            Path: 저장된 파일 경로
        """
        filename = self._get_filename(page_type, page_title)
        filepath = self.export_dir / filename
        
        # 메타데이터 추가
        if add_metadata:
            metadata_header = self._create_metadata_header(page_title)
            full_content = f"{metadata_header}\n\n{content}"
        else:
            full_content = content
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_content)
            
            logger.info(f"Markdown 파일 저장 완료: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Markdown 파일 저장 실패: {e}")
            raise
    
    def _create_metadata_header(self, page_title: str) -> str:
        """
        Markdown 파일 헤더에 메타데이터 추가
        
        Args:
            page_title: 페이지 제목
            
        Returns:
            str: 메타데이터 헤더
        """
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        header = f"""---
title: {page_title}
project: {self.project_name}
generated_at: {now}
generator: Python Knowledge Base Generator
---"""
        
        return header
    
    def export_all_pages(self, pages: Dict[str, Dict]) -> list:
        """
        모든 페이지를 Markdown 파일로 내보내기
        
        Args:
            pages: 페이지 딕셔너리
                {page_type: {'title': ..., 'content': ...}}
                
        Returns:
            list: 저장된 파일 경로 목록
        """
        exported_files = []
        
        for page_type, page_data in pages.items():
            try:
                filepath = self.export_page(
                    page_type=page_type,
                    page_title=page_data['title'],
                    content=page_data['content']
                )
                exported_files.append(filepath)
            except Exception as e:
                logger.error(f"페이지 내보내기 실패 ({page_type}): {e}")
        
        logger.info(f"총 {len(exported_files)}개 페이지 내보내기 완료")
        return exported_files
    
    def get_export_summary(self) -> Dict:
        """
        내보내기 요약 정보 가져오기
        
        Returns:
            Dict: 요약 정보
        """
        if not self.export_dir.exists():
            return {
                'export_dir': str(self.export_dir),
                'files': [],
                'total_files': 0
            }
        
        files = []
        for md_file in self.export_dir.glob('*.md'):
            files.append({
                'name': md_file.name,
                'path': str(md_file),
                'size': md_file.stat().st_size,
                'modified': datetime.fromtimestamp(md_file.stat().st_mtime).isoformat()
            })
        
        return {
            'export_dir': str(self.export_dir),
            'files': sorted(files, key=lambda x: x['name']),
            'total_files': len(files)
        }

