---
title: 규칙 및 규약 (명명 규칙, 규칙 등)
project: python_kb
generated_at: 2025-10-19 18:37:42
generator: Python Knowledge Base Generator
---

# 컨벤션

## 개요
이 문서는 `python_kb` 프로젝트의 개발자들이 코드를 작성하고 유지보수할 때 따라야 할 명명 규칙, 코딩 스타일, 코드 구성 및 기타 표준을 정의합니다. 일관된 컨벤션은 코드의 가독성을 높이고, 협업을 용이하게 하며, 장기적인 유지보수 비용을 절감하는 데 기여합니다.

## 명명 규칙

### 파일 명명
-   **패턴**: Python 소스 파일은 `snake_case.py` 패턴을 따릅니다. 기타 파일은 용도에 따라 `kebab-case.txt` 또는 `UPPER_CASE.md`를 사용합니다.
-   **예시**:
    -   `main.py`
    -   `cache_manager.py`
    -   `llm_mermaid_validator.py`
    -   `requirements.txt`
    -   `README.md`
    -   `.env.example`
-   **규칙**:
    -   Python 모듈 파일명은 모두 소문자로 작성하며, 여러 단어는 밑줄(`_`)로 구분합니다.
    -   설정 파일이나 의존성 파일은 하이픈(`-`)을 사용하여 단어를 구분할 수 있습니다.
    -   주요 문서 파일은 대문자로 시작하거나 모두 대문자로 작성합니다.

### 디렉토리 명명
-   **패턴**: 프로젝트 내부의 코드 관련 디렉토리는 없지만, 캐시 및 가상 환경 관련 디렉토리는 `snake_case/` 또는 `.hidden_directory/` 패턴을 따릅니다.
-   **예시**:
    -   `python_kb/` (프로젝트 루트)
    -   `__pycache__/` (Python 인터프리터 생성)
    -   `.adalflow/wikicache/` (프로젝트 생성 캐시 및 결과물)
    -   `.venv/` (가상 환경)
-   **규칙**:
    -   디렉토리명은 소문자로 작성하며, 여러 단어는 밑줄(`_`)로 구분합니다.
    -   숨겨진 디렉토리(예: 캐시, 설정)는 이름 앞에 점(`.`)을 붙입니다.

### 코드 명명

#### 변수
-   **컨벤션**: `snake_case`를 사용합니다. 변수의 목적을 명확히 설명하는 이름을 사용합니다.
-   **예시**:
    ```python
    project_path = "../python_chunking/"
    is_cache_enabled = True
    output_language = "en"
    ```

#### 함수/메서드
-   **컨벤션**: `snake_case`를 사용합니다. 동사-명사 형태로 함수의 동작을 명확히 나타냅니다.
-   **예시**:
    ```python
    def analyze_project_structure(path: str) -> dict:
        # ...
        pass

    def generate_wiki_page(prompt: str, data: dict) -> str:
        # ...
        pass

    class CacheManager:
        def load_cache(self, project_name: str) -> dict:
            # ...
            pass
    ```

#### 클래스
-   **컨벤션**: `CamelCase` (PascalCase)를 사용합니다. 명사 형태로 클래스의 역할을 명확히 나타냅니다.
-   **예시**:
    ```python
    class FileTreeAnalyzer:
        # ...
        pass

    class GeminiClient:
        # ...
        pass

    class WikiGenerator:
        # ...
        pass
    ```

#### 상수
-   **컨벤션**: `UPPER_SNAKE_CASE`를 사용합니다. 모듈 수준에서 변경되지 않는 값을 정의할 때 사용합니다.
-   **예시**:
    ```python
    # config.py 또는 .env에서 로드된 값
    GEMINI_API_KEY = "AIzaSyCrt6pBUq-2YfeputHnBVqXHBCRc0_YbtQ"
    DEFAULT_LANGUAGE = "ko"
    CACHE_DIR_NAME = ".adalflow/wikicache"
    ```

## 코드 구성

### 파일 구조
-   `python_kb` 프로젝트의 모든 핵심 Python 소스 파일(`*.py`)은 프로젝트의 루트 디렉토리에 평면적으로 배치됩니다.
-   설정 파일(`config.py`, `.env`), 의존성 파일(`requirements.txt`), 문서(`README.md`) 또한 루트 디렉토리에 위치합니다.
-   테스트 파일은 `test_` 접두사를 사용하여 루트 디렉토리에 배치됩니다.
-   생성된 캐시 및 Markdown 출력 파일은 `python_kb/.adalflow/wikicache/<project_name>/` 경로에 저장됩니다.

### 모듈 구성
-   각 `.py` 파일은 특정 기능 또는 책임 영역을 담당하는 독립적인 모듈로 구성됩니다.
    -   예: `file_tree_analyzer.py`는 파일 구조 분석, `gemini_client.py`는 Gemini API 통신, `wiki_generator.py`는 Wiki 생성 로직을 담당합니다.
