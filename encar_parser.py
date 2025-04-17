import asyncio
from playwright.async_api import async_playwright
import time

async def parse_encar(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        await page.wait_for_load_state("networkidle")

        # Заголовок
        try:
            title_elem = await page.locator('h2[data-testid="car-name"]').text_content()
            title = title_elem.strip() if title_elem else "Не найден"
        except:
            title = "Не найден"

        # Цена
        try:
            price_elem = await page.locator('strong.price').text_content()
            price = price_elem.strip() if price_elem else "Не указана"
        except:
            price = "Не указана"

        # Пробег и год выпуска
        characteristics = {}
        try:
            rows = await page.locator('dl.info-basic > div').all()
            for row in rows:
                label = await row.locator('dt').text_content()
                value = await row.locator('dd').text_content()
                if label and value:
                    characteristics[label.strip()] = value.strip()
        except:
            characteristics = {"Ошибка": "Не удалось считать характеристики"}

        # VIN
        try:
            vin_block = await page.locator("text=/VIN/i").element_handle()
            if vin_block:
                vin = await vin_block.evaluate("el => el.nextElementSibling?.textContent?.trim()")
            else:
                vin = "Не найден"
        except:
            vin = "Не найден"

        # Фотографии
        photos = []
        try:
            thumbs = await page.locator("div.swiper-slide img").all()
            for img in thumbs:
                src = await img.get_attribute("src")
                if src and "http" in src:
                    photos.append(src)
        except:
            photos = []

        await browser.close()

        return {
            "Заголовок": title,
            "Цена": price,
            "VIN": vin,
            "Характеристики": characteristics,
            "Фотографии": photos[:10]
        }

# Тест
if __name__ == "__main__":
    test_url = "https://fem.encar.com/cars/detail/39024513?listAdvType=share"
    result = asyncio.run(parse_encar(test_url))
    for key, value in result.items():
        print(f"{key}: {value}")
    time.sleep(300)
