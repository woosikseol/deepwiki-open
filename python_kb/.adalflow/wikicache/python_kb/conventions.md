---
title: 규칙 및 규약 (명명 규칙, 규칙 등)
project: python_kb
generated_at: 2025-10-15 16:59:44
generator: Python Knowledge Base Generator
---

# Conventions

## 개요
이 문서는 `python_kb` 프로젝트의 코딩 컨벤션, 명명 규칙 및 모범 사례를 설명합니다. 이 규칙들을 준수함으로써 코드의 가독성을 높이고, 유지보수를 용이하게 하며, 팀원 간의 협업을 효율적으로 만들 수 있습니다.

## 명명 규칙

### 파일 명명
- 패턴: snake_case를 사용합니다. 파일명은 소문자로 작성하고, 단어 사이는 밑줄(_)로 구분합니다.
- 예시: `main.py`, `file_tree_analyzer.py`, `cache_manager.py`
- 규칙:
    - 모든 Python 파일은 `.py` 확장자를 가집니다.
    - 파일명은 파일의 주요 기능을 나타내는 명확한 이름으로 짓습니다.

### 디렉토리 명명
- 패턴: snake_case를 사용합니다. 디렉토리명은 소문자로 작성하고, 단어 사이는 밑줄(_)로 구분합니다 (현재 프로젝트에서는 디렉토리 구조가 단순하여 snake_case를 강제하지 않음).
- 예시: `python_kb` (프로젝트 루트 디렉토리), `.adalflow` (캐시 디렉토리)
- 규칙:
    - 디렉토리명은 디렉토리의 내용을 명확하게 나타내는 이름으로 짓습니다.
    - 특수한 목적을 가지는 디렉토리(예: 캐시 디렉토리)는 점(.)으로 시작할 수 있습니다.

### 코드 명명

#### 변수
- 컨벤션: snake_case를 사용합니다. 변수명은 소문자로 작성하고, 단어 사이는 밑줄(_)로 구분합니다.
- 예시:
    - `project_path` (main.py)
    - `cache_dir` (cache_manager.py)
    - `file_path` (file_tree_analyzer.py)
- 규칙:
    - 변수명은 변수의 역할을 명확하게 나타내는 이름으로 짓습니다.
    - 짧은 루프 카운터 변수 등에는 `i`, `j` 등의 짧은 이름을 사용할 수 있습니다.
    - 임시 변수에는 `_`를 접두사로 사용할 수 있습니다.

#### 함수/메서드
- 컨벤션: snake_case를 사용합니다. 함수/메서드명은 소문자로 작성하고, 단어 사이는 밑줄(_)로 구분합니다.
- 예시:
    - `analyze_file_tree` (file_tree_analyzer.py)
    - `generate_wiki_page` (wiki_generator.py)
    - `load_from_cache` (cache_manager.py)
- 규칙:
    - 함수/메서드명은 수행하는 작업을 명확하게 나타내는 동사로 시작합니다.
    - Boolean 값을 반환하는 함수의 경우 `is_`, `has_` 등의 접두사를 사용하여 의미를 명확하게 할 수 있습니다.

#### 클래스
- 컨벤션: CamelCase를 사용합니다. 클래스명은 각 단어의 첫 글자를 대문자로 작성합니다.
- 예시:
    - `CacheManager` (cache_manager.py)
    - `GeminiClient` (gemini_client.py)
    - `MarkdownExporter` (markdown_exporter.py)
- 규칙:
    - 클래스명은 클래스의 역할을 명확하게 나타내는 명사로 짓습니다.

#### 상수
- 컨벤션: UPPER_SNAKE_CASE를 사용합니다. 상수명은 모든 글자를 대문자로 작성하고, 단어 사이는 밑줄(_)로 구분합니다.
- 예시:
    - `DEFAULT_CACHE_DIR` (config.py)
    - `EXCLUDED_DIRS` (file_tree_analyzer.py)
- 규칙:
    - 상수명은 상수 값을 명확하게 나타내는 이름으로 짓습니다.

## 코드 구성

### 파일 구조
- 각 파일은 특정 기능을 수행하는 클래스, 함수 및 변수를 포함합니다.
- 관련된 기능들은 하나의 파일에 모아 모듈성을 높입니다.
- 설정 정보는 `config.py`에, 로깅 설정은 `logging_config.py`에, LLM 클라이언트는 `gemini_client.py`에 정의하는 방식으로 관심사를 분리합니다.

### 모듈 구성
- 프로젝트는 여러 모듈로 구성되어 있으며, 각 모듈은 특정 기능을 담당합니다.
- 모듈 간의 의존성을 최소화하여 유지보수성을 높입니다.
- `__init__.py` 파일을 사용하여 디렉토리를 패키지로 만듭니다.

### Import 컨벤션
- 표준 라이브러리, 써드파티 라이브러리, 로컬 모듈 순서로 import 합니다.
- 각 그룹 내에서는 알파벳 순서로 정렬합니다.
- `from module import ...` 구문보다는 `import module` 구문을 사용하는 것을 선호합니다 (네임스페이스 충돌 방지). 다만, 필요한 경우 명확성을 위해 `from ... import ...` 구문을 사용할 수 있습니다.
- 사용하지 않는 import 문은 제거합니다.

