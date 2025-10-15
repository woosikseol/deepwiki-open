"""
Wiki 생성용 프롬프트 모듈
DeepWiki 프로젝트의 프롬프트를 참조하여 작성되었습니다.
"""

# 프로젝트 구조 페이지 생성 프롬프트
PROJECT_STRUCTURE_PROMPT = """You are an expert technical writer analyzing a software project to create comprehensive documentation.

<task>
Generate a "Project Structure & Overview (and Key Features) including Architecture Diagram & Module Diagram & Flow Diagram" page for the project: {project_name}

This documentation should provide readers with a complete understanding of the project structure, key features, and how different components interact.
</task>

<requirements>
1. Start with a brief project overview based on the README content
2. Provide a detailed project structure analysis including:
   - Directory and file organization
   - Main modules and their purposes
   - Key files and their roles
3. List and explain key features with:
   - Feature descriptions
   - Implementation details
   - Related files and modules
4. Create a system architecture diagram using Mermaid syntax:
   - Show main components and their relationships
   - Include data flow between components
   - Use appropriate diagram types (graph, flowchart, etc.)
5. Create a module diagram using Mermaid syntax:
   - Show module dependencies and relationships
   - Illustrate module hierarchies
   - Highlight key modules and their interactions
6. Create a data/execution flow diagram using Mermaid syntax:
   - Illustrate how the system processes data
   - Show the sequence of operations
   - Highlight critical paths
</requirements>

<context>
Project Name: {project_name}

README Content:
{readme_content}

File Tree Structure:
{file_tree}

Project Statistics:
- Total files: {total_files}
- Code files: {code_files}
- Documentation files: {doc_files}
- Languages: {languages}
</context>

<output_format>
Generate the content in Markdown format with the following structure:

# Project Structure & Overview

## Overview
[Project overview based on README]

## Project Structure

### Directory Organization
[Detailed explanation of directory structure]

### Key Components
[List and explain main components/modules]

### Important Files
[Highlight critical files and their purposes]

## Key Features

### Feature 1: [Feature Name]
- Description: [What it does]
- Implementation: [How it's implemented]
- Related Files: [Files involved]

[... more features ...]

## Architecture Diagram

```mermaid
[Architecture diagram showing components and relationships]
```

## Module Diagram

```mermaid
[Module diagram showing module dependencies and hierarchies]
```

## Flow Diagram

```mermaid
[Flow diagram showing data/execution flow]
```

## File Structure Details
[Detailed file tree with annotations]
</output_format>

<important>
- Output language MUST be {language_name}
- Use proper Mermaid syntax for diagrams
- Be specific and reference actual files/directories from the project
- Provide actionable insights, not generic descriptions
- DO NOT use markdown code fences (```) at the beginning or end of your response
- Start directly with the content
</important>

Generate the content now:
"""

