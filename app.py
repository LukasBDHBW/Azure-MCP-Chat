import os
import asyncio
from typing import List, Dict, Any, Optional

import streamlit as st
from dotenv import load_dotenv

# MCP & Agent stack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage

load_dotenv()

st.set_page_config(page_title="Azure GPT + MCP Chat", page_icon="🤖", layout="centered",
    menu_items={})
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stDeployButton"] {display: none;}
    </style>
""", unsafe_allow_html=True)
st.title("🤖 Azure GPT MCP Chat")


# --- Sidebar configuration

default_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", os.getenv("AZURE_OPENAI_MODEL", "gpt-4o"))
model_name = default_deployment

# MCP server config
default_cmd = os.getenv("MCP_SERVER_CMD", "python")
default_script = os.getenv("MCP_SERVER_SCRIPT", "C:/Users/lukas/OneDrive/Dokumente/Test/server.py")
mcp_cmd = default_cmd
mcp_script = default_script

system_prompt = "Du bist ein hilfreicher Assistent. Nutze verfügbare Tools, wenn sie nützlich sind."

# --- Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content=system_prompt)
    ]
# Update system message if changed
if isinstance(st.session_state.messages[0], SystemMessage) and st.session_state.messages[0].content != system_prompt:
    st.session_state.messages[0] = SystemMessage(content=system_prompt)

def render_history():
    for m in st.session_state.messages[1:]:  # skip system
        role = "assistant" if isinstance(m, AIMessage) else "user"
        with st.chat_message(role):
            st.markdown(m.content)

render_history()

user_input = st.chat_input("Schreibe eine Nachricht…")

async def run_agent(user_text: str) -> str:
    """
    Spins up an MCP stdio session, loads tools, builds a ReAct agent and returns the assistant response text.
    """
    server = StdioServerParameters(command=mcp_cmd, args=[mcp_script])
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)

            llm = init_chat_model(
                model=model_name,
                model_provider="azure_openai",
            )
            agent = create_react_agent(llm, tools)

            # We pass the whole history (minus System, provided separately) to keep context
            history_for_agent = [msg for msg in st.session_state.messages if not isinstance(msg, SystemMessage)]
            # Append latest user message
            history_for_agent.append(HumanMessage(content=user_text))

            # LangGraph prebuilt agent expects a dict with "messages"
            result = await agent.ainvoke({"messages": history_for_agent})
            # result['messages'] is a list; we want the last AI message content
            ai_text = ""
            for msg in reversed(result["messages"]):
                if isinstance(msg, AIMessage):
                    ai_text = msg.content
                    break
            return ai_text or "*(Kein Output vom Agent erhalten.)*"

if user_input:
    # Show immediately in UI
    st.session_state.messages.append(HumanMessage(content=user_input))
    with st.chat_message("assistant"):
        with st.spinner("Denke nach…"):
            try:
                reply_text = asyncio.run(run_agent(user_input))
            except RuntimeError as e:
                # In case we're already inside an event loop (rare), fallback
                reply_text = f"Fehler beim Ausführen: {e}"
            st.markdown(reply_text)
    st.session_state.messages.append(AIMessage(content=reply_text))
    st.rerun()
