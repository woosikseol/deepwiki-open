---
title: 환경 설정 및 가이드
project: python_chunking
generated_at: 2025-10-18 16:15:29
generator: Python Knowledge Base Generator
---

# 환경 설정 및 가이드

이 문서는 `python_chunking` 프로젝트 개발을 위한 환경 설정 방법을 안내합니다.

## 선행 조건

### 시스템 요구 사항
-   **운영 체제**: Linux, macOS, Windows (Tree-sitter 파서 컴파일을 위해 C/C++ 빌드 도구가 필요합니다.)
-   **Python 버전**: Python 3.8 이상
-   **기타 도구**:
    *   **Git**: 저장소 클론을 위해 필요합니다.
    *   **PostgreSQL**: 벡터 임베딩 및 유사도 검색을 위해 필요하며, `pgvector` 확장 기능이 활성화되어야 합니다.
    *   **C/C++ 컴파일러 및 `make`**: Tree-sitter 파서 소스를 컴파일하는 데 필요합니다.
        *   **Linux**: `build-essential` 패키지 (예: `sudo apt install build-essential`)
        *   **macOS**: Xcode Command Line Tools (예: `xcode-select --install`)
        *   **Windows**: Visual Studio Build Tools (C++ 데스크톱 개발 워크로드 포함)

### 필수 의존성
`requirements.txt` 파일에 명시된 Python 패키지들이 필요합니다. 주요 의존성은 다음과 같습니다:
-   `tree-sitter`
-   `asyncpg`
-   `sentence-transformers` (특정 버전 범위 내에서 설치 권장)
-   `numpy`
-   `tiktoken`
-   `fastapi` (LanceDB 인덱스 사용 시)
-   `uvicorn` (LanceDB 인덱스 사용 시)
-   `lancedb` (LanceDB 인덱스 사용 시)

## 설치 가이드

