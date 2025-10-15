---
title: 프로젝트 구조 및 개요 (주요 기능 포함, 아키텍처 다이어그램 & 모듈 다이어그램 & 플로우 다이어그램 포함)
project: python_chunking
generated_at: 2025-10-16 00:42:39
generator: Python Knowledge Base Generator
---

# 프로젝트 구조 및 개요 (주요 기능 포함)

## 개요
`python_chunking` 프로젝트는 TypeScript 기반의 Continue 프로젝트에서 사용되는 코드 청킹 시스템을 Python으로 포팅한 것입니다. 이 시스템은 Tree-sitter를 활용하여 Java, JavaScript, Python과 같은 다양한 프로그래밍 언어의 소스 코드를 구조적으로 파싱하고 청킹합니다. 주요 기능으로는 Tree-sitter 기반의 스마트 청킹, 다중 언어 지원, PostgreSQL + pgvector를 사용한 벡터 임베딩 저장 및 검색, JSONB 기반의 풍부한 메타데이터 관리, 그리고 파일 간 참조 관계를 분석하는 크로스 파일 분석 기능이 있습니다. 이를 통해 코드 베이스에 대한 심층적인 이해와 효율적인 검색 기능을 제공합니다.

## 프로젝트 구조

### 디렉토리 구성
프로젝트의 디렉토리 구조는 핵심 로직과 외부 의존성, 실행 스크립트가 명확하게 분리되어 있습니다.

*   **`python_chunking/`**: 프로젝트의 최상위 디렉토리입니다.
    *   **`core/`**: 프로젝트의 핵심 로직을 포함하는 패키지입니다. 청킹, 임베딩, 인덱싱, LLM 관련 유틸리티 및 Tree-sitter 래퍼 등 주요 기능이 이곳에 구현되어 있습니다.
        *   **`embeddings/`**: 임베딩 모델을 관리하고 벡터를 생성하는 로직을 담고 있습니다.
        *   **`indexing/`**: 청크를 생성하고 데이터베이스에 저장/검색하는 로직을 담당합니다.
            *   **`chunk/`**: 코드 파일을 청킹하는 구체적인 전략(기본, 코드, 메타데이터)을 구현한 서브 모듈입니다.
        *   **`llm/`**: 토큰 카운팅 등 LLM 관련 유틸리티를 포함합니다.
        *   **`util/`**: Tree-sitter 래퍼 및 URI 처리와 같은 일반적인 유틸리티 함수를 제공합니다.
    *   **`vendor/`**: Tree-sitter 파서 소스 코드를 저장하는 디렉토리입니다. `setup_vendor.py` 스크립트에 의해 다운로드됩니다.
    *   **`test_files/`**: 다양한 언어의 예제 코드 파일들이 포함되어 있어, 청킹 및 인덱싱 기능을 테스트하는 데 사용됩니다.
*   **루트 디렉토리 파일**:
    *   `main.py`: 코드 디렉토리를 인덱싱하는 메인 실행 스크립트입니다.
    *   `setup_vendor.py`: Tree-sitter 파서 소스를 다운로드하는 스크립트입니다.
    *   `build_parsers.py`: 다운로드된 Tree-sitter 파서 소스를 컴파일하는 스크립트입니다.
    *   `db_test.py`: 데이터베이스에 저장된 청크를 확인하고 검색 기능을 테스트하는 스크립트입니다.
    *   `drop_table.py`: 청크 데이터를 삭제하거나 테이블을 삭제하는 유틸리티 스크립트입니다.
    *   `requirements.txt`: 프로젝트의 Python 의존성 목록을 정의합니다.

### 주요 구성 요소 (모듈)

*   **`core.index`**: `PathAndCacheKey`와 같은 핵심 데이터 타입 정의를 포함합니다. 시스템 전반에 걸쳐 사용되는 기본적인 데이터 구조를 제공합니다.
*   **`core.embeddings.embeddings_provider`**: 임베딩 모델을 초기화하고, 텍스트 청크로부터 벡터 임베딩을 생성하는 인터페이스를 제공합니다.
*   **`core.indexing.pgvector_index`**: PostgreSQL + pgvector 데이터베이스와의 상호작용을 담당하는 주요 인덱스 클래스입니다. 청크 저장, 검색, 초기화 등의 기능을 수행합니다.
*   **`core.indexing.chunk.code`**: Tree-sitter를 활용하여 AST 기반의 구조적인 코드 청킹 로직을 구현합니다. 특정 언어의 구문 구조를 이해하고 이에 따라 청크를 생성합니다.
*   **`core.indexing.chunk.basic`**: 코드 파일이 아닌 일반 텍스트 파일이나 지원되지 않는 언어에 대한 기본적인 청킹 전략을 제공합니다.
*   **`core.util.tree_sitter`**: Tree-sitter 라이브러리를 Python에서 사용하기 위한 래퍼 함수와 파서 로딩 로직을 포함합니다. 다양한 언어 파서를 관리하고 AST를 생성하는 핵심 유틸리티입니다.
*   **`core.llm.count_tokens`**: 텍스트 청크의 토큰 수를 계산하는 유틸리티입니다. 청크 크기 제한을 준수하는 데 사용됩니다.

### 중요 파일

