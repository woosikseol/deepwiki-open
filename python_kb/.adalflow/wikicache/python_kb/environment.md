---
title: 환경 설정 및 가이드
project: python_kb
generated_at: 2025-10-17 04:52:18
generator: Python Knowledge Base Generator
---

# 환경 설정 및 가이드

이 문서는 `python_kb` 프로젝트 개발을 위한 환경 설정 방법을 안내합니다.

## 전제 조건

### 시스템 요구 사항
- **운영 체제**: Linux, macOS, Windows (Python 3.11.9를 지원하는 모든 OS)
- **Python 버전**: `Python 3.11.9`
- **기타 도구**:
    - `pip` (Python 패키지 관리자)
    - `git` (소스 코드 관리)
    - `Google Gemini API 키` ([Google AI Studio](https://makersuite.google.com/app/apikey)에서 발급)

### 필수 의존성
`requirements.txt` 파일에 명시된 주요 Python 패키지들은 다음과 같습니다:
- `google-generativeai>=0.8.0`: Google Gemini API와의 상호작용을 위한 라이브러리.
- `python-dotenv>=1.0.0`: `.env` 파일에서 환경 변수를 로드하기 위한 라이브러리.

이 프로젝트는 상위 `deepwiki-open` 프로젝트의 공유 가상 환경 (`../.venv`)을 사용하도록 설계되었습니다.

## 설치 가이드

### 1단계: Python 및 가상 환경 설정
`python_kb`는 상위 `deepwiki-open` 프로젝트의 가상 환경을 공유합니다. 먼저 `deepwiki-open` 저장소를 클론하고 가상 환경을 설정합니다.

```bash
# 1. deepwiki-open 저장소 클론 (이미 클론했다면 생략)
# git clone https://github.com/your-org/deepwiki-open.git
# cd deepwiki-open

# 2. 가상 환경 생성 및 활성화 (deepwiki-open 프로젝트 루트에서)
# .venv 디렉토리가 없다면 생성
python3.11 -m venv .venv
source .venv/bin/activate

# 3. python_kb 디렉토리로 이동
cd python_kb
```

### 2단계: 의존성 설치
`python_kb` 프로젝트 디렉토리로 이동한 후, `requirements.txt`에 명시된 모든 의존성을 설치합니다.

```bash
# python_kb 디렉토리 내에서 실행
pip install -r requirements.txt
```

### 3단계: 환경 변수 설정

#### 환경 변수 파일 (`.env`) 생성
프로젝트의 루트 디렉토리 (`python_kb/`)에 `.env` 파일을 생성하고, 필요한 환경 변수들을 설정합니다. 특히 `GEMINI_API_KEY`는 필수입니다.

```bash
# python_kb/.env 파일 생성
cat > .env << 'EOF'
# Gemini API Configuration
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE

# PostgreSQL Configuration (향후 사용을 위해 포함될 수 있음)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=deepwiki
DB_USER=postgres
DB_PASSWORD=
EOF
```
**주의**: `YOUR_GEMINI_API_KEY_HERE` 부분을 [Google AI Studio](https://makersuite.google.com/app/apikey)에서 발급받은 실제 Gemini API 키로 교체해야 합니다.

#### Gemini API 키 발급 방법
1.  [Google AI Studio](https://makersuite.google.com/app/apikey)에 접속합니다.
2.  "Get API Key" 버튼을 클릭합니다.
3.  생성된 API 키를 복사하여 `.env` 파일의 `GEMINI_API_KEY` 값으로 입력합니다.

#### 설정 파일
현재 프로젝트는 `.env` 파일을 통해 환경 변수를 관리하며, 별도의 복잡한 설정 파일은 없습니다. `config.py` 파일에서 이러한 환경 변수들을 로드하여 사용합니다.

## 검증

### 설치 확인
Python 버전과 설치된 패키지 목록을 확인하여 환경 설정이 올바르게 되었는지 검증합니다.

```bash
# 가상 환경이 활성화된 상태에서 Python 버전 확인
python --version

# 설치된 패키지 목록 확인
pip list | grep -E 'google-generativeai|python-dotenv'
```
**예상 출력**:
```
Python 3.11.9
google-generativeai             0.8.0
python-dotenv                   1.0.0
```
(버전은 다를 수 있습니다.)

### 테스트 실행
프로젝트에 포함된 테스트 스크립트를 실행하여 기본적인 기능이 올바르게 작동하는지 확인합니다. `pytest`가 `requirements.txt`에 포함되어 있지 않으므로, 필요하다면 별도로 설치해야 합니다.

```bash
# pytest 설치 (아직 설치되지 않았다면)
pip install pytest

# 테스트 실행
pytest
```
**예상 출력**:
```
============================= test session starts ==============================
...
collected 2 items

test_example.py ..                                                       [100%]
test_llm_validator.py ..                                                 [100%]

============================== 2 passed in X.XXs ===============================
```
(테스트 결과는 프로젝트의 현재 상태에 따라 다를 수 있습니다.)

### 예상 출력
성공적인 환경 설정 후, `main.py` 스크립트를 실행하면 지정된 프로젝트의 분석 결과가 Markdown 파일로 `python_kb/.adalflow/wikicache/<project_name>/` 디렉토리에 생성됩니다.

```bash
# 예시: python_chunking 프로젝트 분석 실행
python main.py ../python_chunking/

# 생성된 파일 목록 확인
ls -la .adalflow/wikicache/python_chunking/
```
**예상 출력**:
```
total 160
drwxr-xr-x   9 user  group   288  1 15 10:00 .
drwxr-xr-x   3 user  group    96  1 15 10:00 ..
-rw-r--r--   1 user  group  1024  1 15 10:00 architecture.json
-rw-r--r--   1 user  group  2048  1 15 10:00 architecture.md
-rw-r--r--   1 user  group  1024  1 15 10:00 conventions.json
-rw-r--r--   1 user  group  2048  1 15 10:00 conventions.md
-rw-r--r--   1 user  group  1024  1 15 10:00 environment.json
-rw-r--r--   1 user  group  2048  1 15 10:00 environment.md
-rw-r--r--   1 user  group  1024  1 15 10:00 project_metadata.json
-rw-r--r--   1 user  group  1024  1 15 10:00 project_structure.json
-rw-r--r--   1 user  group  2048  1 15 10:00 project_structure.md
```
(파일 목록 및 크기는 분석 대상 프로젝트에 따라 다를 수 있습니다.)

## 개발 워크플로우

### 프로젝트 실행

#### 개발 모드
개발 중에는 `--verbose` 플래그를 사용하여 상세 로그를 확인하거나, `--no-cache` 또는 `--force` 플래그를 사용하여 캐시를 무시하고 새로 생성할 수 있습니다.

```bash
# 가상 환경 활성화 (deepwiki-open 프로젝트 루트에서)
# source ../.venv/bin/activate
# cd python_kb

# 상세 로그와 함께 python_chunking 프로젝트 분석 (캐시 사용 안 함)
python main.py ../python_chunking/ --verbose --no-cache

# 기존 캐시를 무시하고 강제로 재생성
python main.py ../python_chunking/ --force

# 영어로 Wiki 생성
python main.py ../python_chunking/ --language en
```

#### 프로덕션 모드
`python_kb`는 CLI 도구이므로, "프로덕션 모드"는 일반적으로 추가적인 디버깅 플래그 없이 도구를 실행하여 지식 기반을 생성하는 것을 의미합니다.

```bash
# 가상 환경 활성화 (deepwiki-open 프로젝트 루트에서)
# source ../.venv/bin/activate
# cd python_kb

# python_chunking 프로젝트 분석 (기본 설정, 캐시 사용)
python main.py ../python_chunking/

# 현재 디렉토리의 프로젝트 분석
python main.py ./
```

### 일반 명령어
- `python main.py <project_path>`: 지정된 프로젝트의 지식 기반을 생성합니다.
- `python main.py <project_path> --language en`: 지식 기반을 영어로 생성합니다.
- `python main.py <project_path> --no-cache`: 캐시를 사용하지 않고 새로 생성합니다.
- `python main.py <project_path> --force`: 기존 캐시를 무시하고 강제로 재생성합니다.
- `python main.py <project_path> --verbose`: 상세 로그를 출력합니다.
- `python main.py <project_path> --cache-only`: 캐시된 데이터만 사용하여 Markdown을 생성합니다.
- `python main.py <project_path> --validate-mermaid`: Mermaid 다이어그램 구문만 검증합니다.
- `python main.py <project_path> --fix-mermaid`: Mermaid 구문 오류를 자동으로 수정합니다.

## 문제 해결

### 문제 1: Gemini API 키 누락 또는 오류
**문제**: `google.generativeai.types.core.APIError: API key not found.` 또는 인증 오류가 발생합니다.
**해결**:
1.  `python_kb/.env` 파일이 올바르게 생성되었는지 확인합니다.
2.  `.env` 파일 내의 `GEMINI_API_KEY` 값이 [Google AI Studio](https://makersuite.google.com/app/apikey)에서 발급받은 유효한 API 키인지 다시 확인합니다.
3.  API 키 앞뒤에 공백이 없는지 확인합니다.

### 문제 2: 가상 환경이 활성화되지 않음
**문제**: `ModuleNotFoundError`가 발생하거나 `pip install` 명령이 전역 Python 환경에 패키지를 설치합니다.
**해결**:
1.  `deepwiki-open` 프로젝트 루트 디렉토리로 이동합니다.
2.  `source .venv/bin/activate` 명령을 사용하여 가상 환경을 활성화합니다.
3.  가상 환경이 활성화되면 터미널 프롬프트에 `(.venv)`와 같은 표시가 나타나는지 확인합니다.

### 문제 3: `requirements.txt` 파일을 찾을 수 없음
**문제**: `pip install -r requirements.txt` 명령 실행 시 `No such file or directory: 'requirements.txt'` 오류가 발생합니다.
**해결**:
1.  현재 작업 디렉토리가 `python_kb` 프로젝트 루트인지 확인합니다. `pwd` 명령으로 현재 경로를 확인하고, 필요하다면 `cd python_kb`로 이동합니다.
2.  `requirements.txt` 파일이 `python_kb` 디렉토리 내에 존재하는지 확인합니다.

## 추가 자료
- **Google AI Studio**: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey) (Gemini API 키 발급)
- **Deepwiki 프로젝트**: [https://github.com/deep-wiki/deepwiki-open](https://github.com/deep-wiki/deepwiki-open) (이 프로젝트의 기반이 된 원본 프로젝트)

## 개발 팁
- **캐시 활용**: `python_kb/.adalflow/wikicache/<project_name>/` 디렉토리에 생성되는 캐시 파일을 이해하면 LLM 호출 비용을 절약하고 개발 속도를 높일 수 있습니다. `--no-cache` 또는 `--force` 옵션을 사용하여 캐시 동작을 제어할 수 있습니다.
- **Mermaid 다이어그램 검증**: `--validate-mermaid` 및 `--fix-mermaid` 옵션을 활용하여 LLM이 생성한 Mermaid 다이어그램의 구문 오류를 쉽게 검증하고 수정할 수 있습니다. 이는 다이어그램의 품질을 높이는 데 매우 유용합니다.
- **로깅**: `--verbose` 플래그를 사용하여 상세한 로그를 확인하면 문제 발생 시 디버깅에 큰 도움이 됩니다. `logging_config.py` 파일을 통해 로깅 설정을 커스터마이징할 수도 있습니다.