---
title: 규칙 및 규약 (명명 규칙, 규칙 등)
project: python_kb
generated_at: 2025-10-17 04:52:18
generator: Python Knowledge Base Generator
---

# 컨벤션

## 개요
이 문서는 `python_kb` 프로젝트의 코드 작성 및 구성에 대한 표준과 모범 사례를 정의합니다. 모든 개발자가 이 컨벤션을 준수함으로써 코드의 일관성, 가독성 및 유지보수성을 높이는 것을 목표로 합니다.

## 명명 규칙

### 파일 명명
-   **패턴**: 모든 Python 소스 파일(`.py`)은 `snake_case`를 사용합니다.
-   **예시**:
    -   `main.py`
    -   `config.py`
    -   `file_tree_analyzer.py`
    -   `gemini_client.py`
    -   `wiki_generator.py`
    -   `test_example.py`
-   **규칙**:
    -   파일 이름은 소문자와 밑줄(`_`)로 구성됩니다.
    -   파일의 목적을 명확하게 나타내야 합니다.
    -   테스트 파일은 `test_` 접두사를 사용합니다.

### 디렉토리 명명
-   **패턴**: 프로젝트의 서브 디렉토리 및 패키지 이름은 `snake_case`를 사용합니다. 숨김 디렉토리는 `.`으로 시작하며 `snake_case` 또는 `kebab-case`를 사용할 수 있습니다.
-   **예시**:
    -   `python_kb/` (프로젝트 루트)
    -   `.adalflow/wikicache/` (캐시 디렉토리)
-   **규칙**:
    -   패키지 및 모듈을 포함하는 디렉토리는 `snake_case`를 사용합니다.
    -   숨김 디렉토리는 `.git`, `.venv`와 같이 일반적으로 소문자와 하이픈(`-`) 또는 밑줄(`_`)을 사용합니다.

### 코드 명명

#### 변수
-   **컨벤션**: 지역 변수 및 인스턴스 변수는 `snake_case`를 사용합니다.
-   **예시**:
    -   `project_path`
    -   `language`
    -   `file_content`
    -   `cache_enabled`
-   **규칙**:
    -   변수 이름은 소문자와 밑줄(`_`)로 구성됩니다.
    -   변수의 목적을 명확하게 설명해야 합니다.
    -   짧고 의미 있는 이름을 선호합니다.

#### 함수/메서드
-   **컨벤션**: 함수 및 메서드 이름은 `snake_case`를 사용합니다.
-   **예시**:
    -   `analyze_project()`
    -   `generate_wiki()`
    -   `load_config()`
    -   `parse_readme()`
    -   `_validate_mermaid_syntax()` (내부/비공개 메서드)
-   **규칙**:
    -   함수/메서드 이름은 소문자와 밑줄(`_`)로 구성됩니다.
    -   동사 또는 동사구로 시작하여 해당 함수/메서드의 동작을 나타냅니다.
    -   내부적으로만 사용되는 메서드는 단일 밑줄(`_`)로 시작할 수 있습니다.

#### 클래스
-   **컨벤션**: 클래스 이름은 `CamelCase` (CapWords)를 사용합니다.
-   **예시**:
    -   `FileTreeAnalyzer`
    -   `GeminiClient`
    -   `WikiGenerator`
    -   `CacheManager`
    -   `MermaidValidator`
-   **규칙**:
    -   클래스 이름은 각 단어의 첫 글자를 대문자로 하고 공백 없이 연결합니다.
    -   명사 또는 명사구로 구성되어 해당 클래스가 나타내는 개념을 설명합니다.

#### 상수
-   **컨벤션**: 모듈 수준의 상수는 `UPPER_SNAKE_CASE`를 사용합니다.
-   **예시**:
    -   `GEMINI_API_KEY` (환경 변수)
    -   `DB_HOST`
    -   `DEFAULT_LANGUAGE`
    -   `CACHE_DIR_NAME`
-   **규칙**:
    -   상수 이름은 대문자와 밑줄(`_`)로 구성됩니다.
    -   값은 프로그램 실행 중에 변경되지 않아야 합니다.

## 코드 구성

### 파일 구조
-   **설명**: `python_kb` 프로젝트는 비교적 평평한(flat) 파일 구조를 가지고 있으며, 각 `.py` 파일은 특정 기능 영역을 담당하는 모듈로 구성됩니다. `main.py`는 애플리케이션의 진입점 역할을 합니다.
-   **예시**:
    ```
    python_kb/
    ├── main.py                 # 메인 실행 파일
    ├── config.py               # 설정 관리
    ├── prompts.py              # LLM 프롬프트 템플릿
    ├── file_tree_analyzer.py   # 파일 트리 분석 로직
    ├── gemini_client.py        # Gemini API 클라이언트
    ├── wiki_generator.py       # Wiki 생성 로직
    └── ...
    ```

