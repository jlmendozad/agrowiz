import requests
from openai import OpenAI
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import random

# Carga de variables de entorno
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
JINA_KEY = os.getenv('JINA_API_KEY')

# Importamos el analista (asegúrate de que el archivo analyst.py exista)
try:
    from analyst import analyze_strategic_impact
except ImportError:
    print("⚠️ [ADVERTENCIA] No se pudo importar analyst.py")

def get_raw_news_list():
    """Diagnóstico usando el formato de URL validado: s.jina.ai/word+word"""
    try:
        print("\n" + "-"*30 + " [ INICIO DIAGNÓSTICO ] " + "-"*30, flush=True)
        topics = [
            "fertilizer market trends 2026",
            "logistics freight Central America",
            "agritech innovation",
            "global urea price analysis",
            "corn and soy trade logistics"
        ]
        selected_topic = random.choice(topics).replace(" ", "+")
        cache_buster = random.randint(1, 10000)
        query = f"{selected_topic}+news+Central+America+2026?cb={cache_buster}"
        search_url = f"https://s.jina.ai/{query}"
        
        headers = {"Accept": "application/json", "Authorization": f"Bearer {JINA_KEY}"}
        
        print(f"📡 [LOG] Petición Jina (Formato Validado): {search_url}", flush=True)
        response = requests.get(search_url, headers=headers, timeout=30)
        print(f"📊 [LOG] Status Code: {response.status_code}", flush=True)
        
        if response.status_code == 200:
            data = response.json().get('data', [])[:5] 
            print(f"✅ [LOG] Éxito. {len(data)} noticias obtenidas.", flush=True)
            print(f"🏁 [LOG] DIAGNÓSTICO FINALIZADO.", flush=True)
            return [{"title": item.get('title'), "url": item.get('url')} for item in data]
        
        raise Exception(f"HTTP {response.status_code}")

    except Exception as e:
        print(f"🚨 [LOG] Fallback activado: {e}", flush=True)
        print(f"🏁 [LOG] DIAGNÓSTICO FINALIZADO (Modo Backup).", flush=True)
        return [
            {"title": "Reuters Agriculture News", "url": "https://www.reuters.com/markets/commodities/"},
            {"title": "Central America Data", "url": "https://www.centralamericadata.com/"}
        ]

def fetch_all_news(topic="agriculture"):
    """Ciclo estratégico optimizado con PARALELISMO para mayor velocidad"""
    try:
        print("\n" + "="*60, flush=True)
        print(f"🚀 [SISTEMA] INICIANDO CICLO ESTRATÉGICO PARALELO", flush=True)
        print("="*60, flush=True)

        if isinstance(input_data, list):
            # Si recibimos una lista, ya tenemos los datos, no buscamos en Jina
            data = input_data[:5]
            print(f"📊 [LOG] Usando {len(data)} noticias desde MEMORIA CACHÉ...", flush=True)
        else
            # Reemplazamos espacios por '+' para que la URL sea válida
            clean_topic = topic.replace(" ", "+")
            cache_buster = random.randint(1, 1000)
    
            # Construimos el query dinámico manteniendo tus filtros de calidad
            query = f"{clean_topic}+logistics+news+Central+America+2026?cb={cache_buster}"
            search_url = f"https://s.jina.ai/{query}"
            headers = {"Accept": "application/json", "Authorization": f"Bearer {JINA_KEY}"}
        
            response = requests.get(search_url, headers=headers, timeout=30)
            if response.status_code != 200:
                print(f"❌ [LOG] Error Jina {response.status_code}.", flush=True)
                return []

            data = response.json().get('data', [])[:5]
            print(f"📊 [LOG] Analizando {len(data)} noticias simultáneamente...", flush=True)

        # Usamos ThreadPoolExecutor para que las 5 noticias se analicen al mismo tiempo
        with ThreadPoolExecutor() as executor:
            futures = []
            for item in data:
                content = item.get('content', '')
                url = item.get('url', 'No URL')
                title = item.get('title', 'Untitled News')
                if len(content) > 200:
                    futures.append(executor.submit(analyze_strategic_impact, content, url, title))
            
            all_reports = [f.result() for f in futures]
        
        print("\n" + "="*60, flush=True)
        print(f"🏁 [SISTEMA] CICLO FINALIZADO CON ÉXITO", flush=True)
        print("="*60 + "\n", flush=True)
        return all_reports

    except Exception as e:
        print(f"\n🚨 [ERROR] Fallo en el ciclo: {e}", flush=True)
        return []