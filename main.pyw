#!/usr/bin/env python3
import ui
import asyncio
import discord
import logging
from tkinter import messagebox

root_logger = logging.getLogger()
root_logger.setLevel(logging.ERROR)

fh = logging.FileHandler('DAP_errors.log', delay=True)
fh.setLevel(logging.ERROR)

root_logger.addHandler(fh)

async def ready_bot(bot_ui, bot):
    await bot.wait_until_ready()
    
    bot_ui.set_cred(bot.user.name)
    bot_ui.set_servers([guild for guild in bot.guilds])
    
async def ready_user(bot_ui):
    await asyncio.sleep(5)
    
    bot_ui.set_cred(bot.user.name)
    bot_ui.set_servers([guild for guild in bot.guilds])

try:
    token = open('token.txt', 'r').read()
    token = token.strip()
 
    is_bot = True
    if '$' in token:
        is_bot = False
        token = token[:-1]

    bot = discord.Client()
    bot_ui = ui.UI(bot)

    asyncio.ensure_future(bot_ui.run_tk())
    
    if is_bot:
        asyncio.ensure_future(ready_bot(bot_ui, bot))
    else:
        asyncio.ensure_future(ready_user(bot_ui))
        
    bot.run(token, bot=is_bot)

except FileNotFoundError:
    messagebox.showerror('Token Error', "token.txt was not found")

except discord.errors.LoginFailure:
    messagebox.showerror('Login Failed', "Invalid credentials")

except:
    logging.exception('Error on main')
