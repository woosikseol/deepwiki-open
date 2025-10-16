"""
Gemini API client for python_rag
"""
import logging
from typing import Optional, Dict, Any
import google.generativeai as genai

from api.config import GEMINI_API_KEY, GEMINI_MODEL

logger = logging.getLogger(__name__)


class GeminiClient:
    """Client for Google Gemini API"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize Gemini client
        
        Args:
            api_key: Gemini API key (defaults to config)
            model: Model name (defaults to config)
        """
        self.api_key = api_key or GEMINI_API_KEY
        self.model_name = model or GEMINI_MODEL
        
        if not self.api_key:
            raise ValueError("Gemini API key is required")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Initialize model
        self.model = genai.GenerativeModel(self.model_name)
        
        logger.info(f"Initialized Gemini client with model: {self.model_name}")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate response from Gemini
        
        Args:
            prompt: Input prompt
            **kwargs: Additional generation parameters
            
        Returns:
            Generated text response
        """
        try:
            # Set default generation config
            generation_config = {
                "temperature": kwargs.get("temperature", 0.7),
                "top_p": kwargs.get("top_p", 0.95),
                "top_k": kwargs.get("top_k", 40),
                "max_output_tokens": kwargs.get("max_output_tokens", 8192),
            }
            
            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating response from Gemini: {e}")
            raise
    
    async def generate_async(self, prompt: str, **kwargs) -> str:
        """
        Async version of generate (currently synchronous wrapper)
        
        Args:
            prompt: Input prompt
            **kwargs: Additional generation parameters
            
        Returns:
            Generated text response
        """
        # For now, wrap synchronous call
        # In production, you might want to use aiohttp or similar
        return self.generate(prompt, **kwargs)

