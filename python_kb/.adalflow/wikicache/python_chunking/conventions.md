---
title: 규칙 및 규약 (명명 규칙, 규칙 등)
project: python_chunking
generated_at: 2025-10-18 16:15:29
generator: Python Knowledge Base Generator
---

# 컨벤션

## 개요
이 문서는 `python_chunking` 프로젝트의 개발자들이 코드를 작성하고 유지보수할 때 따라야 할 코딩 컨벤션, 명명 규칙 및 모범 사례를 설명합니다. 일관된 코딩 스타일은 코드 가독성을 높이고, 협업을 용이하게 하며, 잠재적인 오류를 줄이는 데 기여합니다.

## 명명 컨벤션

### 파일 명명
-   **패턴**: 모든 Python 소스 파일은 `snake_case`를 사용합니다.
-   **예시**:
    -   `embeddings_provider.py`
    -   `pgvector_index.py`
    -   `count_tokens.py`
    -   `tree_sitter.py`
    -   `main.py`
    -   `setup_vendor.py`
    -   `build_parsers.py`
-   **규칙**:
    -   파일 이름은 소문자와 밑줄(`_`)만 사용합니다.
    -   파일의 목적을 명확하게 나타내는 이름을 사용합니다.

### 디렉토리 명명
-   **패턴**: 모든 디렉토리 이름은 `snake_case`를 사용합니다.
-   **예시**:
    -   `core/`
    -   `embeddings/`
    -   `indexing/`
    -   `llm/`
    -   `util/`
    -   `chunk/`
    -   `vendor/`
    -   `test_files/`
-   **규칙**:
    -   디렉토리 이름은 소문자와 밑줄(`_`)만 사용합니다.
    -   디렉토리가 포함하는 모듈이나 기능의 그룹을 명확하게 나타내는 이름을 사용합니다.

### 코드 명명

#### 변수
-   **컨벤션**: 변수 이름은 `snake_case`를 사용합니다. 짧고 설명적인 이름을 선호합니다.
-   **예시**:
    -   `embeddings_provider`
    -   `file_item`
    -   `chunks`
    -   `n_retrieve`
    -   `base_path`

#### 함수/메서드
-   **컨벤션**: 함수 및 메서드 이름은 `snake_case`를 사용합니다. 동사로 시작하여 해당 함수가 수행하는 작업을 명확히 나타냅니다. 비동기 함수는 `async def` 키워드를 사용합니다.
-   **예시**:
    -   `main()`
    -   `initialize()`
    -   `get_chunks()`
    -   `insert_chunks()`
    -   `retrieve()`

#### 클래스
-   **컨벤션**: 클래스 이름은 `PascalCase` (CapWords)를 사용합니다. 명사로 시작하여 해당 클래스가 나타내는 개념을 명확히 합니다.
-   **예시**:
    -   `EmbeddingsProvider`
    -   `PgVectorIndex`
    -   `PathAndCacheKey`

#### 상수
-   **컨벤션**: 프로젝트 내에서 변경되지 않는 상수는 `ALL_CAPS_SNAKE_CASE`를 사용합니다.
-   **예시**: (코드베이스에 명시적인 예시는 없으나, Python 표준에 따라 권장)
    -   `MAX_TOKENS_PER_CHUNK`
    -   `EMBEDDING_DIMENSION`

## 코드 조직

### 파일 구조
-   프로젝트의 핵심 로직은 `core/` 디렉토리 아래에 기능별로 모듈화되어 있습니다.
-   `main.py`는 애플리케이션의 주요 진입점 역할을 합니다.
-   `db_test.py`, `drop_table.py`와 같은 유틸리티 스크립트는 프로젝트 루트에 위치합니다.
-   `setup_vendor.py` 및 `build_parsers.py`는 외부 의존성(Tree-sitter 파서) 설정 및 빌드를 위한 스크립트입니다.
-   `vendor/` 디렉토리는 Tree-sitter 파서의 소스 코드를 포함합니다.
-   `test_files/` 디렉토리는 청킹 시스템 테스트를 위한 예시 소스 코드 파일을 포함합니다.

### 모듈 조직
-   `core/` 디렉토리 내의 각 하위 디렉토리(예: `embeddings/`, `indexing/`, `llm/`, `util/`, `chunk/`)는 관련 기능을 캡슐화하는 Python 패키지(`__init__.py` 파일 포함)로 구성됩니다.
-   각 모듈은 단일 책임 원칙을 따르도록 노력합니다. 예를 들어, `embeddings/`는 임베딩 관련 로직을, `indexing/`는 인덱싱 로직을 담당합니다.

