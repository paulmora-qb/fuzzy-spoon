"""Functions for the llm callback pipeline."""

from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
import os
from typing import Any
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import importlib


def prompt_wrapper(
    system_message: str,
    instruction_message: str,
    pydantic_object_path: str,
) -> str:
    """Building the prompt through instruction and system messages.

    Args:
        system_message (str): System message which states how the AI should behave.
        instruction_message (str): Instruction message which states what the AI should
            do.
        pydantic_object_path (str): Path of where the pydantic object is stored. This
            object states what attributes the output class should have.

    Returns:
        str: The output of the pipeline. This oftentimes is a class which has different
            attributes.
    """

    prompt = _build_prompt(
        instruction_message=instruction_message, system_message=system_message
    )
    llm = _get_openai_endpoint()
    output_parser = _build_output_parser(pydantic_object_path=pydantic_object_path)

    chain = prompt | llm | output_parser
    return chain.invoke(
        {"format_instructions": output_parser.get_format_instructions()}
    )


def _get_openai_endpoint(
    model_name: str = "gpt-3.5-turbo", temperature: float = 0.0
) -> ChatOpenAI:
    """Initializing the OpenAI endpoint.

    Args:
        model_name (str, optional): Name of the instance of the openai model name.
            Defaults to "gpt-3.5-turbo".
        temperature (float, optional): The temperature states the certainty that the AI
            has. Defaults to 0.0.

    Returns:
        ChatOpenAI: OpenAI endpoint.
    """

    # Extract the OpenAI credentials.
    openai_api_base = os.environ.get("OPENAI_BASE_URL")
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    return ChatOpenAI(
        temperature=temperature,
        model_name=model_name,
        openai_api_key=openai_api_key,
        openai_api_base=openai_api_base,
        request_timeout=15,
        max_retries=2,
    )


def _build_output_parser(pydantic_object_path: str):

    pydantic_object = _load_obj(pydantic_object_path)
    return PydanticOutputParser(pydantic_object=pydantic_object)


def _load_obj(path: str) -> Any:
    """Loading an object from a string path.

    Args:
        path (str): Path of the object.

    Returns:
        Any: The object that was loaded.
    """
    # Split the string into module name and class name
    module_name, class_name = path.rsplit(".", 1)

    # Import the module dynamically
    module = importlib.import_module(module_name)

    # Get the class from the module
    return getattr(module, class_name)


def _build_prompt(instruction_message: str, system_message: str) -> ChatPromptTemplate:
    """Building the prompt through instruction and system messages.

    Args:
        instruction_message (str): Instruction message which states what the AI should
            do.
        system_message (str): System message which states how the AI should behave.

    Returns:
        ChatPromptTemplate: The prompt that is built.
    """
    instruction_message = HumanMessagePromptTemplate.from_template(instruction_message)
    system_message = SystemMessagePromptTemplate.from_template(system_message)
    return ChatPromptTemplate.from_messages([system_message, instruction_message])
