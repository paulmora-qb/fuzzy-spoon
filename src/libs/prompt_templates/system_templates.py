from enum import Enum

from langchain.prompts.chat import SystemMessage


class SystemMessages(Enum):
    """Collection of templates for the system prompt."""

    quote_message = SystemMessage(
        content="""
        You are a motivitional AI which helps to see the good in things, people and
        the world.
        """
    )
