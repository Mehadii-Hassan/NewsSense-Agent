<h1 align="center">🗞️ NewsSense Agent</h1>

<p align="center">
  <strong>Your AI-powered News Assistant using OpenAI Multi-Agent Architecture </strong><br>
  Get trending headlines, fact-check news claims, and summarize articles – all in one place.
</p>

<hr>

<h2>📌 Project Overview</h2>

<p>
NewsIntel is a multi-agent system designed to help users navigate the fast-paced world of news using AI. It intelligently detects user intent and routes the request to the right specialist:
</p>

<ul>
  <li>📰 <strong>Trending News Agent</strong>: Pulls latest headlines from popular categories</li>
  <li>🔍 <strong>Fact Checker Agent</strong>: Verifies claims using simulated RAG and evidence</li>
  <li>📝 <strong>News Summarizer Agent</strong>: Condenses articles into bullet-point summaries</li>
</ul>

<hr>

<h2>🚀 Features</h2>

<ul>
  <li>🧠 Intent detection & multi-agent orchestration via OpenAI</li>
  <li>💬 Natural language responses instead of JSON outputs</li>
  <li>⚙️ Built with <code>Python</code>, <code>Pydantic</code>, <code>AsyncOpenAI</code>, and <code>dotenv</code></li>
  <li>🔌 Simulated tools for trending news, claim verification, and summarization</li>
</ul>

<hr>

<h2>🧠 How It Works</h2>

<ol>
  <li>The main <code>Conversation Agent</code> receives a user query</li>
  <li>It detects the intent (trending news, fact-checking, summarization)</li>
  <li>The query is routed to the corresponding agent with specialized tools</li>
  <li>The selected agent returns a human-like response</li>
</ol>

<hr>

<h2>📂 Folder Structure</h2>

<pre>
newsintel-agent/
│
├── .gitignore
├── newssense.py             ← Main script
├── .env                     ← Contains BASE_URL, API_KEY, MODEL_NAME
└── README.md
</pre>

<hr>

<h2>⚙️ Setup Instructions</h2>

<ol>
  <li>Clone the repository</li>
  
  <pre><code>git clone https://github.com/Mehadii-Hassan/NewsSense-Agent</code></pre>

  <li>Install dependencies</li>

  <pre><code>pip install -r requirements.txt</code></pre>

  <li>Create a <code>.env</code> file with your OpenAI credentials</li>

  <pre><code>
BASE_URL="https://api.openai.com/v1"
API_KEY="your-api-key-here"
MODEL_NAME="openai/gpt-4.1-nano"
  </code></pre>

  <li>Run the program</li>

  <pre><code>python newssense.py</code></pre>
</ol>

<hr>

<h2>🧪 Sample Queries</h2>

<ul>
  <li><code>What’s trending in AI today?</code></li>
  <li><code>Is OpenAI partnering with Apple?</code></li>
  <li><code>Summarize this article about the G20 summit.</code></li>
</ul>

<hr>

<h2>🙌 Credits</h2>

<p>
Created by <strong>Mehadi Hassan</strong> using OpenAI multi-agent SDK and Python tooling.
</p>

<hr>

<p align="center">⭐ Star this repo if it helps you stay informed!</p>
