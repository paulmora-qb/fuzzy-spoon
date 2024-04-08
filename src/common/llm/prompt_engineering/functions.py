"""Functions for the llm callback pipeline."""

from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from common.llm.flow_modules.generate_query import Quote, Hashtag, Fact
from langchain_community.llms import GPT4All

PYDANTIC_OUTPUT_PARSER = {
    "quote": Quote,
    "hashtag": Hashtag,
    "fact": Fact,
}


def prompt_wrapper(
    system_message: str,
    instruction_message: str,
    output_parser_key: str,
) -> str:
    """Building the prompt through instruction and system messages.

    Args:
        system_message (str): System message which states how the AI should behave.
        instruction_message (str): Instruction message which states what the AI should
            do.
        output_parser_key (str): Name of the pipeline. Used to find the correct output
            parser object.

    Returns:
        str: The output of the pipeline. This oftentimes is a class which has different
            attributes.
    """
    prompt = _build_prompt(
        instruction_message=instruction_message, system_message=system_message
    )

    llm = _get_openai_endpoint()
    # llm = GPT4All(model="libs/nous-hermes-llama2-13b.Q4_0.gguf")
    output_parser = PydanticOutputParser(
        pydantic_object=PYDANTIC_OUTPUT_PARSER[output_parser_key]
    )

    chain = prompt | llm | output_parser
    return chain.invoke(
        {"format_instructions": output_parser.get_format_instructions()}
    )


from langchain_openai import ChatOpenAI


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
    openai_base_url = "https://openai.prod.ai-gateway.quantumblack.com/0eb64a5a-829e-449d-b328-cab86eaf9437/v1"
    openai_api_key = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJhZXNKN2kxNGNidnVuTU40MTJrOU5yZ2ROeENhTlJudTNPbC1TU08ycFlJIn0.eyJleHAiOjE3MTI1NjY4OTMsImlhdCI6MTcxMjU2NTA5MywiYXV0aF90aW1lIjoxNzEyNTY0ODk5LCJqdGkiOiJmZjExNTdkOC0wZmYzLTQ4MDAtOWZhMS0yNTNjZGJlMmIyYWEiLCJpc3MiOiJodHRwczovL2F1dGgubWNraW5zZXkuaWQvYXV0aC9yZWFsbXMvciIsImF1ZCI6ImJjZDIzNzI4LTNkMjctNDQ3Yy1hMGE5LWVhY2FmMzkzYTZmNSIsInN1YiI6ImI3ZmY3ZmYxLWU2NTYtNGQyNi1iNDdlLTcyYWIzMDE4Njk0ZSIsInR5cCI6IklEIiwiYXpwIjoiYmNkMjM3MjgtM2QyNy00NDdjLWEwYTktZWFjYWYzOTNhNmY1Iiwibm9uY2UiOiJIejFhcmRxNmFuUF9tS0NJeFM3WWt6S2lyTF9Wdkh6M2dSYk1CN3F2QURVIiwic2Vzc2lvbl9zdGF0ZSI6IjE0YTFhNjdiLTE5NDgtNDYxNS1iMTVmLWYwYzFhMWI0M2NlZCIsImF0X2hhc2giOiJnSHFyaTZpMTItVzB1aC1ONl9aMHR3IiwibmFtZSI6IlBhdWwgTW9yYSIsImdpdmVuX25hbWUiOiJQYXVsIiwiZmFtaWx5X25hbWUiOiJNb3JhIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiODA3ZDg1ZWRjNzhlMjMwYSIsImVtYWlsIjoiUGF1bF9Nb3JhQG1ja2luc2V5LmNvbSIsImFjciI6IjEiLCJzaWQiOiIxNGExYTY3Yi0xOTQ4LTQ2MTUtYjE1Zi1mMGMxYTFiNDNjZWQiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZm1ubyI6IjMwOTM4NyIsImdyb3VwcyI6WyJBbGwgRmlybSBVc2VycyIsIjBlYjY0YTVhLTgyOWUtNDQ5ZC1iMzI4LWNhYjg2ZWFmOTQzNyJdfQ.SLiAh-iZvnwrKmITjNMTKl7vPaw78WMkIQExA9RvLGh266cKIhYE0IGVR7ekYKYq3tQdH6OMJqmelinYH2hq_7C9kC2nu5TnCV2ajR1eSir5BIzoRmCHYbWVrjzBZ8X6_m5JgX8liNHSRpS-t_p-XDomX6mxu4KSW1jOBwaVf6BV8BAd8DnzniaLo4MnmEFkjPzrmX8WSwoQFP6JFDGeouOh8Oz63gxehwLvOrVZQKa6a2Au7ekAnyQyQhwhQ-FEjS3acdQphECR14xdJLuvhBrdE7fUfIYI74lxuIh2eEVrb1UthdtSfiOa40y54zvBp4PKTN7FS8Uam0RFxbLo8w"

    return ChatOpenAI(
        temperature=temperature,
        model_name=model_name,
        openai_api_key=openai_api_key,
        openai_api_base=openai_base_url,
        request_timeout=15,
        max_retries=2,
    )


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
