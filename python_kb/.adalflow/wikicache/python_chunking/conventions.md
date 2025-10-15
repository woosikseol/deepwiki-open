---
title: 규칙 및 규약 (명명 규칙, 규칙 등)
project: python_chunking
generated_at: 2025-10-16 00:42:39
generator: Python Knowledge Base Generator
---

# 컨벤션

## 개요
이 문서는 `python_chunking` 프로젝트의 개발자들이 코드를 일관성 있게 작성하고 유지보수성을 높일 수 있도록 코딩 컨벤션과 표준을 안내합니다. 이 가이드는 프로젝트의 현재 코드베이스를 분석하여 식별된 패턴과 Python 커뮤니티의 일반적인 모범 사례를 기반으로 합니다.

## 명명 컨벤션

### 파일 명명
-   **패턴**: 모든 Python 파일(`.py`)은 소문자 스네이크 케이스(`snake_case`)를 사용합니다. 스크립트 파일도 이 규칙을 따릅니다.
-   **예시**:
    -   `main.py`
    -   `db_test.py`
    -   `drop_table.py`
    -   `setup_vendor.py`
    -   `build_parsers.py`
    -   `embeddings_provider.py`
    -   `pgvector_index.py`
    -   `count_tokens.py`
    -   `__init__.py` (패키지 초기화 파일)
-   **규칙**:
    -   파일 이름은 모두 소문자로 작성합니다.
    -   단어는 밑줄(`_`)로 구분합니다.
    -   간결하고 파일의 목적을 명확히 나타내야 합니다.

### 디렉토리 명명
-   **패턴**: 디렉토리 이름은 모두 소문자 스네이크 케이스(`snake_case`)를 사용합니다.
-   **예시**:
    -   `core/`
    -   `embeddings/`
    -   `indexing/`
    -   `chunk/`
    -   `llm/`
    -   `util/`
    -   `vendor/`
    -   `test_files/`
-   **규칙**:
    -   디렉토리 이름은 모두 소문자로 작성합니다.
    -   단어는 밑줄(`_`)로 구분합니다.
    -   모듈의 논리적 그룹화를 반영해야 합니다.

### 코드 명명

#### 변수
-   **컨벤션**: 소문자 스네이크 케이스(`snake_case`)를 사용합니다.
-   **예시**:
    ```python
    embeddings_provider = EmbeddingsProvider()
    file_item = PathAndCacheKey(path="example.py", cache_key="hash123")
    chunks = await index.get_chunks(file_item, "your code content here")
    n_retrieve = 10
    ```

#### 함수/메서드
-   **컨벤션**: 소문자 스네이크 케이스(`snake_case`)를 사용합니다.
-   **예시**:
    ```python
    async def main():
    await index.initialize()
    async def get_chunks(self, file_item, content: str):
    await index.insert_chunks(chunks, embeddings)
    results = await index.retrieve("calculator class", n_retrieve=10)
    ```

#### 클래스
-   **컨벤션**: 파스칼 케이스(PascalCase, 각 단어의 첫 글자를 대문자로 하는 카멜 케이스)를 사용합니다.
-   **예시**:
    ```python
    class EmbeddingsProvider:
    class PgVectorIndex:
    class PathAndCacheKey:
    ```

#### 상수
-   **컨벤션**: 명확한 상수는 제공된 코드베이스에서 직접 확인되지 않았지만, Python 표준에 따라 모든 문자를 대문자로 하고 단어를 밑줄(`_`)로 구분하는 `UPPER_SNAKE_CASE`를 사용하는 것이 좋습니다.
-   **예시 (가상)**:
    ```python
    MAX_CHUNK_SIZE = 1024
    DEFAULT_EMBEDDING_DIMENSION = 384
    ```

## 코드 조직

