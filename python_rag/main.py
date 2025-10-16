#!/usr/bin/env python3
"""
python_rag - Main CLI entry point

Usage:
    python main.py "Your question here"
    python main.py "A 함수 대신에 B 함수를 새로 생성한다면 영향 받을 부분들의 모든 위치와 컨텍스트를 표시해줘."

This program performs RAG (Retrieval-Augmented Generation) Q&A using:
- PostgreSQL + pgvector for vector storage
- Gemini API for generation
- all-MiniLM-L6-v2 for embeddings
"""
import sys
import asyncio
import argparse
import logging
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from api.config import validate_config, DEFAULT_LANGUAGE
from api.rag import RAG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_separator(char="=", length=80):
    """Print a separator line"""
    print(char * length)


def print_context_info(contexts):
    """Print information about retrieved contexts"""
    print_separator()
    print(f"📚 Retrieved {len(contexts)} relevant contexts:")
    print_separator()
    
    for i, context in enumerate(contexts, 1):
        print(f"\n[Context {i}]")
        print(f"  File: {context.filepath}")
        print(f"  Lines: {context.start_line}-{context.end_line}")
        
        if context.metadata and context.metadata.symbol_name:
            print(f"  Symbol: {context.metadata.symbol_type} {context.metadata.symbol_name}")
        
        # Print first few lines of content
        content_lines = context.content.split('\n')[:3]
        print(f"  Preview: {content_lines[0][:70]}...")
    
    print_separator()


def print_answer(answer: str):
    """Print the answer"""
    print_separator("=", 80)
    print("💡 Answer:")
    print_separator("=", 80)
    print()
    print(answer)
    print()
    print_separator("=", 80)


def save_result_to_file(args, result):
    """Save RAG result to a markdown file"""
    from datetime import datetime
    import os
    
    # Auto-generate filename if not specified
    if args.output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = Path(f"results/rag_analysis_{timestamp}.md")
    else:
        output_path = Path(args.output)
    
    # Create directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Generate markdown content
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = f"""# RAG Q&A 분석 결과

## 📋 실행 정보

- **실행 시간**: {timestamp}
- **프로그램**: python_rag
- **모델**: gemini-2.0-flash-exp
- **임베딩 모델**: all-MiniLM-L6-v2
- **출력 언어**: {result.language}
- **검색된 컨텍스트 수**: {len(result.contexts)}개

---

## ❓ 질문 (User Query)

```
{result.query}
```

---

## 📚 검색된 관련 컨텍스트 (Retrieved Contexts)

"""
    
    # Add contexts
    for i, context in enumerate(result.contexts, 1):
        content += f"### Context {i}: `{context.filepath}` (Lines {context.start_line}-{context.end_line})\n"
        if context.metadata and context.metadata.symbol_name:
            content += f"- **타입**: {context.metadata.symbol_type}\n"
            content += f"- **심볼**: `{context.metadata.symbol_name}`\n"
        content += f"- **미리보기**: `{context.content.split(chr(10))[0][:70]}...`\n\n"
    
    # Add answer
    content += f"""---

## 💡 생성된 답변 (Generated Answer)

{result.answer}

---

## 💾 메타데이터

- **분석 도구**: python_rag
- **데이터베이스**: PostgreSQL + pgvector
- **벡터 차원**: 384 (all-MiniLM-L6-v2)
- **검색 방식**: 코사인 유사도
- **생성 모델**: Gemini 2.0 Flash Exp
- **사용된 컨텍스트**: {len(result.contexts)}개 코드 청크

---

**생성 일시**: {timestamp}  
**분석 도구**: python_rag v1.0  
**파일 위치**: `{output_path.absolute()}`
"""
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ 결과가 저장되었습니다: {output_path}")
    print(f"   파일 크기: {os.path.getsize(output_path) / 1024:.2f} KB")


async def main():
    """Main function"""
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="RAG-based Q&A system for code analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "What does this codebase do?"
  %(prog)s "A 함수 대신에 B 함수를 새로 생성한다면 영향 받을 부분들의 모든 위치와 컨텍스트를 표시해줘."
  %(prog)s "Explain the RAG implementation" --language en
  %(prog)s "How does the chunking work?" --top-k 5
        """
    )
    
    parser.add_argument(
        "query",
        type=str,
        help="Question to ask about the codebase"
    )
    
    parser.add_argument(
        "--language", "-l",
        type=str,
        default=DEFAULT_LANGUAGE,
        choices=["ko", "en", "ja", "zh", "zh-tw", "es", "vi", "pt-br", "fr", "ru"],
        help=f"Output language (default: {DEFAULT_LANGUAGE})"
    )
    
    parser.add_argument(
        "--top-k", "-k",
        type=int,
        default=10,
        help="Number of top contexts to retrieve (default: 10)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed context information"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Custom output file path (default: auto-generated in results/ with timestamp)"
    )
    
    args = parser.parse_args()
    
    # Set debug logging if requested
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Validate configuration
        logger.info("Validating configuration...")
        validate_config()
        
        # Initialize RAG
        logger.info("Initializing RAG system...")
        rag = RAG(language=args.language, top_k=args.top_k)
        await rag.initialize()
        
        # Print query
        print_separator()
        print(f"❓ Question: {args.query}")
        print_separator()
        print()
        
        # Process query
        logger.info("Processing query...")
        result = await rag.answer(args.query, language=args.language)
        
        # Print results
        if args.verbose and result.contexts:
            print_context_info(result.contexts)
            print()
        
        print_answer(result.answer)
        
        # Print context count
        print(f"ℹ️  Answer generated using {len(result.contexts)} code contexts")
        
        # Always save to file (auto-generate filename if not specified)
        save_result_to_file(args, result)
        
        # Close RAG
        rag.close()
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        return 1
        
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=args.debug)
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