```python
# 예시 (main.py)
import argparse
import os

from cache_manager import CacheManager
from config import DEFAULT_CACHE_DIR, LANGUAGES
from file_tree_analyzer import FileTreeAnalyzer
from gemini_client import GeminiClient
from logging_config import setup_logging
from markdown_exporter import MarkdownExporter
from mermaid_validator import MermaidValidator
from prompts import prompts
from readme_parser import ReadmeParser
from wiki_generator import WikiGenerator
```

## 코딩 스타일

### 포맷팅
- PEP 8 스타일 가이드를 준수합니다.
- Black, flake8, pylint 등의 도구를 사용하여 코드 포맷팅 및 스타일을 일관성 있게 유지합니다. (실제 프로젝트에 해당 설정이 적용되어 있는지는 확인 필요)
- 공백 4칸 들여쓰기를 사용합니다.
- 한 줄의 최대 길이는 79자 (또는 120자)를 넘지 않도록 합니다.
- 함수/클래스 정의 위에는 빈 줄 두 개, 함수/메서드 내에서는 빈 줄 한 개를 사용하여 가독성을 높입니다.

### 문서화
- 모든 함수, 클래스, 모듈에는 docstring을 작성합니다.
- docstring은 Google 스타일 가이드를 따릅니다.
- 코드의 복잡한 부분에는 주석을 추가하여 설명을 제공합니다.
- 주석은 코드의 의도를 명확하게 설명해야 하며, 불필요한 주석은 제거합니다.

```python
# 예시 (cache_manager.py)
class CacheManager:
    """캐시 파일을 관리하는 클래스입니다."""

    def __init__(self, cache_dir):
        """CacheManager 클래스의 생성자입니다.

        Args:
            cache_dir (str): 캐시 파일이 저장될 디렉토리 경로입니다.
        """
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
```

### 오류 처리
- try-except 블록을 사용하여 예외를 처리합니다.
- except 블록에서는 구체적인 예외 유형을 명시합니다.
- 예외 발생 시 적절한 로깅을 수행합니다.
- 예상치 못한 예외가 발생할 경우, 프로그램을 종료하는 대신 사용자에게 유용한 오류 메시지를 표시합니다.

```python
# 예시 (main.py)
try:
    project_path = os.path.abspath(args.project_path)
    if not os.path.exists(project_path):
        raise ValueError(f"프로젝트 경로 '{project_path}'가 존재하지 않습니다.")
except ValueError as e:
    logger.error(f"잘못된 프로젝트 경로: {e}")
    sys.exit(1)
```

## 프로젝트-특정 컨벤션

### 테스팅
- (test_example.py 파일이 존재하지만, 자세한 테스트 컨벤션은 정의되지 않음)
- 각 모듈/클래스에 대한 단위 테스트를 작성합니다 (권장).
- pytest 등의 테스트 프레임워크를 사용하여 테스트를 자동화합니다 (권장).
- 테스트 코드는 `test_`로 시작하는 파일에 작성합니다 (권장).

### 설정
- 설정 파일은 `.env` 파일에 저장합니다.
- `python-dotenv` 라이브러리를 사용하여 환경 변수를 로드합니다.
- 설정 값에 대한 기본값은 `config.py` 파일에 정의합니다.

### 빌드 및 배포
- (빌드 및 배포 컨벤션은 현재 정의되지 않음)
- `requirements.txt` 파일을 사용하여 프로젝트 의존성을 관리합니다.
- Docker를 사용하여 애플리케이션을 컨테이너화합니다 (권장).
- CI/CD 파이프라인을 구축하여 빌드, 테스트 및 배포를 자동화합니다 (권장).

## 모범 사례

- 코드 리뷰를 통해 코드 품질을 향상시킵니다.
- 변경 사항을 커밋하기 전에 항상 테스트를 실행합니다.
- 코드 변경 사항에 대한 설명을 명확하게 작성합니다.
- 지속적인 통합 및 배포 (CI/CD)를 사용하여 개발 프로세스를 자동화합니다.
- 정기적으로 코드베이스를 리팩토링하여 유지보수성을 높입니다.

## 예시

### 좋은 예시
```python
# file_tree_analyzer.py
def analyze_file_tree(project_path, excluded_dirs=EXCLUDED_DIRS):
    """프로젝트의 파일 트리를 분석합니다.

    Args:
        project_path (str): 분석할 프로젝트의 경로입니다.
        excluded_dirs (list): 분석에서 제외할 디렉토리 목록입니다.

    Returns:
        dict: 파일 트리 분석 결과입니다.
    """
    file_tree = {}
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in excluded_dirs]  # Exclude dirs in place
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, project_path)
            file_tree[relative_path] = {}  # You might want to add more file info here later
    return file_tree
```

### 피해야 할 안티 패턴
- 너무 긴 함수 또는 클래스 (단일 책임 원칙 위반)
- 과도한 중첩 (가독성 저하)
- 하드코딩된 값 (유연성 부족)
- 주석 없는 복잡한 로직 (이해하기 어려움)
- 예외 처리 없는 코드 (예상치 못한 오류 발생 가능성 증가)
