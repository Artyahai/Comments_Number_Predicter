from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
import asyncio
import psycopg2 

conn = psycopg2.connect("")
async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        page = await browser.new_page()
        await page.goto("https://x.com/BBCWorld/status/2019429088679628925")
        await page.wait_for_selector("[data-testid='like']")
        await page.wait_for_selector("[data-testid='reply']")
        likes = await page.inner_text("[data-testid=like]")
        replies = await page.inner_text("[data-testid=reply]")
        print(f"Replies: {replies} \n Likes: {likes}")
        await page.screenshot(path="experiments/whh.png")
        await page.title( )
        await browser.close()


asyncio.run(main())              

class Create_Dataset(): # Creating class that hepls to collect data
    def __init__(self, link, topic, length_of_data):
        self.link = link
        self.topic = topic
        self.length_of_data = length_of_data
    def save_to_db(self):
        like_count, reply_count, comments_count = _get_data(self.link)
        

    def _get_data(link):
        with sync_playwright() as p:
            browser = p.firefox.launch()
            page = browser.new_page()
            if link.startswith('https://x.com/', 'http://x.com/'): 
                page.goto(link)
                page.wait_for_selector("[data-testid='like']")
                page.wait_for_selector("[data-testid='reply']")
                page.wait_for_selector("[data-testid='retweet']")
                like_count = page.inner_text("[data-testid='like']")
                reply_count = page.inner_text("[data-testid='reply']")
                comments_count = page.inner_text("[data-testid='retweet']")
                return like_count, comments_count, reply_count
            else:
                raise ValueError("Wrong type of link")
            
            
            
            


        