-   `__init__.py` 파일은 `python_kb` 디렉토리가 Python 패키지임을 나타냅니다.

### 임포트 컨벤션
-   임포트 문은 파일 상단에 위치하며, 다음 순서를 따릅니다 (PEP 8 권장):
    1.  표준 라이브러리 임포트 (예: `os`, `sys`, `logging`)
    2.  서드파티 라이브러리 임포트 (예: `google.generativeai`, `dotenv`)
    3.  로컬 프로젝트 모듈 임포트 (예: `from config import settings`, `from . import cache_manager`)
-   각 그룹 사이에는 한 줄의 공백을 두어 구분합니다.
-   절대 임포트를 선호하며, 필요한 경우 상대 임포트를 사용합니다.

## 코딩 스타일

### 포맷팅
-   **PEP 8 준수**: Python 코드 스타일 가이드인 PEP 8을 따릅니다.
    -   **들여쓰기**: 4개의 공백을 사용하여 들여쓰기합니다. 탭은 사용하지 않습니다.
    -   **줄 길이**: 한 줄의 최대 길이는 79자 또는 99자로 제한합니다.
    -   **공백**: 연산자 주변, 콤마 뒤 등에 적절한 공백을 사용합니다.
    -   **빈 줄**: 함수, 클래스 정의 사이, 논리적 블록 사이에 빈 줄을 사용하여 가독성을 높입니다.
-   **자동 포매터**: 명시적인 자동 포매터(예: Black, autopep8)는 언급되지 않았지만, PEP 8 준수를 위해 사용을 권장합니다.

### 문서화
-   **README.md**: 프로젝트의 개요, 설치, 사용법, 구조 등 전반적인 정보를 상세히 기술합니다.
-   **Docstrings**: 모든 모듈, 클래스, 함수, 메서드에는 PEP 257을 따르는 Docstring을 작성합니다. Docstring은 해당 코드 블록의 목적, 인자, 반환 값 등을 설명해야 합니다.
-   **주석**: 복잡한 로직이나 특정 구현 결정에 대한 설명을 위해 인라인 주석을 사용합니다. "왜" 그렇게 했는지에 초점을 맞춥니다.
-   **타입 힌트**: Python 3.5+의 타입 힌트(Type Hints)를 적극적으로 사용하여 함수의 인자와 반환 값의 타입을 명시합니다.

### 에러 핸들링
-   **예외 처리**: 예상되는 오류 상황에 대해서는 `try-except` 블록을 사용하여 예외를 명확하게 처리합니다.
-   **구체적인 예외**: 가능한 한 `Exception`과 같은 일반적인 예외보다는 `FileNotFoundError`, `ValueError`, `requests.exceptions.RequestException` 등 구체적인 예외 타입을 잡습니다.
-   **로깅**: `logging_config.py`를 통해 설정된 로깅 시스템을 사용하여 오류, 경고, 정보 메시지를 기록합니다. 사용자에게 직접적인 오류 메시지를 보여주기보다는 로그를 통해 문제를 진단할 수 있도록 합니다.
-   **재시도 로직**: 외부 API 호출 등 불안정한 작업에는 적절한 재시도(retry) 로직을 구현할 수 있습니다.

## 프로젝트-특정 컨벤션

### 테스팅
-   **테스트 파일 명명**: 테스트 파일은 `test_` 접두사를 사용하여 명명합니다 (예: `test_example.py`, `test_llm_validator.py`).
-   **테스트 함수/메서드 명명**: 테스트 함수 또는 메서드도 `test_` 접두사를 사용합니다.
-   **테스트 위치**: 테스트 파일은 현재 프로젝트의 루트 디렉토리에 위치합니다.
-   **테스트 프레임워크**: `pytest` 또는 `unittest` 프레임워크를 사용하는 것으로 보입니다.

### 설정
-   **환경 변수**: 민감한 정보(API 키, 데이터베이스 자격 증명)는 `.env` 파일을 통해 환경 변수로 관리하며, `python-dotenv` 라이브러리를 사용하여 로드합니다.
-   **애플리케이션 설정**: `config.py` 파일은 애플리케이션 전반에 걸쳐 사용되는 일반적인 설정 값(예: 캐시 경로, 기본 언어)을 정의합니다.
-   `.env.example` 파일은 필요한 환경 변수의 목록과 예시를 제공하여 다른 개발자가 쉽게 환경을 설정할 수 있도록 합니다.

