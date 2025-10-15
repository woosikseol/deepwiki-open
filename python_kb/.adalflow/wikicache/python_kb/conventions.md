---
title: 규칙 및 규약 (명명 규칙, 규칙 등)
project: python_kb
generated_at: 2025-10-16 00:51:36
generator: Python Knowledge Base Generator
---

# 컨벤션

## 개요
이 문서는 `python_kb` 프로젝트의 개발자들이 코드를 작성하고 유지보수할 때 따라야 할 명명 규칙, 코딩 스타일, 코드 구성 및 기타 표준을 정의합니다. 이러한 컨벤션을 준수함으로써 코드의 가독성, 일관성 및 유지보수성을 향상시키고, 협업을 원활하게 합니다.

## 명명 규칙

### 파일 명명
-   **패턴**: 모든 Python 소스 파일은 소문자로 작성되며, 여러 단어는 밑줄(`_`)로 구분하는 스네이크 케이스(`snake_case`)를 사용합니다.
-   **예시**:
    -   `main.py`
    -   `config.py`
    -   `file_tree_analyzer.py`
    -   `gemini_client.py`
    -   `wiki_generator.py`
    -   `test_example.py`
-   **규칙**:
    -   `.py` 확장자를 사용합니다.
    -   파일 이름은 해당 파일의 주요 기능을 명확하게 나타내야 합니다.

### 디렉토리 명명
-   **패턴**: 디렉토리 이름은 일반적으로 소문자를 사용하며, 여러 단어는 밑줄(`_`)로 구분하는 스네이크 케이스(`snake_case`)를 사용합니다. 프로젝트의 루트 디렉토리는 소문자 단일 이름을 사용합니다.
-   **예시**:
    -   `python_kb/` (프로젝트 루트 디렉토리)
    -   `.adalflow/wikicache/` (내부 캐시 디렉토리)
-   **규칙**:
    -   디렉토리 이름은 해당 디렉토리의 내용을 명확하게 설명해야 합니다.
    -   숨겨진 디렉토리(예: `.adalflow`)는 점(`.`)으로 시작합니다.

### 코드 명명

#### 변수
-   **컨벤션**: 변수 이름은 소문자로 작성되며, 여러 단어는 밑줄(`_`)로 구분하는 스네이크 케이스(`snake_case`)를 사용합니다.
-   **예시**:
    -   `project_path`
    -   `language`
    -   `no_cache`
    -   `gemini_api_key`
    -   `is_verbose`
    -   `file_content`

#### 함수/메서드
-   **컨벤션**: 함수 및 메서드 이름은 소문자로 작성되며, 여러 단어는 밑줄(`_`)로 구분하는 스네이크 케이스(`snake_case`)를 사용합니다.
-   **예시**:
    -   `analyze_project_structure()` (추정)
    -   `generate_wiki_pages()` (추정)
    -   `load_config()` (추정)
    -   `parse_readme()` (추정)
    -   `validate_mermaid_syntax()` (추정)

#### 클래스
-   **컨벤션**: 클래스 이름은 각 단어의 첫 글자를 대문자로 하는 파스칼 케이스(`PascalCase`) 또는 캡워드(`CapWords`)를 사용합니다.
-   **예시**:
    -   `FileTreeAnalyzer` (추정)
    -   `GeminiClient` (추정)
    -   `WikiGenerator` (추정)
    -   `CacheManager` (추정)
    -   `MarkdownExporter` (추정)
    -   `MermaidValidator` (추정)

#### 상수
-   **컨벤션**: 전역 상수는 모든 글자를 대문자로 작성하며, 여러 단어는 밑줄(`_`)로 구분하는 `ALL_CAPS_WITH_UNDERSCORES`를 사용합니다.
-   **예시**:
    -   `GEMINI_API_KEY`
    -   `DB_HOST`
    -   `DB_PORT`
    -   `CACHE_DIR_NAME` (추정)
    -   `DEFAULT_LANGUAGE` (추정)

## 코드 구성

### 파일 구조
프로젝트는 기능별로 모듈화된 Python 파일을 포함하는 표준 Python 패키지 구조를 따릅니다.
-   `__init__.py`: 패키지 초기화를 나타냅니다.
-   `main.py`: 애플리케이션의 메인 진입점입니다.
-   `config.py`: 애플리케이션의 설정 및 환경 변수 로딩을 담당합니다.
-   `prompts.py`: LLM 프롬프트 템플릿을 정의합니다.
-   각 `_*.py` 파일은 특정 기능(예: `file_tree_analyzer.py`, `gemini_client.py`, `wiki_generator.py`)을 캡슐화합니다.
-   `requirements.txt`: 프로젝트의 모든 Python 의존성을 나열합니다.

