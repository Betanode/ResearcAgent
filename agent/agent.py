from typing import Annotated, Literal

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langgraph.prebuilt import ToolNode, tools_condition

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
    ToolMessage,
)

from agent.llm import get_llm
from agent.prompt import SYSTEM_PROMPT

from agent.tools import TOOLS


# -------------------------------
# Agent State
# -------------------------------

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# -------------------------------
# LLMs
# -------------------------------

planner_llm = get_llm().bind_tools(TOOLS)

research_llm = get_llm()


# -------------------------------
# Tool Node
# -------------------------------

tool_node = ToolNode(TOOLS)


# -------------------------------
# Planner Agent
# -------------------------------

def planner_node(state: AgentState):

    messages = state["messages"]

    planner_prompt = SystemMessage(
        content="""
You are a Planning Agent.

Your job is NOT to answer the user's question.

You ONLY decide which tools are needed.

Available tools:

1. retrieval_tool
   - Use when the answer may exist inside uploaded research papers.

2. web_tool
   - Use when the question requires latest information from the web.

Rules:

- Use retrieval_tool if document knowledge is required.
- Use web_tool if current information is required.
- You may call BOTH tools.
- Never answer the question yourself.
- If a tool is required, call it.
"""
    )

    response = planner_llm.invoke(
        [planner_prompt] + messages
    )

    return {
        "messages": [response]
    }


# -------------------------------
# Routing
# -------------------------------

def should_continue(
    state: AgentState,
) -> Literal["tools", "research"]:

    last_message = state["messages"][-1]

    if getattr(last_message, "tool_calls", None):
        return "tools"

    return "research"


# -------------------------------
# Research Agent
# -------------------------------

def research_node(state: AgentState):

    messages = state["messages"]

    context = ""

    # Tool outputs collect karo
    for message in messages:
        if isinstance(message, ToolMessage):
            context += message.content
            context += "\n\n"

    question = ""

    # Original user question nikal lo
    for message in messages:
        if isinstance(message, HumanMessage):
            question = message.content
            break

    prompt = SystemMessage(
        content=SYSTEM_PROMPT(context)
    )

    response = research_llm.invoke(
        [
            prompt,
            *messages
        ]
    )

    return {
        "messages": [response]
    }


# -------------------------------
# Build Graph
# -------------------------------

builder = StateGraph(AgentState)

builder.add_node("planner", planner_node)

builder.add_node("tools", tool_node)

builder.add_node("research", research_node)


# -------------------------------
# Edges
# -------------------------------

builder.add_edge(START, "planner")

builder.add_conditional_edges(
    "planner",
    should_continue,
    {
        "tools": "tools",
        "research": "research"
    }
)

builder.add_edge(
    "tools",
    "research"
)

builder.add_edge(
    "research",
    END
)


# -------------------------------
# Compile
# -------------------------------

graph = builder.compile()