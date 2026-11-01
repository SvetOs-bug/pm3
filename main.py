import asyncio
import logging
from config import Config
from initialization import initialize_uniparser, initialize_pymorphy
from analyzers import UniParserAnalyzer, PymorphyAnalyzer
from text_processor import TextProcessor
from bot import LinguisticBot


async def main():
    uniparser = UniParserAnalyzer(initialize_uniparser())
    pymorphy = PymorphyAnalyzer(initialize_pymorphy())

    processor = TextProcessor(uniparser, pymorphy)

    telegram_bot = LinguisticBot(
        token=Config.BOT_TOKEN,
        text_processor=processor
    )

    await telegram_bot.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот успешно остановлен.")
