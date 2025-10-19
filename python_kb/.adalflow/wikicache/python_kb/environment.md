---
title: 환경 설정 및 가이드
project: python_kb
generated_at: 2025-10-19 18:37:42
generator: Python Knowledge Base Generator
---

# 환경 설정 및 가이드

이 문서는 `python_kb` 프로젝트 개발을 위한 환경 설정 방법을 안내합니다.

## 전제 조건

### 시스템 요구 사항
- **운영 체제**: Linux, macOS, Windows (Python 및 Node.js를 지원하는 모든 OS)
- **Python 버전**: `3.11.9`
- **기타 도구**:
    - **Node.js 및 npm/npx**: Mermaid CLI 설치 및 실행에 필요합니다.
    - **Chrome 브라우저**: Mermaid CLI (Puppeteer)가 다이어그램을 렌더링하는 데 필요합니다.

### 필수 의존성
- `google-generativeai>=0.8.0`: Google Gemini API 연동
- `python-dotenv>=1.0.0`: 환경 변수 관리
- `npx puppeteer`: Mermaid CLI가 Chrome을 제어하여 다이어그램을 렌더링하는 데 사용됩니다.

## 설치 가이드

### 1단계: Python 및 가상 환경 설정
`python_kb` 프로젝트는 상위 `deepwiki-open` 프로젝트의 공유 가상 환경을 사용하도록 설계되었습니다.

