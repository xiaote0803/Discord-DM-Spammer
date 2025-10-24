import os
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import functools
import json

load_dotenv()

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
MESSAGE_COUNT = config['message_count']
MESSAGE_CONTENT = config['message_content']

tokens = []
i = 0
while True:
    key = "MAIN_TOKEN" if i == 0 else f"BOT_{i}_TOKEN"
    token = os.getenv(key)
    if not token:
        break
    tokens.append(token)
    i += 1

num_bots = len(tokens)
if num_bots < 1:
    print("Error: At least MAIN_TOKEN is required.")
    exit(1)

GUILD_ID = os.getenv("GUILD_ID")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bots = [commands.Bot(command_prefix="!", intents=intents) for _ in range(num_bots)]
main_bot = bots[0]

bot_logins = {}

async def send_message(bot_instance: commands.Bot, user_id: int, message: str = MESSAGE_CONTENT, count: int = MESSAGE_COUNT, delay: float = 0):
    try:
        user = await bot_instance.fetch_user(user_id)
        dm_channel = await user.create_dm()
        tasks = [dm_channel.send(message) for _ in range(count)]
        await asyncio.gather(*tasks)
        if delay > 0:
            await asyncio.sleep(delay)
    except discord.errors.Forbidden:
        print(f"[{bot_instance.user}] Cannot send DM to {user_id}: User has DMs disabled or bot is blocked.")
    except Exception as e:
        print(f"[{bot_instance.user}] Failed to send {message} to {user_id}: {e}")

@main_bot.tree.command(name="send", description=f"Send '{MESSAGE_CONTENT}' to a user via {num_bots-1} other bots ({MESSAGE_COUNT} times each)")
@app_commands.describe(user="The user to send the message to")
async def send_command(interaction: discord.Interaction, user: discord.User):
    await interaction.response.send_message(f"Triggering bots to send '{MESSAGE_CONTENT}' to {user.mention} {MESSAGE_COUNT} times each", ephemeral=True)
    for bot in bots[1:]:
        asyncio.create_task(send_message(bot, user.id))

@main_bot.command(name="send")
async def send_text(ctx: commands.Context, user: discord.User):
    await ctx.send(f"Triggering bots to send '{MESSAGE_CONTENT}' to {user.mention} {MESSAGE_COUNT} times each")
    for bot in bots[1:]:
        asyncio.create_task(send_message(bot, user.id))

async def on_ready(bot_index):
    global bot_logins
    bot_name = "Main Bot" if bot_index == 0 else f"Bot {bot_index}"
    bot_logins[bot_index] = f"{bot_name} logged in as {bots[bot_index].user}"
    if bot_index == 0:
        try:
            if GUILD_ID:
                guild = discord.Object(id=int(GUILD_ID))
                bots[bot_index].tree.copy_global_to(guild=guild)
                synced = await bots[bot_index].tree.sync(guild=guild)
                synced_msg = "Commands synced successfully"
            else:
                synced = await bots[bot_index].tree.sync()
                synced_msg = "Commands synced successfully"
        except discord.errors.Forbidden:
            synced_msg = "Failed to sync commands: Bot lacks permissions. Ensure 'applications.commands' scope is enabled."
        except Exception as e:
            synced_msg = f"Failed to sync commands: {e}"
        bot_logins['synced'] = synced_msg
    
    if len(bot_logins) == num_bots + 1:
        print("\033[1A\033[K", end="")
        for i in range(num_bots):
            print(bot_logins[i])
        print(bot_logins['synced'])

for i, bot in enumerate(bots):
    bot.add_listener(functools.partial(on_ready, i), "on_ready")

async def main():
    print("Starting bots...")
    try:
        await asyncio.gather(
            *[bot.start(token) for bot, token in zip(bots, tokens)]
        )
    except discord.errors.LoginFailure:
        print("Error: Invalid token(s). Please verify your tokens in the .env file.")
    except KeyboardInterrupt:
        print("Shutting down...")
    except Exception as e:
        print(f"Error starting bots: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await asyncio.gather(*[bot.close() for bot in bots])

if __name__ == "__main__":
    asyncio.run(main())