# 아키텍처 페이지 생성 프롬프트  
ARCHITECTURE_PROMPT = """You are an expert software architect analyzing a software project to document its architecture and design patterns.

<task>
Generate an "Overall System Architecture & Design Patterns (including Architecture Diagram & Module Diagram & Flow Diagram) used in major features" page for the project: {project_name}

This documentation should help developers understand the architectural decisions, design patterns used, and how the system is structured at a high level.
</task>

<requirements>
1. Describe the overall system architecture:
   - Architectural style (e.g., layered, microservices, MVC, etc.)
   - Major architectural decisions and their rationale
   - Component interactions and dependencies
2. Identify and explain design patterns used:
   - Pattern name and type
   - Where it's used in the codebase
   - Why it was chosen
   - Implementation details
3. Create architecture diagrams using Mermaid syntax:
   - High-level system architecture
   - Component interaction diagram
4. Create module diagrams using Mermaid syntax:
   - Module dependency graph
   - Module hierarchies and relationships
   - Package/module organization
5. Create flow diagrams for major features using Mermaid syntax:
   - Feature execution flow
   - Data processing pipeline
   - User interaction flow
5. Discuss architectural trade-offs and considerations
</requirements>

<context>
Project Name: {project_name}

README Content:
{readme_content}

File Tree Structure:
{file_tree}

Project Statistics:
- Total files: {total_files}
- Code files: {code_files}
- Languages: {languages}
</context>

<output_format>
Generate the content in Markdown format with the following structure:

# Overall System Architecture & Design Patterns

## System Architecture Overview

### Architectural Style
[Description of the architectural approach]

### Key Architectural Decisions
[Major decisions and their rationale]

### Component Overview
[Main components and their responsibilities]

## Architecture Diagrams

### High-Level Architecture
```mermaid
[System architecture diagram]
```

### Component Interaction
```mermaid
[Component interaction diagram]
```

### Module Dependencies
```mermaid
[Module dependency diagram]
```

## Design Patterns

### Pattern 1: [Pattern Name]
- **Type**: [Creational/Structural/Behavioral]
- **Location**: [Where in the codebase]
- **Purpose**: [Why it's used]
- **Implementation**: [How it's implemented]

[... more patterns ...]

## Major Feature Architectures

### Feature 1: [Feature Name]

#### Architecture
[Description of feature architecture]

#### Flow Diagram
```mermaid
[Feature flow diagram]
```

#### Key Components
[Components involved in this feature]

[... more features ...]

## Architectural Considerations

### Scalability
[How the architecture supports scalability]

### Maintainability
[How the architecture supports maintainability]

### Extensibility
[How the architecture supports extensibility]
</output_format>

<important>
- Output language MUST be {language_name}
- Use proper Mermaid syntax for all diagrams
- Be specific about actual patterns found in the code
- Reference actual files and code structures
- Provide architectural insights, not surface-level descriptions
- DO NOT use markdown code fences (```) at the beginning or end of your response
- Start directly with the content
</important>

Generate the content now:
"""

# 규약 페이지 생성 프롬프트
CONVENTIONS_PROMPT = """You are an expert technical writer analyzing a software project to document its coding conventions and standards.

<task>
Generate a "Conventions (Naming Conventions, Rules, …)" page for the project: {project_name}

This documentation should help developers understand and follow the project's coding standards, naming conventions, and best practices.
</task>

<requirements>
1. Analyze the codebase to identify naming conventions:
   - File naming patterns
   - Directory naming patterns
   - Variable naming conventions
   - Function/method naming conventions
   - Class naming conventions
   - Constant naming conventions
2. Document code organization rules:
   - File structure standards
   - Import/export conventions
   - Module organization patterns
3. Identify coding style guidelines:
   - Code formatting standards
   - Comment and documentation practices
   - Error handling patterns
4. Note any project-specific conventions:
   - Testing conventions
   - Configuration file patterns
   - Build and deployment conventions
5. Provide examples from the actual codebase
</requirements>

<context>
Project Name: {project_name}

README Content:
{readme_content}

File Tree Structure:
{file_tree}

Project Statistics:
- Total files: {total_files}
- Code files: {code_files}
- Languages: {languages}
</context>

<output_format>
Generate the content in Markdown format with the following structure:

# Conventions

## Overview
[Brief introduction to the project's conventions]

## Naming Conventions

### File Naming
- Pattern: [Description]
- Examples: [Actual examples from the project]
- Rules: [Specific rules]

### Directory Naming
- Pattern: [Description]
- Examples: [Actual examples from the project]
- Rules: [Specific rules]

### Code Naming

#### Variables
- Convention: [Description]
- Examples: [Examples]

#### Functions/Methods
- Convention: [Description]
- Examples: [Examples]

#### Classes
- Convention: [Description]
- Examples: [Examples]

#### Constants
- Convention: [Description]
- Examples: [Examples]

## Code Organization

### File Structure
[How files are typically organized]

### Module Organization
[How modules are structured]

### Import Conventions
[Import statement conventions]

## Coding Style

### Formatting
[Code formatting standards]

### Documentation
[Comment and docstring conventions]

### Error Handling
[Error handling patterns]

## Project-Specific Conventions

### Testing
[Testing conventions and patterns]

### Configuration
[Configuration file conventions]

### Build and Deployment
[Build and deployment conventions]

## Best Practices
[List of recommended best practices for this project]

## Examples

### Good Example
```
[Code example following conventions]
```

### Anti-patterns to Avoid
[Common mistakes to avoid]
</output_format>

<important>
- Output language MUST be {language_name}
- Base all conventions on actual patterns found in the codebase
- Provide real examples from the project files
- Be specific and actionable
- If certain conventions are not clearly defined, note that
- DO NOT use markdown code fences (```) at the beginning or end of your response
- Start directly with the content
</important>

Generate the content now:
"""

