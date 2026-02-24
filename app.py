from fastapi import FastAPI
from pydantic import BaseModel
from playwright.async_api import async_playwright

app = FastAPI()


class BlogPost(BaseModel):
    title: str
    content: str


@app.get("/")
def health():
    return {"status": "running"}


@app.post("/write-blog")
async def write_blog(data: BlogPost):

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True
        )

        context = await browser.new_context(
            storage_state="naver_session.json"
        )

        page = await context.new_page()

        # 블로그 글쓰기 페이지
        await page.goto(
            "https://blog.naver.com/PostWriteForm.naver"
        )

        await page.wait_for_timeout(5000)

        # 제목 입력 (selector는 실제 변경될 수 있음)
        await page.fill(
            "textarea.se-textarea",
            data.title
        )

        await page.wait_for_timeout(2000)

        # 본문 입력
        await page.keyboard.type(data.content)

        await page.wait_for_timeout(2000)

        # 발행 버튼 클릭 (selector 변경 가능)
        await page.click("button.publish_btn")

        await page.wait_for_timeout(5000)

        await browser.close()

    return {
        "result": "posted"
    }
