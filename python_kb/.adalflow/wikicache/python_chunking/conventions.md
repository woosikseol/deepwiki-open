---
title: 규칙 및 규약 (명명 규칙, 규칙 등)
project: python_chunking
generated_at: 2025-10-15 18:25:42
generator: Python Knowledge Base Generator
---

# Conventions

## Overview
이 문서는 `python_chunking` 프로젝트의 코딩 컨벤션과 표준을 설명합니다. 이 문서를 통해 개발자들은 일관성 있고 유지보수 가능한 코드를 작성할 수 있습니다. 이 프로젝트는 TypeScript 기반의 Continue 프로젝트의 코드 청킹 시스템을 Python으로 포팅한 것이며, Tree-sitter를 사용하여 소스코드를 구조적으로 청킹합니다. 따라서 기존 Continue 프로젝트의 컨벤션과 유사한 부분이 있을 수 있습니다.

## Naming Conventions

### File Naming
- Pattern: snake_case.py
- Examples: `main.py`, `build_parsers.py`, `tree_sitter.py`, `pgvector_index.py`
- Rules: Python 파일은 snake_case를 사용하여 이름을 짓습니다. 모든 단어는 소문자로 작성하고, 단어 사이에는 밑줄(_)을 사용합니다.

### Directory Naming
- Pattern: lowercase
- Examples: `core`, `indexing`, `embeddings`, `util`, `vendor`, `test_files`
- Rules: 디렉토리 이름은 모두 소문자로 작성합니다. 여러 단어를 조합할 경우, 밑줄(_)을 사용하지 않습니다.

### Code Naming

#### Variables
- Convention: snake_case
- Examples: `embeddings_provider`, `cache_key`, `start_line`, `end_line`, `n_retrieve`
- Variables should be named using snake_case.

#### Functions/Methods
- Convention: snake_case
- Examples: `get_chunks`, `get_embeddings`, `insert_chunks`, `retrieve`, `count_tokens`
- Functions and methods should be named using snake_case.

#### Classes
- Convention: PascalCase
- Examples: `PgVectorIndex`, `EmbeddingsProvider`, `PathAndCacheKey`
- Classes should be named using PascalCase (also known as UpperCamelCase).

#### Constants
- Convention: UPPER_SNAKE_CASE (명확하게 정의된 상수가 없음, 추론)
- Examples: (코드에 명확한 상수가 없지만, 일반적으로 Python에서 상수는 대문자와 밑줄로 표현됩니다.)
- Rules: Constants should be named using UPPER_SNAKE_CASE.  Although there aren't clear examples in the current code, following general Python convention is recommended.

## Code Organization

### File Structure
- 각 기능별로 파일을 분리합니다.
- `core` 디렉토리에는 핵심 로직과 관련된 파일들이 위치합니다.
- `indexing` 디렉토리에는 코드 청킹과 관련된 파일들이 위치합니다.
- `embeddings` 디렉토리에는 임베딩 모델과 관련된 파일들이 위치합니다.
- `util` 디렉토리에는 유틸리티 함수들이 위치합니다.
- `vendor` 디렉토리에는 외부 라이브러리(Tree-sitter 파서)들이 위치합니다.
- `test_files` 디렉토리에는 테스트에 사용되는 파일들이 위치합니다.

### Module Organization
- 모듈은 관련 있는 기능들을 그룹화합니다.
- 예를 들어, `core.indexing` 모듈은 코드 청킹과 관련된 클래스와 함수들을 포함합니다.
- 모듈 내에서는 클래스, 함수, 변수 등을 정의합니다.

### Import Conventions
- 표준 라이브러리 import는 먼저 위치합니다.
- 외부 라이브러리 import는 그 다음에 위치합니다.
- 프로젝트 내부 모듈 import는 가장 마지막에 위치합니다.
- `from x import y` 형태의 import를 사용할 때는 필요한 모듈만 명시적으로 import합니다.
- 사용하지 않는 import는 제거합니다.

```python
import asyncio
import json

from sentence_transformers import SentenceTransformer

from core.index import PathAndCacheKey
from core.indexing.pgvector_index import PgVectorIndex
from core.embeddings.embeddings_provider import EmbeddingsProvider
```

## Coding Style

### Formatting
- PEP 8 스타일 가이드를 따릅니다.
- 들여쓰기는 4개의 공백을 사용합니다.
- 한 줄의 최대 길이는 79자입니다.
- 함수와 클래스 정의 사이에는 두 줄의 빈 줄을 삽입합니다.
- 클래스 내의 메서드 사이에는 한 줄의 빈 줄을 삽입합니다.

### Documentation
- 모든 함수, 클래스, 모듈에는 독스트링을 작성합니다.
- 독스트링은 함수의 기능, 인자, 반환 값 등을 명확하게 설명해야 합니다.
- 복잡한 로직에는 주석을 추가하여 코드의 의도를 설명합니다.

```python
async def main():
    # 임베딩 프로바이더 초기화
    embeddings_provider = EmbeddingsProvider()
    ...
```

### Error Handling
- `try...except` 블록을 사용하여 예외를 처리합니다.
- 예외 발생 시 적절한 로그를 남깁니다.
- 가능하다면, 예외를 복구하고 프로그램을 계속 실행합니다.

## Project-Specific Conventions

### Testing
- `test_files` 디렉토리에 테스트 파일을 위치시킵니다.
- 단위 테스트 및 통합 테스트를 작성합니다.
- 테스트 코드는 가능한 한 독립적으로 작성합니다.

### Configuration
- (코드에서 명확한 설정 파일 패턴을 찾을 수 없음)
- 일반적으로 설정 파일은 `config.py` 또는 `.env` 파일 형태로 관리됩니다.
- 설정 값은 환경 변수 또는 파일에서 읽어옵니다.

### Build and Deployment
- `requirements.txt` 파일을 사용하여 의존성 관리를 합니다.
- `setup_vendor.py` 스크립트를 사용하여 Tree-sitter 파서를 설정합니다.
- `build_parsers.py` 스크립트를 사용하여 Tree-sitter 파서를 컴파일합니다.

## Best Practices
- 코드를 모듈화하고 재사용성을 높입니다.
- 복잡한 로직은 함수로 분리합니다.
- 변수 이름은 의미 있게 짓습니다.
- 불필요한 코드는 제거합니다.
- 코드 리뷰를 통해 코드 품질을 향상시킵니다.

## Examples

### Good Example
```python
class PgVectorIndex:
    def __init__(self, embeddings_provider: EmbeddingsProvider, base_path: str = "."):
        self.embeddings_provider = embeddings_provider
        self.base_path = base_path
        self.connection = None
        self.model = None

    async def initialize(self):
        self.connection = await asyncpg.connect(
            user="postgres",
            password="",
            database="code_chunks",
            host="localhost",
        )
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
```

### Anti-patterns to Avoid
- 과도하게 긴 함수 또는 클래스
- 의미 없는 변수 이름
- 중복된 코드
- 예외를 무시하는 `except:` 블록
- 하드코딩된 설정 값
