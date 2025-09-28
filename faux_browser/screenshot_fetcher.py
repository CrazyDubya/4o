import asyncio
from pathlib import Path

from pyppeteer import launch

WHITELIST = [
    "https://example.com",
]

OUTPUT_DIR = Path("repository/screenshots")


async def fetch_screenshots() -> None:
    browser = await launch(headless=True, args=["--no-sandbox"])
    page = await browser.newPage()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for url in WHITELIST:
        await page.goto(url)
        domain = url.split("//", 1)[-1].split("/", 1)[0]
        await page.screenshot({"path": str(OUTPUT_DIR / f"{domain}.png")})
    await browser.close()


if __name__ == "__main__":
    asyncio.run(fetch_screenshots())
