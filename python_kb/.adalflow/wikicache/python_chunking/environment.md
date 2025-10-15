---
title: 환경 설정 및 가이드
project: python_chunking
generated_at: 2025-10-15 18:25:42
generator: Python Knowledge Base Generator
---

# 개발 환경 설정 및 가이드

## 사전 준비 사항

### 시스템 요구 사항
- 운영체제: 모든 주요 운영체제 (Linux, macOS, Windows)
- Python 버전: 3.7 이상 (3.8, 3.9, 3.10, 3.11 권장)
- 기타 도구: PostgreSQL, pgvector

### 필요한 의존성
- sentence-transformers (>=2.5.0, <3.0.0)
- huggingface_hub (>=0.19.0, <0.25.0)
- Tree-sitter
- PostgreSQL + pgvector
- 기타 `requirements.txt`에 명시된 모든 의존성

## 설치 가이드

### 1단계: Python 설치
```bash
# 예시: Ubuntu
sudo apt update
sudo apt install python3 python3-pip python3-venv

# 예시: macOS (Homebrew 사용)
brew install python3
```

### 2단계: 저장소 복제
```bash
git clone <저장소 URL>
cd python_chunking
```

### 3단계: 의존성 설치
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 또는
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 4단계: 설정

#### 환경 변수
`.env` 파일을 생성하고 다음 변수를 추가합니다. (필요한 경우)
```
# 예시: PostgreSQL 연결 정보
DATABASE_URL=postgresql://사용자명:비밀번호@localhost:5432/code_chunks
```

#### 설정 파일
PostgreSQL 및 pgvector 설정을 완료해야 합니다. 아래 SQL 스크립트를 실행하여 데이터베이스와 테이블을 생성합니다.
```sql
CREATE DATABASE code_chunks;
\c code_chunks;
CREATE EXTENSION vector;

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

CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON chunks USING gin (metadata);
CREATE INDEX ON chunks (path);
CREATE INDEX ON chunks (cachekey);
```

또한 Tree-sitter 파서를 설정해야 합니다.
```bash
python setup_vendor.py
python build_parsers.py
```

## 검증

### 설치 확인
다음 명령을 실행하여 필요한 의존성이 설치되었는지 확인합니다.
```bash
pip list
```
PostgreSQL이 실행 중인지 확인합니다.
```bash
# macOS 예시
brew services list
```

### 테스트 실행
`db_test.py` 스크립트를 실행하여 데이터베이스 연결 및 기본 검색 기능을 테스트합니다.
```bash
python db_test.py
```

### 예상 출력
`db_test.py` 스크립트는 데이터베이스에 연결하고 몇 가지 검색 쿼리를 실행하여 결과를 출력합니다. 오류 없이 성공적으로 실행되면 설치가 완료된 것입니다.

## 개발 워크플로우

### 프로젝트 실행

#### 개발 모드
```bash
python main.py ./test_files
```
이 명령은 `./test_files` 디렉터리의 코드를 인덱싱합니다.

#### 프로덕션 모드
프로덕션 환경에서는 적절한 디렉터리를 지정하고, 필요한 환경 변수를 설정해야 합니다.
```bash
python main.py /path/to/your/code
```

### 일반적인 명령어
- `python main.py <디렉토리>`: 지정된 디렉터리의 코드를 인덱싱합니다.
- `python db_test.py`: 데이터베이스 연결 및 검색을 테스트합니다.
- `python drop_table.py`: 데이터베이스 테이블을 삭제합니다. (주의해서 사용)

## 문제 해결

### 문제 1: `sentence-transformers` 설치 오류
**문제**: `sentence-transformers` 설치 중 호환성 문제 발생.
**해결**: `requirements.txt`에 명시된 버전을 확인하고, 필요한 경우 명시적으로 버전을 지정하여 설치합니다.
```bash
pip install "huggingface_hub>=0.19.0,<0.25.0"
pip install "sentence-transformers>=2.5.0,<3.0.0"
```

### 문제 2: PostgreSQL 연결 오류
**문제**: PostgreSQL에 연결할 수 없음.
**해결**: PostgreSQL이 실행 중인지 확인하고, `DATABASE_URL` 환경 변수가 올바르게 설정되었는지 확인합니다.  사용자 이름, 비밀번호, 호스트, 포트, 데이터베이스 이름이 정확한지 확인하십시오.

## 추가 자료
- Continue 프로젝트: [https://continue.dev/](https://continue.dev/) (원본 TypeScript 프로젝트)
- Tree-sitter: [https://tree-sitter.github.io/tree-sitter/](https://tree-sitter.github.io/tree-sitter/)
- pgvector: [https://github.com/pgvector/pgvector](https://github.com/pgvector/pgvector)

## 개발 팁
- 가상 환경을 사용하여 프로젝트 의존성을 격리합니다.
- 코드 변경 후에는 항상 테스트를 실행하여 변경 사항이 예상대로 작동하는지 확인합니다.
- 디버깅 도구를 사용하여 코드의 문제를 해결합니다. (예: `pdb`)