### 파일 구조
-   **핵심 로직**: `core/` 디렉토리 아래에 프로젝트의 주요 로직이 모듈별로 구성됩니다.
    -   `core/index.py`: 핵심 데이터 타입 정의.
    -   `core/embeddings/`: 임베딩 관련 로직.
    -   `core/indexing/`: 인덱싱 및 청킹 로직.
    -   `core/llm/`: LLM 관련 유틸리티 (토큰 카운팅 등).
    -   `core/util/`: 범용 유틸리티 함수.
-   **스크립트**: 최상위 디렉토리에 실행 가능한 스크립트(`main.py`, `db_test.py`, `setup_vendor.py` 등)를 배치합니다.
-   **외부 의존성**: `vendor/` 디렉토리는 Tree-sitter 파서와 같은 외부 소스 코드를 관리합니다.
-   **테스트 파일**: `test_files/` 디렉토리는 예시 코드 파일 및 테스트에 사용되는 파일을 포함합니다.

### 모듈 조직
-   각 서브디렉토리는 `__init__.py` 파일을 포함하여 Python 패키지로 구성됩니다.
-   관련 기능은 동일한 모듈 또는 패키지 내에 그룹화됩니다. 예를 들어, `core/indexing/chunk/`는 다양한 청킹 전략을 위한 모듈을 포함합니다.
-   모듈은 단일 책임 원칙을 따르도록 노력합니다. 예를 들어, `count_tokens.py`는 토큰 카운팅에만 집중합니다.

### 임포트 컨벤션
-   **절대 임포트**: 프로젝트 루트 또는 `core`와 같은 최상위 패키지에서 시작하는 절대 임포트를 선호합니다.
    ```python
    from core.indexing.pgvector_index import PgVectorIndex
    from core.embeddings.embeddings_provider import EmbeddingsProvider
    from core.index import PathAndCacheKey
    ```
-   **표준 라이브러리**: 표준 라이브러리 임포트는 외부 라이브러리 임포트보다 먼저 배치하고, 알파벳 순서를 따릅니다.
-   **외부 라이브러리**: `asyncio`와 같은 외부 라이브러리 임포트는 프로젝트 내부 모듈 임포트보다 먼저 배치합니다.
-   **상대 임포트**: 같은 패키지 내에서는 상대 임포트(`from .chunk import basic`)를 사용할 수 있으나, 가독성을 위해 최소화하는 것이 좋습니다. 현재 코드베이스에서는 주로 절대 임포트가 사용됩니다.

## 코딩 스타일

### 포맷팅
-   **들여쓰기**: 4개의 스페이스를 사용하여 들여쓰기합니다. 탭은 사용하지 않습니다.
-   **줄 길이**: PEP 8 권장 사항을 따르며, 한 줄의 최대 길이는 79~120자 사이로 유지하도록 노력합니다.
-   **공백**:
    -   연산자 주위에 하나의 공백을 사용합니다 (`a = b + c`).
    -   함수 정의 시 매개변수와 기본값 사이에 공백을 사용합니다 (`def func(param1, param2=None):`).
    -   콤마(`,`), 세미콜론(`;`), 콜론(`:`) 뒤에는 공백을 사용합니다.
-   **빈 줄**:
    -   최상위 함수 및 클래스 정의 사이에는 두 개의 빈 줄을 사용합니다.
    -   클래스 내 메서드 정의 사이에는 하나의 빈 줄을 사용합니다.
    -   코드 블록의 논리적 부분을 구분하기 위해 빈 줄을 사용할 수 있습니다.

### 문서화
-   **주석**: 코드의 복잡하거나 중요한 부분에 설명을 추가하여 가독성을 높입니다.
    -   예시: `# 임베딩 프로바이더 초기화`, `# PgVector 인덱스 초기화`
