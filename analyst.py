from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

<<<<<<< HEAD
# PROMPT ESPECIALIZADO: Aquí es donde ocurre la magia para DISAGRO
=======
>>>>>>> fa8b515 (refactor: preparing local changes for synchronization)
DISAGRO_ANALYST_PROMPT = """
You are the Senior Strategy Consultant for Disagro. 
Analyze the provided agriculture news and explain its CRITICAL IMPORTANCE for Disagro.

Focus on:
1. Supply Chain: Impact on fertilizer or raw material logistics.
2. Market Leadership: Competitive advantages in Central America.
3. Opportunities: Regional political changes, AgTech trends, or tariffs.

Structure:
- **Business Line:**
- **Executive Summary:**
- **STRATEGIC IMPORTANCE FOR DISAGRO:** (Be specific and analytical)
- **Actionable Recommendation:**
All responses must be in English.
"""

def analyze_strategic_impact(news_content, source_url, title):
<<<<<<< HEAD
    """Llamada a GPT-4o para análisis de BI"""
    try:
        print(f"   🧠 [ANALYST] Interpretando impacto para: {title[:30]}...", flush=True)
=======
    """Llamada a GPT-4o para análisis"""
    try:
        print(f"   🧠 [ANALYST] Generating insights for: {title[:30]}...", flush=True)
>>>>>>> fa8b515 (refactor: preparing local changes for synchronization)
        user_input = f"Headline: {title}\nSource: {source_url}\nContent: {news_content}"
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": DISAGRO_ANALYST_PROMPT},
                {"role": "user", "content": user_input}
            ],
            temperature=0.3
        )
        analysis = response.choices[0].message.content
        header = f"### 📰 NEWS: {title}\n🔗 **Source:** <{source_url}>\n"
        
        return f"{header}\n{analysis}"
    except Exception as e:
<<<<<<< HEAD
        return f"❌ Error en análisis de '{title}': {e}"
=======
        return f"❌ Analysis error for '{title}': {e}"
>>>>>>> fa8b515 (refactor: preparing local changes for synchronization)