### 1단계: Python 설치
Python 3.8 이상 버전이 설치되어 있지 않다면, 다음 링크에서 다운로드하여 설치하십시오:
[Python 공식 웹사이트](https://www.python.org/downloads/)

설치 후 터미널에서 Python 버전을 확인합니다:
```bash
python3 --version
# 또는
python --version
```

### 2단계: PostgreSQL 및 pgvector 설치 및 설정

#### PostgreSQL 설치
-   **macOS (Homebrew 사용)**:
    ```bash
    brew install postgresql pgvector
    brew services start postgresql
    ```
-   **Linux (Debian/Ubuntu)**:
    ```bash
    sudo apt update
    sudo apt install postgresql postgresql-contrib
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
    ```
-   **Windows**:
    [PostgreSQL 공식 웹사이트](https://www.postgresql.org/download/windows/)에서 설치 프로그램을 다운로드하여 설치합니다.

#### 데이터베이스 및 pgvector 확장 설정
PostgreSQL이 실행 중인지 확인한 후, 다음 명령어를 사용하여 데이터베이스를 생성하고 `pgvector` 확장을 활성화합니다.

```bash
psql postgres -U postgres # 기본 사용자 'postgres'로 접속
```
`psql` 프롬프트에서 다음 SQL 명령어를 실행합니다:
```sql
CREATE DATABASE code_chunks;
\c code_chunks;
CREATE EXTENSION vector;

-- 청크 데이터를 저장할 테이블 생성
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

-- 인덱스 생성 (검색 성능 향상)
CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON chunks USING gin (metadata);
CREATE INDEX ON chunks (path);
CREATE INDEX ON chunks (cachekey);
```
설정이 완료되면 `\q`를 입력하여 `psql` 프롬프트를 종료합니다.

### 3단계: 저장소 클론
프로젝트 저장소를 로컬 머신으로 클론합니다:
```bash
git clone https://github.com/your-username/python_chunking.git # 실제 저장소 URL로 변경
cd python_chunking
```

### 4단계: 가상 환경 설정 (권장)
프로젝트 의존성을 격리하기 위해 가상 환경을 사용하는 것을 강력히 권장합니다.
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 또는
.venv\Scripts\activate     # Windows
```

### 5단계: Python 의존성 설치
가상 환경을 활성화한 후, `requirements.txt`에 명시된 모든 Python 패키지를 설치합니다.
```bash
pip install -r requirements.txt
```
**`sentence-transformers` 설치에 문제가 발생할 경우:**
호환되는 버전을 수동으로 설치합니다.
```bash
pip install "huggingface_hub>=0.19.0,<0.25.0"
pip install "sentence-transformers>=2.5.0,<3.0.0"
```

### 6단계: Tree-sitter 파서 설정
Tree-sitter 파서를 다운로드하고 컴파일해야 합니다.
#### 6-1. 파서 소스 다운로드
```bash
python setup_vendor.py
```
이 스크립트는 `vendor/` 디렉토리에 `tree-sitter-python`, `tree-sitter-javascript`, `tree-sitter-java` 파서 소스를 다운로드합니다.

#### 6-2. 파서 컴파일
```bash
python build_parsers.py
```
이 스크립트는 다운로드된 소스를 컴파일하여 `build/` 디렉토리에 `.so` (Linux/macOS) 또는 `.pyd` (Windows) 파일을 생성합니다. 이 파일들은 Python에서 Tree-sitter 파서를 사용할 수 있게 합니다.

## 설정

### 환경 변수
`python_chunking` 프로젝트는 PostgreSQL 데이터베이스 연결을 위해 다음 환경 변수를 사용합니다. 프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 다음 변수들을 설정하는 것을 권장합니다.

```
PG_HOST=localhost
PG_PORT=5432
PG_USER=postgres
PG_PASSWORD= # PostgreSQL 설치 시 설정한 비밀번호 (없으면 비워둠)
PG_DATABASE=code_chunks
```
**참고**: `PG_PASSWORD`는 PostgreSQL 설치 시 설정한 비밀번호로 대체해야 합니다. 기본적으로 `postgres` 사용자는 비밀번호가 없을 수도 있습니다.

`.env` 파일을 사용하려면 `python-dotenv` 라이브러리를 설치하고 코드에서 로드해야 하지만, 이 프로젝트는 `os.getenv`를 직접 사용하므로 `.env` 파일이 자동으로 로드되지는 않습니다. 개발 시에는 쉘에서 직접 환경 변수를 설정하거나, `python-dotenv`를 사용하여 스크립트 시작 시 로드하도록 코드를 수정할 수 있습니다.

**쉘에서 환경 변수 설정 (예시):**
```bash
export PG_HOST=localhost
export PG_PORT=5432
export PG_USER=postgres
export PG_PASSWORD=your_password
export PG_DATABASE=code_chunks
```
Windows에서는 `set` 명령어를 사용합니다.

### 설정 파일
현재 프로젝트는 별도의 전역 설정 파일을 사용하지 않습니다. 대부분의 설정은 코드 내에서 직접 관리되거나 환경 변수를 통해 주입됩니다.

## 확인

### 설치 확인
1.  **Python 및 가상 환경 확인**:
    ```bash
    python --version
    pip list
    ```
    `pip list` 출력에 `requirements.txt`의 패키지들이 포함되어야 합니다.
2.  **Tree-sitter 파서 컴파일 확인**:
    `build/` 디렉토리에 `languages-python.so`, `languages-javascript.so`, `languages-java.so` (또는 Windows의 경우 `.pyd`) 파일이 존재하는지 확인합니다.
    ```bash
    ls build/
    ```
3.  **PostgreSQL 연결 확인**:
    `psql`을 사용하여 `code_chunks` 데이터베이스에 접속할 수 있는지 확인합니다.
    ```bash
    psql -h localhost -p 5432 -U postgres -d code_chunks
    ```
    접속 후 `\dt`를 입력하여 `chunks` 테이블이 생성되었는지 확인합니다.

### 테스트 실행
프로젝트에 포함된 스크립트를 사용하여 기본 기능을 테스트합니다.

1.  **샘플 파일 인덱싱**:
    ```bash
    python main.py ./test_files
    ```
    이 명령어는 `test_files` 디렉토리의 샘플 코드 파일들을 파싱하고 청킹하여 PostgreSQL에 저장합니다.

2.  **데이터 확인 및 검색 테스트**:
    ```bash
    python db_test.py
    ```
    이 스크립트는 데이터베이스에 저장된 청크를 확인하고, 임베딩 검색 기능을 테스트합니다.

### 예상 출력
-   `python main.py ./test_files` 실행 시, 파일 파싱 및 인덱싱 진행 상황에 대한 로그 메시지가 출력되고, 오류 없이 완료되어야 합니다.
-   `python db_test.py` 실행 시, 데이터베이스에서 청크를 성공적으로 검색하고, 검색 결과가 출력되어야 합니다. 예를 들어, "Retrieved chunks:"와 함께 검색된 코드 청크의 내용이 표시됩니다.

## 개발 워크플로우

### 프로젝트 실행

#### 개발 모드
개발 중에는 `main.py` 스크립트를 사용하여 특정 디렉토리의 코드를 인덱싱하거나, `db_test.py`를 사용하여 데이터베이스 기능을 테스트할 수 있습니다.

**코드 인덱싱:**
```bash
# 현재 디렉토리의 'test_files' 하위 디렉토리 인덱싱
python main.py ./test_files

# 다른 경로의 코드 인덱싱
python main.py /path/to/your/code_project
```

**데이터 확인 및 검색:**
```bash
python db_test.py
```

#### 운영 모드
`python_chunking`은 주로 다른 시스템에 통합되어 코드 청킹 및 임베딩 기능을 제공하는 라이브러리 또는 서비스 컴포넌트입니다. 운영 환경에서는 `main.py` 스크립트를 주기적으로 실행하여 코드베이스를 업데이트하거나, 이 프로젝트의 `core` 모듈을 다른 애플리케이션에서 임포트하여 직접 사용할 수 있습니다.

예를 들어, Docker와 같은 컨테이너 환경에서 `main.py`를 실행하거나, FastAPI와 같은 웹 프레임워크를 사용하여 청킹 및 검색 기능을 API로 노출할 수 있습니다.

### 자주 사용하는 명령어
-   **가상 환경 활성화**:
    ```bash
    source .venv/bin/activate  # Linux/macOS
    .venv\Scripts\activate     # Windows
    ```
-   **Python 의존성 설치**:
    ```bash
    pip install -r requirements.txt
    ```
-   **Tree-sitter 파서 소스 다운로드**:
    ```bash
    python setup_vendor.py
    ```
-   **Tree-sitter 파서 컴파일**:
    ```bash
    python build_parsers.py
    ```
-   **코드 디렉토리 인덱싱**:
    ```bash
    python main.py <path_to_code_directory>
    ```
-   **데이터베이스 테스트 및 검색**:
    ```bash
    python db_test.py
    ```
-   **데이터베이스 청크 데이터 삭제**:
    ```bash
    python drop_table.py          # 확인 요청 후 삭제
    python drop_table.py --force  # 확인 없이 즉시 삭제 (주의!)
    python drop_table.py --drop-table --force # 테이블 자체를 삭제 (주의!)
    ```

### 디버깅 설정
-   **IDE 디버거**: VS Code, PyCharm과 같은 통합 개발 환경(IDE)은 Python 디버깅 기능을 강력하게 지원합니다. 프로젝트를 IDE로 열고, 브레이크포인트를 설정한 후 디버그 모드로 스크립트를 실행할 수 있습니다.
-   **`pdb` 사용**: Python 내장 디버거인 `pdb`를 사용하여 코드에 `import pdb; pdb.set_trace()`를 삽입하여 특정 지점에서 실행을 멈추고 변수를 검사할 수 있습니다.
-   **로깅**: `print()` 문 대신 `logging` 모듈을 사용하여 상세한 로그를 출력하고 문제의 원인을 파악합니다.

## 문제 해결

### 문제 1: Tree-sitter 파서 컴파일 오류
**문제**: `python build_parsers.py` 실행 시 "command 'make' not found" 또는 C/C++ 컴파일러 관련 오류가 발생합니다.
**해결**: 시스템에 C/C++ 빌드 도구가 설치되어 있지 않거나 경로에 없습니다.
-   **Linux (Debian/Ubuntu)**: `sudo apt install build-essential`
-   **macOS**: `xcode-select --install`
-   **Windows**: Visual Studio Build Tools를 설치하고 "C++ 데스크톱 개발" 워크로드를 선택합니다.

### 문제 2: `sentence-transformers` 설치 오류
**문제**: `pip install -r requirements.txt` 실행 중 `sentence-transformers` 관련하여 버전 충돌 또는 설치 실패 오류가 발생합니다.
**해결**: `requirements.txt`에 명시된 버전 범위가 현재 환경과 충돌할 수 있습니다. `README.md`에 안내된 대로 호환되는 버전을 수동으로 설치해 봅니다.
```bash
pip install "huggingface_hub>=0.19.0,<0.25.0"
pip install "sentence-transformers>=2.5.0,<3.0.0"
```

### 문제 3: PostgreSQL 연결 오류
**문제**: `psql` 또는 Python 스크립트에서 PostgreSQL 데이터베이스에 연결할 수 없습니다.
**해결**:
1.  **PostgreSQL 서비스 확인**: PostgreSQL 서비스가 실행 중인지 확인합니다. (예: `brew services list` 또는 `sudo systemctl status postgresql`)
2.  **환경 변수 확인**: `.env` 파일 또는 쉘에 설정된 `PG_HOST`, `PG_PORT`, `PG_USER`, `PG_PASSWORD`, `PG_DATABASE` 환경 변수가 올바른지 확인합니다.
3.  **`pgvector` 확장 확인**: `code_chunks` 데이터베이스에 접속하여 `CREATE EXTENSION vector;` 명령어가 성공적으로 실행되었는지 확인합니다. `\dx` 명령어로 설치된 확장을 볼 수 있습니다.
4.  **방화벽**: 로컬 방화벽이 PostgreSQL 포트(기본 5432)를 차단하고 있지 않은지 확인합니다.

### 문제 4: `ModuleNotFoundError`
**문제**: Python 스크립트 실행 시 `ModuleNotFoundError: No module named 'some_module'` 오류가 발생합니다.
**해결**:
1.  **가상 환경 활성화**: 가상 환경이 활성화되어 있는지 확인합니다. `(venv)`와 같은 접두사가 터미널 프롬프트에 표시되어야 합니다.
2.  **의존성 설치**: `pip install -r requirements.txt` 명령어를 다시 실행하여 모든 의존성이 올바르게 설치되었는지 확인합니다.

## 추가 자료
-   **프로젝트 README**: [README.md](README.md)
-   **크로스 파일 분석 문서**: [CROSS_FILE_ANALYSIS.md](CROSS_FILE_ANALYSIS.md)
-   **Tree-sitter 공식 문서**: [https://tree-sitter.github.io/tree-sitter/](https://tree-sitter.github.io/tree-sitter/)
-   **pgvector GitHub 저장소**: [https://github.com/pgvector/pgvector](https://github.com/pgvector/pgvector)

## 개발 팁
-   **IDE 활용**: VS Code, PyCharm과 같은 IDE를 사용하면 코드 탐색, 자동 완성, 디버깅, 가상 환경 관리 등 개발 생산성을 크게 향상시킬 수 있습니다.
-   **Tree-sitter 이해**: `core/util/tree_sitter.py` 및 `core/indexing/chunk/code.py` 파일을 통해 Tree-sitter 파싱 및 AST 기반 청킹 로직을 이해하는 것이 중요합니다.
-   **데이터베이스 관리**: `psql` 명령어를 숙지하고, `chunks` 테이블의 데이터를 직접 쿼리하여 청킹 및 임베딩 결과를 확인하는 습관을 들이십시오.
-   **코드 구조 파악**: `core/` 디렉토리 아래의 `index.py` (핵심 타입), `embeddings/` (임베딩), `indexing/` (인덱싱 및 청킹 로직) 등의 모듈 구조를 이해하면 프로젝트 기여에 도움이 됩니다.