"""
캐시 관리 모듈
Wiki 생성 결과를 JSON 캐시로 저장하고 로드합니다.
DeepWiki와 동일한 캐시 구조를 사용합니다.
"""

import json
import logging
import hashlib
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

from config import CACHE_ROOT

logger = logging.getLogger(__name__)


class CacheManager:
    """캐시 관리자"""
    
    def __init__(self, project_name: str, language: str = 'ko'):
        """
        Args:
            project_name: 프로젝트 이름 (캐시 디렉토리명으로 사용)
            language: 출력 언어 ('ko' 또는 'en')
        """
        self.project_name = self._sanitize_project_name(project_name)
        self.language = language
        self.cache_dir = CACHE_ROOT / self.project_name
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"캐시 관리자 초기화: {self.cache_dir} (언어: {language})")
    
    def _sanitize_project_name(self, name: str) -> str:
        """
        프로젝트 이름을 파일시스템에 안전한 이름으로 변환
        
        Args:
            name: 원본 프로젝트 이름
            
        Returns:
            str: 안전한 이름
        """
        # 특수 문자 제거 및 공백을 언더스코어로 변환
        safe_name = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in name)
        return safe_name.lower()
    
    def _get_cache_key(self, page_type: str) -> str:
        """
        페이지 타입으로부터 캐시 키 생성
        
        Args:
            page_type: 페이지 타입
            
        Returns:
            str: 캐시 키
        """
        return f"{page_type}.json"
    
    def save_wiki_page(
        self,
        page_type: str,
        page_title: str,
        content: str,
        metadata: Optional[Dict] = None
    ) -> Path:
        """
        Wiki 페이지를 캐시에 저장
        
        Args:
            page_type: 페이지 타입
            page_title: 페이지 제목
            content: 페이지 내용 (Markdown)
            metadata: 추가 메타데이터
            
        Returns:
            Path: 저장된 캐시 파일 경로
        """
        cache_file = self.cache_dir / self._get_cache_key(page_type)
        
        # 캐시 데이터 구조
        cache_data = {
            'page_type': page_type,
            'page_title': page_title,
            'content': content,
            'metadata': metadata or {},
            'created_at': datetime.now().isoformat(),
            'content_hash': self._hash_content(content)
        }
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"캐시 저장 완료: {cache_file}")
            return cache_file
            
        except Exception as e:
            logger.error(f"캐시 저장 실패: {e}")
            raise
    
    def load_wiki_page(self, page_type: str) -> Optional[Dict]:
        """
        캐시에서 Wiki 페이지 로드
        
        Args:
            page_type: 페이지 타입
            
        Returns:
            Optional[Dict]: 캐시 데이터 (없으면 None)
        """
        cache_file = self.cache_dir / self._get_cache_key(page_type)
        
        if not cache_file.exists():
            logger.info(f"캐시 파일 없음: {cache_file}")
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            logger.info(f"캐시 로드 완료: {cache_file}")
            return cache_data
            
        except Exception as e:
            logger.error(f"캐시 로드 실패: {e}")
            return None
    
    def cache_exists(self, page_type: str) -> bool:
        """
        캐시 파일 존재 여부 확인
        
        Args:
            page_type: 페이지 타입
            
        Returns:
            bool: 캐시 존재 여부
        """
        cache_file = self.cache_dir / self._get_cache_key(page_type)
        return cache_file.exists()
    
    def clear_cache(self, page_type: Optional[str] = None):
        """
        캐시 삭제
        
        Args:
            page_type: 페이지 타입 (None이면 전체 삭제)
        """
        if page_type:
            # 특정 페이지 캐시 삭제
            cache_file = self.cache_dir / self._get_cache_key(page_type)
            if cache_file.exists():
                cache_file.unlink()
                logger.info(f"캐시 삭제: {cache_file}")
        else:
            # 전체 캐시 삭제
            if self.cache_dir.exists():
                for cache_file in self.cache_dir.glob('*.json'):
                    cache_file.unlink()
                logger.info(f"전체 캐시 삭제: {self.cache_dir}")
    
    def get_all_cached_pages(self) -> list:
        """
        모든 캐시된 페이지 목록 가져오기
        
        Returns:
            list: 캐시된 페이지 타입 목록
        """
        if not self.cache_dir.exists():
            return []
        
        pages = []
        for cache_file in self.cache_dir.glob('*.json'):
            page_type = cache_file.stem
            pages.append(page_type)
        
        return sorted(pages)
    
    def _hash_content(self, content: str) -> str:
        """
        콘텐츠의 해시 생성
        
        Args:
            content: 콘텐츠
            
        Returns:
            str: SHA256 해시
        """
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def save_project_metadata(self, metadata: Dict):
        """
        프로젝트 메타데이터 저장
        
        Args:
            metadata: 메타데이터
        """
        metadata_file = self.cache_dir / 'project_metadata.json'
        
        try:
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            logger.info(f"프로젝트 메타데이터 저장: {metadata_file}")
            
        except Exception as e:
            logger.error(f"메타데이터 저장 실패: {e}")
    
    def load_project_metadata(self) -> Optional[Dict]:
        """
        프로젝트 메타데이터 로드
        
        Returns:
            Optional[Dict]: 메타데이터 (없으면 None)
        """
        metadata_file = self.cache_dir / 'project_metadata.json'
        
        if not metadata_file.exists():
            return None
        
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"메타데이터 로드 실패: {e}")
            return None

