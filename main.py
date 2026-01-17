import json
import sys
import discord
from discord.ext import commands
from config import TOKEN
from sc import s1, s2, s3, s4, s5, s6 , s7
from sc import c1, c2, c3, c4, c5, c6 , c7
import sqlite3
import aiohttp
import io
from groq import Groq

GROQ_API_KEY = "your-groq-api-key-here"
groq_client = Groq(api_key=GROQ_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def init_db():
    conn = sqlite3.connect("sorular.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sorular (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            user_id INTEGER,
            question TEXT,
            is_voice BOOLEAN DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    try:
        cursor.execute("ALTER TABLE sorular ADD COLUMN is_voice BOOLEAN DEFAULT 0")
        conn.commit()
    except sqlite3.OperationalError:
        pass
    
    conn.commit()
    conn.close()

def save_question(user_name, user_id, question, is_voice=False):
    conn = sqlite3.connect("sorular.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sorular (user_name, user_id, question, is_voice)
        VALUES (?, ?, ?, ?)
    ''', (user_name, user_id, question, is_voice))
    conn.commit()
    conn.close()

async def transcribe_audio(audio_url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(audio_url) as resp:
                if resp.status != 200:
                    return None
                audio_data = await resp.read()
        
        audio_file = io.BytesIO(audio_data)
        audio_file.name = "voice.ogg"
        
        transcription = groq_client.audio.transcriptions.create(
            file=("voice.ogg", audio_file),
            model="whisper-large-v3-turbo",
            language="tr",
            response_format="text"
        )
        
        return transcription
        
    except Exception as e:
        print(f"Ses çevirme hatası: {e}")
        return None

def is_question(text):
    if not text:
        return False
    
    text_lower = text.lower().strip()
    
    question_words = ['ne', 'nasıl', 'neden', 'niçin', 'kim', 'nerede', 'ne zaman', 
                      'hangi', 'kaç', 'ne kadar', 'mi', 'mı', 'mu', 'mü']
    
    if '?' in text:
        return True
    
    for word in question_words:
        if text_lower.startswith(word):
            return True
    
    words = text_lower.split()
    if len(words) > 0 and words[0] in question_words:
        return True
    
    return False

@bot.event
async def on_ready():
    init_db()
    print(f"{bot.user} giriş yaptı.")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command(name="menu")
async def menu(ctx):
    embed = discord.Embed(
        title="📋 Menü",
        description="Aşağıdaki butonlardan birini seçiniz.",
        color=discord.Color.blue()
    )
    view = discord.ui.View()

    soru_button = discord.ui.Button(label="❓ SORU SOR", style=discord.ButtonStyle.primary)
    async def soru_callback(interaction):
        modal = discord.ui.Modal(title="Soru Sor")
        question_input = discord.ui.TextInput(
            label="Sorunuz",
            style=discord.TextStyle.paragraph,
            placeholder="Sorunuzu buraya yazın...",
            required=True,
            max_length=1000
        )
        modal.add_item(question_input)
        
        async def modal_submit(modal_interaction):
            question = question_input.value
            user_name = modal_interaction.user.name
            user_id = modal_interaction.user.id
            save_question(user_name, user_id, question)
            await modal_interaction.response.send_message(
                f"✅ Sorunuz alındı, {user_name}! Yönetici en kısa sürede ilgilenecek.",
                ephemeral=True
            )
        
        modal.on_submit = modal_submit
        await interaction.response.send_modal(modal)
    
    soru_button.callback = soru_callback
    view.add_item(soru_button)

    sss_button = discord.ui.Button(label="📚 SSS", style=discord.ButtonStyle.success)
    async def sss_callback(interaction):
        await interaction.response.send_message(
            "📚 **Sıkça Sorulan Sorular**\nLink: https://docs.google.com/document/d/1_wiMdxW5MKdz_lBwdJMk6xi6hME3E1SZ2HgF4KA4vGI/edit?pli=1&tab=t.0",
            ephemeral=True
        )
    sss_button.callback = sss_callback
    view.add_item(sss_button)

    dokuman_button = discord.ui.Button(label="📄 Doküman", style=discord.ButtonStyle.danger)
    async def dokuman_callback(interaction):
        await interaction.response.send_message(
            "📄 **Doküman**\nLink: https://docs.google.com/document/d/1hHJyXQmZDdEejEN0t5Z4crUwxv74dvn7N7OIPyJrR3o/edit?usp=sharing",
            ephemeral=True
        )
    dokuman_button.callback = dokuman_callback
    view.add_item(dokuman_button)

    await ctx.send(embed=embed, view=view)

@bot.command(name="soru")
async def soru(ctx, *, question=None):
    if question is None:
        await ctx.send("❌ Sorunuzu lütfen `!soru <sorunuz>` şeklinde yazınız.")
        return
    
    user_name = ctx.author.name
    user_id = ctx.author.id
    save_question(user_name, user_id, question)
    await ctx.send(f"✅ Sorunuz alındı, {user_name}! Yönetici en kısa sürede ilgilenecek.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!"):
        await bot.process_commands(message)
        return

    content = message.content.strip().lower()

    response_sent = False
    
    if content in s1:
        await message.channel.send(c1)
        response_sent = True
    elif content in s2:
        await message.channel.send(c2)
        response_sent = True
    elif content in s3:
        await message.channel.send(c3)
        response_sent = True
    elif content in s4:
        await message.channel.send(c4)
        response_sent = True
    elif content in s5:
        await message.channel.send(c5)
        response_sent = True
    elif content in s6:
        await message.channel.send(c6)
        response_sent = True
    elif content in s7:
        await message.channel.send(c7)
        response_sent = True
    
    if message.attachments:
        for attachment in message.attachments:
            if attachment.content_type and 'audio' in attachment.content_type:
                await message.add_reaction('🎙️')
                
                transcript = await transcribe_audio(attachment.url)
                
                if transcript:
                    if is_question(transcript):
                        user_name = message.author.name
                        user_id = message.author.id
                        save_question(user_name, user_id, transcript, is_voice=True)
                        
                        await message.reply(
                            f"🎙️ **Sesli mesajınız alındı!**\n"
                            f"📝 Metin: `{transcript}`\n"
                            f"✅ Sorunuz kaydedildi. Yönetici en kısa sürede ilgilenecek."
                        )
                    else:
                        await message.reply(
                            f"🎙️ **Sesli mesaj işlendi**\n"
                            f"📝 Metin: `{transcript}`\n"
                            f"ℹ️ Bu bir soru gibi görünmüyor. Soru sormak için `!soru` komutunu kullanabilirsiniz."
                        )
                else:
                    await message.reply("❌ Sesli mesaj işlenirken bir hata oluştu.")
                
                return
    
    if not response_sent and is_question(message.content):
        await message.reply(
            "❓ Bu bir soru gibi görünüyor!\n"
            "Sorunuzu kaydetmek için `!soru <sorunuz>` komutunu veya `!menu` butonlarını kullanabilirsiniz."
        )


bot.run(TOKEN)
