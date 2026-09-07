import discord
from discord.ext import commands

WIN_EXP = 900
LOSS_EXP = 700
AVG_EXP = (WIN_EXP + LOSS_EXP) / 2  # half wins, half losses

# ----------------------------------------
# Progress Bar
# ----------------------------------------
def make_progress_bar(current, total, length=30):
    ratio = current / total
    filled = int(ratio * length)
    bar = "🟩" * filled + "⬛" * (length - filled)
    percent = ratio * 100
    return f"{bar}  **{percent:.1f}%**"

# ----------------------------------------
# EXP Table (Rank 1 → Rank 30)
# ----------------------------------------
def build_exp_table():
    exp_table = [0]  # Rank 1 = 0 EXP
    exp = 0

    for level in range(2, 31):  # ranks 2–30
        if 2 <= level <= 4:
            exp += 2000
        elif 5 <= level <= 9:
            exp += 3000
        elif 10 <= level <= 14:
            exp += 4000
        elif 15 <= level <= 19:
            exp += 5500
        elif 20 <= level <= 24:
            exp += 7500
        elif 25 <= level <= 29:
            exp += 10000
        elif level == 30:
            exp += 20000  # Rank 30 requires 20,000 EXP

        exp_table.append(exp)

    return exp_table

EXP_TABLE = build_exp_table()

# ----------------------------------------
# Bot Setup
# ----------------------------------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)


# ----------------------------------------
# Intro
# ----------------------------------------
@bot.event
async def on_ready():
    print("Thancred has arrived — and rest assured, I'll handle this.")

# ----------------------------------------
# !helpcc — Command List
# ----------------------------------------
@bot.command()
async def helpcc(ctx):
    embed = discord.Embed(
        title="📘 Thancred's Crystalline Conflict Toolkit",
        description="If you need guidance, I’m right here.",
        color=discord.Color.gold()
    )

    embed.add_field(
        name="`!cc <current_rank> <exp_toward_next> <target_rank>`",
        value="Calculate matches needed to reach your target rank.\nShows min, max, average matches + progress bar.",
        inline=False
    )

    embed.add_field(
        name="`!ccmax <current_rank> <exp_toward_next>`",
        value="Shows how close you are to Rank 30 (max rank).",
        inline=False
    )

    embed.add_field(
        name="`!ccgraph`",
        value="Displays the full EXP chart for ranks 1–30.",
        inline=False
    )

    embed.add_field(
        name="`!cccompare <rank1> <exp1> <rank2> <exp2> <target_rank>`",
        value="Compare two players’ progress toward a target rank.",
        inline=False
    )

    embed.add_field(
        name="`!ccleaderboard`",
        value="Shows the server EXP leaderboard.",
        inline=False
    )

    embed.add_field(
        name="`!thancred`",
        value="Hear from Thancred himself — lore‑flavored lines.",
        inline=False
    )

    embed.add_field(
        name="`!thancredquote`",
        value="Shadowbringers‑inspired Thancred quotes.",
        inline=False
    )

    embed.set_footer(text="Thancred: I’ll handle this.")
    await ctx.send(embed=embed)

# ----------------------------------------
# !thancred — Personality Command
# ----------------------------------------
@bot.command()
async def thancred(ctx):
    import random

    lines = [
        "I’ve been through worse than a few PvP matches. Let’s get to work.",
        "If you need a hand — or a blade — you know who to call.",
        "Crystalline Conflict? Hah. Child’s play compared to the First.",
        "I’ll handle this. You just focus on winning.",
        "If you fall, I’ll pick you up. If you falter, I’ll steady you.",
        "Rank grinding? Trust me, I’ve survived far more tedious tasks.",
        "Let’s see how sharp your skills are — I’ll be watching."
    ]

    embed = discord.Embed(
        title="Thancred Waters",
        description=random.choice(lines),
        color=discord.Color.dark_gray()
    )

    embed.set_thumbnail(url="https://i.imgur.com/8fQeYkS.png")
    embed.set_footer(text="Thancred at your service.")

    await ctx.send(embed=embed)

# ----------------------------------------
# !thancredquote — Shadowbringers Quotes
# ----------------------------------------
@bot.command()
async def thancredquote(ctx):
    import random

    quotes = [
        "I've walked the First and the Source — danger feels the same no matter the world.",
        "You learn a lot about yourself when you're forced to fight alone.",
        "If there's one thing Shadowbringers taught me, it's that hesitation can cost lives.",
        "I’ve faced Lightwardens and worse. A few PvP matches won’t shake me.",
        "Strength isn’t just steel and skill — it’s resolve.",
        "Even in the darkest places, someone has to keep moving forward.",
        "I’ll keep watch. You press on.",
        "I’ve had worse."
    ]

    embed = discord.Embed(
        title="Thancred — Shadowbringers Reflections",
        description=random.choice(quotes),
        color=discord.Color.dark_gray()
    )

    embed.set_thumbnail(url="https://i.imgur.com/8fQeYkS.png")
    embed.set_footer(text="Thancred: Stay sharp.")

    await ctx.send(embed=embed)