*   **`main.py`**: 프로젝트의 주요 진입점입니다. 특정 디렉토리의 코드 파일을 스캔하고, `PgVectorIndex`를 사용하여 청킹 및 인덱싱 프로세스를 시작합니다.
*   **`setup_vendor.py`**: Tree-sitter 파서의 C++ 소스 코드를 `vendor/` 디렉토리에 다운로드하는 스크립트입니다. 프로젝트를 처음 설정할 때 필수적입니다.
*   **`build_parsers.py`**: `vendor/` 디렉토리에 다운로드된 Tree-sitter 파서 소스를 컴파일하여 Python에서 사용할 수 있는 `.so` (또는 `.dll`, `.dylib`) 파일을 `build/` 디렉토리에 생성합니다.
*   **`requirements.txt`**: 프로젝트 실행에 필요한 모든 Python 라이브러리 의존성을 명시합니다. `pip install -r requirements.txt` 명령으로 설치됩니다.
*   **`core/indexing/pgvector_index.py`**: 실제 데이터베이스 연동 및 청크 관리를 담당하는 핵심 파일입니다. `EmbeddingsProvider`와 `Chunking` 로직을 통합하여 동작합니다.
*   **`core/util/tree_sitter.py`**: Tree-sitter 파서 로딩 및 AST(추상 구문 트리) 생성과 관련된 모든 기능을 캡슐화한 파일입니다. 청킹 과정에서 AST를 얻는 데 필수적입니다.

## 주요 기능

### 1. Tree-sitter 기반 파싱
-   **설명**: C++ 기반의 고성능 Tree-sitter 파서를 Python에서 직접 사용하여 소스 코드를 추상 구문 트리(AST)로 파싱합니다. 이는 코드의 구조를 정확하게 이해하는 기반이 됩니다.
-   **구현**: `setup_vendor.py`와 `build_parsers.py` 스크립트를 통해 Tree-sitter 파서 라이브러리(`.so` 파일)를 빌드하고, `core.util.tree_sitter` 모듈에서 이들을 로드하고 활용합니다. `get_parser` 함수는 언어에 맞는 파서를 반환합니다.
-   **관련 파일**: `setup_vendor.py`, `build_parsers.py`, `core/util/tree_sitter.py`, `vendor/` 디렉토리.

### 2. 스마트 청킹
-   **설명**: 단순히 텍스트를 고정된 크기로 자르는 것이 아니라, AST 노드(예: 클래스, 함수, 메서드)를 기반으로 코드의 의미론적 단위를 보존하면서 구조적으로 청킹을 수행합니다. 이를 통해 더 의미 있는 코드 조각을 생성합니다.
-   **구현**: `core.indexing.chunk.code` 모듈의 `get_smart_collapsed_chunks` 함수가 이 로직을 구현합니다. Tree-sitter 파싱 결과인 AST를 순회하며, 특정 노드 타입을 기준으로 청크를 분할하고 병합하는 전략을 사용합니다. 토큰 수 제한도 고려됩니다.
-   **관련 파일**: `core/indexing/chunk/code.py`, `core/util/tree_sitter.py`, `core/llm/count_tokens.py`.

### 3. 다중 언어 지원
-   **설명**: Java, JavaScript, Python 등 다양한 프로그래밍 언어의 소스 코드에 대해 동일한 청킹 및 인덱싱 파이프라인을 적용할 수 있습니다.
-   **구현**: `setup_vendor.py` 스크립트가 여러 언어(Python, JavaScript, Java 등)의 Tree-sitter 파서 소스를 다운로드하고, `build_parsers.py`가 이들을 컴파일합니다. `core.util.tree_sitter.get_parser`는 파일 확장자에 따라 적절한 파서를 동적으로 로드합니다.
-   **관련 파일**: `setup_vendor.py`, `build_parsers.py`, `core/util/tree_sitter.py`, `vendor/tree-sitter-*/` 디렉토리.

### 4. pgvector 벡터 저장
-   **설명**: PostgreSQL 데이터베이스에 `pgvector` 확장을 사용하여 코드 청크의 벡터 임베딩을 저장하고 관리합니다. 이를 통해 유사도 검색을 효율적으로 수행할 수 있습니다.
-   **구현**: `core.indexing.pgvector_index.py` 모듈이 `pgvector` 확장이 활성화된 PostgreSQL 데이터베이스와 상호작용합니다. `insert_chunks` 메서드는 임베딩된 청크를 테이블에 저장하고, `retrieve` 메서드는 벡터 유사도 검색을 수행합니다.
-   **관련 파일**: `core/indexing/pgvector_index.py`, `db_test.py`, `drop_table.py`, `PGVECTOR_SETUP.sql` (README에 포함된 SQL).

### 5. 통합 메타데이터
-   **설명**: 각 코드 청크와 관련된 풍부한 메타데이터(예: 심볼, import/export, 참조 관계, 청크 유형 등)를 PostgreSQL의 JSONB 필드를 활용하여 저장합니다. 이는 검색 및 분석의 정확도를 높입니다.
-   **구현**: `core.indexing.chunk.metadata.py` 모듈에서 메타데이터 추출 로직을 정의하고, `core.indexing.pgvector_index.py`에서 청크와 함께 `chunks` 테이블의 `metadata` JSONB 컬럼에 저장합니다. 크로스 파일 분석 결과도 이 메타데이터에 업데이트됩니다.
-   **관련 파일**: `core/indexing/chunk/metadata.py`, `core/indexing/pgvector_index.py`.

### 6. 크로스 파일 분석
-   **설명**: 단일 파일 분석을 넘어 프로젝트 전체를 대상으로 파일 간의 관계(누가 나를 참조하는지 `referenced_by`, 누가 나를 상속하는지 `subclasses`, 내가 의존하는 파일들 `dependencies`, 누가 나에게 의존하는지 `dependents`)를 자동