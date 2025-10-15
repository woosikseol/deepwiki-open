---
title: 환경 설정 및 가이드
project: python_kb
generated_at: 2025-10-15 16:59:44
generator: Python Knowledge Base Generator
---

# 환경 설정 가이드

## 사전 준비 사항

### 시스템 요구 사항
- 운영체제: 모든 주요 운영체제 (macOS, Linux, Windows)
- Python 버전: 3.11.9 이상
- 기타 도구: Git

### 필수 의존성
- google-generativeai>=0.8.0
- python-dotenv>=1.0.0

## 설치 가이드

### 1단계: Python 설치
```bash
# Homebrew를 사용하는 macOS의 경우:
brew install python@3.11

# apt를 사용하는 Ubuntu/Debian의 경우:
sudo apt update
sudo apt install python3.11 python3.11-venv

# Windows의 경우:
# Python 공식 웹사이트 (https://www.python.org/downloads/)에서 설치 프로그램을 다운로드하여 실행합니다.
# 설치 시 "Add Python to PATH" 옵션을 선택해야 합니다.
```

### 2단계: 저장소 복제
```bash
git clone <저장소 URL>
cd python_kb
```

### 3단계: 의존성 설치
프로젝트 루트 디렉토리에서 다음 명령을 실행합니다.
```bash
# 프로젝트 루트의 가상환경 사용 (python_chunking과 공유하는 경우)
cd /Users/woosik/repository/deepwiki-open # 필요에 따라 경로 조정
source .venv/bin/activate

# python_kb 디렉토리로 이동
cd python_kb

pip install -r requirements.txt
```

### 4단계: 환경 설정

#### 환경 변수
`.env` 파일을 생성하고 Gemini API 키를 설정합니다. `.env.example` 파일을 복사하여 편집하는 것이 좋습니다.
```bash
cp .env.example .env
```

`.env` 파일 내용 예시:
```
GEMINI_API_KEY=your_actual_api_key_here
```

**Gemini API 키 발급 방법:**
1. [Google AI Studio](https://makersuite.google.com/app/apikey)에 접속합니다.
2. "Get API Key"를 클릭합니다.
3. 생성된 API 키를 `.env` 파일에 입력합니다.

#### 설정 파일
`config.py` 파일은 필요에 따라 수정할 수 있습니다. 기본 설정은 대부분의 경우에 적합합니다.

## 검증

### 설치 확인
Python 및 필요한 패키지가 제대로 설치되었는지 확인합니다.
```bash
python --version
pip show google-generativeai python-dotenv
```

### 테스트 실행
테스트 코드는 `test_example.py` 에 존재합니다. 다음 명령어로 실행할 수 있습니다.

```bash
# pytest 설치 (필요한 경우)
pip install pytest

# 테스트 실행
pytest
```

### 예상 출력
테스트가 성공적으로 실행되면, 모든 테스트가 통과했다는 메시지가 표시됩니다.

## 개발 워크플로우

### 프로젝트 실행

#### 개발 모드
```bash
# python_chunking 프로젝트 분석 (개발 모드)
python main.py ../python_chunking/ --verbose
```

#### 운영 모드
운영 환경에서는 `--verbose` 옵션을 제거하여 로그 출력을 최소화할 수 있습니다.
```bash
# python_chunking 프로젝트 분석 (운영 모드)
python main.py ../python_chunking/
```

### 일반적인 명령어
- `python main.py <project_path>`: 지정된 프로젝트 경로를 분석하고 Knowledge Base를 생성합니다.
- `python main.py <project_path> --no-cache`: 캐시를 사용하지 않고 새로운 Knowledge Base를 생성합니다.
- `python main.py <project_path> --language en`: Knowledge Base를 영어로 생성합니다.

## 문제 해결

### 문제 1: Gemini API 키 오류
**문제**: `GEMINI_API_KEY` 환경 변수가 설정되지 않았거나 잘못 설정되었습니다.
**해결 방법**: `.env` 파일에 올바른 API 키가 입력되었는지 확인하고, 가상 환경이 활성화되었는지 확인합니다.

### 문제 2: 의존성 설치 오류
**문제**: `requirements.txt`에 명시된 패키지가 설치되지 않았습니다.
**해결 방법**: `pip install -r requirements.txt` 명령어를 다시 실행하고, 오류 메시지를 확인하여 누락된 시스템 의존성이 있는지 확인합니다.

## 추가 자료
- [Google AI Studio](https://makersuite.google.com/app/apikey): Gemini API 키 발급
- [Deepwiki GitHub](https://github.com/deep-wiki/deepwiki-open): Deepwiki 프로젝트

## 개발 팁
- 코드를 변경하기 전에 항상 최신 버전을 가져오고, 새로운 브랜치를 생성하여 작업합니다.
- 코드 변경 후에는 반드시 테스트를 실행하여 변경 사항이 기존 기능에 영향을 미치지 않는지 확인합니다.
- 커밋 메시지는 명확하고 간결하게 작성합니다.
