# AgroWiz: Strategic Intelligence Agent for Disagro
### MIT Applied Agentic AI - Digital Transformation Hub

**AgroWiz** is an autonomous intelligence agent designed to support high-level decision-making for **Disagro**. It functions as a specialized node that monitors, filters, and analyzes global agricultural trends, fertilizers, and logistics with a specific focus on the Central American market.

## 🧠 Agentic Architecture
Unlike standard search bots, AgroWiz implements an "agentic workflow" to ensure data quality and strategic relevance:

1.  **Dynamic Topic Orchestration**: The agent utilizes two distinct intelligence modes:
    * **Autonomous Mode**: Rotates through 10 strategic industry keywords (Fertilizer markets, CBOT prices, Agritech innovation, etc.).
    * **Diagnostic Mode**: Executes targeted global database scans for broader market context.
2.  **Real-Time Research (Jina AI)**: Uses the Jina Reader API with a custom **cache-busting logic** (dynamic URL generation) to bypass stale data and fetch real-time reports.
3.  **Strategic Synthesis (GPT-4o)**: Raw data is processed through a specialized "Analyst Layer" that extracts corporate impact, risks, and opportunities tailored to Disagro’s business model.

## 🛠️ Discord Command Terminal
The system is designed for a seamless "Plug & Play" experience via Discord:

* `!news`: **Autonomous Strategic Analysis**. The agent selects a random strategic topic from the corporate core, performs real-time research, and generates a Top 3 findings report.
* `!list_news`: **Global Database Sync**. Executes a diagnostic scan of the latest agricultural news in Central America to provide general context.
* `!next`: **Intelligence Navigation**. Accesses the secondary findings backlog of the current research session.
* `!about`: Displays system diagnostics, development status, and metadata.

## ⚙️ Engineering Standard
* **Orchestration**: `discord.py` (Async)
* **Intelligence Engine**: OpenAI GPT-4o
* **Search Infrastructure**: Jina AI (JSON Protocol)
* **Execution Environment**: Python 3.10+ / Linux-based Cloud Node

---
*Developed for the MIT Professional Education: Applied Agentic AI course.*