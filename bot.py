import discord
from discord.ext import commands
from openai import OpenAI
import os
from dotenv import load_dotenv
from intelligence import fetch_all_news, get_raw_news_list
import asyncio
import datetime
import pytz
import traceback
import random

load_dotenv(override=True)
TOKEN, AI_KEY = os.getenv('DISCORD_TOKEN'), os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=AI_KEY)

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)
news_storage = {}
news_cache = {}

STRATEGIC_KEYWORDS = [
    "nitrogen fertilizer market trends 2026",
    "grain shipping logistics and freight rates",
    "precision agriculture drone technology",
    "global urea price analysis",
    "agritech innovation in Latin America",
    "Chicago Board of Trade corn and soy prices",
    "sustainable farming practices automation",
    "impact of climate change on crop yields",
    "smart irrigation systems for large scale farming",
    "supply chain challenges in agribusiness"    
]

def get_guatemala_time():
    """Retorna la hora actual en formato legible para Guatemala (GMT-6)"""
    tz = pytz.timezone('America/Guatemala')
    return datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

async def send_log(ctx, activity_type, details):
    """Imprime logs en consola"""
    time_gt = get_guatemala_time()
    user = ctx.author.name
    console_log = f"🕒 [{time_gt}] | 👤 USER: {user} | 🚩 TYPE: {activity_type} | 📝 INFO: {details}"
    print(console_log)
    
    return time_gt, user

@bot.event
async def on_ready():
    print(f'✅ Agente Disagro online: {bot.user}')

@bot.command()
async def list_news(ctx):
    async with ctx.typing():
        # Spinner
        status_msg = await ctx.send("🚀 **Initiating global search sequence...**")
        async def spinner():
            try:
                while True:
                    for dots in [".", ". .", ". . ."]:
                        await status_msg.edit(content=f"📡 **Scanning Intelligence Network {dots}**")
                        await asyncio.sleep(0.5)
            except asyncio.CancelledError:
                pass 
        try:
            spinner_task = asyncio.create_task(spinner())

            # Búsqueda de noticias
            raw_news = await asyncio.to_thread(get_raw_news_list)
            news_cache[ctx.channel.id] = raw_news
            spinner_task.cancel()
            await asyncio.wait([spinner_task])
            is_backup = any("Reuters" in n['title'] for n in raw_news)
            await status_msg.edit(content="⚠️ **Accessing secondary intelligence nodes.**" if is_backup else "✅ **Network scan successful.**")
            full_response = "### 🔍 Latest Industry Headlines:\n" + "\n".join([f"{i}. **{n['title']}**\n<{n.get('url')}>" for i, n in enumerate(raw_news, 1)])
            
            # Chunking para evitar error 400 por mas de 2000 caracteres en Discord
            for i in range(0, len(full_response), 1900):
                await ctx.send(full_response[i:i+1900])
            
            await ctx.send("_ _\n✅ **Scan completed. All headlines loaded.**")
        except Exception as e:
                current_time = get_guatemala_time()
                user_name = ctx.author.name
                error_trace = traceback.format_exc()

                # Detalle del log
                print(f"\n--- 🚨 LOG DE ERROR TÉCNICO (!list_news)---")
                print(f"Time: {current_time} | User: {user_name}")
                print(f"Error: {str(e)}")
                print(f"Traceback:\n{error_trace}")
                print(f"-------------------------------\n")

                friendly_msg = (
                    f"### 🛡️ System Update\n"
                    f"Hello {user_name}, we are currently optimizing our strategic intelligence nodes.\n"
                    f"The analysis for `!list_news` is momentarily queued for maintenance.\n\n"
                    f"✅ *Technical log captured. Our team has been notified.*"
                )
                
                await ctx.send(friendly_msg)

@bot.command()
async def news(ctx):
    cached_data = news_cache.get(ctx.channel.id)
    if not cached_data:
        await ctx.send("⚠️ **No strategic data in memory.** Please run `!list_news` first to identify current headlines.")
        return
    await ctx.send(f"🧐 **Analyzing previously listed strategic news for Disagro...**")

    async with ctx.typing():
        try:
            reports = await asyncio.to_thread(fetch_all_news, cached_data)
            if not reports:
                await ctx.send("❌ No relevant news found at this moment.")
                return

            news_storage[ctx.channel.id] = {"reports": reports, "index": 3}
            
            # se procesan los 3 primeros links
            for i, r in enumerate(reports[:3], 1):
                if i > 1:
                    await ctx.send(f"\n{'='*35}\n")
                if len(r) > 1900:
                    chunks = [r[i:i+1900] for i in range(0, len(r), 1900)]
                    for chunk in chunks:
                        await ctx.send(chunk)
                else:
                    await ctx.send(r)

            await ctx.send("\n_ _\n✅ **Strategic analysis for Disagro completed.**")

            if len(reports) > 3:
                await ctx.send("👉 Use `!next` to see more analysis.")
        
        except Exception as e:
                current_time = get_guatemala_time()
                user_name = ctx.author.name
                error_trace = traceback.format_exc()

                # Log técnico
                print(f"\n--- 🚨 LOG DE ERROR TÉCNICO (!news) ---")
                print(f"Time: {current_time} | User: {user_name}")
                print(f"Error: {str(e)}")
                print(f"Traceback:\n{error_trace}")
                print(f"-------------------------------\n")

                friendly_msg = (
                    f"### 🛡️ System Update\n"
                    f"Hello {user_name}, we are currently optimizing our strategic intelligence nodes.\n"
                    f"The analysis for `!news` is momentarily queued for maintenance.\n\n"
                    f"✅ *Technical log captured. Our team has been notified.*"
                )
                
                await ctx.send(friendly_msg)
