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
from chromedriver_py import binary_path

#to get the user home dir
import os

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

svc = webdriver.ChromeService(executable_path=binary_path)
browser = webdriver.Chrome(service=svc)

#get the home directory
userHome = os.path.expanduser('~')
csvFile = userHome + "/nfl_" + str(iCurrentYear) + ".csv"

with open(csvFile, mode='w', newline='') as nfl_schedule:
   schedule_writer = csv.writer(nfl_schedule)

   #Always add 1 because the end value is NOT included in the range
   for i in range(ifromWeek,itoWeek + 1):
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
      tdatetime = ''
      
      for j in range(0,len(gamedays)):
        #the date
        all_game_days = gamedays[j].find_elements(By.CLASS_NAME, "d3-o-section-title")
      
        #the games on a gameday
        all_games_on_gameday = gamedays[j].find_elements(By.CLASS_NAME,'nfl-c-matchup-strip')
         
        for game_day in all_game_days:
            #breakpoint()

            for game in all_games_on_gameday:
                thisGame = game.find_element(By.CLASS_NAME,'nfl-c-matchup-strip__left-area')
                GameNode = game.find_element(By.CLASS_NAME,'nfl-c-matchup-strip__game')
                thisTeams = GameNode.find_elements(By.CLASS_NAME,'nfl-c-matchup-strip__team-fullname')
                
                if(all_game_days[0].text == 'GAMES NOT YET SCHEDULED'):
                    thisTime = ''
                    tdatetime = 'TBD'
                else:    
                    thisTime = game.find_element(By.CLASS_NAME,'nfl-c-matchup-strip__date-time').text
                    try:
                        #transform something like THURSDAY, SEPTEMBER 10TH into a date object
                        cYear = ' ' + str(iCurrentYear)                            
                        tdatetime = datetime.strptime(all_game_days[0].text[:-2] + cYear, '%A, %B %d %Y')

                        #Adjust the year. The season starts in September of the current year and ends in
                        #February of the following yeasr. Hence a month of 1 or 2 must be next year
                        #I couldn't find a year on the website, that would be easy
                        if(tdatetime.month < 3):
                            tdatetime = tdatetime.replace(year = tdatetime.year + 1)
                    except:
                        tdatetime = "not a date: " + all_game_days[0].text
                            
                schedule_writer.writerow([tdatetime,thisTime,thisTeams[0].text, thisTeams[1].text])              

                          
browser.close
browser.quit()




