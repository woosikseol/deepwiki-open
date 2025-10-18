---
title: 규칙 및 규약 (명명 규칙, 규칙 등)
project: python_rag
generated_at: 2025-10-18 15:17:59
generator: Python Knowledge Base Generator
---

# 컨벤션

## 개요
이 문서는 `python_rag` 프로젝트의 코딩 컨벤션, 명명 규칙 및 모범 사례를 설명합니다. 개발자들이 일관된 코드 스타일을 유지하고 프로젝트의 가독성 및 유지보수성을 높이는 데 도움을 주기 위해 작성되었습니다.

## 명명 규칙

### 파일 명명
-   **패턴**:
    *   Python 소스 파일: 소문자 스네이크 케이스 (`snake_case.py`)
    *   문서 및 설정 파일: 대문자 스네이크 케이스 (`UPPER_SNAKE_CASE.md`) 또는 소문자 (`.env`, `requirements.txt`)
-   **예시**:
    *   `main.py`
    *   `api/config.py`
    *   `api/gemini_client.py`
    *   `README.md`
    *   `requirements.txt`
    *   `.env`
-   **규칙**:
    *   Python 모듈 이름은 짧고 모두 소문자여야 하며, 가독성을 위해 밑줄을 사용할 수 있습니다.
    *   주요 문서 파일은 대문자 스네이크 케이스를 사용하여 쉽게 식별할 수 있도록 합니다.

### 디렉토리 명명
-   **패턴**: 소문자 스네이크 케이스 (`snake_case/`)
-   **예시**:
    *   `api/`
    *   `results/`
-   **규칙**:
    *   패키지 및 디렉토리 이름은 모두 소문자여야 하며, 가독성을 위해 밑줄을 사용할 수 있습니다.

### 코드 명명

#### 변수
-   **컨벤션**:
    *   지역 변수 및 함수 매개변수: 소문자 스네이크 케이스 (`snake_case`)
    *   환경 변수 및 전역 상수: 대문자 스네이크 케이스 (`UPPER_SNAKE_CASE`)
-   **예시**:
    *   `language` (CLI 인자)
    *   `top_k_results` (함수 내 변수)
    *   `GEMINI_API_KEY` (환경 변수)
    *   `DEFAULT_LANGUAGE` (환경 변수/상수)

#### 함수/메서드
-   **컨벤션**: 소문자 스네이크 케이스 (`snake_case`)
-   **예시**:
    *   `answer` (RAG 클래스의 메서드)
    *   `main` (main.py의 진입점 함수)
    *   `_load_config` (내부 사용을 위한 private 메서드)

#### 클래스
-   **컨벤션**: 파스칼 케이스 (`PascalCase`)
-   **예시**:
    *   `RAG`
    *   `GeminiClient` (api/gemini_client.py에 정의될 것으로 예상)

#### 상수
-   **컨벤션**: 대문자 스네이크 케이스 (`UPPER_SNAKE_CASE`)
-   **예시**:
    *   `EMBEDDING_DIMENSION` (config.py 또는 .env에서)
    *   `TOP_K_RESULTS` (config.py 또는 .env에서)
    *   `DB_HOST` (환경 변수)

## 코드 구성

### 파일 구조
-   **표준**:
    *   프로젝트 루트에는 `main.py` (CLI 진입점), `requirements.txt`, `.env` 및 주요 문서 파일 (`README.md` 등)이 위치합니다.
    *   핵심 로직은 `api/` 디렉토리 내의 모듈로 구성됩니다.
    *   생성된 결과물은 `results/` 디렉토리에 저장됩니다.
-   **예시**:
    ```
    python_rag/
    ├── api/
    │   ├── __init__.py
    │   ├── config.py          # 설정 관리
    │   ├── prompts.py         # 프롬프트 템플릿
    │   ├── gemini_client.py   # Gemini API 클라이언트
    │   └── rag.py             # RAG 구현
    ├── main.py                # CLI 진입점
    ├── requirements.txt       # Python 의존성
    ├── .env                   # 환경 설정
    └── README.md              # 프로젝트 설명
    ```

### 모듈 구성
-   **패턴**: `api/` 디렉토리는 핵심 애플리케이션 로직을 위한 패키지 역할을 합니다. 각 파일은 특정 기능을 담당하는 모듈로 분리됩니다.
-   **예시**:
    *   `api/config.py`: 환경 변수 로딩 및 애플리케이션 설정 관리
    *   `api/prompts.py`: Gemini 모델에 전달될 프롬프트 템플릿 정의
    *   `api/gemini_client.py`: Gemini API와의 상호작용을 캡슐화
    *   `api/rag.py`: RAG 시스템의 핵심 로직 (임베딩, 검색, 생성) 구현

### 임포트 컨벤션
-   **표준**: 표준 Python 임포트 규칙을 따릅니다.
    *   프로젝트 내부 모듈은 절대 경로 임포트를 사용합니다 (예: `from api.config import settings`).
    *   동일 패키지 내의 모듈 간에는 상대 경로 임포트를 사용할 수 있습니다 (예: `from .prompts import get_rag_prompt`).
    *   외부 라이브러리 임포트는 별도의 그룹으로 분리하고 알파벳 순서로 정렬합니다.

## 코딩 스타일

