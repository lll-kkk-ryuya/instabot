from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary
import os 
import time
import random
import numpy
import instaloader
import random

class InstagramBot:
    
    def __init__(self,username,password):
        self.loader = instaloader.Instaloader()
        self.loggedin = False
        self.username = username
        self.password = password
        self.base_url = "https://www.instagram.com"
        self.followersCount = 0
        self.followingCount = 0
        self.followedList = []
        self.doNotFollowList = []
        self.whitelist =[]
        self.CreateFiles()
        self.get_follow()


  ############# Chooser ###################

    def Choose(self):
        #The UI
        print("...............")
        choice = input("[1] Follow Followers\n[2] Unfollowed\nChoice:\t")
        if choice == "1":
            self.FollowFollowers()
        elif choice == "2":
            self.UnfolloedFollowed()
        elif choice == "q":
            return
        
        self.Choose()

        
  ############# Helper Methods ##############    
    def ConvertToNumber(self,text):
        #Convvert instagram's shorthand to a number
        if "万" in text:
            return int((float(text.replace("万","")))*10000)
        elif "m" in text:
            return int((float(text.replace("m","")))*1000000)
        else:
            return int(text)
        
    def Wait(self,min,max):
        # Pauses for random amount of time
        time.sleep(random.choice(numpy.arange(min,max,0.1)))
    
    def GotoUser(self,user):
        #Go to a user's page
        self.driver.get("{}/{}/".format(self.base_url,user))
        self.Wait(1,2)
        
    def UnfollowerUser(self,user):
        # Unfollows a user through their page
        self.Login()
        self.GetInfo()
        self.GotoUser(user)
        div = self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]")
        button = div.find_elements_by_xpath(".//button")
        if (button and button[0].text != "フォローする"):
            if (len(button) > 2):
                button[1].click()
            else:
                button[0].click()
            self.Wait(1,1.5)
            self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]/button[1]").click()
            
                                                
        
    def CreateFiles(self):
        #Creates files for user if they don't exist
        temp = open("[Followed][{}]".format(self.username),"a+")
        temp.close
        temp = open("[DoNotFollow][{}]".format(self.username),"a+")
        temp.close
        
    def ReadFliles(self):
        #Obtains previously followed useraname from file
        with open("[Followed][{}]".format(self.username),"r+") as flist:
            lines = flist.readlines()
            for line in lines :
                self.followedList.append(line.strip())
        with open("[DoNotFollow][{}]".format(self.username),"r+") as flist:
            lines = flist.readlines()
            for line in lines :
                self.doNotFollowList.append(line.strip())
                
    def AddFOllowedList(self,name):
        # Remove followed username from file
        with open("[Followed][{}]".format(self.username),"r+") as flist:
            temp = name.strip()+"\n"
            flist.write(temp)
        with open("[DoNotFollow][{}]".format(self.username),"r+") as flist:
            temp = name.strip()+"\n"
            flist.write(temp)        
    
    def RemFollowedList(self,name):
        #Remove followed username from file
        with open("[Followed][{}]".format(self.username),"r+") as flist:
            lines = flist.readlines()
        with open("[Followed][{}]".format(self.username),"r+") as flist:
            for line in lines:
                if line.strip() != name:
                    flist.write(line)
                    
    def get_followers(self):
        user = input("Account username:\t")
        self.loader.login(self.username, self.password)

        #指定したIDのprofileオブジェクトを作成
        profile = instaloader.Profile.from_username(self.loader.context, user)
        followers = []
            #指定したIDのフォロワーを全件取得
        for follower in profile.get_followers():
            followers.append(follower.username)
        return followers
    
    
    def get_follow(self):
        user = input("Account username:\t")
        self.loader.login(self.username, self.password)

        #指定したIDのprofileオブジェクトを作成
        profile = instaloader.Profile.from_username(self.loader.context, user)
        followers = profile.get_followees()
            #指定したIDのフォロワーを全件取得
        for follower in followers:
            print(follower.username)
            
        
        
      
        
    ########### Logging In ################
    
    def Login(self):
        self.driver = webdriver.Chrome()
        print("Logging In:{}".format(self.username))
        self.driver.get("{}/accounts/login".format(self.base_url))
        self.Wait(2,3)
        self.driver.find_element_by_name("username").send_keys(self.username)
        self.Wait(2,3)
        self.driver.find_element_by_name("password").send_keys(self.password)
        #self.driver.find_elements_by_xpath("//div[contains(text(),'Log In')]")[0].click()
        self.driver.find_element_by_xpath("//*[@id='loginForm']/div/div[3]").click()
        print("Logged In:{}".format(self.username))
        self.loggedin = True
        self.Wait(3,4)
        
    def GetInfo(self):
        #Gets followers & following amounts
        self.GotoUser(self.username)
        #Get number of follower
        temp = self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[2]/a/div/span").text
        self.followersCount = self.ConvertToNumber(temp)
        #Get number of following
        temp = self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[3]/a/div/span").text
        self.followingCount = self.ConvertToNumber(temp)
        print(self.followersCount,self.followingCount)
        self.ReadFliles()
        
        
     ################# Following Followers ###############
    
    def FollowFollowers(self):
        # Follows the followers of a user 
        # Gets username and number of followers to follow
        self.Login()
        self.GetInfo()
        user = input("Account username:\t")
        self.GotoUser(user)
        temp = self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[2]/a/div/span").text
        numoffolowers = self.ConvertToNumber(temp)
        amount = int(input("How many to follow? (Less than {})\t".format(numoffolowers)))
        while amount > numoffolowers:
            amount = int(input("How many to follow? (Less than {})\t".format(temp)))
        
        
        # Click followers tab and goes through the list one by one 
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[2]/a/div").click()
        i,k = 1,1
        while (k <= amount):
            self.Wait(1,1.5)
            currentUser = self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[2]/ul/div/li[{}]/div".format(i))
            button = currentUser.find_elements_by_xpath(".//button")
            name = currentUser.find_element_by_css_selector(".notranslate").text
            # If a strictly "Follow" button exist, it click it
            if (button) and (button[0].text == "フォローする"):
                self.Wait(10,15)
                button[0].click()
                self.AddFOllowedList(name) # Writes username to file
                print("[{}]{} followed {}".format(k,self.username,name))
                k += 1
            self.Wait(1,1.5)
            # Scroll down for the user to  be at the top of the tab
            self.driver.execute_script("arguments[0].scrollIntoView()", currentUser)
            i +=1
            
            
            
    def follow1(self):
        #Follow random follower of followy
        self.get_followers()
        random.shuffle(followers)
        self.GotoUser(user)
        temp = self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[2]/a/div/span").text
        numoffolowers = self.ConvertToNumber(temp)
        amount = int(input("How many to follow? (Less than {})\t".format(numoffolowers)))
        i,k = 1,1
        while (k <= amount):
            for parent_account in followers:
                self.Wait(10,15)
                self.GotoUser(parent_account)
                button = self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/button")
                if button.text == "フォローする":
                    self.Wait(1,1.3)
                    button.click()
                    print("[{}]{} followed {}".format(k,self.username,parent_account))
                    k += 1
                self.Wait(1,1.5)
                i += 1
                    
                
                # If a strictly "Follow" button exist, it click it

        
        
        
             
     
   
        
        
TestRuns = InstagramBot("_llll_kid_.xx_","Rima31243124")