### 모듈 구성
-   **설명**: 각 Python 파일은 하나의 논리적 단위 또는 관련 기능 집합을 캡슐화하는 모듈로 작동합니다. 이는 코드의 응집도를 높이고 결합도를 낮추는 데 기여합니다.
-   **예시**:
    -   `gemini_client.py`: Gemini API와의 모든 상호작용을 처리합니다.
    -   `cache_manager.py`: 캐시 생성, 읽기, 쓰기 등 캐시 관련 로직을 관리합니다.
    -   `mermaid_validator.py`: Mermaid 다이어그램 구문 검증 로직을 포함합니다.

### 임포트 컨벤션
-   **설명**: 표준 Python 임포트 규칙을 따르며, 가독성을 위해 임포트 순서를 지킵니다.
-   **규칙**:
    1.  표준 라이브러리 임포트 (예: `os`, `sys`, `logging`)
    2.  서드파티 라이브러리 임포트 (예: `google.generativeai`, `dotenv`)
    3.  로컬 애플리케이션/프로젝트 관련 임포트 (예: `from config import settings`, `import cache_manager`)
    -   각 그룹 내에서는 알파벳 순서를 유지합니다.
    -   `from ... import ...` 형식을 선호하여 필요한 객체만 임포트합니다.
    -   순환 임포트를 피합니다.

## 코딩 스타일

### 포맷팅
-   **설명**: PEP 8 스타일 가이드를 준수합니다. 일관된 코드 포맷팅을 위해 자동 포매터(예: `black`) 사용을 권장합니다.
-   **규칙**:
    -   **들여쓰기**: 4개의 공백을 사용합니다. 탭은 사용하지 않습니다.
    -   **줄 길이**: 한 줄의 길이는 79자(최대 99자)를 넘지 않도록 합니다.
    -   **공백**: 연산자 주위, 콤마 뒤 등에 적절한 공백을 사용합니다.
    -   **빈 줄**: 함수/클래스 정의 사이, 논리적 블록 사이에 빈 줄을 사용하여 가독성을 높입니다.

### 문서화
-   **설명**: 코드의 이해를 돕기 위해 적절한 주석과 독스트링을 작성합니다.
-   **규칙**:
    -   **모듈 독스트링**: 각 `.py` 파일의 시작 부분에 모듈의 목적과 주요 기능을 설명하는 독스트링을 작성합니다.
    -   **클래스 독스트링**: 각 클래스 정의 바로 아래에 클래스의 역할, 속성, 사용법 등을 설명하는 독스트링을 작성합니다.
    -   **함수/메서드 독스트링**: 각 함수/메서드 정의 바로 아래에 함수의 목적, 인자(`Args`), 반환 값(`Returns`), 발생 가능한 예외(`Raises`) 등을 설명하는 독스트링을 작성합니다. Google 스타일 독스트링을 권장합니다.
    -   **주석**: 복잡한 로직이나 특정 결정에 대한 설명을 위해 코드 내에 인라인 주석을 사용합니다. `TODO`, `FIXME` 주석을 사용하여 개선이 필요한 부분을 표시합니다.

### 에러 핸들링
-   **설명**: 예상되는 오류 상황에 대해 `try-except` 블록을 사용하여 견고한 코드를 작성합니다.
-   **규칙**:
    -   **구체적인 예외 처리**: 일반적인 `except Exception:` 대신 가능한 한 구체적인 예외를 잡습니다 (예: `FileNotFoundError`, `requests.exceptions.RequestException`).
    -   **예외 전파**: 처리할 수 없는 예외는 적절히 로깅한 후 다시 발생시키거나(re-raise) 상위 호출자에게 전파합니다.
    -   **로깅**: 에러 발생 시 `logging` 모듈을 사용하여 상세한 에러 메시지를 기록합니다.
    -   **사용자 피드백**: 사용자에게 의미 있는 에러 메시지를 제공하여 문제 해결을 돕습니다.

## 프로젝트-특정 컨벤션

### 테스팅
-   **컨벤션**: 테스트 파일은 `test_` 접두사를 사용하며, 테스트 함수도 `test_` 접두사를 사용합니다. `pytest` 프레임워크를 사용하는 것으로 보입니다.
-   **예시**:
    -   `test_example.py`
    -   `test_llm_validator.py`
    -   `def test_file_parsing():`
-   **규칙**:
    -   테스트 파일은 프로젝트 루트에 위치하거나 별도의 `tests/` 디렉토리에 위치할 수 있습니다.
    -   각 테스트 함수는 특정 기능 또는 시나리오를 검증해야 합니다.
    -   테스트는 독립적이고 반복 가능해야 합니다.

### 설정
-   **컨벤션**: 애플리케이션의 일반 설정은 `config.py` 파일에서 관리하며, 민감한 정보(API 키, DB 자격 증명)는 `.env` 파일을 통해 환경 변수로 관리합니다.
-   **예시**:
    -   `config.py` (예: `DEFAULT_LANGUAGE = "ko"`)
    -   `.env` (예: `GEMINI_API_KEY=...`, `DB_HOST=localhost`)
