import datetime
from discord.ext import commands, tasks
import discord
from dataclasses import dataclass

BOT_TOKEN ="Your_Bot_Token_Here"
CHANNEL_ID = Your_Channel_ID_Here

REMINDER_MINUTES = 120

@dataclass
class Session:

    # Session variables
    is_active: bool = False
    start_time: int = 0

    # Game stats
    games: int = 0
    wins: int = 0
    losses: int = 0
    ACS: int = 0
    Kills: int = 0
    Deaths: int = 0
    Assists: int = 0
    ECON: int = 0
    FBS: int = 0
    Plants: int = 0
    Defuses: int = 0



bot = commands.Bot(command_prefix = "/", intents = discord.Intents.all())
session = Session()

# Startup message
@bot.event
async def on_ready():
    print("READY!!!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello! Valorant Stat Bot is ready!")

# Reminds the user every 2 hours to take a break
@tasks.loop(minutes=REMINDER_MINUTES)
async def reminder():

    if reminder.current_loop == 0:
        return

    channel = bot.get_channel(CHANNEL_ID)   
    await channel.send(f"**Take a break!** You've been playing for {REMINDER_MINUTES} minutes straight!")

# Starts the gaming session
@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active!")
        return

    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    if reminder.is_running():
        reminder.restart()
    else:
        reminder.start()
    await ctx.send(f"New session started.")

# Gives current session stats
@bot.command()
async def current_stats(ctx):
    
    if not session.is_active:
        await ctx.send("No session is currently active!")
        return
    
    session.end_time = ctx.message.created_at.timestamp()
    duration = session.end_time - session.start_time
    simple_duration = str(datetime.timedelta(seconds=int(duration)))
    
    # current stat avgs
    win_percentage = (session.wins / session.games * 100) if session.games else 0
    avg_ACS = session.ACS / session.games if session.games else 0
    avg_Kills = session.Kills / session.games if session.games else 0
    avg_Deaths = session.Deaths / session.games if session.games else 0
    avg_Assists = session.Assists / session.games if session.games else 0
    avg_ECON = session.ECON / session.games if session.games else 0
    avg_FBS = session.FBS / session.games if session.games else 0
    avg_Plants = session.Plants / session.games if session.games else 0
    avg_Defuses = session.Defuses / session.games if session.games else 0

    # current summary
    summary = f"""You have been playing for {simple_duration}.
    Games Played: {session.games}
    Win Percentage: {win_percentage:.2f}%
    Average ACS: {avg_ACS:.2f}
    Average Kills: {avg_Kills:.2f}
    Average Deaths: {avg_Deaths:.2f}
    Average Assists: {avg_Assists:.2f}
    Average ECON: {avg_ECON:.2f}
    Average FBs: {avg_FBS:.2f}
    Average Plants: {avg_Plants:.2f}
    Average Defuses: {avg_Defuses:.2f}
    """
    await ctx.send(summary)

    # resets
    win_percentage = 0
    avg_ACS = 0
    avg_Kills = 0
    avg_Deaths = 0
    avg_Assists = 0
    avg_ECON = 0
    avg_FBS = 0
    avg_FBS = 0
    avg_Plants = 0
    avg_Defuses = 0

# Ends the gaming session
@bot.command()
async def end(ctx):
    
    if not session.is_active:
        await ctx.send("No session is currently active!")
        return

    session.is_active = False
    session.end_time = ctx.message.created_at.timestamp()
    duration = session.end_time - session.start_time
    simple_duration = str(datetime.timedelta(seconds=int(duration)))
    if reminder.is_running():
        reminder.stop()

    # Session stat avgs
    win_percentage = (session.wins / session.games * 100) if session.games else 0
    avg_ACS = session.ACS / session.games if session.games else 0
    avg_Kills = session.Kills / session.games if session.games else 0
    avg_Deaths = session.Deaths / session.games if session.games else 0
    avg_Assists = session.Assists / session.games if session.games else 0
    avg_ECON = session.ECON / session.games if session.games else 0
    avg_FBS = session.FBS / session.games if session.games else 0
    avg_Plants = session.Plants / session.games if session.games else 0
    avg_Defuses = session.Defuses / session.games if session.games else 0

    # Session summary
    summary = f"""Session ended after {simple_duration}.
    Games Played: {session.games}
    Win Percentage: {win_percentage:.2f}%
    Average ACS: {avg_ACS:.2f}
    Average Kills: {avg_Kills:.2f}
    Average Deaths: {avg_Deaths:.2f}
    Average Assists: {avg_Assists:.2f}
    Average ECON: {avg_ECON:.2f}
    Average FBs: {avg_FBS:.2f}
    Average Plants: {avg_Plants:.2f}
    Average Defuses: {avg_Defuses:.2f}
    """
    await ctx.send(summary)

    # Reset session data
    session.games = 0
    session.wins = 0
    session.losses = 0
    session.ACS = 0
    session.Kills = 0
    session.Deaths = 0
    session.Assists = 0
    session.ECON = 0
    session.FBS = 0
    session.Plants = 0
    session.Defuses = 0

# Gets game stats
@bot.command()
async def game_stats(ctx):
    if not session.is_active:
        await ctx.send("No session is currently active!")
        return

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Did you win or lose? (Type 'win' or 'loss')")
    msg = await bot.wait_for('message', check=check)
    WL = msg.content.lower()

    if WL in ['win', 'won']:
        session.wins += 1
    elif WL in ['loss', 'lost']:
        session.losses += 1
    else:
        await ctx.send("Invalid input. Aborting.")
        return

    session.games += 1

    for field in ["ACS", "Kills", "Deaths", "Assists", "ECON", "FBS", "Plants", "Defuses"]:
        await ctx.send(f"Enter the value for {field}: ")
        msg = await bot.wait_for('message', check=check)
        setattr(session, field, getattr(session, field) + int(msg.content))

    await ctx.send("Stats for this game have been recorded.")

bot.run(BOT_TOKEN)
