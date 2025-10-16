# python_rag 프로젝트 요약

## 프로젝트 개요

`python_rag`는 Deepwiki 프로젝트의 RAG 구현을 참조하여 Python으로 새롭게 작성된 독립적인 RAG(Retrieval-Augmented Generation) 시스템입니다.

### 주요 특징

- ✅ PostgreSQL + pgvector 기반 벡터 검색
- ✅ Gemini API(gemini-2.0-flash-exp) 사용한 답변 생성
- ✅ all-MiniLM-L6-v2 임베딩 모델 (python_chunking과 동일)
- ✅ 10개 언어 지원 (한국어 기본)
- ✅ CLI 기반 간편한 사용
- ✅ python_chunking과 완전 통합

## 프로젝트 구조

```
python_rag/
├── api/
│   ├── __init__.py           # 패키지 초기화
│   ├── config.py             # 환경 설정 관리
│   ├── prompts.py            # 프롬프트 템플릿
│   ├── gemini_client.py      # Gemini API 클라이언트
│   └── rag.py                # RAG 핵심 로직
├── main.py                   # CLI 진입점
├── requirements.txt          # Python 의존성
├── .env                      # 환경 변수 (gitignore)
├── .gitignore               # Git 제외 파일
├── README.md                # 프로젝트 문서
├── USAGE.md                 # 사용 가이드
├── SUMMARY.md               # 이 파일
└── test_rag.sh              # 테스트 스크립트
```

## 핵심 컴포넌트

### 1. api/config.py
- 환경 변수 로드 및 관리
- PostgreSQL 연결 설정
- Gemini API 설정
- 다국어 매핑

### 2. api/prompts.py
- RAG 시스템 프롬프트 (영어)
- Jinja2 템플릿 기반 프롬프트 구성
- 원본 deepwiki-open/api/prompts.py 구조 유지

### 3. api/gemini_client.py
- Google Gemini API 클라이언트
- 동기/비동기 생성 지원
- 커스텀 생성 파라미터 지원

### 4. api/rag.py
- RAG 핵심 로직
- PostgreSQL + pgvector에서 컨텍스트 검색
- python_chunking의 EmbeddingsProvider 사용
- python_chunking의 PgVectorIndex 사용
- 프롬프트 포매팅 및 답변 생성

### 5. main.py
- CLI 진입점
- argparse 기반 명령줄 인터페이스
- 상세 로깅 및 에러 처리
- 다양한 옵션 지원

## 기술 스택

### 백엔드
- **Python 3.11.9**: 기본 런타임
- **PostgreSQL + pgvector**: 벡터 데이터베이스
- **psycopg2-binary**: PostgreSQL 어댑터

### AI/ML
- **Google Gemini API**: 텍스트 생성 (gemini-2.0-flash-exp)
- **sentence-transformers**: 임베딩 생성
- **all-MiniLM-L6-v2**: 임베딩 모델 (384차원)

### 유틸리티
- **python-dotenv**: 환경 변수 관리
- **jinja2**: 프롬프트 템플릿
- **tiktoken**: 토큰 카운팅
- **tree-sitter**: 코드 파싱 (python_chunking에서 사용)

## 워크플로우

```
1. 사용자 질문 입력
   ↓
2. 질문 임베딩 생성 (all-MiniLM-L6-v2)
   ↓
3. PostgreSQL + pgvector에서 유사 컨텍스트 검색
   ↓
4. 검색된 컨텍스트와 질문을 프롬프트로 구성
   ↓
5. Gemini API로 답변 생성
   ↓
6. 마크다운 포맷 답변 출력
```

## python_chunking과의 통합

`python_rag`는 `python_chunking`의 다음 모듈을 직접 import하여 사용합니다:

```python
from core.embeddings.embeddings_provider import EmbeddingsProvider
from core.indexing.pgvector_index import PgVectorIndex
from core.index import Chunk
```

이를 통해:
- ✅ 동일한 임베딩 모델 사용
- ✅ 동일한 데이터베이스 스키마 사용
- ✅ 코드 중복 방지
- ✅ 일관된 데이터 처리

## 원본 프로젝트와의 차이점

### 유사한 점
1. **프롬프트**: 원본 `api/prompts.py`의 RAG_SYSTEM_PROMPT와 RAG_TEMPLATE 사용
2. **구조**: `api/` 디렉토리 구조 유지
3. **워크플로우**: 검색-증강-생성 프로세스 동일

### 다른 점
1. **adalflow 미사용**: 순수 Python으로 구현
2. **LLM**: Gemini API만 사용 (OpenAI, OpenRouter 등 미지원)
3. **백엔드**: FastAPI 없음 (CLI만)
4. **프론트엔드**: React 없음
5. **메모리**: 대화 히스토리 미지원 (단일 질문-답변)

