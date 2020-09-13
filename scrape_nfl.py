from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
import csv
from datetime import datetime

iWeek1 = int(input("Enter start week: "))
iWeek2 = int(input("Enter end week: "))

iWeek2 += 1


browser = webdriver.Chrome(ChromeDriverManager().install())

from selenium.webdriver.chrome.options import Options

opts = Options()
opts.headless=True

with open('c:/users/michael/nlf_2020.csv', mode='w', newline='') as nfl_schedule:
   schedule_writer = csv.writer(nfl_schedule)

   for i in range(iWeek1,iWeek2):
      schedule_writer.writerow(["Week",i])
      website = "https://www.nfl.com/schedules/2020/REG" + str(i)
      browser.get(website)
      gamedays = WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "nfl-o-matchup-group")))
      awayteam = ""
      for j in range(0,len(gamedays)):
         game_on = gamedays[j].find_elements_by_class_name('d3-o-section-title')
         games = gamedays[j].find_elements_by_class_name('nfl-c-matchup-strip')
         for game_day in game_on:
            for game in games:
               gametime = game.find_elements_by_class_name('nfl-c-matchup-strip__date-time')
               teams = game.find_elements_by_class_name('nfl-c-matchup-strip__team-fullname')
   
               for game_at in gametime:
                  k = 0  
                  for matchup in teams:
                     k += 1
                     if(k == 1):
                        awayteam = matchup.text
                     if(k == 2):
                        try:
                           datetime_object = datetime.strptime(game_day.text[:-2] + ' 2020', '%A, %B %d %Y')
                        except:
                           datetime_object = "not a date: " + game_day.text
                           
                        schedule_writer.writerow([datetime_object,game_at.text,awayteam, matchup.text])              
                       
      browser.close
      browser.quit()


