from __future__ import annotations

import logging
from typing import Any, Awaitable, Callable

try:
    from telegram import Bot, Update
    from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
except Exception:  # pragma: no cover
    Bot = None
    Update = Any  # type: ignore
    Application = None
    CommandHandler = None
    ContextTypes = Any  # type: ignore
    MessageHandler = None
    filters = None


logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self, token: str, command_handler: Callable[..., Awaitable[dict[str, Any]]]) -> None:
        self.token = token
        self.command_handler = command_handler
        self.bot = Bot(token) if Bot and token else None
        self.application = None

    @property
    def enabled(self) -> bool:
        return bool(self.token and self.bot and Application)

    async def start(self) -> None:
        if not self.enabled:
            logger.info("Telegram bot disabled (missing token or library)")
            return

        self.application = Application.builder().token(self.token).build()
        self.application.add_handler(CommandHandler("start", self.cmd_start))
        self.application.add_handler(CommandHandler("help", self.cmd_help))
        self.application.add_handler(CommandHandler("status", self.cmd_status))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.application.add_handler(MessageHandler(filters.VOICE, self.handle_voice))

        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        logger.info("Telegram bot started")

    async def stop(self) -> None:
        if self.application:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Hello. I am your AI assistant. Send text or voice commands.")

    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Try: 'Send email to ...', 'Open Chrome', 'Weather in Mumbai'.")

    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("System is online.")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_id = str(update.effective_user.id)
        chat_id = str(update.effective_chat.id)
        text = update.message.text
        result = await self.command_handler(user_id=user_id, command=text, source="telegram", chat_id=chat_id)
        await update.message.reply_text(result.get("response_text", "Done"))

    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_id = str(update.effective_user.id)
        chat_id = str(update.effective_chat.id)
        result = await self.command_handler(user_id=user_id, command="", source="telegram", chat_id=chat_id)
        await update.message.reply_text(result.get("response_text", "Voice received"))

    async def send_message(self, chat_id: str, text: str) -> None:
        if not self.bot:
            return
        await self.bot.send_message(chat_id=chat_id, text=text)

    async def send_notification(self, chat_id: str, title: str, body: str) -> None:
        if not self.bot:
            return
        await self.bot.send_message(chat_id=chat_id, text=f"{title}\n\n{body}")
