from playwright.sync_api import sync_playwright
import psycopg2 

class Create_Dataset(): # Creating class that hepls to collect data
    def __init__(self, link, topic, length_of_data):
        self.link = link
        self.topic = topic
        self.length_of_data = length_of_data
    def save_to_db(self):
        like_count, retweet_count, comments_count, views = self._get_data(self.link)
        self._insert_to_psql(self.link, self.topic, like_count, retweet_count, comments_count, views)
    
    def _insert_to_psql(self,link,topic,like_count, reposts_count, comments_count, views):
        
        conn = psycopg2.connect(host='localhost', port=5432, database="dataset", user='postgres', password='postgres')
        cur = conn.cursor()
        for n in range(self.length_of_data):
            cur.execute(""" INSERT INTO Xinfo (link,topic, likes, repostscount, commentcount, views) VALUES (%s,%s, %s, %s, %s, %s)""",
                        (link,topic, like_count,reposts_count, comments_count, views))
        conn.commit()
        cur.close()
        conn.close()

    def _get_data(self,link):
            with sync_playwright() as p:
               browser = p.firefox.launch()
               page = browser.new_page()
               if link.startswith(('https://x.com/', 'http://x.com/')): 
                   page.goto(link)
                   page.wait_for_selector("[data-testid='like']")
                   page.wait_for_selector("[data-testid='reply']")
                   page.wait_for_selector("[data-testid='retweet']")
                   page.wait_for_selector('a[href*="analytics"]')
                   like_count = self._replace_vws_to_int(page.inner_text("[data-testid='like']"))
                   reply_count = self._replace_vws_to_int(page.inner_text("[data-testid='reply']"))
                   views = self._replace_vws_to_int(page.inner_text('a[href*="analytics"]'))
                   retweet_count = self._replace_vws_to_int(page.inner_text("[data-testid='retweet']"))
                   return like_count, retweet_count, reply_count, views
               else:
                   raise ValueError("Wrong type of link")
    def _replace_vws_to_int(self, views):
        text = views.replace("Views", "").strip()
        if text == "" or text =="-":
            return 0
        multiplier = 1
        if text.endswith("K"):
            multiplier = 1000
            text = text[:-1]
        elif text.endswith("M"):
            multiplier = 1_000_000
            text = text[:-1]
        elif text.endswith("B"):
            multiplier = 1_000_000_000
            text= text[:-1]

        text = text.replace(",", ".")
        try:
            return int(float(text) * multiplier)
        except:
            return 0 
        

