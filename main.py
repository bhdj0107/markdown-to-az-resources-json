import asyncio
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_core.model_context import UnboundedChatCompletionContext
import dotenv
import os

dotenv.load_dotenv()

# Example of how you might use this team:
async def main(prompt, markdown_path):
    # Create the Azure OpenAI model client
    azure_openai_client = AzureOpenAIChatCompletionClient(
        model="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment="gpt-4o",
        api_version="2024-12-01-preview",
        temperature=0
    )

    # Create an unbounded chat completion context
    unbounded_context = UnboundedChatCompletionContext()

    # Create the system message for the agent
    system_message = prompt

    # Create the detail agent
    detail_agent = AssistantAgent(
        name="Detail_Agent",
        model_client=azure_openai_client,
        tools=[],  # Empty tools list as specified in the JSON
        model_context=unbounded_context,
        description="An agent that provides assistance with ability to use tools.",
        system_message=system_message,
        model_client_stream=False,
        reflect_on_tool_use=False,
        tool_call_summary_format="{result}"
    )

    # Create termination condition
    termination_condition = TextMentionTermination(text="resources")

    # Create the RoundRobinGroupChat team
    team = RoundRobinGroupChat(
        participants=[detail_agent],
        termination_condition=termination_condition
    )
    # load md
    with open(markdown_path, "r") as file:
        input_text = file.read()
    # Initialize the chat
    chat_result = await team.run(
        task=input_text,
        cancellation_token=None
    )
    result = chat_result.messages[-1].content
    result = result.removeprefix("```json").removesuffix("```")
    return result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str)
    parser.add_argument("--markdown", type=str, default="info.md")
    args = parser.parse_args()
    
    if args.mode == "suggest":
        with open("prompts/suggestion-from-info.txt", "r") as file:
            prompt = file.read()
    elif args.mode == "parsing":
        with open("prompts/suggestion-from-info.txt", "r") as file:
            prompt = file.read()
    else:
        raise ValueError(f"Invalid mode: {args.mode}\nValid modes: suggest, parsing")
    
    print(asyncio.run(main(prompt, args.markdown)))