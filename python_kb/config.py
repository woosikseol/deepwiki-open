"""
설정 관리 모듈
환경 변수 및 프로젝트 설정을 관리합니다.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# Gemini API 설정
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
GEMINI_MODEL = "gemini-2.0-flash-exp"  # gemini-2.5-flash-lite 대신 gemini-2.0-flash-exp 사용

# 다국어 지원 설정 (출력 언어)
OUTPUT_LANGUAGES = {
    'ko': 'Korean',
    'en': 'English'
}

DEFAULT_LANGUAGE = 'ko'  # 기본 언어

# PostgreSQL 설정
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '5432')),
    'database': os.getenv('DB_NAME', 'deepwiki'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
}

# 캐시 디렉토리 설정 (프로젝트 내부)
CACHE_ROOT = Path(__file__).parent / '.adalflow' / 'wikicache'
CACHE_ROOT.mkdir(parents=True, exist_ok=True)

# 지원하는 프로그래밍 언어 (코드 분석용)
SUPPORTED_LANGUAGES = {
    'python': ['.py'],
    'java': ['.java'],
    'javascript': ['.js', '.jsx'],
    'typescript': ['.ts', '.tsx'],
}

# 파일 확장자 목록
CODE_EXTENSIONS = []
for exts in SUPPORTED_LANGUAGES.values():
    CODE_EXTENSIONS.extend(exts)

DOC_EXTENSIONS = ['.md', '.txt', '.rst']

# 제외할 디렉토리 및 파일 (deepwiki-open과 동일)
EXCLUDED_DIRS = [
    '.git', '.svn', '.hg',
    'node_modules', 'bower_components',
    '__pycache__', '.pytest_cache', '.mypy_cache',
    'venv', '.venv', 'env', 'virtualenv',
    'dist', 'build', 'target', 'bin', 'obj',
    '.idea', '.vscode', '.vs',
    'logs', 'log', 'tmp', 'temp',
]

EXCLUDED_FILES = [
    '.DS_Store', 'Thumbs.db',
    '*.pyc', '*.pyo', '*.pyd',
    '*.so', '*.dll', '*.dylib',
    '*.egg-info', '*.dist-info',
    'package-lock.json', 'yarn.lock',
    '.gitignore', '.gitattributes',
]

# Wiki 페이지 템플릿 (다국어 지원)
WIKI_PAGES = {
    'project_structure': {
        'ko': {
            'title': '프로젝트 구조 및 개요 (주요 기능 포함)',
            'description': '프로젝트 구조 개요 및 주요 기능'
        },
        'en': {
            'title': 'Project Structure & Overview (and Key Features) including Architecture Diagram & Flow Diagram',
            'description': 'Project structure overview and key features including architecture and flow diagrams'
        }
    },
    'architecture': {
        'ko': {
            'title': '전체 시스템 아키텍처 및 주요 기능에서 사용되는 디자인 패턴 (아키텍처 다이어그램 및 플로우 다이어그램 포함)',
            'description': '주요 기능에서 사용되는 시스템 아키텍처 및 디자인 패턴 (아키텍처 다이어그램 및 플로우 다이어그램 포함)'
        },
        'en': {
            'title': 'Overall System Architecture & Design Patterns (including Architecture Diagram & Flow Diagram) used in major features',
            'description': 'System architecture and design patterns used in major features including architecture and flow diagrams'
        }
    },
    'conventions': {
        'ko': {
            'title': '규칙 및 규약 (명명 규칙, 규칙 등)',
            'description': '명명 규칙, 코딩 규칙 및 모범 사례'
        },
        'en': {
            'title': 'Conventions (Naming Conventions, Rules, …)',
            'description': 'Naming conventions, coding rules, and best practices'
        }
    },
    'environment': {
        'ko': {
            'title': '환경 설정 및 가이드',
            'description': '환경 설정 및 구성 가이드'
        },
        'en': {
            'title': 'Environment Setting and the Guide',
            'description': 'Environment setup and configuration guide'
        }
    }
}

# LLM 설정
LLM_LANGUAGE = 'en'  # 프롬프트는 영어로 고정
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 4096