-   **규칙**:
    -   `python-dotenv` 라이브러리를 사용하여 `.env` 파일의 환경 변수를 로드합니다.
    -   `config.py`는 기본값, 상수, 또는 환경 변수에서 파생된 설정을 제공합니다.
    -   `.env` 파일은 버전 관리 시스템에 포함하지 않으며, `.env.example` 파일을 제공하여 필요한 변수를 명시합니다.

### 빌드 및 배포
-   **컨벤션**: Python 패키지 의존성은 `requirements.txt` 파일에 명시하고, 가상 환경(`venv` 또는 `.venv`)을 사용하여 프로젝트별 의존성을 격리합니다.
-   **예시**:
    -   `requirements.txt`
    -   `.venv/`
-   **규칙**:
    -   `pip install -r requirements.txt` 명령어를 사용하여 의존성을 설치합니다.
    -   프로젝트 실행 전 항상 가상 환경을 활성화합니다.
    -   `python main.py` 명령어를 통해 애플리케이션을 실행합니다.

## 모범 사례

-   **PEP 8 준수**: Python 코드의 가독성과 일관성을 위해 PEP 8 스타일 가이드를 철저히 준수합니다.
-   **모듈성**: 각 모듈은 단일 책임 원칙(Single Responsibility Principle)을 따르도록 설계하여, 특정 기능에 집중하고 다른 모듈과의 의존성을 최소화합니다.
-   **명확한 변수/함수 이름**: 변수, 함수, 클래스 이름은 그 목적과 역할을 명확하게 나타내야 합니다.
-   **적절한 주석 및 독스트링**: 코드의 "왜(Why)"를 설명하는 주석과 "무엇(What)"을 설명하는 독스트링을 충분히 작성합니다.
-   **예외 처리**: 사용자 입력, 외부 API 호출, 파일 I/O 등 오류가 발생할 수 있는 모든 지점에서 적절한 예외 처리를 구현합니다.
-   **로깅 활용**: `print()` 문 대신 `logging` 모듈을 사용하여 애플리케이션의 상태, 경고, 오류 등을 기록합니다.

## 예시

### 좋은 예시
```python
# gemini_client.py

import logging
import os
from typing import Optional

import google.generativeai as genai
from dotenv import load_dotenv

# 로깅 설정 로드 (logging_config.py에서 설정되었다고 가정)
logger = logging.getLogger(__name__)

class GeminiClient:
    """
    Google Gemini API와 상호작용하는 클라이언트 클래스입니다.

    환경 변수에서 GEMINI_API_KEY를 로드하여 API 요청을 처리합니다.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        GeminiClient를 초기화합니다.

        Args:
            api_key (Optional[str]): Gemini API 키. 제공되지 않으면 .env에서 로드합니다.
        """
        load_dotenv()  # .env 파일 로드
        self._api_key = api_key if api_key else os.getenv("GEMINI_API_KEY")
        if not self._api_key:
            logger.error("GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")
            raise ValueError("GEMINI_API_KEY is not set.")
        genai.configure(api_key=self._api_key)
        self._model = genai.GenerativeModel('gemini-1.5-flash-latest')
        logger.info("GeminiClient가 성공적으로 초기화되었습니다.")

    def generate_content(self, prompt: str, temperature: float = 0.7) -> str:
        """
        주어진 프롬프트를 사용하여 Gemini 모델로부터 콘텐츠를 생성합니다.

        Args:
            prompt (str): LLM에 전달할 프롬프트 문자열.
            temperature (float): 생성 다양성을 제어하는 온도 값 (0.0 ~ 1.0).

        Returns:
            str: Gemini 모델이 생성한 텍스트 콘텐츠.

        Raises:
            Exception: API 호출 중 오류가 발생한 경우.
        """
        try:
            response = self._model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(temperature=temperature)
            )
            if response.candidates:
                generated_text = response.candidates[0].content.parts[0].text
                logger.debug(f"Gemini 응답: {generated_text[:100]}...")
                return generated_text
            else:
                logger.warning("Gemini API 응답에 후보가 없습니다.")
                return ""
        except Exception as e:
            logger.error(f"Gemini API 호출 중 오류 발생: {e}")
            raise # 예외를 다시 발생시켜 상위 호출자에게 알림

```

### 피해야 할 안티패턴
```python
# bad_code.py

import os, sys # 여러 임포트를 한 줄에
from config import * # 와일드카드 임포트

class myclass: # 클래스 이름이 CamelCase가 아님
    def __init__(self, key):
        self.key = key
        self.model = None # 초기화되지 않은 변수

    def getdata(self, p): # 함수 이름이 snake_case가 아님
        try:
            # 복잡한 로직...
            if p == "":
                print("프롬프트가 비어있습니다.") # 로깅 대신 print 사용
                return None
            # API 키가 설정되지 않았을 때 오류 처리 없음
            self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
            res = self.model.generate_content(p)
            return res.candidates[0].content.parts[0].text
        except: # 일반적인 예외 처리
            print("오류 발생!") # 상세 정보 없이 오류 메시지 출력
            pass # 예외를 무시

# 전역 변수 사용
API_KEY = os.getenv("GEMINI_API_KEY")
```