# ----------------------------------------
# !cc — Main Calculator
# ----------------------------------------
@bot.command()
async def cc(ctx, current_rank: int, exp_toward_next: int, target_rank: int):

    if target_rank < current_rank:
        await ctx.send("Your target rank is lower than your current rank.")
        return

    if target_rank > 30:
        await ctx.send("Target rank must be between 1 and 30.")
        return

    base_exp = EXP_TABLE[current_rank - 1]
    total_exp = base_exp + exp_toward_next

    target_exp = EXP_TABLE[target_rank - 1]

    if total_exp >= target_exp:
        await ctx.send(f"🎉 You already reached Rank {target_rank}!")
        return

    exp_needed = target_exp - total_exp

    min_matches = exp_needed / WIN_EXP
    max_matches = exp_needed / LOSS_EXP
    avg_matches = exp_needed / AVG_EXP

    progress_bar = make_progress_bar(total_exp, target_exp)

    embed = discord.Embed(
        title=f"Crystalline Conflict Progress — Rank {current_rank} → {target_rank}",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="📈 Progress Toward Target Rank",
        value=progress_bar,
        inline=False
    )

    embed.add_field(
        name="📊 EXP Details",
        value=(
            f"**Current EXP:** {total_exp}\n"
            f"**Target EXP:** {target_exp}\n"
            f"**Remaining EXP:** {exp_needed}"
        ),
        inline=False
    )

    embed.add_field(
        name="🏆 Minimum Matches (all wins)",
        value=f"**{min_matches:.1f} matches**",
        inline=False
    )

    embed.add_field(
        name="🎲 Average Matches (half wins / half losses)",
        value=f"**{avg_matches:.1f} matches**",
        inline=False
    )

    embed.add_field(
        name="💀 Maximum Matches (all losses)",
        value=f"**{max_matches:.1f} matches**",
        inline=False
    )

    embed.set_footer(text="Thancred: Stay sharp — victory favors the prepared.")

    await ctx.send(embed=embed)

# ----------------------------------------
# !ccmax — Progress Toward Rank 30
# ----------------------------------------
@bot.command()
async def ccmax(ctx, current_rank: int, exp_toward_next: int):

    base_exp = EXP_TABLE[current_rank - 1]
    total_exp = base_exp + exp_toward_next

    target_exp = EXP_TABLE[29]  # Rank 30 EXP

    exp_needed = target_exp - total_exp

    progress_bar = make_progress_bar(total_exp, target_exp)

    embed = discord.Embed(
        title=f"Crystalline Conflict — Rank {current_rank} → Rank 30",
        color=discord.Color.orange()
    )

    embed.add_field(
        name="📈 Progress Toward Rank 30",
        value=progress_bar,
        inline=False
    )

    embed.add_field(
        name="📊 EXP Details",
        value=(
            f"**Current EXP:** {total_exp}\n"
            f"**Rank 30 EXP:** {target_exp}\n"
            f"**Remaining EXP:** {exp_needed}"
        ),
        inline=False
    )

    embed.set_footer(text="Thancred: The final stretch — give it your all.")

    await ctx.send(embed=embed)

# ----------------------------------------
# Leaderboard Storage
# ----------------------------------------
leaderboard = {}  # {user_id: total_exp}

# ----------------------------------------
# !ccleaderboard — Server EXP Leaderboard
# ----------------------------------------
@bot.command()
async def ccleaderboard(ctx):

    if not leaderboard:
        await ctx.send("No EXP data recorded yet.")
        return

    sorted_lb = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)

    embed = discord.Embed(
        title="🏆 Crystalline Conflict Leaderboard",
        color=discord.Color.purple()
    )

    desc = ""
    for i, (user_id, exp) in enumerate(sorted_lb, start=1):
        user = await bot.fetch_user(user_id)
        desc += f"**{i}. {user.name}** — {exp} EXP\n"

    embed.add_field(
        name="Top Players",
        value=desc,
        inline=False
    )

    embed.set_footer(text="Thancred: Competition sharpens the blade.")

    await ctx.send(embed=embed)

# ----------------------------------------
# Auto‑record EXP whenever !cc or !ccmax is used
# ----------------------------------------
async def record_exp(user_id, total_exp):
    leaderboard[user_id] = total_exp

# Patch into !cc and !ccmax
old_cc = cc
async def cc(ctx, current_rank: int, exp_toward_next: int, target_rank: int):
    await old_cc(ctx, current_rank, exp_toward_next, target_rank)
    base_exp = EXP_TABLE[current_rank - 1]
    total_exp = base_exp + exp_toward_next
    await record_exp(ctx.author.id, total_exp)

bot.remove_command("cc")
bot.command()(cc)

old_ccmax = ccmax
async def ccmax(ctx, current_rank: int, exp_toward_next: int):
    await old_ccmax(ctx, current_rank, exp_toward_next)
    base_exp = EXP_TABLE[current_rank - 1]
    total_exp = base_exp + exp_toward_next
    await record_exp(ctx.author.id, total_exp)

bot.remove_command("ccmax")
bot.command()(ccmax)

# ----------------------------------------
# Run Bot
# ----------------------------------------
import os
bot.run(os.getenv("BOT_TOKEN"))