### Import 컨벤션
-   **절대 경로 임포트**: 프로젝트 내부 모듈을 임포트할 때는 프로젝트 루트(`python_chunking`)를 기준으로 하는 절대 경로 임포트를 사용합니다.
-   **예시**:
    ```python
    from core.indexing.pgvector_index import PgVectorIndex
    from core.embeddings.embeddings_provider import EmbeddingsProvider
    from core.index import PathAndCacheKey
    ```
-   **표준 라이브러리/외부 라이브러리**: 표준 라이브러리 및 외부 라이브러리는 직접 임포트합니다.
-   **예시**:
    ```python
    import asyncio
    ```
-   **순서**: 일반적으로 다음 순서로 임포트합니다:
    1.  표준 라이브러리 임포트
    2.  외부 라이브러리 임포트
    3.  프로젝트 내부 모듈 임포트
    각 그룹 사이에는 한 줄의 공백을 두어 가독성을 높입니다.

## 코딩 스타일

### 포맷팅
-   **들여쓰기**: 4개의 공백을 사용하여 들여쓰기합니다 (탭 사용 금지).
-   **줄 길이**: 명시적인 제한은 없으나, 가독성을 위해 80~120자 이내로 유지하는 것을 권장합니다.
-   **공백**: 연산자 주위, 콤마 뒤 등 표준 Python 스타일 가이드(PEP 8)를 따릅니다.
-   **빈 줄**: 논리적으로 분리된 코드 블록 사이에 빈 줄을 사용하여 가독성을 높입니다.
-   **예시**: `main.py`의 `main` 함수 구조를 따릅니다.

### 문서화
-   **주석**: 복잡한 로직이나 비즈니스 규칙을 설명할 때 주석을 사용합니다. 코드 자체로 명확한 부분에는 과도한 주석을 피합니다.
-   **독스트링 (Docstrings)**: 모든 모듈, 클래스, 함수 및 메서드에는 독스트링을 작성하여 그 목적, 인자, 반환 값 등을 설명합니다. Google 스타일 독스트링을 권장합니다.
-   **예시**: (README에는 독스트링 예시가 없으나, 다음 형식을 권장)
    ```python
    def get_chunks(self, file_item: PathAndCacheKey, content: str) -> list[Chunk]:
        """
        주어진 파일 내용에서 코드 청크를 생성합니다.

        Args:
            file_item (PathAndCacheKey): 파일 경로 및 캐시 키 정보.
            content (str): 청킹할 파일의 전체 내용.

        Returns:
            list[Chunk]: 생성된 코드 청크 리스트.
        """
        # ... 구현 ...
    ```

### 에러 핸들링
-   예외 처리는 `try-except` 블록을 사용하여 명시적으로 처리합니다.
-   예외를 포괄적으로 잡기보다는 특정 예외 유형을 지정하여 처리하는 것을 권장합니다.
-   예외 발생 시 적절한 로깅을 수행하여 문제 진단에 도움을 줍니다.

## 프로젝트-특정 컨벤션

### 테스팅
-   `test_files/` 디렉토리는 Tree-sitter 기반 청킹 시스템이 올바르게 작동하는지 확인하기 위한 다양한 언어의 예시 소스 코드 파일을 포함합니다. 이는 단위 테스트보다는 기능 테스트 또는 통합 테스트의 입력으로 사용됩니다.
-   `db_test.py` 스크립트는 PostgreSQL 및 pgvector 인덱스와의 상호작용을 테스트하고 저장된 데이터를 확인하는 데 사용됩니다.
-   명시적인 단위 테스트 프레임워크(예: `unittest`, `pytest`) 사용에 대한 컨벤션은 정의되어 있지 않으나, 핵심 로직에 대한 단위 테스트 작성을 권장합니다.

### 설정
-   **데이터베이스 설정**: PostgreSQL 및 pgvector 설정은 `psql` 명령어를 통해 수동으로 데이터베이스 및 테이블을 생성하고 확장 기능을 활성화하는 방식으로 이루어집니다. `PGVECTOR_SETUP.sql`과 같은 SQL 스크립트를 사용하여 자동화할 수 있습니다.
-   **애플리케이션 설정**: `PgVectorIndex` 초기화 시 `base_path`와 같은 설정 값은 코드 내에서 직접 전달됩니다. 환경 변수나 전용 설정 파일을 통한 동적인 설정 로딩은 현재 명시되어 있지 않습니다.

