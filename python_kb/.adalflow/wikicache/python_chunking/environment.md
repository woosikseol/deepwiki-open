---
title: 환경 설정 및 가이드
project: python_chunking
generated_at: 2025-10-16 00:42:39
generator: Python Knowledge Base Generator
---

# 환경 설정 및 가이드

이 문서는 `python_chunking` 프로젝트 개발을 위한 환경 설정 방법을 안내합니다.

## 필수 구성 요소 (Prerequisites)

### 시스템 요구 사항 (System Requirements)
- **운영 체제**: Linux, macOS, Windows (Python, PostgreSQL, Tree-sitter 컴파일을 지원하는 모든 환경)
- **Python 버전**: 3.9 이상 (가상 환경 사용을 권장합니다.)
- **PostgreSQL**: 13 이상 (pgvector 확장을 위해 필요합니다.)
- **기타 도구**:
    - `git`: 소스 코드 클론을 위해 필요합니다.
    - `pip`: Python 패키지 관리를 위해 필요합니다.
    - C/C++ 컴파일러: Tree-sitter 파서 컴파일을 위해 필요합니다.
        - **Linux**: `build-essential` 패키지 (예: `sudo apt-get install build-essential`)
        - **macOS**: Xcode Command Line Tools (`xcode-select --install`)
        - **Windows**: Visual Studio Build Tools (C++ 빌드 도구 포함)

### 필수 의존성 (Required Dependencies)
`requirements.txt`에 명시된 모든 Python 패키지 및 `pgvector` PostgreSQL 확장. 주요 의존성은 다음과 같습니다:
- `tree-sitter`
- `sentence-transformers` (특정 버전 범위 `huggingface_hub>=0.19.0,<0.25.0`, `sentence-transformers>=2.5.0,<3.0.0` 권장)
- `psycopg2-binary`
- `pgvector` (PostgreSQL 확장)
- `fastembed`
- `asyncio`

## 설치 가이드 (Installation Guide)

### 1단계: Python 설치 및 가상 환경 설정
Python 3.9 이상이 설치되어 있지 않다면 먼저 설치합니다. 운영 체제에 맞는 설치 방법을 사용하세요 (예: `pyenv`, `conda`, 시스템 패키지 관리자 또는 공식 웹사이트).

프로젝트를 위한 가상 환경을 설정하는 것을 강력히 권장합니다.
```bash
# 가상 환경 생성
python -m venv .venv

# 가상 환경 활성화 (Linux/macOS)
source .venv/bin/activate

# 가상 환경 활성화 (Windows)
# .venv\Scripts\activate
```

### 2단계: PostgreSQL 및 pgvector 설치
PostgreSQL을 설치하고 `pgvector` 확장을 활성화해야 합니다.

#### macOS (Homebrew 사용)
```bash
# PostgreSQL 및 pgvector 설치
brew install postgresql pgvector

# PostgreSQL 서비스 시작
brew services start postgresql
```

#### Linux/Windows
각 운영 체제에 맞는 PostgreSQL 설치 가이드를 따르세요. `pgvector` 확장은 PostgreSQL 설치 후 수동으로 추가해야 할 수 있습니다.

#### 데이터베이스 및 pgvector 확장 설정
PostgreSQL이 실행 중인 상태에서 다음 명령을 사용하여 데이터베이스를 생성하고 `pgvector` 확장을 활성화합니다.
```bash
# psql 클라이언트로 접속
psql postgres

# 데이터베이스 생성 (원하는 이름으로 변경 가능)
CREATE DATABASE code_chunks;

# 생성한 데이터베이스에 연결
\c code_chunks;

# pgvector 확장 활성화
CREATE EXTENSION vector;

# 테이블 생성 (이 테이블은 청킹된 코드 조각을 저장합니다)
CREATE TABLE chunks (
    id SERIAL PRIMARY KEY,
    uuid TEXT UNIQUE NOT NULL,
    path TEXT NOT NULL,
    cachekey TEXT NOT NULL,
    content TEXT NOT NULL,
    start_line INTEGER NOT NULL,
    end_line INTEGER NOT NULL,
    index INTEGER NOT NULL,
    metadata JSONB,
    embedding vector(384)
);

-- 인덱스 생성 (성능 최적화)
CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON chunks USING gin (metadata);
CREATE INDEX ON chunks (path);
CREATE INDEX ON chunks (cachekey);

# psql 종료
\q
```

