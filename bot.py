from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
from selenium.webdriver.common.action_chains import ActionChains
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import re

BLACKLIST_WORDS=["网红","论文","涨粉","复刻","奢侈","增粉"]

class instaBot:

    def __init__(self, name, key):
        self.password=key
        self.username=name
        self.driver=webdriver.Firefox()
        self.driver.implicitly_wait(25)
        self. chatbot = ChatBot("instagramBot",read_only=True)
        self.chatbot.set_trainer(ListTrainer)

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")

        enter_name=self.driver.find_element_by_xpath("//input[@name='username']")

        enter_password = self.driver.find_element_by_xpath("//input[@name='password']")

        enter_name.clear()
        enter_password.clear()

        enter_name.send_keys(self.username)
        enter_password.send_keys(self.password)

        enter_password.send_keys(Keys.RETURN)
        time.sleep(4)

    def search(self, search_query):
        '''open a photo of that specific tag and return the number of photo under that tag'''
        search_box=self.driver.find_element_by_xpath("//input[@type='text']")
        search_box.send_keys(search_query)
        time.sleep(3)
        search_box.send_keys(Keys.ARROW_DOWN)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        number = self.driver.find_element_by_xpath("//span[contains(@class, 'g47SY')]").text
        result = int(''.join(number.split(',')))

        continue_pics = self.driver.find_element_by_xpath("//a//*[@role='button']")
        time.sleep(2)
        action = ActionChains(self.driver)
        action.move_to_element(continue_pics).perform()

        action.click().perform()
        time.sleep(3)
        print(type(result),result)

    def grab_comment(self):
        user_comment=self.driver.find_element_by_xpath("//*[contains(@class, 'C4VMK')]/span").text
        user_comment=re.sub("#\w*|@\w*","",user_comment)
        return user_comment


    def like_photo(self):

        like_button = self.driver.find_element_by_xpath("//*[contains(@class, 'HeartOpen')]")

        like_button.send_keys(Keys.RETURN)
        time.sleep(2)

    def send_comment(self,comment):
        try:

            comment_button = self.driver.find_element_by_xpath("//span[contains(@class, 'Comment')]")
            comment_button.send_keys(Keys.RETURN)
        except NoSuchElementException:
            print("can't load comment_button")

        try:
            text_area=self.driver.find_element_by_xpath("//textarea")
            text_area.click()
            text_area.send_keys(comment)
            text_area.send_keys(Keys.RETURN)
        except StaleElementReferenceException:
            pass



    def post_comment(self):

        user_comment=self.grab_comment()

        response = str(self.chatbot.get_response(user_comment))
        print(response)
        self.send_comment(response)


    def next_photo(self):
        next_button = self.driver.find_element_by_xpath("//a[contains(@class, 'RightPaginationArrow')]")
        next_button.send_keys(Keys.RETURN)

    def closerDriver(self):
        self.driver.close()

    def find_follower(self):
        self.driver.get("https://www.instagram.com/{}".format(self.username))

        follower_button = self.driver.find_element_by_xpath("//a[contains(@href, 'follower')]")
        follower_number = follower_button.find_element_by_tag_name("span").text
        result = int(follower_number)
        follower_button.send_keys(Keys.RETURN)
        print(result)
        time.sleep(2)
        return result

    def get_all_followers(self,num):
        '''<iframe name="f22dd05976f1a5c" '''

        num_of_page=set()
        blacklist=set()  #"//div[@class='foB1c']"
        scr1 = self.driver.find_element_by_xpath('//body/div[3]/div/div[2]/div/div[2]')

        while len(num_of_page) + len(blacklist) <= 24:
            page = self.driver.find_element_by_xpath("//div[contains(@class,'_1xe_U')]")
            hrefs = page.find_elements_by_xpath("//div[@class='foB1c']")

            for elem in hrefs:
                header=elem.find_element_by_class_name("Um26G").text
                link = elem.find_element_by_tag_name("a").get_attribute('href')
                for i in BLACKLIST_WORDS:
                    if i in header:
                        blacklist.add(link)
                else:
                    num_of_page.add(link)

            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scr1)
            time.sleep(1)
            print(len(num_of_page))
        return blacklist,num_of_page

    def blacklist(self,link):

        self.driver.get(link)
        time.sleep(1)
        button=self.driver.find_element_by_class_name("dCJp8")
        button.click()


        black_button = self.driver.find_element_by_xpath("//div[@class='mt3GC']/button[2]")
        black_button.click()

        make_sure=self.driver.find_element_by_class_name('bIiDR')
        make_sure.click()

        close_button=self.driver.find_element_by_xpath("//button[contains(@class,'HoLwm')]")
        close_button.click()
        time.sleep(2)

    def check_header(self,link):
        self.driver.get(link)
        try:
            introduction = self.driver.find_element_by_xpath("//div[@class='-vDIg']/span")

            for i in BLACKLIST_WORDS:
                if i in introduction.text:
                    return True
            return False
        except NoSuchElementException:
            return False

    def filter_followers(self,list1,list2):
        blacklist=list1
        raw_list=list2
        for i in blacklist:
            self.blacklist(i)
        for i in raw_list:
            if (self.check_header(i)):
                self.blacklist(i)

if __name__=="__main__":
    insta1=instaBot('lindashuuu', 'yanglu158')
    insta1.login()
    # insta1.blacklist("https://www.instagram.com/vivi2017423/")



    # insta1.search("food")
    # for i in range(10):
    #     insta1.like_photo()
    #     insta1.post_comment()
    #     insta1.next_photo()
    #     time.sleep(3)

    follow_num=insta1.find_follower()
    blist,raw_list=insta1.get_all_followers(follow_num)
    print(len(blist),len(raw_list))
    insta1.filter_followers(blist,raw_list)