### 빌드 및 배포
-   **의존성 관리**: 모든 Python 패키지 의존성은 `requirements.txt` 파일에 명시하며, `pip install -r requirements.txt` 명령으로 설치합니다.
-   **가상 환경**: 프로젝트 개발 및 실행 시 반드시 가상 환경(`venv` 또는 `.venv`)을 활성화하여 사용합니다.
-   **Mermaid CLI**: Mermaid 다이어그램 렌더링을 위해 `npx puppeteer browsers install chrome` 명령을 통해 Puppeteer Chrome을 설치하고 `.puppeteerrc.cjs`를 설정해야 합니다.

## 모범 사례

-   **PEP 8 준수**: 항상 PEP 8 스타일 가이드를 따르도록 노력합니다.
-   **의미 있는 이름**: 변수, 함수, 클래스 이름은 그 목적과 역할을 명확히 나타내야 합니다.
-   **명확한 문서화**: Docstring과 주석을 통해 코드의 의도를 명확히 설명합니다.
-   **작고 응집력 있는 함수**: 각 함수는 하나의 명확한 작업을 수행하도록 작고 집중적으로 만듭니다.
-   **타입 힌트 사용**: 코드의 가독성과 유지보수성을 높이기 위해 타입 힌트를 적극적으로 사용합니다.
-   **예외 처리**: 예상되는 모든 오류 상황에 대해 견고한 예외 처리 로직을 구현합니다.
-   **로깅 활용**: `print()` 대신 `logging` 모듈을 사용하여 애플리케이션의 상태와 오류를 기록합니다.

## 예시

### 좋은 예시
다음은 `python_kb` 프로젝트의 컨벤션을 따르는 가상의 코드 예시입니다.

```python
import logging
from typing import Optional, Dict

from config import settings
from .cache_manager import CacheManager

logger = logging.getLogger(__name__)

class ProjectAnalyzer:
    """
    주어진 프로젝트 경로의 파일 구조를 분석하고 메타데이터를 추출하는 클래스입니다.
    """
    DEFAULT_EXCLUDE_PATTERNS = settings.EXCLUDE_PATTERNS

    def __init__(self, project_root_path: str, cache_manager: CacheManager):
        self.project_root_path = project_root_path
        self.cache_manager = cache_manager
        logger.debug(f"ProjectAnalyzer 초기화: {project_root_path}")

    def analyze_structure(self, force_rebuild: bool = False) -> Optional[Dict]:
        """
        프로젝트의 파일 구조를 분석하고 결과를 반환합니다.
        캐시가 활성화되어 있고 force_rebuild가 False이면 캐시된 데이터를 사용합니다.

        Args:
            force_rebuild (bool): 캐시를 무시하고 강제로 재분석할지 여부.

        Returns:
            Optional[Dict]: 분석된 프로젝트 구조 데이터 또는 None.
        """
        if not force_rebuild and self.cache_manager.is_cache_valid(self.project_root_path, "structure"):
            logger.info(f"캐시된 프로젝트 구조 데이터 로드: {self.project_root_path}")
            return self.cache_manager.load_cache(self.project_root_path, "structure")

        try:
            # 실제 파일 시스템 분석 로직 (가상)
            structure_data = {
                "name": self.project_root_path.split('/')[-1],
                "files": ["main.py", "config.py"],
                "directories": ["__pycache__"]
            }
            self.cache_manager.save_cache(self.project_root_path, "structure", structure_data)
            logger.info(f"프로젝트 구조 분석 완료 및 캐시 저장: {self.project_root_path}")
            return structure_data
        except FileNotFoundError:
            logger.error(f"프로젝트 경로를 찾을 수 없습니다: {self.project_root_path}")
            return None
        except Exception as e:
            logger.exception(f"프로젝트 구조 분석 중 예외 발생: {e}")
            return None

```

### 피해야 할 안티패턴
-   **일반적인 예외 처리**: `except Exception:`과 같이 모든 예외를 한 번에 잡는 것은 디버깅을 어렵게 하고 예상치 못한 오류를 숨길 수 있습니다. 항상 구체적인 예외를 잡도록 노력합니다.
-   **매직 넘버/문자열**: 코드 내에 의미를 알 수 없는 숫자나 문자열 리터럴을 직접 사용하는 대신, 상수로 정의하여 사용합니다.
-   **긴 함수/메서드**: 한 함수나 메서드가 너무 많은 책임을 지거나 너무 길어지는 것을 피합니다. 기능을 분리하여 작고 재사용 가능한 단위로 만듭니다.
-   **불분명한 변수명**: `a`, `b`, `temp`와 같이 의미를 알 수 없는 변수명 대신, `file_path`, `is_processed`, `temporary_data`와 같이 명확한 이름을 사용합니다.
-   **주석 없는 코드**: 복잡한 로직이나 비즈니스 규칙이 포함된 코드에는 반드시 주석이나 Docstring을 추가하여 의도를 설명합니다.