### 3단계: 저장소 클론 (Clone the Repository)
```bash
git clone https://github.com/your-username/python_chunking.git # 실제 저장소 URL로 대체하세요
cd python_chunking
```

### 4단계: Python 의존성 설치 (Install Python Dependencies)
활성화된 가상 환경에서 `requirements.txt`에 명시된 모든 Python 패키지를 설치합니다.
```bash
pip install -r requirements.txt
```

**`sentence-transformers` 설치에 문제가 발생할 경우:**
버전 충돌로 인해 설치 오류가 발생할 수 있습니다. 다음 명령어를 사용하여 호환되는 버전을 수동으로 설치해보세요.
```bash
pip install "huggingface_hub>=0.19.0,<0.25.0"
pip install "sentence-transformers>=2.5.0,<3.0.0"
```

### 5단계: Tree-sitter 파서 설정 (Tree-sitter Parser Setup)
Tree-sitter는 C++ 기반 파서를 사용하므로, 이를 다운로드하고 컴파일해야 합니다. C/C++ 컴파일러가 시스템에 설치되어 있어야 합니다.

#### 5-1. 파서 소스 다운로드
```bash
python setup_vendor.py
```
이 스크립트는 `vendor/` 디렉토리에 `tree-sitter-python`, `tree-sitter-javascript`, `tree-sitter-java` 파서 소스를 다운로드합니다.

#### 5-2. 파서 컴파일
```bash
python build_parsers.py
```
이 스크립트는 다운로드된 파서 소스를 컴파일하여 `build/` 디렉토리에 `.so` (Linux/macOS) 또는 `.pyd` (Windows) 파일을 생성합니다 (예: `build/languages-python.so`). 이 파일들은 런타임에 Tree-sitter 파싱에 사용됩니다.

## 구성 (Configuration)

### 환경 변수 (Environment Variables)
현재 프로젝트는 `README.md`에 명시된 바와 같이 `.env` 파일을 통한 명시적인 환경 변수 설정을 요구하지 않습니다. PostgreSQL 연결 정보는 `core/indexing/pgvector_index.py` 내부에서 기본값으로 설정되거나, 코드 내에서 직접 지정될 수 있습니다.

하지만, 프로덕션 환경에서는 민감한 정보(예: PostgreSQL 비밀번호, LLM API 키)를 환경 변수로 관리하는 것이 좋습니다. 다음과 같은 변수를 `.env` 파일에 추가하거나 시스템 환경 변수로 설정할 수 있습니다:
```
# PostgreSQL 연결 정보 (필요한 경우 설정)
PG_HOST=localhost
PG_PORT=5432
PG_USER=your_pg_user
PG_PASSWORD=your_pg_password
PG_DATABASE=code_chunks

# LLM API 키 (향후 사용될 경우)
OPENAI_API_KEY=sk-your_openai_api_key
HUGGINGFACE_API_TOKEN=hf_your_hf_token
```

### 구성 파일 (Configuration Files)
이 프로젝트는 별도의 전역 구성 파일을 사용하지 않습니다. 대부분의 설정은 Python 코드 내에서 직접 이루어지거나, 스크립트 실행 시 인자로 전달됩니다 (예: `main.py`에 디렉토리 경로 전달).

## 검증 (Verification)

### 설치 검증 (Verify Installation)
모든 구성 요소가 올바르게 설치되었는지 확인합니다.

1.  **Python 및 가상 환경**:
    ```bash
    python --version
    pip freeze
    ```
    (활성화된 가상 환경에서 `pip freeze`를 실행하여 설치된 패키지 목록을 확인합니다.)
