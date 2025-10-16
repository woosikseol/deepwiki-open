# python_rag 사용 가이드

## 개요

`python_rag`는 코드베이스에 대한 질문-답변(Q&A) 기능을 제공하는 RAG(Retrieval-Augmented Generation) 시스템입니다.

## 사전 준비

### 1. 데이터베이스 준비

먼저 `python_chunking`을 사용하여 코드베이스를 인덱싱해야 합니다:

```bash
cd ../python_chunking
source .venv/bin/activate
python main.py /path/to/your/codebase --db
```

### 2. 환경 설정

`.env` 파일에서 다음 설정을 확인하세요:

```bash
# Gemini API Key (필수)
GEMINI_API_KEY=your_api_key_here

# PostgreSQL 연결 정보
DB_HOST=localhost
DB_PORT=5432
DB_NAME=code_chunks
DB_USER=postgres
DB_PASSWORD=postgres

# RAG 설정
DEFAULT_LANGUAGE=ko
TOP_K_RESULTS=10
```

## 기본 사용법

### 간단한 질문

```bash
# 가상환경 활성화
source .venv/bin/activate

# 한국어 질문 (기본)
python main.py "이 프로젝트는 무엇을 하나요?"

# 영어 질문
python main.py "What does this project do?" --language en
```

### 옵션 사용

```bash
# 상세 컨텍스트 정보 표시
python main.py "RAG는 어떻게 동작하나요?" --verbose

# 검색 결과 개수 조정
python main.py "임베딩 모델은 무엇인가요?" --top-k 5

# 디버그 모드
python main.py "Your question" --debug
```

## 질문 예시

### 1. 코드 이해

```bash
# 특정 기능 이해
python main.py "RAG 클래스는 어떤 기능을 제공하나요?"

# 구현 방법 이해
python main.py "임베딩은 어떻게 생성되나요?"

# 아키텍처 이해
python main.py "pgvector는 어떻게 사용되나요?"
```

### 2. 영향 분석

```bash
# 파일 수정 영향도
python main.py "pgvector_index.py를 수정하면 어떤 파일들이 영향을 받나요?"

# 함수 변경 영향도
python main.py "A 함수 대신에 B 함수를 새로 생성한다면 영향 받을 부분들의 모든 위치와 컨텍스트를 표시해줘."

# 의존성 분석
python main.py "embeddings_provider는 어디에서 사용되나요?"
```

### 3. 기술적 질문

```bash
# 기술 스택
python main.py "이 프로젝트에서 사용하는 주요 라이브러리는 무엇인가요?"

# 데이터 흐름
python main.py "데이터는 어떻게 처리되나요?"

# 에러 처리
python main.py "에러 처리는 어떻게 되나요?"
```

### 4. 다국어 질문

```bash
# 한국어 (기본)
python main.py "이 코드는 무엇을 하나요?"

# 영어
python main.py "What does this code do?" --language en

# 일본어
python main.py "このコードは何をしますか？" --language ja

# 중국어
python main.py "这段代码是做什么的？" --language zh
```

## 고급 사용법

### 1. 프로그래밍 방식 사용

```python
import asyncio
from api.rag import RAG
from api.config import validate_config

async def main():
    # 설정 검증
    validate_config()
    
    # RAG 초기화
    rag = RAG(language="ko", top_k=10)
    await rag.initialize()
    
    # 질문하기
    result = await rag.answer("RAG는 어떻게 동작하나요?")
    
    # 결과 출력
    print(f"Answer: {result.answer}")
    print(f"Contexts: {len(result.contexts)}")
    
    # 정리
    rag.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### 2. 커스텀 필터 사용

```python
from api.rag import RAG

async def search_with_filter():
    rag = RAG()
    await rag.initialize()
    
    # 특정 파일에서만 검색
    result = await rag.answer(
        "임베딩 함수는 어떻게 동작하나요?",
        filters={"path": "embeddings_provider.py"}
    )
    
    rag.close()
```

### 3. 생성 파라미터 조정

```python
async def custom_generation():
    rag = RAG()
    await rag.initialize()
    
    # 생성 파라미터 조정
    result = await rag.answer(
        "코드를 설명해주세요.",
        temperature=0.5,  # 더 결정적인 답변
        max_output_tokens=4096  # 더 긴 답변
    )
    
    rag.close()
```

## 성능 최적화

### 1. 검색 결과 개수 조정

```bash
# 빠른 응답이 필요한 경우
python main.py "간단한 질문" --top-k 3

# 더 정확한 답변이 필요한 경우
python main.py "복잡한 질문" --top-k 20
```

### 2. 데이터베이스 최적화

PostgreSQL 연결 풀 설정:

```python
# config.py에서 연결 설정 조정
DB_POOL_SIZE = 5
DB_MAX_OVERFLOW = 10
```

### 3. 캐싱

자주 사용하는 질문의 결과를 캐싱하여 성능 향상:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_answer(query: str):
    # 캐시된 답변 반환
    pass
```

## 문제 해결

### 1. 연결 오류

```bash
# PostgreSQL 실행 확인
psql -h localhost -U postgres -d code_chunks

# 연결 문자열 확인
python -c "from api.config import get_db_connection_string; print(get_db_connection_string())"
```

### 2. 검색 결과 없음

```bash
# 데이터 확인
psql -h localhost -U postgres -d code_chunks -c "SELECT COUNT(*) FROM chunks;"

# 인덱스 재생성
cd ../python_chunking
python main.py /path/to/codebase --db
```

### 3. API 오류

```bash
# API 키 확인
python -c "from api.config import GEMINI_API_KEY; print(GEMINI_API_KEY[:10] + '...')"

# API 키 테스트
python -c "from api.gemini_client import GeminiClient; client = GeminiClient(); print(client.generate('test'))"
```

## 팁과 트릭

### 1. 효과적인 질문 작성

좋은 질문:
- ✅ "pgvector_index.py의 retrieve 함수는 어떻게 동작하나요?"
- ✅ "embeddings_provider는 어떤 모델을 사용하나요?"
- ✅ "RAG 시스템의 전체 워크플로우를 설명해주세요."

피해야 할 질문:
- ❌ "코드" (너무 모호함)
- ❌ "이거 뭐야?" (맥락 부족)
- ❌ "전부 설명해줘" (너무 광범위함)

### 2. 컨텍스트 활용

```bash
# verbose 모드로 어떤 컨텍스트가 검색되는지 확인
python main.py "질문" --verbose

# 검색 결과를 보고 질문을 더 구체화
python main.py "더 구체적인 질문" --verbose
```

### 3. 다국어 활용

```bash
# 영어로 질문하면 영어 답변
python main.py "How does it work?" --language en

# 한국어로 질문하면 한국어 답변
python main.py "어떻게 동작하나요?" --language ko

# 질문 언어와 무관하게 특정 언어로 답변
python main.py "How does it work?" --language ko
```

## 참고 자료

- [README.md](README.md) - 프로젝트 개요
- [python_chunking](../python_chunking/) - 인덱싱 시스템
- [Gemini API 문서](https://ai.google.dev/docs)
- [pgvector 문서](https://github.com/pgvector/pgvector)

