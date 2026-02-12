import re
import logging
from typing import List
from app.config import get_settings

logger = logging.getLogger(__name__)


class OutputFilter:
    def __init__(self):
        settings = get_settings()
        self.filter_patterns = [
            pattern.strip()
            for pattern in settings.filter_patterns.split(',')
        ]
        self.enabled = settings.filter_enabled
        logger.info(f"Output Filter initialized. Enabled: {self.enabled}")

    async def filter(self, text: str) -> str:
        """
        Filter sensitive content from output text
        
        Args:
            text: The text to filter
        
        Returns:
            Filtered text with sensitive patterns replaced
        """
        if not self.enabled:
            return text

        filtered_text = text
        
        for pattern in self.filter_patterns:
            # Create regex pattern for case-insensitive matching
            regex = re.compile(re.escape(pattern), re.IGNORECASE)
            filtered_text = regex.sub('[FILTERED]', filtered_text)
        
        # Additional pattern matching for common sensitive data
        # Credit card numbers (simple pattern)
        filtered_text = re.sub(
            r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
            '[CREDIT_CARD]',
            filtered_text
        )
        
        # API keys (simple pattern: alphanumeric strings of certain length)
        filtered_text = re.sub(
            r'\b[A-Za-z0-9]{32,}\b',
            '[API_KEY]',
            filtered_text
        )
        
        return filtered_text

    def add_pattern(self, pattern: str) -> None:
        """
        Add a new pattern to filter
        """
        if pattern not in self.filter_patterns:
            self.filter_patterns.append(pattern)
            logger.info(f"Added filter pattern: {pattern}")

    def remove_pattern(self, pattern: str) -> None:
        """
        Remove a pattern from the filter
        """
        if pattern in self.filter_patterns:
            self.filter_patterns.remove(pattern)
            logger.info(f"Removed filter pattern: {pattern}")

    def get_patterns(self) -> List[str]:
        """
        Get all filter patterns
        """
        return self.filter_patterns.copy()
