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

def fetch_all_news(input_data="agriculture"):
    """Ciclo estratégico optimizado con soporte para MEMORIA o búsqueda nueva"""
    try:
        print("\n" + "="*60, flush=True)
        print(f"🚀 [SISTEMA] INICIANDO CICLO ESTRATÉGICO", flush=True)
        print("="*60, flush=True)

        # 1. DETECCIÓN DE DATOS (Arreglado el nombre de la variable)
        if isinstance(input_data, list):
            data = input_data[:5]
            print(f"📊 [LOG] Usando {len(data)} noticias desde MEMORIA CACHÉ...", flush=True)
        else:
            # Si es un string, hacemos la búsqueda normal
            clean_topic = str(input_data).replace(" ", "+")
            cache_buster = random.randint(1, 1000)
            query = f"{clean_topic}+logistics+news+Central+America+2026?cb={cache_buster}"
            search_url = f"https://s.jina.ai/{query}"
            headers = {"Accept": "application/json", "Authorization": f"Bearer {JINA_KEY}"}
        
            response = requests.get(search_url, headers=headers, timeout=30)
            if response.status_code != 200:
                print(f"❌ [LOG] Error Jina {response.status_code}.", flush=True)
                return []
            data = response.json().get('data', [])[:5]
            print(f"📊 [LOG] Analizando {len(data)} noticias de búsqueda nueva...", flush=True)

        # 2. PROCESAMIENTO CON BLINDAJE (Aquí es donde pones lo de url vs link)
        with ThreadPoolExecutor() as executor:
            futures = []
            for item in data:
                # BLINDAJE: Jina a veces usa 'content', a veces 'description'
                content = item.get('content') or item.get('description') or ""
                
                # BLINDAJE: !list_news usa 'url', pero por si acaso buscamos 'link'
                url = item.get('url') or item.get('link') or "No URL"
                
                title = item.get('title', 'Untitled News')

                # Bajamos el requisito a 100 caracteres para ser menos estrictos
                if len(content) > 100:
                    futures.append(executor.submit(analyze_strategic_impact, content, url, title))
                else:
                    print(f"⚠️ [LOG] Noticia saltada por contenido insuficiente: {title}", flush=True)
            
            all_reports = [f.result() for f in futures]
        
        print("\n" + "="*60, flush=True)
        print(f"🏁 [SISTEMA] CICLO FINALIZADO CON ÉXITO", flush=True)
        print("="*60 + "\n", flush=True)
        return all_reports

    except Exception as e:
        print(f"\n🚨 [ERROR] Fallo en el ciclo: {e}", flush=True)
        return []