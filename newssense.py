import os
import json
import asyncio
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled, InputGuardrailTripwireTriggered

# --- Load environment variables ---
load_dotenv()
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError("Please set BASE_URL, API_KEY, and MODEL_NAME.")

client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(disabled=True)

# --- Models (optional for future use) ---
class TrendingNews(BaseModel):
    category: str
    headlines: List[str]
    summary: Optional[str] = None

class FactCheckResult(BaseModel):
    claim: str
    verdict: str
    evidence: List[str]

class NewsSummary(BaseModel):
    topic: str
    bullet_points: List[str]

@dataclass
class UserContext:
    user_id: str
    preferred_categories: List[str] = None
    session_start: datetime = None

    def __post_init__(self):
        if self.preferred_categories is None:
            self.preferred_categories = []
        if self.session_start is None:
            self.session_start = datetime.now()

# --- Tools ---
@function_tool
def get_trending_news(topic: str) -> str:
    """Simulate retrieving trending news headlines for a topic."""
    dummy_headlines = {
        "AI": ["Meta releases new LLM", "Elon Musk updates Grok AI"],
        "Politics": ["New tax bill passed", "World leaders meet at G20"],
        "Finance": ["Stocks rally after Fed announcement", "Crypto market surges"]
    }
    headlines = dummy_headlines.get(topic, ["No trending news found"])
    return json.dumps({"category": topic, "headlines": headlines})

@function_tool
def fact_check_claim(claim: str) -> str:
    """Simulate fact checking a claim using RAG."""
    dummy_response = {
        "Did Apple acquire OpenAI?": {
            "verdict": "False",
            "evidence": [
                "No official statement from Apple or OpenAI.",
                "Sources suggest only partnership talks."
            ]
        }
    }
    result = dummy_response.get(claim, {
        "verdict": "Unverified",
        "evidence": ["Not enough sources available."]
    })
    return json.dumps({"claim": claim, **result})

@function_tool
def summarize_news(article_text: str) -> str:
    """Simulate summarizing a news article into bullet points."""
    return json.dumps({
        "topic": "Sample Topic",
        "bullet_points": [
            "Main event occurred today.",
            "Key people involved.",
            "Impacts discussed."
        ]
    })

# --- Agents ---
conversation_agent = Agent[UserContext](
    name="Conversation Agent",
    handoff_description="Entry point agent for detecting intent and routing",
    instructions="""
    You are the main agent users interact with. Detect user intent: Trending News, Fact Checking, or Summarization.
    Then hand off to the correct agent. Be helpful and conversational. Explain clearly what you're doing and answer like you're talking to a human.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
)

trending_news_agent = Agent[UserContext](
    name="Trending News Agent",
    handoff_description="Pull trending news headlines",
    instructions="""
    You specialize in trending topics and news. Use get_trending_news to fetch data.
    Respond in plain, friendly language: summarize the headlines naturally instead of listing raw JSON.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    tools=[get_trending_news],
)

fact_checker_agent = Agent[UserContext](
    name="Fact Checker Agent",
    handoff_description="Verify news claims",
    instructions="""
    You verify the truthfulness of claims using fact_check_claim. Present the verdict in a clear sentence and explain the evidence naturally.
    Be concise but helpful.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    tools=[fact_check_claim],
)

news_summarizer_agent = Agent[UserContext](
    name="News Summarizer Agent",
    handoff_description="Summarize news articles or topics",
    instructions="""
    You summarize long news content into simple bullet points or short summaries. Use summarize_news tool.
    Speak in a helpful, natural tone, like explaining to a friend.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    tools=[summarize_news],
)

# --- Set up handoffs ---
conversation_agent.handoffs = [
    trending_news_agent,
    fact_checker_agent,
    news_summarizer_agent
]

# --- Main ---
async def main():
    user_context = UserContext(user_id="news_user_1", preferred_categories=["AI", "Politics"])

    queries = [
        "What’s trending in AI today?",
        "Is OpenAI partnering with Apple?",
        "Summarize this article about the G20 summit."
    ]

    for query in queries:
        print("\n" + "=" * 50)
        print(f"QUERY: {query}")
        print("=" * 50)

        try:
            result = await Runner.run(conversation_agent, query, context=user_context)
            print("\nRESPONSE:")
            print(result.final_output)
        except InputGuardrailTripwireTriggered as e:
            print("\n⚠️ GUARDRAIL TRIGGERED ⚠️")

if __name__ == "__main__":
    asyncio.run(main())
