import asyncio
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from config import Config
from initialization import initialize_uniparser, initialize_pymorphy
from analyzers import UniParserAnalyzer, PymorphyAnalyzer
from text_processor import TextProcessor
from bot import LinguisticBot

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is running")
    def log_message(self, format, *args):
        return  

def run_health_server():
    import os
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    logging.info(f"Вспомогательный веб-сервер запущен на порту {port}")
    server.serve_forever()

async def main():
    threading.Thread(target=run_health_server, daemon=True).start()
    
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
