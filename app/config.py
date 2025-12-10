from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path



class Config(BaseSettings):
    gemini_key: str
    
    model_config = SettingsConfigDict(
            env_file=(Path(__file__).parent.parent.resolve() / ".env"),
            env_file_encoding="utf-8",
            case_sensitive=False,  
            extra="ignore",  
            populate_by_name=True
        )
    
    
CONFIG = Config()

