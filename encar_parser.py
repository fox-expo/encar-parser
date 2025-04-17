import asyncio
from playwright.async_api import async_playwright

async def parse_encar(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)

        await page.wait_for_selector(".title", timeout=30000)

        title = await page.locator(".title").inner_text()

        try:
            price = await page.locator(".price").inner_text()
        except:
            price = "Нет цены"

        try:
            vin = await page.locator(".carfax > div:nth-child(2)").inner_text()
        except:
            vin = "VIN не найден"

        specs = {}
        spec_items = await page.locator(".spec > ul > li").all()
        for item in spec_items:
            key = await item.locator(".label").inner_text()
            value = await item.locator(".text").inner_text()
            specs[key] = value

        images = []
        thumbs = await page.locator(".pic_thumb img").all()
        for img in thumbs:
            src = await img.get_attribute("src")
            if src:
                images.append(src)

        await browser.close()

        return {
            "Заголовок": title,
            "Цена": price,
            "VIN": vin,
            "Характеристики": specs,
            "Фотографии": images[:5]
        }

if __name__ == "__main__":
    test_url = "https://fem.encar.com/cars/detail/39394778"
    result = asyncio.run(parse_encar(test_url))
    for key, value in result.items():
        print(f"{key}: {value}")
