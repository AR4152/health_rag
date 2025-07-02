"""MLHub Toolkit for health_rag - chat_mode.

Command-line tool for interactive chat assistant with memory.

Usage:
    ml chat_mode health_rag [--session-id SESSION_ID]
"""

import argparse
import sys
import threading
import time

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field


class InMemoryHistory(BaseChatMessageHistory, BaseModel):  # type: ignore
    """Simple in-memory message history."""

    messages: list[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages: list[BaseMessage]) -> None:
        """Add messages to history."""
        self.messages.extend(messages)

    def clear(self) -> None:
        """Clear chat history."""
        self.messages = []


class ChatAssistant:
    """Interactive chat assistant with memory."""

    GREEN = "\033[92m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

    def __init__(
        self,
        model: str = "llama3.2:1b",
        temperature: float = 0.7,
        system_prompt: str = "You are a helpful assistant.",
    ):
        """Initialize the Chat Assistant."""
        # Session store
        self._store: dict[str, InMemoryHistory] = {}

        # LLM setup
        self.llm = ChatOllama(
            model=model,
            temperature=temperature,
        )

        # Prompt template
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
            ]
        )

        # Chain
        self.chain = self.prompt | self.llm

        # Wrap chain with memory
        self.chain_with_memory = RunnableWithMessageHistory(
            self.chain,
            get_session_history=self._get_by_session_id,
            history_messages_key="history",
            input_messages_key="input",
        )

    def _get_by_session_id(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self._store:
            self._store[session_id] = InMemoryHistory()
        return self._store[session_id]

    def _typing_indicator(self, stop_event: threading.Event) -> None:
        dots = ""
        while not stop_event.is_set():
            dots += "."
            if len(dots) > 3:
                dots = ""
            sys.stdout.write(f"\r{self.CYAN}>> LLM: {dots:<3}{self.RESET}")
            sys.stdout.flush()
            time.sleep(0.5)
        sys.stdout.write("\r" + " " * 40 + "\r")
        sys.stdout.flush()

    def run_chat_session(self, session_id: str = "default_session") -> None:
        """Start an interactive chat session."""
        print("=" * 60)
        print("Welcome to Chat Mode!")
        print("Type your questions or prompts below.")
        print("Session ID:", session_id)
        print("To end the session, type 'exit' or 'quit'.")
        print("=" * 60)
        print()

        while True:
            user_input = input(f"{self.GREEN}>> User:{self.RESET} ")
            if user_input.strip().lower() in {"exit", "quit"}:
                print("Exiting chat.")
                break

            stop_event = threading.Event()
            t = threading.Thread(target=self._typing_indicator, args=(stop_event,))
            t.start()

            response = self.chain_with_memory.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": session_id}},
            )

            stop_event.set()
            t.join()

            print(f"{self.CYAN}>> LLM:{self.RESET} {response.content}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Interactive chat assistant with memory.",
        usage="ml chat_mode health_rag [--session-id SESSION_ID]",
    )
    parser.add_argument(
        "--session-id",
        type=str,
        default="default_session",
        help="Unique session ID for the conversation memory.",
    )
    args = parser.parse_args()

    assistant = ChatAssistant()
    assistant.run_chat_session(session_id=args.session_id)