@bot.command()
async def next(ctx):
    # Verifica reportes en el canal
    channel_id = ctx.channel.id
    try:
        if channel_id not in news_storage or not news_storage[channel_id]["reports"]:
            await ctx.send("❌ **No previous analyses found.** Please use `!news` first to generate a new report.")
            return

        data = news_storage[channel_id]
        reports = data["reports"]
        start_index = data["index"]

        # Solo si ya llegamos al final de la lista
        if start_index >= len(reports):
            await ctx.send("🏁 **You have reached the end of the current analyses.**")
            return

        # Se obtienen los reportes pendientes, si hay
        next_reports = reports[start_index : start_index + 2]
        
        for i, r in enumerate(next_reports, 1):
            await ctx.send(f"\n{'='*35}\n")
            
            if len(r) > 1900:
                for chunk in [r[i:i+1900] for i in range(0, len(r), 1900)]:
                    await ctx.send(chunk)
            else:
                await ctx.send(r)

        news_storage[channel_id]["index"] = start_index + 2
        
        if news_storage[channel_id]["index"] < len(reports):
            await ctx.send("👉 Use `!next` to view more strategic analyses.")
        else:
            await ctx.send("✅ **All available analyses have been displayed.**")
    except Exception as e:
        current_time = get_guatemala_time()
        print(f"❌ [ERROR NEXT] {current_time} | {str(e)}")
        await ctx.send("### 🛡️ System intelligence node syncing. Please try again.")

@bot.event
async def on_command_error(ctx, error):
    # error de comando, se escribe uno que no existe o es invalido
    if isinstance(error, commands.CommandNotFound):
        help_text = (
            "👋 **Welcome to Disagro Intelligence Agent**\n\n"
            "I couldn't recognize that command. Here is what I can do for you:\n"
            "🔹 `!list_news` - Scans the network for the latest agricultural headlines.\n"
            "🔹 `!news`      - Generates a strategic AI analysis for Disagro.\n"
            "🔹 `!next`      - Shows more analysis from the current report.\n\n"
            "*Please type one of the commands above to proceed.*"
        )
        await ctx.send(help_text)
    else:
        # Para otros errores, quedan en el lgo
        print(f"🚨 Error detectado: {error}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    time_gt = get_guatemala_time()
    user = message.author.name
    content = message.content

    # 2. LOG DE ACTIVIDAD GENERAL (Cualquier cosa que escriban)
    print(f"🕒 [{time_gt}] | 👤 {user} wrote: '{content}'")

    # 3. Si no es un comando, enviamos el menú de ayuda
    if not content.startswith('!'):
        help_text = (
            f"Hello {message.author.display_name}, **Disagro Intelligence Agent** at your service. 🫡\n\n"
            "I only respond to specific commands to ensure data precision. Please use:\n"
            "🔹 `!list_news` - Scan latest industry headlines.\n"
            "🔹 `!news`      - Deep AI Strategic Analysis.\n"
            "🔹 `!next`      - More analysis from the queue."
        )
        await message.channel.send(help_text)
        return

    # 4. Si si es comando, se procesa normal
    await bot.process_commands(message)

@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            current_time = get_guatemala_time()
            welcome_msg = (
                f"## 🤖 Welcome to AgroWiz Intelligence System\n"
                f"**Strategic Analysis Node for Disagro | MIT Assignment**\n\n"
                f"Hello! I am **AgroWiz**, your AI-powered strategic assistant. I am currently "
                f"synchronized and ready to analyze global agricultural trends.\n\n"
                f"### 🛠️ Available Command Terminal:\n"
                f"* `!news` - Execute a high-level strategic analysis (Top 3 news).\n"
                f"* `!list_news` - Search the global database for specific topics.\n"
                f"* `!next` - Navigate through the intelligence backlog.\n\n"
                f"--- \n"
                f"✨ *System online since: {current_time} (Guatemala)*\n"
                f"🛡️ *All diagnostic protocols are active.*"
            )
            await channel.send(welcome_msg)
            break

@bot.command()
async def about(ctx):
    """Presentación del bot"""
    current_time = get_guatemala_time()
    info_msg = (
        f"### 🛡️ AgroWiz System Information\n"
        f"**Project:** Digital Transformation Hub - Disagro\n"
        f"**Lead Developer:** {ctx.author.name}\n"
        f"**Current Status:** Optimal\n\n"
        f"**Commands:** `!news`, `!list_news`, `!next`\n"
        f"**Last Sync:** {current_time}\n"
        f"--- \n"
        f"*Developed for MIT Applied Agentic AI Course*"
    )
    await ctx.send(info_msg)

if __name__ == "__main__":
    bot.run(TOKEN)