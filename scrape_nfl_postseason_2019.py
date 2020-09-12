from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import csv


def writecsv(iMin, iMax, lHeader):
  if lHeader == True:
    playoff_writer.writerow([gametypes[iMin].text.replace(chr(10), " ").title()])
  else:
    for i in range(iMin,iMax,1):
      cTime = []
      cAMPM = []
      cTZ = []  

      if gametimes[0].text != "FINAL":
        cTime = gametimes[0].find_elements_by_class_name('time')
        cAMPM = gametimes[0].find_elements_by_class_name('pm')
        cTZ = gametimes[0].find_elements_by_class_name('et')
        playoff_writer.writerow([cTime[0].text,cAMPM[0].text,cTZ[0].text,awayteams[i].text.capitalize(), hometeams[i].text.capitalize()])
      else:
        playoff_writer.writerow(["","","",awayteams[i].text.capitalize(), hometeams[i].text.capitalize()])
        


opts = Options()
opts.headless=True

browser = Chrome(options=opts)
browser.get('http://www.nfl.com/schedules/2019/POST')

schedules = browser.find_elements_by_class_name('schedules-table')

with open('c:/users/michael/nlfplayoffs_2020.csv', mode='w', newline='') as playoff_file:
  playoff_writer = csv.writer(playoff_file)

  for i in range(1,len(schedules)):
    
    gametypes = schedules[i].find_elements_by_class_name('schedules-list-date')
    gametimes = schedules[i].find_elements_by_class_name('list-matchup-row-time')

    for j in range(0,len(gametypes)):

      writecsv(j,j,True)

      awayteams = schedules[i].find_elements_by_class_name('team-name.away')
      hometeams = schedules[i].find_elements_by_class_name('team-name.home')

      if len(awayteams) == 4:  #Wild Card and Divisional round
        if(j == 0):
          writecsv(0,2,False)
        else:
          writecsv(2,4,False)
      elif len(awayteams) == 2: #Conference Finals
          writecsv(0,2,False)
      else: #ProBowl and Superbowl
          writecsv(0,1,False)

browser.close


