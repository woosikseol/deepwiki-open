# python_rag 설치 및 설정 가이드

## 빠른 시작 (Quick Start)

```bash
# 1. 디렉토리 이동
cd /Users/woosik/repository/deepwiki-open/python_rag

# 2. 가상환경 활성화 (이미 생성되어 있음)
source .venv/bin/activate

# 3. 질문하기
python main.py "RAG는 어떻게 동작하나요?"
```

## 상세 설치 가이드

### 1. 사전 요구사항

#### 1.1 Python 환경
- Python 3.11.9 (필수)
- pip (최신 버전)

#### 1.2 PostgreSQL 설정
```bash
# PostgreSQL 설치 확인
psql --version

# PostgreSQL 실행 확인
psql -h localhost -U postgres

# code_chunks 데이터베이스 확인
psql -h localhost -U postgres -c "\l" | grep code_chunks
```

#### 1.3 pgvector 확장 설치
```bash
# PostgreSQL에 연결
psql -h localhost -U postgres -d code_chunks

# pgvector 확장 확인
SELECT * FROM pg_extension WHERE extname = 'vector';

# 확장이 없으면 설치
CREATE EXTENSION IF NOT EXISTS vector;
```

### 2. 프로젝트 설정

#### 2.1 가상환경 생성 (이미 완료됨)
```bash
cd /Users/woosik/repository/deepwiki-open/python_rag

# 가상환경이 없는 경우만
python3.11 -m venv .venv
```

#### 2.2 가상환경 활성화
```bash
# macOS/Linux
source .venv/bin/activate

# Windows
# .venv\Scripts\activate
```

#### 2.3 의존성 설치 (이미 완료됨)
```bash
# pip 업그레이드
pip install --upgrade pip

# 의존성 설치
pip install -r requirements.txt
```

설치되는 주요 패키지:
- `google-generativeai`: Gemini API 클라이언트
- `sentence-transformers`: 임베딩 모델
- `psycopg2-binary`: PostgreSQL 어댑터
- `numpy`: 수치 연산 (< 2.0.0)
- `pgvector`: PostgreSQL 벡터 확장
- `jinja2`: 템플릿 엔진
- `tiktoken`: 토큰 카운팅
- `tree-sitter`: 코드 파싱

### 3. 환경 변수 설정

#### 3.1 .env 파일 확인 (이미 생성됨)
```bash
cat .env
```

내용 확인:
```bash
# Gemini API Configuration
GEMINI_API_KEY=AIzaSyCrt6pBUq-2YfeputHnBVqXHBCRc0_YbtQ

# PostgreSQL Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=code_chunks
DB_USER=postgres
DB_PASSWORD=postgres

# RAG Configuration
DEFAULT_LANGUAGE=ko
EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
TOP_K_RESULTS=10
```

#### 3.2 환경 변수 검증
```bash
# config.py를 통한 검증
python -c "from api.config import validate_config; validate_config(); print('✅ Configuration is valid')"
```

### 4. 데이터베이스 준비

#### 4.1 python_chunking으로 코드 인덱싱

```bash
# python_chunking 디렉토리로 이동
cd ../python_chunking

# 가상환경 활성화
source .venv/bin/activate

# 코드베이스 인덱싱
python main.py /path/to/your/codebase --db

# 예시: deepwiki-open 프로젝트 인덱싱
python main.py /Users/woosik/repository/deepwiki-open --db
```

#### 4.2 데이터 확인
```bash
# PostgreSQL에 연결
psql -h localhost -U postgres -d code_chunks

# chunks 테이블 확인
SELECT COUNT(*) FROM chunks;
SELECT path, COUNT(*) FROM chunks GROUP BY path ORDER BY COUNT(*) DESC LIMIT 10;

# 임베딩 확인
SELECT COUNT(*) FROM chunks WHERE embedding IS NOT NULL;

# 종료
\q
```

### 5. 설치 확인

#### 5.1 모듈 import 테스트
```bash
cd /Users/woosik/repository/deepwiki-open/python_rag
source .venv/bin/activate

python -c "
import api.config
import api.rag
import api.gemini_client
import api.prompts
print('✅ All modules imported successfully')
"
```

#### 5.2 도움말 확인
```bash
python main.py --help
```

#### 5.3 간단한 질문 테스트
```bash
python main.py "테스트 질문입니다"
```

### 6. 문제 해결

#### 6.1 numpy 버전 오류
```
Error: A module that was compiled using NumPy 1.x cannot be run in NumPy 2.x
```

해결:
```bash
pip install 'numpy>=1.24.0,<2.0.0'
```

#### 6.2 ModuleNotFoundError
```
ModuleNotFoundError: No module named 'tiktoken'
```

해결:
```bash
pip install tiktoken tree-sitter tree-sitter-languages
```

#### 6.3 PostgreSQL 연결 오류
```
Error: could not connect to server
```

해결:
```bash
# PostgreSQL 실행 확인
brew services list | grep postgresql
# 또는
sudo systemctl status postgresql

# PostgreSQL 시작
brew services start postgresql
# 또는
sudo systemctl start postgresql

# 연결 테스트
psql -h localhost -U postgres
```

