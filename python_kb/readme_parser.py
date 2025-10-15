"""
README 파서 모듈
프로젝트의 README 파일을 파싱하고 주요 정보를 추출합니다.
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict
import re

logger = logging.getLogger(__name__)


class ReadmeParser:
    """README 파일 파서"""
    
    def __init__(self, root_path: str):
        """
        Args:
            root_path: 프로젝트 루트 경로
        """
        self.root_path = Path(root_path).resolve()
        self.readme_content = ""
        self.readme_path = None
        
    def find_readme(self) -> Optional[Path]:
        """
        README 파일 찾기
        
        Returns:
            Optional[Path]: README 파일 경로 (없으면 None)
        """
        # 우선순위대로 README 파일 검색
        readme_names = [
            'README.md',
            'readme.md',
            'Readme.md',
            'README.MD',
            'README.txt',
            'README.rst',
            'README'
        ]
        
        for name in readme_names:
            readme_path = self.root_path / name
            if readme_path.exists() and readme_path.is_file():
                logger.info(f"README 파일 발견: {readme_path}")
                return readme_path
        
        logger.warning("README 파일을 찾을 수 없습니다")
        return None
    
    def parse(self) -> Dict:
        """
        README 파일 파싱
        
        Returns:
            Dict: 파싱된 README 정보
                - content: 전체 내용
                - title: 제목
                - description: 설명
                - sections: 섹션 목록
                - has_installation: 설치 가이드 포함 여부
                - has_usage: 사용법 포함 여부
        """
        self.readme_path = self.find_readme()
        
        if not self.readme_path:
            return {
                'content': '',
                'title': '',
                'description': '',
                'sections': [],
                'has_installation': False,
                'has_usage': False
            }
        
        try:
            with open(self.readme_path, 'r', encoding='utf-8') as f:
                self.readme_content = f.read()
        except Exception as e:
            logger.error(f"README 파일 읽기 실패: {e}")
            return {
                'content': '',
                'title': '',
                'description': '',
                'sections': [],
                'has_installation': False,
                'has_usage': False
            }
        
        # 제목 추출
        title = self._extract_title()
        
        # 설명 추출
        description = self._extract_description()
        
        # 섹션 추출
        sections = self._extract_sections()
        
        # 주요 섹션 확인
        has_installation = any(
            'install' in s.lower() or 'setup' in s.lower() 
            for s in sections
        )
        has_usage = any(
            'usage' in s.lower() or 'example' in s.lower() or 'quick start' in s.lower()
            for s in sections
        )
        
        logger.info(f"README 파싱 완료: {len(sections)}개 섹션")
        
        return {
            'content': self.readme_content,
            'title': title,
            'description': description,
            'sections': sections,
            'has_installation': has_installation,
            'has_usage': has_usage
        }
    
    def _extract_title(self) -> str:
        """README에서 제목 추출"""
        if not self.readme_content:
            return ""
        
        # 첫 번째 H1 헤딩 찾기
        match = re.search(r'^#\s+(.+)$', self.readme_content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        # HTML 스타일 헤딩 찾기
        match = re.search(r'<h1>(.+?)</h1>', self.readme_content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        # 첫 줄을 제목으로 사용
        lines = self.readme_content.strip().split('\n')
        if lines:
            return lines[0].strip('#').strip()
        
        return ""
    
    def _extract_description(self) -> str:
        """README에서 설명 추출"""
        if not self.readme_content:
            return ""
        
        lines = self.readme_content.strip().split('\n')
        
        # 제목 다음 단락 찾기
        description_lines = []
        found_title = False
        
        for line in lines:
            stripped = line.strip()
            
            # 제목 건너뛰기
            if not found_title:
                if stripped.startswith('#') or stripped.startswith('<h1'):
                    found_title = True
                continue
            
            # 빈 줄 건너뛰기
            if not stripped:
                if description_lines:
                    break
                continue
            
            # 다음 헤딩이 나오면 중단
            if stripped.startswith('#') or stripped.startswith('<h'):
                break
            
            description_lines.append(stripped)
        
        description = ' '.join(description_lines)
        
        # 최대 500자로 제한
        if len(description) > 500:
            description = description[:497] + '...'
        
        return description
    
    def _extract_sections(self) -> list:
        """README에서 섹션 목록 추출"""
        if not self.readme_content:
            return []
        
        sections = []
        
        # Markdown 헤딩 추출 (## 이상)
        for match in re.finditer(r'^##\s+(.+)$', self.readme_content, re.MULTILINE):
            section_title = match.group(1).strip()
            sections.append(section_title)
        
        # HTML 헤딩 추출
        for match in re.finditer(r'<h[2-6]>(.+?)</h[2-6]>', self.readme_content, re.IGNORECASE):
            section_title = match.group(1).strip()
            if section_title not in sections:
                sections.append(section_title)
        
        return sections

