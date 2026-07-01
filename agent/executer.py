from langchain_core.messages import HumanMessage
from agent.agent import graph


def run_agent(query: str) -> str:
    """
    Runs the research agent graph with the given user query and returns the final answer.

    Args:
        query: The user's research question.

    Returns:
        The final text response from the research agent.
    """
    initial_state = {
        "messages": [HumanMessage(content=query)]
    }

    final_state = graph.invoke(initial_state)

    last_message = final_state["messages"][-1]

    return last_message.content


def stream_agent(query: str):
    """
    Streams the research agent graph execution step by step.

    Args:
        query: The user's research question.

    Yields:
        Intermediate state dicts at each graph step.
    """
    initial_state = {
        "messages": [HumanMessage(content=query)]
    }

    for step in graph.stream(initial_state, stream_mode="updates"):
        yield step


if __name__ == "__main__":
    question = "What is attention mechanism in transformers?"
    print("Question:", question)
    print("\nAnswer:")
    print(run_agent(question))