### 모듈 구성
각 `.py` 파일은 특정 책임 영역을 담당하는 독립적인 모듈로 구성됩니다. 예를 들어:
-   `file_tree_analyzer.py`는 프로젝트 파일 구조 분석에 집중합니다.
-   `gemini_client.py`는 Google Gemini LLM과의 상호작용을 처리합니다.
-   `wiki_generator.py`는 Wiki 페이지 생성의 핵심 로직을 포함합니다.
이러한 모듈화는 코드의 재사용성을 높이고, 각 부분의 독립적인 테스트를 용이하게 합니다.

### 임포트 컨벤션
Python의 표준 PEP 8 권장 사항을 따릅니다.
-   **순서**:
    1.  표준 라이브러리 임포트 (예: `os`, `sys`, `json`)
    2.  서드파티 라이브러리 임포트 (예: `google.generativeai`, `dotenv`)
    3.  로컬 애플리케이션/라이브러리 관련 임포트 (예: `from . import config`, `from .cache_manager import CacheManager`)
-   **스타일**:
    -   모든 임포트는 파일의 맨 위에 위치합니다.
    -   절대 임포트(`from project_name import module`)를 선호합니다.
    -   관련 임포트 그룹 사이에는 한 줄을 비워둡니다.

## 코딩 스타일

### 포맷팅
-   **PEP 8 준수**: 모든 코드는 Python Enhancement Proposal 8 (PEP 8) 스타일 가이드를 따릅니다.
-   **들여쓰기**: 4개의 스페이스를 사용하여 들여쓰기합니다. 탭은 사용하지 않습니다.
-   **최대 라인 길이**: 명시적으로 정의되어 있지 않지만, 일반적으로 79~99자 이내를 권장하여 가독성을 높입니다.
-   **공백**: 연산자 주위, 콤마 뒤 등에 적절한 공백을 사용합니다.
-   **빈 줄**: 논리적으로 구분되는 코드 블록 사이에 빈 줄을 사용하여 가독성을 높입니다.

### 문서화
-   **독스트링(Docstrings)**: 모든 모듈, 클래스, 공개 함수 및 메서드에는 독스트링을 포함해야 합니다. 독스트링은 해당 코드의 목적, 인수, 반환 값 및 예외를 설명해야 합니다.
    -   **예시**:
        ```python
        def analyze_project_structure(project_path: str) -> dict:
            """
            주어진 프로젝트 경로의 파일 구조를 분석하고 계층적 맵을 반환합니다.

            Args:
                project_path (str): 분석할 프로젝트의 루트 경로.

            Returns:
                dict: 프로젝트의 파일 및 디렉토리 구조를 나타내는 딕셔너리.
            """
            # ... 구현 ...
        ```
-   **주석**: 복잡하거나 비직관적인 코드 섹션에 대한 설명을 위해 인라인 주석(`_#_`)을 사용합니다. 주석은 코드의 "왜"를 설명해야 하며, "무엇"은 코드 자체로 명확해야 합니다.

### 오류 처리
-   **예외 처리**: `try...except` 블록을 사용하여 예상되는 오류를 적절하게 처리하고, 사용자에게 의미 있는 피드백을 제공합니다.
-   **로깅**: `logging_config.py`에 정의된 로깅 설정을 활용하여 애플리케이션의 중요한 이벤트, 경고 및 오류를 기록합니다. 민감한 정보는 로그에 포함하지 않도록 주의합니다.
-   **특정 예외**: 가능한 경우 일반 `Exception` 대신 `FileNotFoundError`, `ValueError` 등과 같은 특정 예외를 포착합니다.

## 프로젝트별 컨벤션

### 테스팅
-   **테스트 파일 명명**: 테스트 파일은 `test_*.py` 패턴을 따릅니다 (예: `test_example.py`).
-   **테스트 함수 명명**: 테스트 함수는 `test_` 접두사로 시작해야 합니다 (예: `test_basic_functionality`).
-   **테스트 프레임워크**: `pytest`와 같은 표준 Python 테스트 프레임워크를 사용하는 것으로 보입니다.

### 환경 설정
-   **환경 변수**: `python-dotenv` 라이브러리를 사용하여 `.env` 파일에서 환경 변수를 로드합니다. 민감한 정보(예: `GEMINI_API_KEY`)는 환경 변수로 관리해야 합니다.
-   **설정 파일**: `config.py` 파일은 환경 변수를 로드하고 애플리케이션 전반에 걸쳐 사용되는 설정 값을 관리합니다.
-   **의존성 관리**: `requirements.txt` 파일을 사용하여