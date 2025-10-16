# Python Knowledge Base Generator

로컬 프로젝트의 구조를 분석하고 Knowledge Base를 생성하는 도구입니다.

## 개요

이 도구는 Deepwiki 프로젝트의 변환 과정을 참조하여 만들어졌으며, 로컬 프로젝트의 파일 구조를 분석하고 LLM을 사용하여 다음의 Wiki 페이지를 자동으로 생성합니다:

1. **Project Structure & Overview** - 프로젝트 구조 및 주요 기능
2. **Overall System Architecture & Design Patterns** - 시스템 아키텍처 및 디자인 패턴
3. **Conventions** - 명명 규칙 및 코딩 규칙
4. **Environment Setting and Guide** - 환경 설정 가이드

## 특징

- 🔍 **자동 프로젝트 분석**: 파일 구조 및 README 자동 분석
- 🤖 **LLM 기반 생성**: Google Gemini 2.5 Flash Lite를 사용한 고품질 문서 생성
- 💾 **캐시 시스템**: DeepWiki와 동일한 캐시 구조 (프로젝트 내부 .adalflow/wikicache/)
- 📝 **Markdown 출력**: 생성된 Wiki를 Markdown 파일로 저장
- ✅ **LLM 기반 Mermaid 검증**: LLM을 활용한 지능형 다이어그램 구문 검증 및 자동 수정
- 🌐 **다국어 지원**: 한국어/영어 출력 지원
- 🔄 **독립 실행**: python_chunking과 독립적으로 실행 가능

## 지원 언어

- Python (.py)
- Java (.java)
- JavaScript (.js, .jsx)
- TypeScript (.ts, .tsx)

## 설치

### 1. 환경 설정

```bash
# 프로젝트 루트의 가상환경 사용 (python_chunking과 공유)
cd /Users/woosik/repository/deepwiki-open
source .venv/bin/activate
```

### 2. 의존성 설치

```bash
cd python_kb
pip install -r requirements.txt
```

`requirements.txt`에 포함된 패키지:
- `google-generativeai>=0.8.0` - Gemini API
- `python-dotenv>=1.0.0` - 환경 변수 관리

### 3. 환경 변수 설정

`python_kb/.env` 파일을 생성하고 Gemini API 키를 설정하세요:

```bash
# python_kb/.env 파일 생성
cat > .env << 'EOF'
# Gemini API Configuration
GEMINI_API_KEY=AIzaSyCrt6pBUq-2YfeputHnBVqXHBCRc0_YbtQ

# PostgreSQL Configuration (for future use)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=deepwiki
DB_USER=postgres
DB_PASSWORD=
EOF
```

**주의:** 프로덕션 환경에서는 자신의 API 키를 사용하세요.

**Gemini API 키 발급 방법:**
1. [Google AI Studio](https://makersuite.google.com/app/apikey) 접속
2. "Get API Key" 클릭
3. 생성된 API 키를 `.env` 파일에 입력

## Quick Start

### 1. 가상환경 활성화

```bash
# 프로젝트 루트의 가상환경 활성화
cd /Users/woosik/repository/deepwiki-open
source .venv/bin/activate
cd python_kb
```

### 2. 프로젝트 분석 실행

```bash
# python_chunking 프로젝트 분석
python main.py ../python_chunking/

# 또는 영어로 출력
python main.py ../python_chunking/ --language en
```

### 3. 생성된 파일 확인

```bash
# 생성된 파일 목록 확인
ls -la python_kb/.adalflow/wikicache/python_chunking/

# 생성된 Wiki 파일 내용 확인
cat python_kb/.adalflow/wikicache/python_chunking/project_structure.md
cat python_kb/.adalflow/wikicache/python_chunking/architecture.md
cat python_kb/.adalflow/wikicache/python_chunking/conventions.md
cat python_kb/.adalflow/wikicache/python_chunking/environment.md
```

## 사용법

### 기본 사용

```bash
python main.py <project_path>
```

예시:
```bash
# python_chunking 프로젝트 분석
python main.py ../python_chunking/

# 현재 디렉토리의 프로젝트 분석
python main.py ./

# 절대 경로 사용
python main.py /Users/username/my_project/
```

### 옵션

```bash
# 캐시를 사용하지 않고 새로 생성
python main.py ../python_chunking/ --no-cache

# 기존 캐시를 무시하고 강제로 재생성
python main.py ../python_chunking/ --force

# 상세 로그 출력
python main.py ../python_chunking/ --verbose

# 캐시된 데이터만 사용하여 Markdown 생성
python main.py ../python_chunking/ --cache-only

# 영어로 출력
python main.py ../python_chunking/ --language en

# Mermaid 다이어그램 구문 검증
python main.py ../python_chunking/ --validate-mermaid

# Mermaid 구문 오류 자동 수정
python main.py ../python_chunking/ --fix-mermaid
```

## 출력 파일

생성된 파일은 `python_kb/.adalflow/wikicache/<project_name>/` 디렉토리에 저장됩니다:
- 저장 위치는 프로젝트 내부이지만, 규칙과 구조는 DeepWiki와 동일합니다

```
python_kb/.adalflow/wikicache/python_chunking/
├── project_metadata.json          # 프로젝트 메타데이터
├── project_structure.json          # 프로젝트 구조 페이지 캐시
├── architecture.json               # 아키텍처 페이지 캐시
├── conventions.json                # 규칙 페이지 캐시
├── environment.json                # 환경 설정 페이지 캐시
├── project_structure.md            # 프로젝트 구조 Markdown
├── architecture.md                 # 아키텍처 Markdown
├── conventions.md                  # 규칙 Markdown
└── environment.md                  # 환경 설정 Markdown
```

## 프로젝트 구조

```
python_kb/
├── __init__.py                 # 패키지 초기화
├── main.py                     # 메인 실행 파일
├── config.py                   # 설정 관리
├── prompts.py                  # Wiki 생성용 프롬프트 템플릿 (DeepWiki 참조)
├── logging_config.py           # 로깅 설정
├── file_tree_analyzer.py       # 파일 트리 분석
├── readme_parser.py            # README 파싱
├── gemini_client.py            # Gemini 2.5 Flash Lite LLM 클라이언트
├── wiki_generator.py           # Wiki 생성 로직
├── cache_manager.py            # 캐시 관리
├── markdown_exporter.py        # Markdown 내보내기
├── mermaid_validator.py        # Mermaid 다이어그램 구문 검증
├── requirements.txt            # Python 패키지 의존성
├── .env.example                # 환경 변수 예시
└── README.md                   # 이 파일
```

## 제외 규칙

다음 디렉토리와 파일은 자동으로 제외됩니다:

- 버전 관리: `.git`, `.svn`, `.hg`
- 패키지 관리: `node_modules`, `venv`, `.venv`
- 빌드 결과물: `dist`, `build`, `target`
- 캐시: `__pycache__`, `.pytest_cache`, `.mypy_cache`
- IDE 설정: `.idea`, `.vscode`, `.vs`
- 로그: `logs`, `log`, `tmp`, `temp`

## 요구사항

- Python 3.11.9
- Google Gemini API 키 ([Google AI Studio](https://makersuite.google.com/app/apikey)에서 발급)
- 공유 가상환경: `../.venv`

## 개발 정보

- **버전**: 0.1.0
- **기반**: Deepwiki 프로젝트
- **독립성**: python_chunking과 독립적으로 실행 가능

## 라이선스

MIT License

## 참고

이 도구는 [Deepwiki](https://github.com/deep-wiki/deepwiki-open) 프로젝트의 구조와 동작 원리를 참조하여 개발되었습니다.

