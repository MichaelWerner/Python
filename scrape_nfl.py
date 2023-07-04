#Config file
import scrape_nfl_config

#assign config variables to local variables
iWeeks = scrape_nfl_config.iWeeks
iCurrentYear =  scrape_nfl_config.iCurrentYear


iNextYear =  iCurrentYear + 1


#needed to start a browser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

#to get the user home dir
from pathlib import Path

#needed to write a csv file
import csv

#needed to parse a date string
from datetime import datetime

#needed for command line arguments
import argparse

#parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f','--fromWeek', type=int, help='positive integer value to get the from week')
parser.add_argument('-t','--toWeek', type=int, help='positive integer value to get the to week')

args = parser.parse_args()

#check if arguments are available, ask for user input if not
if(args.fromWeek):
   ifromWeek = args.fromWeek
   itoWeek = args.fromWeek
else:   
   ifromWeek = int(input("Enter start week: "))
   itoWeek = int(input("Enter end week: "))

if(args.toWeek):
   itoWeek = args.toWeek

itoWeek += 1

#start the browser with options
browser = webdriver.Chrome(ChromeDriverManager().install())
opts = Options()
opts.headless=True

#get the home directory
userHome = str(Path.home())
csvFile = userHome + "/nfl_" + str(iCurrentYear) + ".csv"

with open(csvFile, mode='w', newline='') as nfl_schedule:
   schedule_writer = csv.writer(nfl_schedule)

   for i in range(ifromWeek,itoWeek):
      schedule_writer.writerow(["Week",i])
      
      if(i <= 18):
         website = "https://www.nfl.com/schedules/" + str(iCurrentYear) + "/REG" + str(i)
      else:
         #for the post season this script is called with week 19, 20, and so on. The NFL start with 1 again
         #so some basic math is needed
         website = "https://www.nfl.com/schedules/" + str(iCurrentYear) + "/POST" + str(i-iWeeks)
         
      browser.get(website)
      
      #the different game days
      gamedays = WebDriverWait(browser, 60).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "nfl-o-matchup-group")))
      awayteam = ""
      
      for j in range(0,len(gamedays)):
         #the date
         game_on = gamedays[j].find_elements_by_class_name('d3-o-section-title')
      
         #the games on a gameday
         games = gamedays[j].find_elements_by_class_name('nfl-c-matchup-strip')
         #games_unscheduled = gamedays[j].find_elements_by_class_name('nfl-c-matchup-strip--pre-game')
         #games.extend(games_unscheduled)
         
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
                           #transform something like THURSDAY, SEPTEMBER 10TH into a date object
                           #I have to calculate the year because there is none on the website
                           #Usually week 16 is still in the current year
                           if(i<17):
                              cYear = ' ' + str(iCurrentYear)
                           else:
                              cYear = ' ' + str(iNextYear)   
                           tdatetime = datetime.strptime(game_day.text[:-2] + cYear, '%A, %B %d %Y')
                        except:
                           tdatetime = "not a date: " + game_day.text
                           
                        schedule_writer.writerow([tdatetime,game_at.text,awayteam, matchup.text])              
                          
browser.close
browser.quit()


