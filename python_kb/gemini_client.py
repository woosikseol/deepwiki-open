"""
Gemini LLM 클라이언트 모듈
Google Gemini API를 사용하여 Wiki 콘텐츠를 생성합니다.
"""

import logging
import re
import time
from typing import Dict, Optional
import google.generativeai as genai

from config import GEMINI_API_KEY, GEMINI_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS, OUTPUT_LANGUAGES, DEFAULT_LANGUAGE
from llm_mermaid_validator import LLMMermaidValidator
from prompts import get_prompt_template

logger = logging.getLogger(__name__)


class GeminiClient:
    """Gemini API 클라이언트"""
    
    def __init__(self, api_key: Optional[str] = None, language: str = DEFAULT_LANGUAGE):
        """
        Args:
            api_key: Gemini API 키 (None이면 환경변수에서 가져옴)
            language: 출력 언어 ('ko' 또는 'en')
        """
        self.api_key = api_key or GEMINI_API_KEY
        self.language = language
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
        
        if self.language not in OUTPUT_LANGUAGES:
            raise ValueError(f"지원하지 않는 언어입니다: {self.language}. 지원 언어: {list(OUTPUT_LANGUAGES.keys())}")
        
        # Gemini API 설정
        genai.configure(api_key=self.api_key)
        
        # 모델 설정
        self.model_name = GEMINI_MODEL
        self.model = genai.GenerativeModel(self.model_name)
        logger.info(f"Gemini 클라이언트 초기화 완료: {GEMINI_MODEL} (언어: {OUTPUT_LANGUAGES[self.language]})")
        
        self.generation_config = {
            'temperature': LLM_TEMPERATURE,
            'max_output_tokens': LLM_MAX_TOKENS,
        }
        
        # LLM 기반 Mermaid 검증기 초기화
        self.mermaid_validator = LLMMermaidValidator(api_key=self.api_key, model_name=self.model_name)
    
    def generate_content(
        self,
        prompt: str,
        retry_count: int = 3,
        retry_delay: float = 1.0
    ) -> str:
        """
        프롬프트로부터 콘텐츠 생성
        
        Args:
            prompt: 생성 프롬프트
            retry_count: 재시도 횟수
            retry_delay: 재시도 대기 시간 (초)
            
        Returns:
            str: 생성된 콘텐츠
        """
        last_error = None
        
        for attempt in range(retry_count):
            try:
                logger.info(f"콘텐츠 생성 시도 {attempt + 1}/{retry_count}")
                
                # Gemini API 사용
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=self.generation_config['temperature'],
                        max_output_tokens=self.generation_config['max_output_tokens']
                    )
                )
                
                # 응답 확인
                if not response or not response.text:
                    raise ValueError("빈 응답을 받았습니다")
                
                text = response.text
                
                logger.info(f"콘텐츠 생성 완료: {len(text)} 문자")
                return text
                
            except Exception as e:
                last_error = e
                logger.warning(f"콘텐츠 생성 실패 (시도 {attempt + 1}/{retry_count}): {e}")
                
                if attempt < retry_count - 1:
                    time.sleep(retry_delay * (attempt + 1))  # 지수 백오프
        
        # 모든 재시도 실패
        error_msg = f"콘텐츠 생성 실패 ({retry_count}회 시도): {last_error}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    
    def generate_wiki_page(
        self,
        page_type: str,
        page_title: str,
        context: Dict
    ) -> str:
        """
        Wiki 페이지 생성
        
        Args:
            page_type: 페이지 타입 (project_structure, architecture, conventions, environment)
            page_title: 페이지 제목
            context: 컨텍스트 정보 (프로젝트 구조, README 등)
            
        Returns:
            str: 생성된 Markdown 콘텐츠
        """
        prompt = self._build_prompt(page_type, page_title, context)
        content = self.generate_content(prompt)
        
        # Mermaid 구문 검증 및 수정
        content = self._validate_and_fix_mermaid(content)
        
        return content
    
    def _validate_and_fix_mermaid(self, content: str) -> str:
        """LLM을 사용하여 Mermaid 다이어그램 구문을 검증하고 수정"""
        try:
            logger.info("LLM 기반 Mermaid 검증 시작...")
            
            # LLM을 사용하여 모든 Mermaid 블록 검증 및 수정
            modified_content, validated_count, fixed_count = self.mermaid_validator.validate_markdown_content(content)
            
            if fixed_count > 0:
                logger.info(f"✓ LLM이 {fixed_count}개의 Mermaid 블록을 수정했습니다 (총 {validated_count}개 검증)")
            elif validated_count > 0:
                logger.info(f"✓ 모든 Mermaid 블록이 유효합니다 (총 {validated_count}개 검증)")
            
            return modified_content
            
        except Exception as e:
            logger.error(f"LLM Mermaid 검증 중 오류 발생: {e}")
            return content  # 오류 발생 시 원본 반환
    
    def _build_prompt(
        self,
        page_type: str,
        page_title: str,
        context: Dict
    ) -> str:
        """
        프롬프트 생성 (prompts.py 사용)
        
        Args:
            page_type: 페이지 타입
            page_title: 페이지 제목
            context: 컨텍스트 정보
            
        Returns:
            str: 생성된 프롬프트
        """
        # 언어 이름
        language_name = OUTPUT_LANGUAGES[self.language]
        
        # 통계 정보 포맷팅
        stats = context.get('statistics', {})
        languages_str = ', '.join([f"{lang}: {count}" for lang, count in stats.get('languages', {}).items()])
        
        # 프롬프트 템플릿 가져오기
        try:
            prompt_template = get_prompt_template(page_type)
        except ValueError as e:
            logger.error(f"프롬프트 템플릿 로드 실패: {e}")
            raise
        
        # 프롬프트 변수 채우기
        prompt = prompt_template.format(
            project_name=context.get('project_name', 'Unknown Project'),
            readme_content=context.get('readme_content', 'No README available'),
            file_tree=context.get('file_tree', 'No file tree available'),
            total_files=stats.get('total_files', 0),
            code_files=stats.get('code_files', 0),
            doc_files=stats.get('doc_files', 0),
            languages=languages_str or 'Unknown',
            language_name=language_name
        )
        
        return prompt
