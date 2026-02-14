import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# --- SEKCJA RENDER (OSZUKUJEMY PORT) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot pracuje i czuwa!"

def run():
    # Render najczęściej używa portu 10000
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ----------------------------------------

# Konfiguracja bota
intents = discord.Intents.default()
intents.members = True          # Do ról na start
intents.message_content = True  # Do czytania komend
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user.name}')
    print('Status: Online na Render.com')

# --- TWOJA LOGIKA RÓL ---

@bot.event
async def on_member_join(member):
    # Tutaj wpisz nazwę roli, którą bot ma dawać każdemu nowemu
    role_name = "Gracz" 
    role = discord.utils.get(member.guild.roles, name=role_name)
    if role:
        await member.add_roles(role)
        print(f'Nadano rolę {role_name} dla {member.name}')
    else:
        print(f'Nie znaleziono roli o nazwie {role_name}')

@bot.command()
async def ranga(ctx, member: discord.Member, *, role_name):
    # Komenda !ranga @użytkownik NazwaRoli
    if ctx.author.guild_permissions.manage_roles:
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            await member.add_roles(role)
            await ctx.send(f'✅ Nadano rangę **{role_name}** użytkownikowi {member.mention}')
        else:
            await ctx.send(f'❌ Nie znalazłem rangi o nazwie {role_name}')
    else:
        await ctx.send('❌ Nie masz uprawnień do zarządzania rolami!')

# --- URUCHOMIENIE ---
keep_alive()

token = os.environ.get('DISCORD_TOKEN')
bot.run(token)
