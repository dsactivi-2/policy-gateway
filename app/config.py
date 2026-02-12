from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # API Settings
    api_title: str = "Policy Gateway"
    api_version: str = "1.0.0"
    
    # Redis Settings (optional for caching)
    redis_host: str = "localhost"
    redis_port: int = 6379
    
    # PII Detection Settings
    pii_threshold: float = 0.5
    anonymize_by_default: bool = False
    
    # Tool Allowlist
    allowed_tools: str = "web_search,calculator,code_interpreter"
    
    # Output Filter
    filter_enabled: bool = True
    filter_patterns: str = "api_key,password,secret,token"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
