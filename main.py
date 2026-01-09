import json
import sys
import discord
from discord.ext import commands
from config import TOKEN
from sc import s1, s2, s3, s4, s5, s6
from sc import c1, c2, c3, c4, c5, c6
import sqlite3

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Veritabanı başlangıç fonksiyonu
def init_db():
    conn = sqlite3.connect("sorular.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sorular (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            user_id INTEGER,
            question TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Soru kaydetme fonksiyonu
def save_question(user_name, user_id, question):
    conn = sqlite3.connect("sorular.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sorular (user_name, user_id, question)
        VALUES (?, ?, ?)
    ''', (user_name, user_id, question))
    conn.commit()
    conn.close()

@bot.event
async def on_ready():
    init_db()  # Bot başladığında veritabanını hazırla
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
    
    # Soru Sor Butonu
    soru_button = discord.ui.Button(label="❓ SORU SOR", style=discord.ButtonStyle.primary)
    
    async def soru_callback(interaction):
        modal = discord.ui.Modal(title="Soru Sor")
        # ✅ DÜZELTME: TextInputStyle yerine TextStyle
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
            
            # Soruyu veritabanına kaydet
            save_question(user_name, user_id, question)
            
            await modal_interaction.response.send_message(
                f"✅ Sorunuz alındı, {user_name}! Yönetici en kısa sürede ilgilenecek.", 
                ephemeral=True
            )
        
        modal.on_submit = modal_submit
        await interaction.response.send_modal(modal)
    
    soru_button.callback = soru_callback
    view.add_item(soru_button)
    
    # SSS Butonu
    sss_button = discord.ui.Button(label="📚 SSS", style=discord.ButtonStyle.success)
    
    async def sss_callback(interaction):
        await interaction.response.send_message(
            "📚 **Sıkça Sorulan Sorular**\nLink: https://docs.google.com/document/d/1_wiMdxW5MKdz_lBwdJMk6xi6hME3E1SZ2HgF4KA4vGI/edit?pli=1&tab=t.0", 
            ephemeral=True
        )
    
    sss_button.callback = sss_callback
    view.add_item(sss_button)
    
    # Doküman Butonu
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
    
    # Soruyu veritabanına kaydet
    save_question(user_name, user_id, question)
    
    await ctx.send(f"✅ Sorunuz alındı, {user_name}! Yönetici en kısa sürede ilgilenecek.")

@bot.event
async def on_message(message):
    # Bot kendi mesajlarına cevap vermesin
    if message.author.bot:
        return

    # Komutları işle
    if message.content.startswith("!"):
        await bot.process_commands(message)
        return

    # Mesaj içeriğini normalize et
    content = message.content.strip().lower()

    # Cevapları kontrol et
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

bot.run(TOKEN)