## 설정 정보

### 환경 변수 (.env)
```bash
# Gemini API
GEMINI_API_KEY=AIzaSyCrt6pBUq-2YfeputHnBVqXHBCRc0_YbtQ

# PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=code_chunks
DB_USER=postgres
DB_PASSWORD=postgres

# RAG 설정
DEFAULT_LANGUAGE=ko
EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
TOP_K_RESULTS=10
```

### 데이터베이스 스키마
python_chunking의 PGVECTOR_SETUP.sql 참조:

```sql
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
```

## 사용 예시

### 기본 사용
```bash
# 가상환경 활성화
source .venv/bin/activate

# 질문하기
python main.py "RAG는 어떻게 동작하나요?"
```

### 고급 사용
```bash
# 영어로 답변
python main.py "Explain the RAG implementation" --language en

# 검색 결과 조정
python main.py "임베딩 모델은?" --top-k 5

# 상세 정보 표시
python main.py "pgvector는?" --verbose

# 디버그 모드
python main.py "질문" --debug
```

## 다국어 지원

지원 언어:
- `ko`: 한국어 (기본)
- `en`: English
- `ja`: 日本語
- `zh`: 中文
- `zh-tw`: 繁體中文
- `es`: Español
- `vi`: Tiếng Việt
- `pt-br`: Português Brasileiro
- `fr`: Français
- `ru`: Русский

시스템 프롬프트는 영어로 고정, 출력만 다국어 지원.

## 성능 특성

### 임베딩
- **모델**: all-MiniLM-L6-v2
- **차원**: 384
- **속도**: ~0.5초 (CPU), ~0.1초 (GPU/MPS)

### 검색
- **인덱스**: HNSW (pgvector)
- **검색 시간**: ~0.1-0.5초 (10개 결과)
- **기본 검색 개수**: 10개

### 생성
- **모델**: gemini-2.0-flash-exp
- **생성 시간**: ~2-5초
- **최대 토큰**: 8192

## 의존성

### 핵심 의존성
```
google-generativeai>=0.7.0     # Gemini API
sentence-transformers>=2.5.0   # 임베딩
psycopg2-binary>=2.9.9         # PostgreSQL
numpy>=1.24.0,<2.0.0          # 수치 연산
pgvector>=0.2.0                # 벡터 확장
```

### 유틸리티
```
python-dotenv>=1.0.0           # 환경 변수
jinja2>=3.1.0                  # 템플릿
tiktoken>=0.5.0                # 토큰 카운팅
tree-sitter>=0.20.4            # 코드 파싱
tree-sitter-languages>=1.10.0  # 언어 지원
```

## 테스트

### 자동 테스트
```bash
# 테스트 스크립트 실행
./test_rag.sh
```

### 수동 테스트
```bash
# 도움말
python main.py --help

# 간단한 질문
python main.py "테스트 질문"

# 상세 정보
python main.py "테스트 질문" --verbose --debug
```

## 문제 해결

### 1. numpy 호환성 문제
```bash
pip install 'numpy>=1.24.0,<2.0.0'
```

### 2. 모듈 없음 오류
```bash
pip install -r requirements.txt
```

### 3. PostgreSQL 연결 오류
```bash
# PostgreSQL 실행 확인
psql -h localhost -U postgres -d code_chunks

# 연결 문자열 확인
python -c "from api.config import get_db_connection_string; print(get_db_connection_string())"
```

### 4. 검색 결과 없음
```bash
# 데이터 확인
psql -h localhost -U postgres -d code_chunks -c "SELECT COUNT(*) FROM chunks;"

# python_chunking으로 재인덱싱
cd ../python_chunking
python main.py /path/to/codebase --db
```

## 향후 개선 사항

### 단기
- [ ] 단위 테스트 추가
- [ ] 대화 히스토리 지원
- [ ] 캐싱 기능
- [ ] 배치 처리

### 중기
- [ ] 다중 LLM 지원 (OpenAI, Anthropic 등)
- [ ] 웹 인터페이스
- [ ] REST API
- [ ] 스트리밍 응답

### 장기
- [ ] 파인튜닝된 임베딩 모델
- [ ] 하이브리드 검색 (벡터 + 키워드)
- [ ] 멀티모달 지원
- [ ] 분산 처리

## 라이선스

Deepwiki-open 프로젝트와 동일한 라이선스 적용.

## 관련 프로젝트

- **deepwiki-open**: 원본 프로젝트
- **python_chunking**: 코드 인덱싱 시스템
- **python_kb**: 지식 베이스 생성 시스템

## 기여

Deepwiki-open 프로젝트의 기여 가이드라인을 따릅니다.

## 연락처

Deepwiki-open 프로젝트 이슈 트래커 사용.

