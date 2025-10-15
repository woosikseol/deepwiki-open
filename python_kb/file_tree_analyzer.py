"""
파일 트리 분석 모듈
로컬 프로젝트의 파일 구조를 분석합니다.
"""

import os
import logging
from pathlib import Path
from typing import Dict, List, Set
from dataclasses import dataclass
import fnmatch

from config import (
    CODE_EXTENSIONS, DOC_EXTENSIONS,
    EXCLUDED_DIRS, EXCLUDED_FILES,
    SUPPORTED_LANGUAGES
)

logger = logging.getLogger(__name__)


@dataclass
class FileInfo:
    """파일 정보"""
    path: str
    relative_path: str
    extension: str
    language: str
    is_code: bool
    size: int


@dataclass
class ProjectStructure:
    """프로젝트 구조 정보"""
    root_path: str
    files: List[FileInfo]
    directory_tree: Dict
    statistics: Dict


class FileTreeAnalyzer:
    """파일 트리 분석기"""
    
    def __init__(self, root_path: str):
        """
        Args:
            root_path: 분석할 프로젝트의 루트 경로
        """
        self.root_path = Path(root_path).resolve()
        if not self.root_path.exists():
            raise ValueError(f"경로가 존재하지 않습니다: {root_path}")
        if not self.root_path.is_dir():
            raise ValueError(f"디렉토리가 아닙니다: {root_path}")
        
        logger.info(f"파일 트리 분석기 초기화: {self.root_path}")
    
    def should_exclude_dir(self, dir_name: str) -> bool:
        """디렉토리를 제외할지 확인"""
        return dir_name in EXCLUDED_DIRS or dir_name.startswith('.')
    
    def should_exclude_file(self, file_name: str) -> bool:
        """파일을 제외할지 확인"""
        # 숨김 파일 제외
        if file_name.startswith('.'):
            return True
        
        # 패턴 매칭으로 제외 파일 확인
        for pattern in EXCLUDED_FILES:
            if fnmatch.fnmatch(file_name, pattern):
                return True
        
        return False
    
    def get_language_from_extension(self, extension: str) -> str:
        """파일 확장자로부터 프로그래밍 언어 판별"""
        for lang, exts in SUPPORTED_LANGUAGES.items():
            if extension in exts:
                return lang
        return 'unknown'
    
    def analyze(self) -> ProjectStructure:
        """
        프로젝트 구조 분석
        
        Returns:
            ProjectStructure: 분석된 프로젝트 구조
        """
        logger.info("프로젝트 구조 분석 시작...")
        
        files = []
        directory_tree = {}
        
        # 통계 정보
        stats = {
            'total_files': 0,
            'code_files': 0,
            'doc_files': 0,
            'languages': {},
            'total_size': 0
        }
        
        # 파일 순회
        for root, dirs, filenames in os.walk(self.root_path):
            # 제외할 디렉토리 필터링
            dirs[:] = [d for d in dirs if not self.should_exclude_dir(d)]
            
            root_path = Path(root)
            relative_root = root_path.relative_to(self.root_path)
            
            for filename in filenames:
                # 제외할 파일 필터링
                if self.should_exclude_file(filename):
                    continue
                
                file_path = root_path / filename
                relative_path = file_path.relative_to(self.root_path)
                
                # 파일 확장자 확인
                extension = file_path.suffix
                
                # 코드 파일 또는 문서 파일만 처리
                is_code = extension in CODE_EXTENSIONS
                is_doc = extension in DOC_EXTENSIONS
                
                if not (is_code or is_doc):
                    continue
                
                # 파일 정보 생성
                try:
                    file_size = file_path.stat().st_size
                except OSError:
                    file_size = 0
                
                language = self.get_language_from_extension(extension) if is_code else 'documentation'
                
                file_info = FileInfo(
                    path=str(file_path),
                    relative_path=str(relative_path),
                    extension=extension,
                    language=language,
                    is_code=is_code,
                    size=file_size
                )
                
                files.append(file_info)
                
                # 통계 업데이트
                stats['total_files'] += 1
                if is_code:
                    stats['code_files'] += 1
                    stats['languages'][language] = stats['languages'].get(language, 0) + 1
                elif is_doc:
                    stats['doc_files'] += 1
                stats['total_size'] += file_size
        
        logger.info(f"분석 완료: 총 {stats['total_files']}개 파일")
        logger.info(f"  - 코드 파일: {stats['code_files']}개")
        logger.info(f"  - 문서 파일: {stats['doc_files']}개")
        logger.info(f"  - 언어별: {stats['languages']}")
        
        # 디렉토리 트리 생성
        directory_tree = self._build_directory_tree(files)
        
        return ProjectStructure(
            root_path=str(self.root_path),
            files=files,
            directory_tree=directory_tree,
            statistics=stats
        )
    
    def _build_directory_tree(self, files: List[FileInfo]) -> Dict:
        """
        파일 목록으로부터 디렉토리 트리 구조 생성
        
        Args:
            files: 파일 정보 리스트
            
        Returns:
            Dict: 디렉토리 트리 구조
        """
        tree = {}
        
        for file_info in files:
            parts = Path(file_info.relative_path).parts
            current = tree
            
            # 디렉토리 경로 순회
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {'_type': 'directory', '_children': {}}
                current = current[part]['_children']
            
            # 파일 추가
            filename = parts[-1]
            current[filename] = {
                '_type': 'file',
                'language': file_info.language,
                'is_code': file_info.is_code,
                'size': file_info.size
            }
        
        return tree
    
    def generate_tree_string(self, tree: Dict = None, prefix: str = "", is_last: bool = True) -> str:
        """
        디렉토리 트리를 문자열로 변환
        
        Args:
            tree: 디렉토리 트리 (None이면 전체 구조)
            prefix: 들여쓰기 접두사
            is_last: 마지막 항목 여부
            
        Returns:
            str: 트리 구조 문자열
        """
        if tree is None:
            structure = self.analyze()
            tree = structure.directory_tree
        
        lines = []
        items = sorted(tree.items())
        
        for i, (name, node) in enumerate(items):
            is_last_item = (i == len(items) - 1)
            connector = "└── " if is_last_item else "├── "
            
            if node.get('_type') == 'directory':
                lines.append(f"{prefix}{connector}{name}/")
                extension = "    " if is_last_item else "│   "
                children = node.get('_children', {})
                if children:
                    lines.append(self.generate_tree_string(
                        children,
                        prefix + extension,
                        is_last_item
                    ))
            else:
                language = node.get('language', '')
                lang_suffix = f" [{language}]" if language != 'documentation' else ""
                lines.append(f"{prefix}{connector}{name}{lang_suffix}")
        
        return '\n'.join(lines)

