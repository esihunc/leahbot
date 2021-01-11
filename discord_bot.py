import discord
from discord.ext import tasks,commands
import os
from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys


class chatbot(discord.Client):

    async def on_ready(self):
        game = discord.Game("버블파이터")
        await client.change_presence(status=discord.Status.online, activity=game)
        print("봇 활성화")
    
    async def on_message(self, message):
        if message.author.bot:
            return None
        msg = message.content.split()
        if message.content == "!test":
            channel = message.channel
            msg = "test message"
            await channel.send(msg)
            return None

        if message.content.startswith("!아레나"):
            msg = message.content.split(" ")
            channel = message.channel
            
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
            
            driver.get("http://bf.nexon.com/Rank/FastStart/List")
            
            usr = msg[1]
            elem = driver.find_element_by_id("searchName")
            elem.send_keys(usr)
            elem.send_keys(Keys.RETURN)
            posting = driver.find_element_by_xpath('//*[@id="form1"]/button')
            posting.click()
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            try:
                lank = soup.select_one(".block .board_list_rk .myL .num").get_text()
                print(lank)
                await channel.send(usr+"님의 아레나 순위는 "+lank+"위 입니다.")
            except:
                print("Not found")
                await channel.send("존재하지 않는 닉네임 혹은 이번 시즌에 아레나를 플레이하지 않은 유저 입니다.")
            driver.quit()
            return None

if __name__ == "__main__":
    client = chatbot()
    access_token = os.environ["BOT_TOKEN"]
    client.run(access_token)