-   **독스트링(Docstrings)**: 함수, 메서드, 클래스 및 모듈에 대한 독스트링을 작성하여 목적, 인자, 반환 값 등을 설명합니다. (제공된 스니펫에는 직접적인 독스트링 예시가 없지만, Python 모범 사례를 따르는 것이 좋습니다.)
    -   예시 (가상):
        ```python
        def get_chunks(self, file_item, content: str):
            """
            주어진 파일 아이템과 내용에 대해 코드 청크를 생성합니다.

            Args:
                file_item (PathAndCacheKey): 파일의 경로 및 캐시 키.
                content (str): 청킹할 파일의 전체 내용.

            Returns:
                list[Chunk]: 생성된 코드 청크 목록.
            """
            # ... 구현 ...
        ```

### 에러 핸들링
-   **예외 처리**: `try-except` 블록을 사용하여 예상치 못한 오류를 적절히 처리합니다.
-   **구체적인 예외**: 가능한 한 일반적인 `Exception` 대신 `FileNotFoundError`, `ValueError` 등 구체적인 예외를 처리합니다.
-   **로깅**: 에러 발생 시 적절한 로깅을 통해 문제 진단에 필요한 정보를 기록합니다. (제공된 코드 스니펫에는 로깅 예시가 없지만, 일반적인 Python 프로젝트의 모범 사례입니다.)

## 프로젝트-특정 컨벤션

### 테스트
-   **테스트 스크립트**: `db_test.py`와 같은 별도의 스크립트를 사용하여 특정 기능(예: 데이터베이스 연결 및 검색)을 테스트합니다.
-   **테스트 파일 디렉토리**: `test_files/` 디렉토리에 다양한 언어의 예시 코드 파일을 포함하여 청킹 시스템의 동작을 검증합니다.
-   **자동화된 테스트**: 명시적인 테스트 프레임워크(예: `pytest`)는 언급되지 않았으나, 추후 도입을 고려하여 테스트 커버리지를 확보하는 것이 좋습니다.

### 설정
-   **의존성 관리**: `requirements.txt` 파일을 사용하여 프로젝트의 Python 의존성을 관리합니다. `pip install -r requirements.txt` 명령으로 설치합니다.
-   **외부 파서 설정**:
    -   `setup_vendor.py`: Tree-sitter 파서 소스 코드를 다운로드합니다.
    -   `build_parsers.py`: 다운로드된 파서 소스를 컴파일하여 `.so` 파일을 생성합니다.
-   **데이터베이스 설정**: `psql` 명령어를 통해 PostgreSQL 데이터베이스와 `pgvector` 확장을 수동으로 설정합니다. `CREATE TABLE` 문은 `README.md`에 명시되어 있습니다.
-   **환경 변수**: 민감한 정보(예: 데이터베이스 접속 정보)는 환경 변수를 통해 관리하는 것이 좋습니다. (현재 코드베이스에는 직접적인 예시가 없습니다.)

### 빌드 및 배포
-   **가상환경**: `python -m venv .venv`를 사용하여 가상환경을 설정하고 활성화하는 것을 권장합니다.
-   **설치 스크립트**: `setup_vendor.py`, `build_parsers.py`와 같은 스크립트를 사용하여 외부 의존성을 준비합니다.
-   **실행 스크립트**: `main.py`를 통해 디렉토리 인덱싱과 같은 주요 기능을 실행합니다.
-   **데이터 관리**: `drop_table.py` 스크립트를 통해 데이터베이스 테이블을 삭제하거나 데이터를 정리할 수 있습니다.

## 모범 사례

-   **PEP 8 준수**: Python 코드 작성 시 PEP 8 스타일 가이드를 최대한 준수합니다.
-   **명확하고 간결한 코드**: 가독성을 높이기 위해 코드를 명확하고 간결하게 작성합니다.
-   **재사용성**: 반복되는 로직은 함수나 클래스로 추상화하여 재사용성을 높입니다.
-   **모듈화**: 각 모듈이 단일 책임을 가지도록 설계하여 유지보수성을 향상시킵니다.
-   **비동기 프로그래밍**: `asyncio`를 활용하는 비동기 코드에서는 `await`를 적절히 사용하여