### 포맷팅
-   **표준**: 이 프로젝트는 상위 `deepwiki-open` 프로젝트와 동일한 컨벤션을 따릅니다. 이는 일반적으로 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 스타일 가이드를 준수함을 의미합니다.
    *   들여쓰기는 4개의 공백을 사용합니다.
    *   한 줄의 최대 길이는 79자 또는 99자로 제한합니다.
    *   연산자 주변에 공백을 사용합니다.

### 문서화
-   **표준**:
    *   코드의 중요한 부분이나 복잡한 로직에는 명확하고 간결한 주석을 사용합니다.
    *   함수, 메서드, 클래스에는 Docstring을 사용하여 목적, 인자, 반환 값 등을 설명하는 것을 권장합니다. (현재 명시된 Docstring 스타일은 없으나, PEP 257을 따르는 것을 권장합니다.)
-   **예시**:
    ```python
    # .env.example 파일의 주석
    # PostgreSQL Configuration
    DB_HOST=localhost
    DB_PORT=5432
    ```

### 에러 핸들링
-   **패턴**: 외부 서비스(데이터베이스, API)와의 상호작용 시 발생할 수 있는 예외를 명시적으로 처리하기 위해 `try-except` 블록을 사용합니다.
-   **예시**:
    ```python
    # README의 문제 해결 섹션에서 암시된 패턴
    try:
        # 데이터베이스 연결 또는 API 호출 로직
        pass
    except SomeDatabaseError:
        print("Error: could not connect to server")
        # 적절한 에러 처리
    except GeminiAPIError:
        print("Error: API key is invalid")
        # 적절한 에러 처리
    ```

## 프로젝트별 컨벤션

### 테스팅
-   **컨벤션**: `pytest` 프레임워크를 사용하여 테스트를 작성합니다.
-   **패턴**: 테스트 파일은 `tests/` 디렉토리 내에 위치하며, `test_*.py` 또는 `*_test.py` 패턴을 따릅니다. (현재 `TODO: Add test suite` 상태이므로, 향후 구현 시 이 컨벤션을 따를 예정입니다.)

### 설정
-   **컨벤션**:
    *   민감한 정보(API 키, DB 자격 증명) 및 환경별 설정은 `.env` 파일을 통해 관리합니다.
    *   `api/config.py` 모듈을 통해 `.env` 파일의 설정을 로드하고 애플리케이션 전반에서 접근할 수 있도록 합니다.
-   **예시**:
    ```bash
    # .env 파일
    GEMINI_API_KEY=your_gemini_api_key_here
    DB_HOST=localhost
    DB_NAME=code_chunks
    ```

### 빌드 및 배포
-   **컨벤션**:
    *   Python 가상 환경 (`.venv`)을 사용하여 프로젝트 의존성을 격리합니다.
    *   `requirements.txt` 파일을 통해 모든 Python 의존성을 명시적으로 관리합니다.
-   **예시**:
    ```bash
    python3.11 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

## 모범 사례
-   **가상 환경 사용**: 항상 프로젝트별 가상 환경을 활성화한 후 작업을 수행합니다.
-   **설정 외부화**: API 키, 데이터베이스 자격 증명 등 민감한 정보는 `.env` 파일을 통해 관리하고, 코드에 직접 하드코딩하지 않습니다.
-   **모듈화**: 코드를 논리적인 단위로 분리하여 `api/` 패키지처럼 모듈화합니다. 이는 코드의 재사용성과 유지보수성을 높입니다.
-   **PEP 8 준수**: Python 코드의 가독성과 일관성을 위해 PEP 8 스타일 가이드를 따릅니다.
-   **명확한 주석 및 Docstring**: 복잡한 로직이나 중요한 함수에는 충분한 주석과 Docstring을 작성하여 코드 이해를 돕습니다.
-   **예외 처리**: 외부 시스템과의 상호작용 시 발생할 수 있는 예외를 예측하고 적절하게 처리하여 애플리케이션의 안정성을 확보합니다.

## 예시

### 좋은 예시
`api/config.py` 파일의 일부 (가상):
```python
# api/config.py
import os
from dotenv import load_dotenv

load_dotenv() # .env 파일 로드

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))
    DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "ko")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    EMBEDDING_DIMENSION: int = int(os.getenv("EMBEDDING_DIMENSION", 384))
    TOP_K_RESULTS: int = int(os.getenv("TOP_K_RESULTS", 10))

settings = Settings()

# main.py 또는 다른 모듈에서 사용 예시
# from api.config import settings
# print(settings.GEMINI_API_KEY)
```

### 피해야 할 안티패턴
-   **하드코딩된 비밀 정보**: API 키나 데이터베이스 비밀번호를 코드 내에 직접 작성하는 것은 보안상 매우 위험합니다. 항상 `.env` 파일을 통해 관리해야 합니다.
-   **모든 것을 한 파일에**: 모든 로직을 `main.py`와 같은 단일 파일에 작성하는 것은 코드의 복잡성을 증가시키고 유지보수를 어렵게 만듭니다. `api/` 디렉토리처럼 기능별로 모듈을 분리해야 합니다.
-   **예외 무시**: `except Exception: pass`와 같이 예외를 단순히 무시하는 것은 문제의 원인을 파악하기 어렵게 만들고 애플리케이션의 안정성을 저해합니다. 항상 구체적인 예외를 처리하고 적절한 로깅 또는 사용자 피드백을 제공해야 합니다.
-   **일관성 없는 명명**: 변수, 함수, 클래스 이름에 일관성 없는 명명 규칙을 사용하는 것은 코드 가독성을 크게 떨어뜨립니다. 위에 명시된 명명 규칙을 따르도록 합니다.