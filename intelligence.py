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

<<<<<<< HEAD
# Importamos el analista (asegúrate de que el archivo analyst.py exista)
try:
    from analyst import analyze_strategic_impact
except ImportError:
    print("⚠️ [ADVERTENCIA] No se pudo importar analyst.py")
=======
# Importamos el analista BI
try:
    from analyst import analyze_strategic_impact
except ImportError:
    print("⚠️ [WARNING] analyst.py could't be imported")
>>>>>>> fa8b515 (refactor: preparing local changes for synchronization)

def get_raw_news_list():
    """Diagnóstico usando el formato de URL validado: s.jina.ai/word+word"""
    try:
<<<<<<< HEAD
        print("\n" + "-"*30 + " [ INICIO DIAGNÓSTICO ] " + "-"*30, flush=True)
        
        # Formato manual para asegurar los signos '+' que funcionaron
=======
        print("\n" + "-"*30 + " [ STARTING ANALYSIS ] " + "-"*30, flush=True)
        
        # Formato manual agregar signo + en la query del url
>>>>>>> fa8b515 (refactor: preparing local changes for synchronization)
        query = "latest+agriculture+news+Central+America"
        search_url = f"https://s.jina.ai/{query}"
        
        headers = {"Accept": "application/json", "Authorization": f"Bearer {JINA_KEY}"}
        
<<<<<<< HEAD
        print(f"📡 [LOG] Petición Jina (Formato Validado): {search_url}", flush=True)
=======
        print(f"📡 [LOG] Query to Jina (Formato is OK): {search_url}", flush=True)
>>>>>>> fa8b515 (refactor: preparing local changes for synchronization)
        response = requests.get(search_url, headers=headers, timeout=30)
        print(f"📊 [LOG] Status Code: {response.status_code}", flush=True)
        
        if response.status_code == 200:
            data = response.json().get('data', [])[:5] 
<<<<<<< HEAD
            print(f"✅ [LOG] Éxito. {len(data)} noticias obtenidas.", flush=True)
=======
            print(f"✅ [LOG] Success. {len(data)} news obtained.", flush=True)
>>>>>>> fa8b515 (refactor: preparing local changes for synchronization)
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
<<<<<<< HEAD
    """Ciclo estratégico optimizado con PARALELISMO para mayor velocidad"""
=======
>>>>>>> fa8b515 (refactor: preparing local changes for synchronization)
    try:
        print("\n" + "="*60, flush=True)
        print(f"🚀 [SISTEMA] INICIANDO CICLO ESTRATÉGICO PARALELO", flush=True)
        print("="*60, flush=True)

        # Reemplazamos espacios por '+' para que la URL sea válida
        clean_topic = topic.replace(" ", "+")
        cache_buster = random.randint(1, 1000)
    
<<<<<<< HEAD
        # Construimos el query dinámico manteniendo tus filtros de calidad
=======
        # Construccion del query
>>>>>>> fa8b515 (refactor: preparing local changes for synchronization)
        query = f"{clean_topic}+logistics+news+Central+America+2026?cb={cache_buster}"
        search_url = f"https://s.jina.ai/{query}"
        headers = {"Accept": "application/json", "Authorization": f"Bearer {JINA_KEY}"}
        
        response = requests.get(search_url, headers=headers, timeout=30)
        if response.status_code != 200:
            print(f"❌ [LOG] Error Jina {response.status_code}.", flush=True)
            return []

        data = response.json().get('data', [])[:5]
        print(f"📊 [LOG] Analizando {len(data)} noticias simultáneamente...", flush=True)

<<<<<<< HEAD
        # Usamos ThreadPoolExecutor para que las 5 noticias se analicen al mismo tiempo
=======
>>>>>>> fa8b515 (refactor: preparing local changes for synchronization)
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