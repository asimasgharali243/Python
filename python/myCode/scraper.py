import asyncio
import random
from playwright.async_api import async_playwright

async def amazon_scraper(search_term, max_results=5):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent=random.choice(user_agents),
            viewport={"width": 1280, "height": 800},
            locale="en-US"
        )
        page = await context.new_page()

        await page.goto("https://www.amazon.com", timeout=60000, wait_until="domcontentloaded")
        await page.wait_for_selector("input#twotabsearchtextbox", timeout=60000)

        await page.fill("input#twotabsearchtextbox", search_term)
        await page.press("input#twotabsearchtextbox", "Enter")

        await page.wait_for_selector("div.s-main-slot div[data-component-type='s-search-result']", timeout=60000)

        # Scroll multiple times to load all product details
        for _ in range(3):
            await page.mouse.wheel(0, 2000)
            await page.wait_for_timeout(1500)

        items = []
        products = await page.query_selector_all("div.s-main-slot div[data-component-type='s-search-result']")

        for product in products[:max_results]:
            # Title with multiple fallbacks
            title_el = await product.query_selector("h2 a span")
            if not title_el:
                title_el = await product.query_selector("h2 a")
            if not title_el:
                title_el = await product.query_selector("img.s-image")  # fallback: image alt
            title = await title_el.inner_text() if title_el else "No title"

            # Image
            image_el = await product.query_selector("img.s-image")
            image = await image_el.get_attribute("src") if image_el else "No image"

            price_el = await product.query_selector("span.a-price > span.a-offscreen")
            price = await price_el.inner_text() if price_el else "No price"

            rating_el = await product.query_selector("span.a-icon-alt")
            rating = await rating_el.inner_text() if rating_el else "No rating"

            items.append({
                "title": title.strip(),
                "price": price.strip(),
                "rating": rating.strip(),
                "image": image
            })

        await browser.close()
        return items


if __name__ == "__main__":
    results = asyncio.run(amazon_scraper("laptop", max_results=5))
    for idx, r in enumerate(results, start=1):
        print(f"{idx}. {r['title']} | {r['price']} | {r['rating']}")
        print(f"   🖼 Image: {r['image']}")
