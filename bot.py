import logging
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

logging.basicConfig(level=logging.INFO)


class LinguisticBot:

    def __init__(self, token: str, text_processor):
        self.bot = Bot(
            token=token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self.dp = Dispatcher()
        self.processor = text_processor
        self._register_handlers()

    def _register_handlers(self) -> None:
        self.dp.message.register(self.command_start_handler, CommandStart())
        self.dp.message.register(self.text_analysis_handler)

    async def command_start_handler(self, message: Message) -> None:
        welcome_text = (
            f"Привет от команды Дениса, Юлии и Светлан, {html.bold(message.from_user.full_name)}! 👋\n\n"
            f"Отправь нам любое предложение, "
            f"и мы проведем его полный анализ с помощью "
            f"{html.code('UniParser')} и {html.code('pymorphy3')}."
        )
        await message.answer(welcome_text)

    async def text_analysis_handler(self, message: Message) -> None:
        if not message.text:
            await message.answer("Отправьте текстовое сообщение, глупышка ;)")
            return

        await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

        try:
            result = self.processor.analyze_sentence(message.text)
            response_lines = [f"📊 {html.bold('Итоговый результат анализа:')}\n"]
            
            for i, item in enumerate(result["results"], start=1):
                response_lines.append(
                    f"{i}. {html.underline(item['word'])}\n"
                    f"   └ Лемма: {html.italic(item['lemma'])}\n"
                    f"   └ Грамматика: {item['grammar']}\n"
                    f"   └ Анализатор: {html.code(item['analyzer'])}\n"
                )
            
            response_lines.append(f"{html.bold('📈 Статистика:')}")
            response_lines.append(f"Всего токенов: {result['total']}")
            response_lines.append(f"Использовано UniParser: {result['uniparser_count']}")
            response_lines.append(f"Использовано pymorphy3: {result['pymorphy_count']}")
            
            full_response = "\n".join(response_lines)
            await message.answer(full_response)

        except Exception as e:
            logging.error(f"Ошибка при анализе текста: {e}", exc_info=True)
            await message.answer("❌ Произошла ошибка во время лингвистического анализа.")

    async def start(self) -> None:
        logging.info("Процесс успешно запущен...")
        await self.dp.start_polling(self.bot)
