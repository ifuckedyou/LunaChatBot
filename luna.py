import asyncio
import re
from aiohttp import ClientSession
from config import ARQ_API_BASE_URL as ARQ_API
from config import ARQ_API_KEY, bot_id, bot_token, owner_id
from pyrogram import Client, filters, idle
from Python_ARQ import ARQ

luna = Client(
    ":memory:",
    bot_token=bot_token,
    api_id=1061393,
    api_hash="dee44b60afe8fd325a96f5237e495d7a",
)
aiohttp_session = ClientSession()
arq = ARQ(ARQ_API, ARQ_API_KEY, aiohttp_session)

async def getresp(query: str, user_id: int):
    luna = await arq.luna(query, user_id)
    response = luna.result
    return response


@luna.on_message(filters.command("repo") & ~filters.edited)
async def repo(_, message):
    await message.reply_text(
        "[Sourcecode](https://t.me/Baby_xD)"
        + " | [Group](t.me/PatheticProgrammers)",
        disable_web_page_preview=True,
    )


@luna.on_message(filters.command("help") & ~filters.edited)
async def start(_, message):
    await luna.send_chat_action(message.chat.id, "typing")
    await message.reply_text("/repo - Get Repo Link")


@luna.on_message(filters.command("shutdown") & filters.user(owner_id) & ~filters.edited)
async def shutdown(_, message):
    await luna.send_chat_action(message.chat.id, "typing")
    await message.reply_text("**Shutted Down!**")
    print("Exited!")
    exit()


@luna.on_message(
    ~filters.private
    & ~filters.command("shutdown")
    & ~filters.command("help")
    & ~filters.edited
)
async def chat(_, message):
    if message.reply_to_message:
        if not message.reply_to_message.from_user:
            return
        if message.reply_to_message.from_user.id != bot_id:
            return
        await luna.send_chat_action(message.chat.id, "typing")
        if not message.text:
            query = "Hello"
        else:
            query = message.text
        if len(query) > 50:
            return
        try:
            res = await getresp(query, message.from_user.id if message.from_user else 0)
            await asyncio.sleep(1)
        except Exception as e:
            res = str(e)
        await message.reply_text(res)
        await luna.send_chat_action(message.chat.id, "cancel")
    else:
        if message.text:
            query = message.text
            if len(query) > 50:
                return
            if re.search("[.|\n]{0,}[l|L][u|U][n|N][a|A][.|\n]{0,}", query):
                await luna.send_chat_action(message.chat.id, "typing")
                try:
                    res = await getresp(query, message.from_user.id if message.from_user else 0)
                    await asyncio.sleep(1)
                except Exception as e:
                    res = str(e)
                await message.reply_text(res)
                await luna.send_chat_action(message.chat.id, "cancel")


@luna.on_message(
    filters.private
    & ~filters.command("shutdown")
    & ~filters.command("help")
    & ~filters.edited
)
async def chatpm(_, message):
    if not message.text:
        return
    await luna.send_chat_action(message.chat.id, "typing")
    query = message.text
    if len(query) > 50:
        return
    try:
        res = await getresp(query, message.from_user.id if message.from_user else 0)
        await asyncio.sleep(1)
    except Exception as e:
        res = str(e)
    await message.reply_text(res)
    await luna.send_chat_action(message.chat.id, "cancel")

luna.start()

print(
    """

-----------------
| Luna Started! |
-----------------
"""
)
idle()
