import os
import logging
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class Config:
    def __init__(self):
        self.telegram_token = self._get_env_var('TELEGRAM_TOKEN')
        self.target_group_id = self._get_env_var('TARGET_GROUP_ID', required=False)
        
        # Validate required config
        if not self.telegram_token:
            raise ValueError("TELEGRAM_TOKEN environment variable is required")
            
        # Convert target_group_id to int if provided
        if self.target_group_id:
            try:
                self.target_group_id = int(self.target_group_id)
            except ValueError:
                logger.warning("TARGET_GROUP_ID is not a valid integer, ignoring")
                self.target_group_id = None
                
        logger.info(f"Bot configured with target group: {self.target_group_id}")
        
    def _get_env_var(self, name: str, default: Optional[str] = None, required: bool = True) -> Optional[str]:
        """Get environment variable with optional default and validation."""
        value = os.getenv(name, default)
        
        if required and not value:
            raise ValueError(f"Environment variable {name} is required but not set")
            
        return value
        
    @property
    def is_target_group_configured(self) -> bool:
        """Check if target group is configured."""
        return self.target_group_id is not None
