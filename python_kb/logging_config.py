"""
로깅 설정 모듈
"""

import logging
import sys
from pathlib import Path


def setup_logging(log_level=logging.INFO):
    """
    로깅 설정 초기화
    
    Args:
        log_level: 로그 레벨 (기본값: INFO)
    """
    # 로그 포맷 설정
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # 루트 로거 설정
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # 특정 라이브러리의 로그 레벨 조정
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info("로깅 설정 완료")