# 환경 설정 페이지 생성 프롬프트
ENVIRONMENT_PROMPT = """You are an expert technical writer creating a comprehensive environment setup guide for a software project.

<task>
Generate an "Environment Setting and the Guide" page for the project: {project_name}

This documentation should guide developers through setting up their development environment to work on this project.
</task>

<requirements>
1. Identify system requirements:
   - Programming language versions
   - Required tools and dependencies
   - Operating system requirements
2. Provide installation instructions:
   - Step-by-step setup process
   - Dependency installation
   - Configuration steps
3. Document configuration requirements:
   - Environment variables
   - Configuration files
   - API keys or credentials
4. Include verification steps:
   - How to verify the setup
   - Running tests
   - Common troubleshooting
5. Provide development workflow guidance:
   - Running the project
   - Development mode setup
   - Debugging setup
</requirements>

<context>
Project Name: {project_name}

README Content:
{readme_content}

File Tree Structure:
{file_tree}

Project Statistics:
- Total files: {total_files}
- Code files: {code_files}
- Languages: {languages}
</context>

<output_format>
Generate the content in Markdown format with the following structure:

# Environment Setting and the Guide

## Prerequisites

### System Requirements
- Operating System: [Requirements]
- [Language] Version: [Required version]
- Other Tools: [List of required tools]

### Required Dependencies
[List major dependencies and their versions]

## Installation Guide

### Step 1: Install [Language/Runtime]
```bash
[Installation commands]
```

### Step 2: Clone the Repository
```bash
[Clone command]
```

### Step 3: Install Dependencies
```bash
[Dependency installation commands]
```

### Step 4: Configuration

#### Environment Variables
Create a `.env` file with the following variables:
```
[Environment variable examples]
```

#### Configuration Files
[Configuration file setup instructions]

## Verification

### Verify Installation
```bash
[Verification commands]
```

### Run Tests
```bash
[Test commands]
```

### Expected Output
[What successful setup looks like]

## Development Workflow

### Running the Project

#### Development Mode
```bash
[Development run commands]
```

#### Production Mode
```bash
[Production run commands]
```

### Common Commands
- [Command 1]: [Description]
- [Command 2]: [Description]
- [Command 3]: [Description]

## Troubleshooting

### Issue 1: [Common Problem]
**Problem**: [Description]
**Solution**: [How to fix]

### Issue 2: [Common Problem]
**Problem**: [Description]
**Solution**: [How to fix]

## Additional Resources
- [Link to documentation]
- [Link to community]
- [Other helpful resources]

## Development Tips
[Helpful tips for developers]
</output_format>

<important>
- Output language MUST be {language_name}
- Base instructions on actual project files (package.json, requirements.txt, etc.)
- Provide complete, working commands
- Include both development and production setup
- Add troubleshooting for common issues
- DO NOT use markdown code fences (```) at the beginning or end of your response
- Start directly with the content
</important>

Generate the content now:
"""

# 프롬프트 매핑
PROMPTS = {
    'project_structure': PROJECT_STRUCTURE_PROMPT,
    'architecture': ARCHITECTURE_PROMPT,
    'conventions': CONVENTIONS_PROMPT,
    'environment': ENVIRONMENT_PROMPT,
}


def get_prompt_template(page_type: str) -> str:
    """
    페이지 타입에 맞는 프롬프트 템플릿 반환
    
    Args:
        page_type: 페이지 타입
        
    Returns:
        str: 프롬프트 템플릿
        
    Raises:
        ValueError: 지원하지 않는 페이지 타입
    """
    if page_type not in PROMPTS:
        raise ValueError(f"지원하지 않는 페이지 타입: {page_type}. 지원 타입: {list(PROMPTS.keys())}")
    
    return PROMPTS[page_type]

