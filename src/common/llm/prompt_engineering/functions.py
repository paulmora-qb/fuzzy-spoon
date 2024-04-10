"""Functions for the llm callback pipeline."""

from common.llm.flow_modules.generate_query import Fact, Hashtag, Quote
from langchain_community.llms import GPT4All
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain_core.runnables.base import RunnableSequence

import os
from langchain_openai import ChatOpenAI

PYDANTIC_OUTPUT_PARSER = {
    "quote": Quote,
    "hashtag": Hashtag,
    "fact": Fact,
}


def prompt_wrapper(
    inputs: dict[str, str],
    template: str,
    output_parser_key: str,
) -> str:
    """Build the prompt through instruction and system messages.

    Args:
    ----
        inputs (dict[str, str]): The inputs to the prompt.
        template (str): The template of the prompt.
        output_parser_key (str): Name of the pipeline. Used to find the correct output
            parser object.

    Returns:
    -------
        str: The output of the pipeline. This oftentimes is a class which has different
            attributes.

    """
    output_parser = PydanticOutputParser(
        pydantic_object=PYDANTIC_OUTPUT_PARSER[output_parser_key]
    )
    prompt = _build_prompt(
        inputs=inputs,
        template=template,
        output_parser=output_parser,
    )

    if os.environ.get("OPENAI_API_KEY"):
        llm = _get_openai_endpoint()
    else:
        llm = GPT4All(model="models/nous-hermes-llama2-13b.Q4_0.gguf")

    chain = prompt | llm | output_parser

    return _retrying_after_failure(chain=chain, inputs=inputs)


def _retrying_after_failure(
    chain: RunnableSequence, inputs: dict[str, str], max_attempts: int = 10
) -> object:
    """Retry the chain after a failure.

    Args:
        chain (RunnableSequence): Chain that invokes the LLM.
        inputs (dict[str, str]): The inputs to the prompt.
        max_attempts (int, optional): Number of attempts tried before accepting failure.
            Defaults to 10.

    Raises:
        Exception: If all attempts fail.

    Returns:
        object: The desired object that is returned by the chain.
    """

    attempts = 0

    while attempts < max_attempts:
        try:
            desired_object = chain.invoke(inputs)
            break
        except Exception as e:
            attempts += 1

    # If the loop completes without breaking, it means all attempts failed
    if attempts == max_attempts:
        raise Exception("All attempts failed.")
    else:
        return desired_object


def _get_openai_endpoint(
    model_name: str = "gpt-3.5-turbo", temperature: float = 0.0
) -> ChatOpenAI:
    """Initialize the OpenAI endpoint.

    Args:
    ----
        model_name (str, optional): Name of the instance of the openai model name.
            Defaults to "gpt-3.5-turbo".
        temperature (float, optional): The temperature states the certainty that the AI
            has. Defaults to 0.0.

    Returns:
    -------
        ChatOpenAI: OpenAI endpoint.

    """
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    openai_base_url = os.environ.get("OPENAI_API_BASE_URL")

    return ChatOpenAI(
        temperature=temperature,
        model_name=model_name,
        openai_api_key=openai_api_key,
        openai_api_base=openai_base_url,
        request_timeout=15,
        max_retries=2,
    )


def _build_prompt(
    template: str, inputs: dict[str, str], output_parser: str
) -> ChatPromptTemplate:
    """Build the prompt through instruction and system messages.

    Args:
    ----
        template (str): The template of the prompt.
        inputs (dict[str, str]): The inputs to the prompt.
        output_parser (str): Name of the pipeline. Used to find the correct output
            parser object.

    Returns:
    -------
        ChatPromptTemplate: The prompt that is built.

    """
    return PromptTemplate(
        template=template,
        input_variables=list(inputs.keys()),
        partial_variables={
            "format_instructions": output_parser.get_format_instructions()
        },
    )
