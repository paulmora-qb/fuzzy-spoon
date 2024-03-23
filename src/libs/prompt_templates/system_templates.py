from enum import Enum

from langchain_core.messages.system import SystemMessage


class SystemMessages(Enum):
    """Collection of templates for the system prompt."""

    system_message = SystemMessage(
        content="""
        You are a motivitional AI which provides famous and uplifting quotes.
        """
    )
