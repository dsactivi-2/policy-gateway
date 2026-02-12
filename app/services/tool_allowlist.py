from typing import Optional, List
import logging
from app.config import get_settings

logger = logging.getLogger(__name__)


class ToolAllowlist:
    def __init__(self):
        settings = get_settings()
        self.allowed_tools = [
            tool.strip() 
            for tool in settings.allowed_tools.split(',')
        ]
        logger.info(f"Tool Allowlist initialized with: {self.allowed_tools}")

    def is_allowed(self, tool_name: str, user_id: Optional[str] = None) -> bool:
        """
        Check if a tool is allowed
        
        Args:
            tool_name: Name of the tool to check
            user_id: Optional user ID for user-specific rules
        
        Returns:
            True if tool is allowed, False otherwise
        """
        # Simple allowlist check
        # Can be extended with user-specific rules, role-based access, etc.
        return tool_name in self.allowed_tools

    def add_tool(self, tool_name: str) -> None:
        """
        Add a tool to the allowlist
        """
        if tool_name not in self.allowed_tools:
            self.allowed_tools.append(tool_name)
            logger.info(f"Added tool to allowlist: {tool_name}")

    def remove_tool(self, tool_name: str) -> None:
        """
        Remove a tool from the allowlist
        """
        if tool_name in self.allowed_tools:
            self.allowed_tools.remove(tool_name)
            logger.info(f"Removed tool from allowlist: {tool_name}")

    def get_allowed_tools(self) -> List[str]:
        """
        Get list of all allowed tools
        """
        return self.allowed_tools.copy()
