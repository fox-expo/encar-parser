import asyncio
from playwright.async_api import async_playwright
import time

async def parse_encar(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)

        # Ждём полной загрузки всей страницы
        await page.wait_for_load_state("networkidle", timeout=60000)

        # Печатаем весь HTML страницы — для диагностики
        print(await page.content())

        # Заголовок
        try:
            title = await page.locator(".title").inner_text()
        except:
            title = "Не удалось получить заголовок"

        # Цена
        try:
            price = await page.locator(".price").inner_text()
        except:
            price = "Нет цены"

        # VIN
        try:
            vin = await page.locator(".carfax > div:nth-child(2)").inner_text()
        except:
            vin = "VIN не найден"

        # Характеристики
        specs = {}
        try:
            spec_items = await page.locator(".spec > ul > li").all()
            for item in spec_items:
                key = await item.locator(".label").inner_text()
                value = await item.locator(".text").inner_text()
                specs[key] = value
        except:
            specs = {"Ошибка": "Не удалось получить характеристики"}

        # Фотографии
        images = []
        try:
            thumbs = await page.locator(".pic_thumb img").all()
            for img in thumbs:
                src = await img.get_attribute("src")
                if src:
                    images.append(src)
        except:
            images = []

        await browser.close()

        return {
            "Заголовок": title,
            "Цена": price,
            "VIN": vin,
            "Характеристики": specs,
            "Фотографии": images[:5]
        }

# Подставляем твою ссылку
if __name__ == "__main__":
    test_url = "https://fem.encar.com/cars/detail/39024513?listAdvType=share"
    result = asyncio.run(parse_encar(test_url))
    for key, value in result.items():
        print(f"{key}: {value}")

    # Добавим паузу, чтобы Render не завершил сразу
    time.sleep(300)
