import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True 
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# --- KONFIGURACJA ---
REQUIRED_ROLE_NAME = "CEO"  # Ranga, która może używać bota
LOG_CHANNEL_ID = 123456789012345678  # WKLEJ TUTAJ ID KANAŁU DO LOGÓW
# ---------------------

async def send_log(ctx, action, member, role):
    """Funkcja pomocnicza do wysyłania logów na kanał"""
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        embed = discord.Embed(title="📝 Log Zarządzania Rolami", color=discord.Color.blue())
        embed.add_field(name="Akcja", value=action, inline=False)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
        embed.add_field(name="Użytkownik", value=member.mention, inline=True)
        embed.add_field(name="Rola", value=role.name, inline=True)
        embed.set_footer(text=f"ID Moderatora: {ctx.author.id}")
        await channel.send(embed=embed)
    else:
        print("Błąd: Nie znaleziono kanału logów. Sprawdź ID!")

@bot.event
async def on_ready():
    print(f'Bot {bot.user} gotowy do logowania akcji!')

@bot.command(aliases=['dr', 'give', 'add'])
async def dajrole(ctx, member: discord.Member, role: discord.Role):
    if not (ctx.author.guild_permissions.administrator or any(r.name == REQUIRED_ROLE_NAME for r in ctx.author.roles)):
        await ctx.send("❌ Brak uprawnień.")
        return

    try:
        await member.add_roles(role)
        await ctx.send(f"✅ Nadano rolę **{role.name}**.")
        await send_log(ctx, "Nadanie roli", member, role)
    except discord.Forbidden:
        await ctx.send("🚫 Błąd uprawnień bota (sprawdź hierarchię ról).")

@bot.command(aliases=['zr', 'take', 'remove'])
async def zabierzrole(ctx, member: discord.Member, role: discord.Role):
    if not (ctx.author.guild_permissions.administrator or any(r.name == REQUIRED_ROLE_NAME for r in ctx.author.roles)):
        await ctx.send("❌ Brak uprawnień.")
        return

    try:
        await member.remove_roles(role)
        await ctx.send(f"⚠️ Odebrano rolę **{role.name}**.")
        await send_log(ctx, "Odebranie roli", member, role)
    except discord.Forbidden:
        await ctx.send("🚫 Błąd uprawnień bota.")

import os
bot.run(os.environ.get('DISCORD_TOKEN'))