2.  **PostgreSQL 및 pgvector**:
    ```bash
    brew services list # macOS의 경우 PostgreSQL이 실행 중인지 확인
    psql -c "SELECT version();" # PostgreSQL 버전 확인
    psql -d code_chunks -c "SELECT * FROM pg_extension WHERE extname = 'vector';" # pgvector 확장 활성화 확인
    ```
    `pg_extension` 쿼리 결과에 `vector` 확장이 나타나야 합니다.
3.  **Tree-sitter 파서**:
    `build/` 디렉토리에 `languages-python.so`, `languages-javascript.so`, `languages-java.so`와 같은 파일이 존재하는지 확인합니다.

### 테스트 실행 (Run Tests)
`db_test.py` 스크립트를 실행하여 데이터베이스 연결 및 기본 청킹/임베딩/검색 기능이 올바르게 작동하는지 확인합니다.
```bash
python db_test.py
```

### 예상되는 출력 (Expected Output)
`db_test.py`를 실행하면 다음과 유사한 출력이 나타나야 합니다.
- 데이터베이스 연결 성공 메시지.
- 예제 파일 (`example.py`)에 대한 청킹 및 임베딩 생성 과정.
- `chunks` 테이블에 데이터가 성공적으로 삽입되었음을 나타내는 메시지.
- "calculator class"와 같은 쿼리에 대한 유사도 검색 결과.
- "add function" 필터링 검색 결과.

성공적인 실행은 오류 없이 프로세스가 완료되고 검색 결과가 반환되는 것을 의미합니다.

## 개발 워크플로우 (Development Workflow)

### 프로젝트 실행 (Running the Project)

#### 개발 모드 (Development Mode)
`main.py` 스크립트를 사용하여 특정 디렉토리의 코드 파일을 인덱싱할 수 있습니다. 이는 개발 중 코드를 테스트하거나 새로운 기능을 추가할 때 유용합니다.
```bash
# 현재 디렉토리의 'test_files' 폴더 인덱싱
python main.py ./test_files

# 다른 코드 디렉토리 인덱싱
python main.py /path/to/your/code
```

#### 프로덕션 모드 (Production Mode)
이 프로젝트는 독립적인 서비스라기보다는 코드 청킹 및 임베딩 기능을 제공하는 라이브러리/도구에 가깝습니다. 따라서 별도의 '프로덕션 모드' 실행 명령은 없습니다. `main.py`는 개발 및 운영 환경 모두에서 코드 인덱싱을 위한 주요 진입점입니다.

`core/index.py`의 `PgVectorIndex`와 `EmbeddingsProvider`를 사용하여 애플리케이션에 직접 통합할 수 있습니다.
```python
import asyncio
from core.indexing.pgvector_index import PgVectorIndex
from core.embeddings.embeddings_provider import EmbeddingsProvider
from core.index import PathAndCacheKey

async def example_usage():
    embeddings_provider = EmbeddingsProvider()
    index = PgVectorIndex(embeddings_provider, base_path="/path/to/your/project")
    await index.initialize()
    
    file_item = PathAndCacheKey(path="example.py", cache_key="hash123")
    chunks = await index.get_chunks(file_item, "your code content here")
    embeddings = await index.get_embeddings(chunks)
    await index.insert_chunks(chunks, embeddings)
    
    results = await index.retrieve("calculator class", n_retrieve=10)
    print("Search Results:", results)

if __name__ == "__main__":
    asyncio.run(example_usage())
```

### 일반적인 명령어 (Common Commands)
- `python -m venv .venv`: 가상 환경 생성
- `source .venv/bin/activate` (또는 Windows용 `venv\Scripts\activate`): 가상 환경 활성화
- `pip install -r requirements.txt`: Python 의존성 설치
- `python setup_vendor.py`: Tree-sitter 파서 소스 다운로드
- `python build_parsers.py`: Tree-sitter 파서 컴파일
- `python main.py [경로]`: 지정된 디렉토리의 코드 파일을 인덱싱
- `python db_test.py`: 데이터베이스 연결 및 청킹/검색 기능 테스트
- `python drop_table.py`: `chunks` 테이블의 데이터 삭제 (대화형)
- `python drop_table.py --force`: `chunks` 테이블의 데이터 강제 삭제
- `python drop_table.