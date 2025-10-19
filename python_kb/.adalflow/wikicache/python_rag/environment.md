---
title: 환경 설정 및 가이드
project: python_rag
generated_at: 2025-10-19 18:50:27
generator: Python Knowledge Base Generator
---

# 환경 설정 및 가이드

이 문서는 `python_rag` 프로젝트 개발 환경을 설정하는 과정을 안내합니다.

## 전제 조건

### 시스템 요구 사항
- **운영 체제**: macOS, Linux, Windows (가상 환경 활성화 스크립트 지원)
- **Python 버전**: Python 3.11.9
- **기타 도구**:
    - **PostgreSQL**: 데이터베이스 시스템
    - **pgvector 확장**: PostgreSQL용 벡터 임베딩 지원 확장
    - **`python_chunking` 프로젝트**: 코드베이스를 색인화하고 청크를 생성하기 위한 필수 도구입니다. `python_rag`는 `python_chunking`에 의해 색인화된 코드에 의존합니다.

### 필수 의존성
`python_rag` 프로젝트는 다음 주요 Python 라이브러리에 의존합니다:
- `google-generativeai`: Gemini API 클라이언트
- `sentence-transformers`: 임베딩 모델 (all-MiniLM-L6-v2)
- `psycopg2-binary`: PostgreSQL 어댑터
- `pgvector`: PostgreSQL 벡터 확장 지원
- `jinja2`: 프롬프트 템플릿 엔진

## 설치 가이드

