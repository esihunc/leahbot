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
        self.notice.start()

    global last_notice 
    last_notice = ""
    global last_notice2 
    last_notice2 = ""

    @tasks.loop(seconds=30)
    async def notice(self):
        global last_notice
        global last_notice2
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('lang=ko_KR')
        chromedriver_path = "chromedriver"
        driver = webdriver.Chrome(os.path.join(os.getcwd(),chromedriver_path),options=options)
        driver.get('http://bf.nexon.com/News/Update')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        update_notice = soup.select_one(".board_list .subject").get_text()
        link = 'http://bf.nexon.com'+soup.select(".board_list .subject")[0].find_all("a")[1].attrs['href']
        if last_notice != update_notice:
            last_notice = update_notice
            print(update_notice)
            #await client.get_guild(797378145744584746).get_channel(797381625247825940).send("새로운 패치를 발견했습니다.\n"+update_notice+'\n'+link)
            embed=discord.Embed(title="패치노트 보러가기 (클릭)", url=link, description=update_notice,color=0x3de2ff)
            await client.get_guild(797378145744584746).get_channel(797381625247825940).send("새로운 업데이트 내역이 추가되었습니다.", embed=embed) # embed와 메시지를 함께 보내고 싶으시면 이렇게 사용하시면 됩니다.
            time.sleep(1)
        else:
            print("Not found new notice")
            #await client.get_guild(797378145744584746).get_channel(797381625247825940).send("Not found new notice")

        driver.get('http://bf.nexon.com/News/Notice/List')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        update_notice = soup.select_one(".board_list .subject").get_text()
        link = 'http://bf.nexon.com'+soup.select(".board_list .subject")[0].find_all("a")[0].attrs['href']
        if last_notice2 != update_notice:
            last_notice2 = update_notice
            print(update_notice)
            #await client.get_guild(797378145744584746).get_channel(797381625247825940).send("새로운 패치를 발견했습니다.\n"+update_notice+'\n'+link)
            embed=discord.Embed(title="공지사항 보러가기 (클릭)", url=link, description=update_notice,color=0x3de2ff)
            await client.get_guild(797378145744584746).get_channel(797381625247825940).send("새로운 공지사항 내역이 추가되었습니다.", embed=embed) # embed와 메시지를 함께 보내고 싶으시면 이렇게 사용하시면 됩니다.
            time.sleep(1)
        else:
            print("Not found new notice")
            #await client.get_guild(797378145744584746).get_channel(797381625247825940).send("Not found new notice")
        driver.quit()
    
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
            options.add_argument('headless')
            options.add_argument('lang=ko_KR')
            chromedriver_path = "chromedriver"
            driver = webdriver.Chrome(os.path.join(os.getcwd(),chromedriver_path),options=options)
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