1.  **Python 3.11.9 설치**: 시스템에 Python 3.11.9가 설치되어 있는지 확인합니다. 설치되어 있지 않다면, [Python 공식 웹사이트](https://www.python.org/downloads/)에서 다운로드하여 설치하세요.
2.  **가상 환경 활성화**: `deepwiki-open` 프로젝트의 루트 디렉토리로 이동하여 가상 환경을 활성화합니다.

    ```bash
    # deepwiki-open 프로젝트 루트 디렉토리로 이동
    cd /Users/woosik/repository/deepwiki-open # 실제 경로로 변경하세요
    
    # 가상 환경 활성화
    source .venv/bin/activate
    
    # python_kb 디렉토리로 이동
    cd python_kb
    ```
    (참고: `.venv` 가상 환경이 없다면, `python3.11 -m venv .venv` 명령으로 생성 후 활성화하세요.)

### 2단계: 저장소 클론
`python_kb`는 `deepwiki-open` 저장소의 하위 디렉토리입니다. `deepwiki-open` 저장소를 클론합니다.

```bash
# 원하는 위치에서 deepwiki-open 저장소 클론
git clone https://github.com/deep-wiki/deepwiki-open.git

# 클론한 디렉토리로 이동
cd deepwiki-open

# python_kb 디렉토리로 이동
cd python_kb
```

### 3단계: 의존성 설치

#### Python 의존성 설치
활성화된 가상 환경에서 `requirements.txt`에 명시된 Python 패키지를 설치합니다.

```bash
# python_kb 디렉토리에서 실행
pip install -r requirements.txt
```

#### Mermaid CLI 및 Chrome 설치
Mermaid 다이어그램 렌더링을 위해 Mermaid CLI와 Puppeteer Chrome을 설치해야 합니다.

```bash
# deepwiki-open 프로젝트 루트 디렉토리로 이동 (python_kb 디렉토리에서 상위로 이동)
cd ..

# Puppeteer Chrome 설치
npx puppeteer browsers install chrome
```
설치 후 `.puppeteerrc.cjs` 파일이 자동으로 생성되며, Mermaid CLI가 Chrome을 찾을 수 있도록 경로를 지정합니다.

### 4단계: 설정

#### 환경 변수
`python_kb` 디렉토리 내에 `.env` 파일을 생성하고 필요한 환경 변수를 설정합니다. 특히 Gemini API 키는 필수입니다.

```bash
# python_kb 디렉토리에서 실행
cat > .env << 'EOF'
# Gemini API Configuration
GEMINI_API_KEY=YOUR_GEMINI_API_KEY # 여기에 발급받은 Gemini API 키를 입력하세요

# PostgreSQL Configuration (향후 사용을 위해 포함)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=deepwiki
DB_USER=postgres
DB_PASSWORD=
EOF
```
**주의**: `GEMINI_API_KEY`는 반드시 본인의 API 키로 교체해야 합니다.
**Gemini API 키 발급 방법**:
1.  [Google AI Studio](https://makersuite.google.com/app/apikey)에 접속합니다.
2.  "Get API Key"를 클릭하여 새로운 API 키를 생성합니다.
3.  생성된 API 키를 `.env` 파일의 `GEMINI_API_KEY` 값으로 입력합니다.

#### 설정 파일
별도의 추가 설정 파일은 필요하지 않습니다. 모든 설정은 `.env` 파일 또는 명령줄 인수를 통해 관리됩니다.

## 검증

### 설치 확인
다음 명령어를 통해 환경 설정이 올바르게 되었는지 확인할 수 있습니다.

1.  **Python 및 패키지 확인**:
    ```bash
    # python_kb 디렉토리에서 실행
    python --version
    pip list | grep -E "google-generativeai|python-dotenv"
    ```
    출력: `Python 3.11.9` 및 설치된 패키지 목록이 보여야 합니다.

2.  **Mermaid CLI 및 Chrome 확인**:
    ```bash
    # deepwiki-open 프로젝트 루트 디렉토리에서 실행
    echo "graph TD
        A[Start] --> B[End]" > /tmp/test.mmd
    mmdc -i /tmp/test.mmd -o /tmp/test.svg
    ```
    성공하면 `Generating single mermaid chart` 메시지가 표시되고 `/tmp/test.svg` 파일이 생성됩니다.

### 테스트 실행
`python_kb` 프로젝트에는 몇 가지 테스트 파일이 포함되어 있습니다. `pytest`를 사용하여 테스트를 실행할 수 있습니다.

```bash
# python_kb 디렉토리에서 실행
pip install pytest # pytest가 설치되어 있지 않다면 설치
pytest
```
모든 테스트가 성공적으로 통과해야 합니다.

### 예상 출력
모든 설치 및 설정이 성공적으로 완료되면, `main.py` 스크립트를 실행하여 프로젝트 분석 및 Wiki 생성을 수행할 수 있습니다.

```bash
# python_kb 디렉토리에서 실행
python main.py ../python_chunking/
```
이 명령을 실행하면 `python_kb/.adalflow/wikicache/python_chunking/` 디렉토리에 Markdown 및 JSON 파일이 생성됩니다.

## 개발 워크플로우

### 프로젝트 실행

#### 개발 모드 (표준 실행)
`python_kb`는 주로 명령줄 도구로 사용됩니다. 개발 중에는 다양한 옵션을 사용하여 실행할 수 있습니다.

```bash
# python_kb 디렉토리에서 실행
# python_chunking 프로젝트 분석 (기본 한국어 출력)
python main.py ../python_chunking/

# 영어로 출력
python main.py ../python_chunking/ --language en

# 캐시를 사용하지 않고 새로 생성
python main.py ../python_chunking/ --no-cache

# 기존 캐시를 무시하고 강제로 재생성
python main.py ../python_chunking/ --force

# 상세 로그 출력
python main.py ../python_chunking/ --verbose

# 캐시된 데이터만 사용하여 Markdown 생성 (LLM 호출 없음)
python main.py ../python_chunking/ --cache-only
```

#### 디버깅 설정
Python 프로젝트 디버깅은 일반적으로 IDE (VS Code, PyCharm 등)의 디버거를 사용하거나 `pdb`와 같은 내장 디버거를 사용합니다.

**VS Code 예시**:
1.  `python_kb` 디렉토리를 VS Code로 엽니다.
2.  `main.py` 파일에 중단점(breakpoint)을 설정합니다.
3.  `Run and Debug` 뷰로 이동하여 `launch.json` 파일을 생성하거나 수정합니다.
    ```json
    {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Current File",
                "type": "python",
                "request": "launch",
                "program": "${file}",
                "console": "integratedTerminal",
                "args": ["../python_chunking/"] // 여기에 필요한 인수를 추가
            }
        ]
    }
    ```
4.  `main.py` 파일을 열고 F5 키를 눌러 디버깅을 시작합니다.

### 일반적인 명령어
- `python main.py <project_path>`: 지정된 프로젝트 경로를 분석하고 Wiki를 생성합니다.
- `python main.py <project_path> --language en`: Wiki를 영어로 생성합니다.
- `python main.py <project_path> --force`: 캐시를 무시하고 모든 내용을 강제로 재생성합니다.
- `pytest`: 프로젝트의 단위 및 통합 테스트를 실행합니다.

## 문제 해결

### 문제 1: Mermaid CLI Chrome 설치 실패 또는 찾을 수 없음
**문제**: `npx puppeteer browsers install chrome` 명령이 실패하거나, `mmdc` 실행 시 Chrome을 찾을 수 없다는 오류가 발생합니다.
**해결**:
1.  **Chrome 버전 확인**: `ls ~/.cache/puppeteer/chrome/` 명령으로 설치된 Chrome 버전을 확인합니다.
2.  **재설치**: 기존 캐시를 제거하고 다시 설치를 시도합니다.
    ```bash
    rm -rf ~/.cache/puppeteer/chrome
    npx puppeteer browsers install chrome
    ```
3.  **Node.js 및 npm 확인**: Node.js와 npm이 올바르게 설치되어 있고 PATH에 추가되어 있는지 확인합니다.

### 문제 2: Gemini API 키 오류 (403 Forbidden, 인증 실패 등)
**문제**: `GEMINI_API_KEY`가 올바르게 설정되지 않았거나 유효하지 않아 LLM 호출이 실패합니다.
**해결**:
1.  **`.env` 파일 확인**: `python_kb/.env` 파일이 올바른 위치에 있고 `GEMINI_API_KEY` 변수가 정확하게 설정되어 있는지 확인합니다.
2.  **API 키 유효성 확인**: [Google AI Studio](https://makersuite.google.com/app/apikey)에서 발급받은 API 키가 유효한지 다시 확인합니다. 만료되었거나 잘못된 키일 수 있습니다.
3.  **환경 변수 로드 확인**: `python-dotenv`가 `.env` 파일을 제대로 로드하는지 확인합니다. 코드 내에서 `os.getenv('GEMINI_API_KEY')`를 출력하여 값이 올바른지 확인해 볼 수 있습니다.

## 추가 자료
- **Google AI Studio**: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey) (Gemini API 키 발급)
- **Deepwiki 프로젝트**: [https://github.com/deep-wiki/deepwiki-open](https://github.com/deep-wiki/deepwiki-open) (이 프로젝트의 기반이 된 원본 프로젝트)
- **Python 공식 문서**: [https://docs.python.org/](https://docs.python.org/)
- **Mermaid CLI**: [https://github.com/mermaid-js/mermaid-cli](https://github.com/mermaid-js/mermaid-cli)

## 개발 팁
- **가상 환경 사용**: 항상 가상 환경 내에서 작업하여 프로젝트 의존성이 시스템 전체에 영향을 미치지 않도록 합니다.
- **API 키 보안**: `.env` 파일은 `.gitignore`에 추가되어 버전 관리 시스템에 커밋되지 않도록 합니다. 절대 API 키를 코드에 직접 하드코딩하지 마세요.
- **캐시 활용**: `python_kb`는 `.adalflow/wikicache/` 디렉토리에 캐시를 저장합니다. LLM 호출 비용을 절약하고 개발 속도를 높이려면 `--no-cache` 또는 `--force` 옵션을 신중하게 사용하세요. `--cache-only` 옵션은 LLM 호출 없이 캐시된 데이터로만 Markdown을 재생성할 때 유용합니다.
- **로그 확인**: `--verbose` 옵션을 사용하여 상세 로그를 확인하면 문제 발생 시 디버깅에 큰 도움이 됩니다.