### 1단계: Python 3.11.9 설치
`python_rag` 프로젝트는 Python 3.11.9 버전을 사용합니다. 시스템에 해당 버전이 설치되어 있지 않다면, 다음 방법 중 하나를 사용하여 설치하십시오:
- **pyenv (권장)**: `pyenv install 3.11.9`
- **공식 Python 웹사이트**: [python.org](https://www.python.org/downloads/release/python-3119/)에서 설치 관리자를 다운로드합니다.
- **운영 체제 패키지 관리자**: `apt`, `brew`, `choco` 등을 사용하여 설치합니다.

### 2단계: PostgreSQL 및 pgvector 확장 설치
`python_rag`는 PostgreSQL 데이터베이스와 `pgvector` 확장을 사용하여 벡터 임베딩을 저장하고 검색합니다.
1.  **PostgreSQL 설치**: 운영 체제에 맞는 PostgreSQL 설치 가이드를 따릅니다.
    -   [PostgreSQL 공식 웹사이트](https://www.postgresql.org/download/)
2.  **pgvector 확장 활성화**: PostgreSQL 설치 후, 데이터베이스에 연결하여 `pgvector` 확장을 생성합니다.
    ```sql
    -- PostgreSQL 클라이언트 (예: psql)에서 실행
    CREATE EXTENSION vector;
    ```
    **참고**: `python_chunking` 프로젝트를 통해 코드베이스를 색인화할 때 `chunks` 테이블과 `embedding` 컬럼이 자동으로 생성됩니다.

### 3단계: `python_rag` 저장소 클론
프로젝트 저장소를 로컬 시스템으로 클론합니다.
```bash
git clone https://github.com/your-org/python_rag.git # 실제 저장소 URL로 대체
cd python_rag
```

### 4단계: 의존성 설치
프로젝트 디렉토리로 이동하여 가상 환경을 생성하고 필요한 Python 패키지를 설치합니다.
```bash
# 1. 가상 환경 생성 및 활성화
python3.11 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows

# 2. 의존성 설치
pip install -r requirements.txt
```

### 5단계: 환경 설정

#### 환경 변수
`.env.example` 파일을 `.env`로 복사하고 필요한 환경 변수를 설정합니다.
```bash
cp .env.example .env
```
`.env` 파일을 열어 다음 변수들을 설정하십시오:
```
# .env
GEMINI_API_KEY=your_gemini_api_key_here # Gemini API 키를 입력하세요.

# PostgreSQL 설정
DB_HOST=localhost
DB_PORT=5432
DB_NAME=code_chunks # python_chunking에서 사용한 데이터베이스 이름과 일치해야 합니다.
DB_USER=postgres
DB_PASSWORD=postgres

# RAG 설정
DEFAULT_LANGUAGE=ko
EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
TOP_K_RESULTS=10
```
-   `GEMINI_API_KEY`: Google Gemini API 키를 [Google AI Studio](https://aistudio.google.com/app/apikey)에서 발급받아 입력합니다.
-   `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`: PostgreSQL 연결 정보를 설정합니다. `DB_NAME`은 `python_chunking`에서 코드베이스를 색인화할 때 사용한 데이터베이스 이름과 일치해야 합니다.

#### 설정 파일
주요 설정은 `.env` 파일을 통해 관리됩니다. `api/config.py` 파일은 `.env`에서 로드된 환경 변수를 사용하여 애플리케이션 내부에서 사용되는 설정을 정의합니다. 일반적으로 이 파일을 직접 수정할 필요는 없습니다.

## 확인

### 설치 확인
가상 환경이 올바르게 활성화되었는지, 그리고 모든 의존성이 설치되었는지 확인합니다.
```bash
# 가상 환경이 활성화되어 있는지 확인
which python
# 출력 예시: /path/to/python_rag/.venv/bin/python

# 설치된 패키지 목록 확인
pip list
# 출력에 google-generativeai, sentence-transformers, psycopg2-binary 등이 포함되어야 합니다.
```

### 테스트 실행
현재 프로젝트에는 테스트 스위트가 `TODO` 상태입니다. 따라서 현재로서는 실행할 테스트가 없습니다.
```bash
# TODO: 테스트 스위트가 추가되면 다음 명령어를 사용하여 테스트를 실행할 수 있습니다.
# pytest tests/
```

### 예상 출력
모든 설정이 완료되고 `python_chunking`을 통해 코드베이스가 색인화되었다면, `python_rag`를 실행하여 질문에 대한 응답을 받을 수 있습니다.
```bash
# 가상 환경 활성화
source .venv/bin/activate

# 질문 실행
python main.py "이 코드베이스는 어떤 역할을 하나요?"
```
**성공적인 설정 시 예상 출력**:
-   질문에 대한 Markdown 형식의 답변이 터미널에 출력됩니다.
-   `results/` 디렉토리에 `rag_analysis_YYYYMMDD_HHMMSS.md` 형식의 파일로 답변이 자동 저장됩니다.
-   관련 컨텍스트가 성공적으로 검색되고 Gemini API를 통해 응답이 생성됩니다.

## 개발 워크플로우

### 프로젝트 실행

#### 개발 모드
개발 중에는 다양한 옵션을 사용하여 프로젝트를 실행하고 디버깅할 수 있습니다.
```bash
# 가상 환경 활성화
source .venv/bin/activate

# 기본 질문 (결과는 results/ 디렉토리에 자동 저장)
python main.py "이 코드베이스는 어떤 역할을 하나요?"

# 출력 언어 지정 (예: 영어)
python main.py "Explain the RAG implementation" --language en

# 검색할 컨텍스트 수 제어
python main.py "How does chunking work?" --top-k 5

# 상세 컨텍스트 정보 표시
python main.py "Where is the embedding logic?" --verbose

# 디버그 로깅 활성화
python main.py "Your question" --debug

# 사용자 지정 출력 파일 지정
python main.py "Your question" --output results/custom_name.md

# 여러 옵션 결합
python main.py "코드 분석해줘" --verbose --output results/detailed_analysis.md
```

#### 프로덕션 모드
`python_rag`는 CLI 도구이므로, "프로덕션 모드"는 일반적으로 디버그 플래그 없이 표준 사용법으로 실행하는 것을 의미합니다.
```bash
# 가상 환경 활성화
source .venv/bin/activate

# 표준 질문 실행
python main.py "프로젝트의 주요 구성 요소는 무엇인가요?"

# 특정 언어로 결과 요청
python main.py "RAG 시스템의 아키텍처를 설명해주세요." --language ko
```

### 일반적인 명령어
-   `python main.py "질문"`: 기본 질문을 실행하고 결과를 `results/` 디렉토리에 저장합니다.
-   `python main.py "질문" --language [언어코드]`: 지정된 언어로 답변을 요청합니다 (예: `en`, `ko`).
-   `python main.py "질문" --top-k [숫자]`: 검색할 관련 코드 청크의 수를 제어합니다.
-   `python main.py "질문" --verbose`: 답변에 사용된 상세 컨텍스트 정보를 함께 표시합니다.
-   `python main.py "질문" --debug`: 디버그 로깅을 활성화하여 상세한 실행 정보를 확인합니다.
-   `python main.py "질문" --output [파일경로]`: 답변을 지정된 파일에 저장합니다.

## 문제 해결

### 문제 1: 데이터베이스 연결 오류
**문제**: `Error: could not connect to server` 또는 유사한 메시지가 발생합니다.
**해결책**:
1.  PostgreSQL 서버가 실행 중인지 확인합니다.
2.  `.env` 파일의 `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` 설정이 올바른지 확인합니다.
3.  `DB_USER`에 `DB_NAME` 데이터베이스에 대한 접근 권한이 있는지 확인합니다.

### 문제 2: 컨텍스트를 찾을 수 없음
**문제**: `죄송합니다. 관련된 정보를 찾을 수 없습니다.` 메시지가 표시됩니다.
**해결책**:
1.  `python_chunking` 프로젝트를 사용하여 코드베이스를 먼저 색인화했는지 확인합니다.
2.  `python_chunking`에서 사용한 데이터베이스 이름(`DB_NAME`)이 `python_rag`의 `.env` 파일 설정과 일치하는지 확인합니다.
3.  질문이 색인화된 코드베이스와 관련이 있는지 확인합니다.

### 문제 3: Gemini API 오류
**문제**: `Error: API key is invalid` 또는 `Authentication failed` 메시지가 발생합니다.
**해결책**:
1.  `.env` 파일의 `GEMINI_API_KEY`가 올바르고 유효한 Gemini API 키인지 확인합니다.
2.  API 키에 필요한 권한이 부여되어 있는지 확인합니다.
3.  네트워크 연결에 문제가 없는지 확인합니다.

## 추가 자료
-   **`python_chunking` 프로젝트**: [저장소 링크 (예시)](https://github.com/your-org/python_chunking) - 코드베이스 색인화 및 청크 생성을 위한 필수 프로젝트입니다.
-   **Google Gemini API 문서**: [Google AI Studio](https://aistudio.google.com/app/apikey) - Gemini API 키 발급 및 사용법에 대한 정보.
-   **PostgreSQL 공식 문서**: [PostgreSQL Documentation](https://www.postgresql.org/docs/) - PostgreSQL 설치 및 관리에 대한 상세 정보.
-   **pgvector GitHub 저장소**: [pgvector](https://github.com/pgvector/pgvector) - pgvector 확장 설치 및 사용법에 대한 정보.

## 개발 팁
-   **코드 스타일**: 이 프로젝트는 상위 `deepwiki-open` 프로젝트와 동일한 코딩 컨벤션을 따릅니다. 일관된 코드 스타일을 유지하는 것이 중요합니다.
-   **`python_chunking`과의 통합**: `python_rag`는 `python_chunking`에 의해 생성된 데이터베이스에 의존합니다. 새로운 코드베이스를 분석하거나 기존 코드베이스가 변경될 경우, `python_chunking`을 다시 실행하여 데이터베이스를 업데이트해야 합니다.
-   **환경 변수 관리**: `.env` 파일은 로컬 개발 환경에서만 사용하고, 프로덕션 환경에서는 시스템 환경 변수 또는 다른 보안 메커니즘을 통해 민감한 정보를 관리하는 것을 권장합니다.
-   **프롬프트 엔지니어링**: `api/prompts.py` 파일에서 프롬프트 템플릿을 수정하여 RAG 시스템의 답변 품질을 개선할 수 있습니다.