### 빌드 및 배포
-   **의존성 관리**: `requirements.txt` 파일을 사용하여 Python 패키지 의존성을 관리합니다. `pip install -r requirements.txt` 명령으로 설치합니다.
-   **가상 환경**: 개발 및 배포 시 Python 가상 환경(`venv`) 사용을 강력히 권장합니다.
-   **Tree-sitter 파서 빌드**:
    -   `python setup_vendor.py`: Tree-sitter 파서 소스 코드를 `vendor/` 디렉토리에 다운로드합니다.
    -   `python build_parsers.py`: 다운로드된 파서 소스를 컴파일하여 `.so` 파일을 `build/` 디렉토리에 생성합니다. 이 과정은 프로젝트 실행에 필수적입니다.

## 모범 사례

-   **PEP 8 준수**: Python 코드 작성 시 PEP 8 스타일 가이드를 최대한 준수합니다.
-   **비동기 프로그래밍**: `asyncio`를 사용하는 비동기 함수는 `await` 키워드를 사용하여 올바르게 호출하고, `async def main()`과 `asyncio.run(main())` 패턴을 따릅니다.
-   **타입 힌트**: 함수 인자 및 반환 값에 타입 힌트를 사용하여 코드의 명확성과 유지보수성을 높입니다.
-   **로깅**: `print()` 문 대신 Python의 `logging` 모듈을 사용하여 애플리케이션의 상태 및 오류를 기록합니다.
-   **환경 변수 사용**: 민감한 정보(예: 데이터베이스 비밀번호)나 환경에 따라 달라지는 설정 값은 환경 변수를 통해 관리하는 것을 고려합니다.

## 예시

### 좋은 예시
`main.py`의 `main` 함수는 프로젝트의 주요 컨벤션을 잘 따르고 있습니다.

```python
import asyncio
from core.indexing.pgvector_index import PgVectorIndex
from core.embeddings.embeddings_provider import EmbeddingsProvider
from core.index import PathAndCacheKey

async def main():
    # 임베딩 프로바이더 초기화 (PascalCase 클래스, snake_case 변수)
    embeddings_provider = EmbeddingsProvider()
    
    # PgVector 인덱스 초기화 (절대 경로 임포트, snake_case 메서드)
    index = PgVectorIndex(
        embeddings_provider,
        base_path="/path/to/your/project" # 설정 값 전달
    )
    await index.initialize() # 비동기 메서드 호출
    
    # 파일 청킹 (snake_case 변수, 메서드)
    file_item = PathAndCacheKey(path="example.py", cache_key="hash123")
    chunks = await index.get_chunks(file_item, "your code content here")
    
    # 임베딩 생성 및 저장
    embeddings = await index.get_embeddings(chunks)
    await index.insert_chunks(chunks, embeddings)
    
    # 검색
    results = await index.retrieve("calculator class", n_retrieve=10)
    
    # 필터링 검색
    results = await index.retrieve(
        "add function",
        n_retrieve=5,
        filters={"path": "example.py"}
    )

if __name__ == "__main__":
    asyncio.run(main()) # 비동기 메인 함수 실행
```

### 피해야 할 안티패턴
-   **하드코딩된 경로**: `base_path`와 같은 중요한 경로나 설정 값을 코드 내에 직접 하드코딩하는 대신, 설정 파일을 통해 관리하거나 환경 변수를 사용하는 것을 고려해야 합니다.
-   **포괄적인 예외 처리**: `except Exception:`과 같이 모든 예외를 포괄적으로 잡는 것은 디버깅을 어렵게 만들 수 있습니다. 가능한 한 구체적인 예외를 처리해야 합니다.
-   **`print()` 디버깅**: `print()` 문을 사용하여 디버깅하는 대신, `logging` 모듈을 활용하여 체계적인 로그를 남기는 것이 좋습니다.
-   **비동기 함수를 `await` 없이 호출**: `async def`로 정의된 함수를 `await` 키워드 없이 호출하면 코루틴 객체만 반환되고 실제 실행은 되지 않습니다. 항상 `await`를 사용하여 코루틴을 실행해야 합니다.