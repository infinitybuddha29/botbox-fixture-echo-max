"""botdepo fixture: minimal maxapi echo bot for MAX. Happy-path acceptance target."""
import asyncio
import logging
import os

from maxapi import Bot, Dispatcher, F
from maxapi.filters.command import CommandStart
from maxapi.types import BotStarted, MessageCreated

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# botdepo passes the token as BOT_TOKEN; maxapi would otherwise look for MAX_BOT_TOKEN.
bot = Bot(token=os.environ["BOT_TOKEN"])
dp = Dispatcher()


@dp.bot_started()
async def bot_started(event: BotStarted) -> None:
    await bot.send_message(chat_id=event.chat_id, text="botdepo fixture is alive. Send me anything and I'll echo it.")


@dp.message_created(CommandStart())
async def start(event: MessageCreated) -> None:
    await event.message.answer("botdepo fixture is alive. Send me anything and I'll echo it.")


@dp.message_created(F.message.body.text)
async def echo(event: MessageCreated) -> None:
    await event.message.answer(event.message.body.text)


async def main() -> None:
    me = await bot.get_me()
    logging.info("starting as %s (@%s)", me.first_name, me.username)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