#### 6.4 pgvector 확장 없음
```
Error: type "vector" does not exist
```

해결:
```bash
# PostgreSQL에 연결
psql -h localhost -U postgres -d code_chunks

# 확장 설치
CREATE EXTENSION IF NOT EXISTS vector;

# 확인
SELECT * FROM pg_extension WHERE extname = 'vector';
```

#### 6.5 Gemini API 오류
```
Error: API key is invalid
```

해결:
```bash
# .env 파일 확인
cat .env | grep GEMINI_API_KEY

# API 키가 없으면 https://makersuite.google.com/app/apikey 에서 생성

# .env 파일 수정
nano .env
```

#### 6.6 검색 결과 없음
```
죄송합니다. 관련된 정보를 찾을 수 없습니다.
```

해결:
```bash
# 데이터 확인
psql -h localhost -U postgres -d code_chunks -c "SELECT COUNT(*) FROM chunks;"

# 데이터가 없으면 python_chunking으로 인덱싱
cd ../python_chunking
source .venv/bin/activate
python main.py /path/to/codebase --db
```

### 7. 추가 설정

#### 7.1 zsh 별칭 설정 (선택사항)
```bash
# ~/.zshrc 편집
nano ~/.zshrc

# 별칭 추가
alias rag='cd /Users/woosik/repository/deepwiki-open/python_rag && source .venv/bin/activate && python main.py'

# 적용
source ~/.zshrc

# 사용
rag "질문"
```

#### 7.2 환경 변수 수정
```bash
# .env 파일 편집
nano .env

# 예: 기본 언어를 영어로 변경
DEFAULT_LANGUAGE=en

# 예: 검색 결과 개수 증가
TOP_K_RESULTS=20
```

#### 7.3 로그 레벨 조정
```bash
# 디버그 모드로 실행
python main.py "질문" --debug

# 일반 모드 (INFO 레벨)
python main.py "질문"
```

### 8. 성능 최적화

#### 8.1 임베딩 모델 캐싱
임베딩 모델은 자동으로 캐싱됩니다:
- 첫 실행: 모델 다운로드 (~90MB)
- 이후 실행: 캐시된 모델 사용

캐시 위치:
```bash
ls -lh ~/.cache/torch/sentence_transformers/
```

#### 8.2 PostgreSQL 인덱스 확인
```sql
-- PostgreSQL에 연결
psql -h localhost -U postgres -d code_chunks

-- 인덱스 확인
SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'chunks';

-- HNSW 인덱스가 있어야 함
-- chunks_embedding_idx: HNSW (vector_cosine_ops)
```

#### 8.3 연결 풀링 (향후 개선)
현재는 단일 연결 사용. 향후 pgbouncer 등으로 개선 가능.

### 9. 테스트 실행

#### 9.1 자동 테스트
```bash
# 테스트 스크립트 실행
./test_rag.sh
```

#### 9.2 수동 테스트
```bash
# 한국어 질문
python main.py "RAG는 어떻게 동작하나요?"

# 영어 질문
python main.py "How does RAG work?" --language en

# 상세 정보
python main.py "pgvector는 무엇인가요?" --verbose

# 검색 결과 조정
python main.py "임베딩 모델" --top-k 5
```

### 10. 업데이트

#### 10.1 의존성 업데이트
```bash
# 현재 버전 확인
pip list

# 특정 패키지 업데이트
pip install --upgrade google-generativeai

# 모든 패키지 업데이트 (주의: 호환성 문제 가능)
pip install --upgrade -r requirements.txt
```

#### 10.2 코드 업데이트
```bash
# git pull로 최신 코드 받기
cd /Users/woosik/repository/deepwiki-open
git pull

# 가상환경 재설치 (필요시)
cd python_rag
rm -rf .venv
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 완료 체크리스트

설치가 완료되었는지 확인:

- [ ] Python 3.11.9 설치 확인
- [ ] PostgreSQL 실행 확인
- [ ] pgvector 확장 설치 확인
- [ ] 가상환경 생성 및 활성화
- [ ] 의존성 설치 완료
- [ ] .env 파일 생성 및 설정
- [ ] python_chunking으로 코드 인덱싱 완료
- [ ] 데이터베이스에 chunks 데이터 확인
- [ ] 모듈 import 테스트 성공
- [ ] 간단한 질문 테스트 성공
- [ ] 도움말 명령 실행 성공

모든 항목이 체크되면 python_rag 사용 준비 완료!

## 다음 단계

설치 완료 후:

1. [USAGE.md](USAGE.md) - 사용 가이드 읽기
2. [README.md](README.md) - 프로젝트 개요 읽기
3. [SUMMARY.md](SUMMARY.md) - 프로젝트 요약 읽기
4. 실제 질문으로 테스트하기

## 지원

문제가 발생하면:
1. 이 가이드의 문제 해결 섹션 참조
2. GitHub 이슈 생성
3. 로그 파일 확인 (--debug 옵션 사용)

