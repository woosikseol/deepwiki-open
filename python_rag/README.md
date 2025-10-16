# python_rag

Python-based RAG (Retrieval-Augmented Generation) system for code analysis.

## Overview

`python_rag` is a standalone RAG implementation that provides Q&A functionality over codebases using:

- **PostgreSQL + pgvector**: Vector storage and similarity search
- **Gemini API**: Text generation (gemini-2.0-flash-exp)
- **all-MiniLM-L6-v2**: Sentence embeddings (same as python_chunking)

This project is designed to work with the indexed code from `python_chunking`.

## Features

- ✅ RAG-based Q&A over indexed codebases
- ✅ Vector similarity search using pgvector
- ✅ Multi-language support (Korean by default)
- ✅ File and symbol context retrieval
- ✅ Markdown-formatted responses

## Prerequisites

1. **Python 3.11.9**
2. **PostgreSQL with pgvector extension**
3. **Indexed codebase** (via `python_chunking`)

## Installation

### 1. Create and activate virtual environment

```bash
cd python_rag
python3.11 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate  # On Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Copy `.env.example` to `.env` and configure:

```bash
# .env
GEMINI_API_KEY=your_gemini_api_key_here

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

## Usage

### Basic Usage

```bash
# Activate virtual environment
source .venv/bin/activate

# Ask a question (results auto-saved to results/ directory)
python main.py "What does this codebase do?"
```

**Note**: 모든 질문 결과는 자동으로 `results/rag_analysis_YYYYMMDD_HHMMSS.md` 형식으로 저장됩니다.

### Advanced Usage

```bash
# Specify output language
python main.py "Explain the RAG implementation" --language en

# Control number of retrieved contexts
python main.py "How does chunking work?" --top-k 5

# Show detailed context information
python main.py "Where is the embedding logic?" --verbose

# Enable debug logging
python main.py "Your question" --debug

# Specify custom output file (otherwise auto-generated with timestamp)
python main.py "Your question" --output results/custom_name.md

# Combine options
python main.py "코드 분석해줘" --verbose --output results/detailed_analysis.md
```

### Example Queries

```bash
# Korean (default)
python main.py "A 함수 대신에 B 함수를 새로 생성한다면 영향 받을 부분들의 모든 위치와 컨텍스트를 표시해줘."

# English
python main.py "What are the main components of this project?" --language en

# Impact analysis
python main.py "pgvector_index.py 파일을 수정하면 어떤 파일들이 영향을 받나요?"

# Code understanding
python main.py "RAG 클래스의 answer 메서드는 어떻게 동작하나요?"
```

## Architecture

### Project Structure

```
python_rag/
├── api/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── prompts.py         # Prompt templates
│   ├── gemini_client.py   # Gemini API client
│   └── rag.py             # RAG implementation
├── main.py                # CLI entry point
├── requirements.txt       # Python dependencies
├── .env                   # Environment configuration
└── README.md             # This file
```

### Workflow

1. **User Query**: User provides a question via CLI
2. **Embedding**: Question is embedded using all-MiniLM-L6-v2
3. **Retrieval**: Similar code chunks are retrieved from PostgreSQL + pgvector
4. **Prompt Construction**: Query and contexts are formatted into a prompt
5. **Generation**: Gemini generates an answer based on the prompt
6. **Output**: Answer is displayed in the requested language

### Database Schema

The system uses the following PostgreSQL schema (from `python_chunking`):

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
    embedding vector(384)  -- all-MiniLM-L6-v2 embeddings
);

CREATE INDEX chunks_embedding_idx ON chunks USING hnsw (embedding vector_cosine_ops);
```

## Configuration

### Language Support

Supported languages (via `--language` flag):
- `ko`: Korean (한국어) - default
- `en`: English
- `ja`: Japanese (日本語)
- `zh`: Mandarin Chinese (中文)
- `zh-tw`: Traditional Chinese (繁體中文)
- `es`: Spanish (Español)
- `vi`: Vietnamese (Tiếng Việt)
- `pt-br`: Brazilian Portuguese (Português Brasileiro)
- `fr`: French (Français)
- `ru`: Russian (Русский)

### Retrieval Parameters

- `TOP_K_RESULTS`: Number of similar chunks to retrieve (default: 10)
- Can be overridden with `--top-k` flag

### Generation Parameters

The system uses Gemini with the following defaults:
- Temperature: 0.7
- Top-p: 0.95
- Top-k: 40
- Max output tokens: 8192

## Integration with python_chunking

`python_rag` is designed to work seamlessly with `python_chunking`:

1. **Index your codebase** with `python_chunking`:
   ```bash
   cd ../python_chunking
   python main.py /path/to/your/code --db
   ```

2. **Query the indexed code** with `python_rag`:
   ```bash
   cd ../python_rag
   python main.py "Your question here"
   ```

## Dependencies

Key dependencies:
- `google-generativeai`: Gemini API client
- `sentence-transformers`: Embedding model (all-MiniLM-L6-v2)
- `psycopg2-binary`: PostgreSQL adapter
- `pgvector`: PostgreSQL vector extension support
- `jinja2`: Template engine for prompts

## Troubleshooting

### Database Connection Error

```
Error: could not connect to server
```

**Solution**: Ensure PostgreSQL is running and credentials in `.env` are correct.

### No Contexts Retrieved

```
죄송합니다. 관련된 정보를 찾을 수 없습니다.
```

**Solution**: Make sure you have indexed your codebase using `python_chunking` first.

### Gemini API Error

```
Error: API key is invalid
```

**Solution**: Check that `GEMINI_API_KEY` in `.env` is valid and has proper permissions.

## Development

### Running Tests

```bash
# TODO: Add test suite
pytest tests/
```

### Code Style

This project follows the same conventions as the parent `deepwiki-open` project.

## License

Same as the parent `deepwiki-open` project.

## Related Projects

- `python_chunking`: Code indexing and chunking system
- `python_kb`: Knowledge base generation system
- `deepwiki-open`: Main DeepWiki project

## Contributing

Contributions are welcome! Please follow the coding standards of the parent project.

