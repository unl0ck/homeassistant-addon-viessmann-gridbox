import os
import time
import logging
import asyncio
from dotenv import load_dotenv
from playwright.async_api import async_playwright
import re

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s - %(message)s")

class GridboxMonitor:
    def __init__(self):
        load_dotenv()
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        if not self.username or not self.password:
            raise ValueError("❌ USERNAME oder PASSWORD nicht in .env gefunden")
        self.auth_file = "auth.json"
        self.screenshot_path = "live_view.png"
        self.traffic_log_path = "api_responses.txt"
    
    async def get_browser(self, playwright):
        browser = await playwright.chromium.launch(channel="msedge", headless=True)
        return browser

    async def save_session(self):
        async with async_playwright() as p:
            browser = await self.get_browser(p)
            context = await browser.new_context()
            page = await context.new_page()

            logging.info("🔐 Navigiere zur Login-Seite …")
            await page.goto("https://mygridbox.viessmann.com/login")
            await page.fill('input[type="email"]', self.username)
            await page.fill('input[type="password"]', self.password)
            await page.click('input[type="submit"]')

            logging.info("⏳ Warte auf Dashboard nach Login …")
            await page.wait_for_url("https://mygridbox.viessmann.com/", timeout=15000)

            await context.storage_state(path=self.auth_file)
            logging.info(f"✅ Session gespeichert in {self.auth_file}")

            await browser.close()

    async def monitor_live_view(self):
        async with async_playwright() as p:
            browser = await self.get_browser(p)
            context = await browser.new_context(storage_state=self.auth_file)
            page = await context.new_page()

            api_data = []
            
            async def log_response(response):
                try:
                    url = response.url
                    # Nur die gewünschten API-Endpunkte aufzeichnen
                    if (re.match(r'https://api\.gridx\.de/systems/.*/live', url) or 
                        re.match(r'https://api\.gridx\.de/systems/.*/historical', url)):
                        
                        body = await response.text()
                        api_data.append(f"=== {response.request.method} {url} ===")
                        api_data.append(f"Status: {response.status}")
                        api_data.append(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                        api_data.append(f"Response Body:")
                        api_data.append(body)
                        api_data.append("=" * 80)
                        api_data.append("")
                        
                        logging.info(f"📊 API-Daten aufgezeichnet: {url}")
                        
                except Exception as e:
                    logging.error(f"Fehler beim Aufzeichnen von {response.url}: {e}")

            page.on("response", log_response)

            logging.info("🌐 Rufe Live-View auf …")
            await page.goto("https://mygridbox.viessmann.com/live-view", wait_until="networkidle")
            await asyncio.sleep(5)  # Etwas länger warten für API-Calls

            await page.screenshot(path=self.screenshot_path)
            logging.info(f"📸 Screenshot gespeichert: {self.screenshot_path}")

            if api_data:
                with open(self.traffic_log_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(api_data))
                logging.info(f"📄 API-Daten gespeichert: {self.traffic_log_path}")
            else:
                logging.warning("⚠️ Keine API-Daten von den gewünschten Endpunkten gefunden")

            await browser.close()

    async def run(self):
        if not os.path.exists(self.auth_file):
            logging.info("Keine gespeicherte Session gefunden – Login wird durchgeführt …")
            await self.save_session()
        else:
            logging.info("Gefundene Session wird verwendet …")
        await self.monitor_live_view()

if __name__ == "__main__":
    bot = GridboxMonitor()
    asyncio.run(bot.run())