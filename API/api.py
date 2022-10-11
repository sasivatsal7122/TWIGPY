from fastapi import FastAPI
import datetime

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException 
from bs4 import BeautifulSoup
import json


from driver_util import start_and_load_cookies

app = FastAPI()


driver = start_and_load_cookies()

@app.get("/")
async def read_root():
    return {"Message": "Hey There User !"}


@app.get("/tw/")
async def get_twitter(username: str):
    
    master_dict = dict()
    timestamp = str(datetime.datetime.now())
    
    driver.get(f"https://twitter.com/{username}")

    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "script[data-testid='UserProfileSchema-test']")))
    
    except TimeoutException:
        return {"Error" : "Couldn't Fetch Requested data please try again"}
    
    else:
        html_source = driver.page_source
        sourcedata = html_source.encode('utf-8')
        
        global soup
        soup = BeautifulSoup( sourcedata , 'html.parser')
            
        js = soup.find("script",{"data-testid":"UserProfileSchema-test"}).text

        js = js.replace("\n","")
        res = json.loads(js)

        user_id = res['author']['identifier']
        screenname = res['author']['additionalName']
        try:
            name = res['author']['givenName']
        except:
            name = "NULL"
        followers_count = res['author']['interactionStatistic'][0]['userInteractionCount']
        following_count = res['author']['interactionStatistic'][1]['userInteractionCount']
        tweet_count = res['author']['interactionStatistic'][2]['userInteractionCount']
        try:
            user_bio = res['author']['description']
            if not user_bio:
                user_bio = "NULL"
        except:
            user_bio = "NULL"
        try:
            bio_link = res['relatedLink'][1]
        except:
            bio_link = "NULL"
        date_joined = res['dateCreated']
        try:
            location = res['author']['homeLocation']['name']
            if not location:
                location = "NULL"
        except:
            location = "NULL"

        is_private = 'False'
        if soup.find("div",{"class":"css-901oao r-1nao33i r-37j5jr r-1yjpyg1 r-1vr29t4 r-ueyrd6 r-5oul0u r-bcqeeo r-fdjqy7 r-qvutc0"}):
            is_private = 'True'


        is_verified = 'False'
        if soup.find("svg",{"aria-label":"Verified account"}):
            is_verified = 'True'

        is_bussiness_acc = 'False' ; bussiness_sector = "NULL"
        if soup.find("span",{"data-testid":"UserProfessionalCategory"}):
            __ = soup.find("span",{"data-testid":"UserProfessionalCategory"})
            bussiness_sector = __.find("span",{'class':'css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0'}).text
            is_bussiness_acc = 'True'

        data = {
            
            "User ID" : user_id,
            "Name" : name,
            "Screen Name" : screenname,
            "Following" : following_count,
            "Followers" : followers_count,
            "Tweets" : tweet_count,
            "bio" : user_bio,
            "Location" : location,
            "URL" : bio_link,
            "Verified" : is_verified,
            "Private" : is_private,
            "is_bussiness_account" : is_bussiness_acc,
            "bussiness_sector" : bussiness_sector,
            "Joined" : date_joined
        }
        master_dictt = dict()
        master_dict.update({screenname:data})
        master_dictt.update({"REQUEST UTC" : timestamp})
        master_dictt.update({"Response" : [master_dict]})
        return master_dictt