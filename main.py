from asyncio import run

from handlers import user_commands
from handlers.interests import interests_messages
from handlers.courses import courses_messages

from callbacks import user_callbacks

from constats import BOT, DP


async def main():
    bot = BOT
    dp = DP

    await bot.delete_webhook(drop_pending_updates=True)

    dp.include_routers(
        user_commands.router,
        interests_messages.router,
        courses_messages.router,
        user_callbacks.router,
    )

    await DP.start_polling(bot)


if __name__ == "__main__":
    run(main())