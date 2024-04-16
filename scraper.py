import requests
import selenium
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


username = input("Please enter a valid 8a.nu username:")
password = input("Please enter a valid 8a.nu password:")


website = "https://www.8a.nu"
ondra_statistics_sport = "https://www.8a.nu/api/users/adam-ondra/statistics/sportclimbing"
ondra_statistics_boulder = "https://www.8a.nu/api/users/adam-ondra/statistics/bouldering"

webdriver = webdriver.Chrome()
actions = ActionChains(webdriver)

webdriver.get(website)
login_button = webdriver.find_elements(By.XPATH, "//*[contains(text(), 'Log in')]")[0]
actions.move_to_element(login_button).click().perform()

webdriver.find_element(By.ID, "username").send_keys(username)
webdriver.find_element(By.ID, "password").send_keys(password)
webdriver.find_element(By.ID, "kc-login").click()

webdriver.implicitly_wait(2)



webdriver.get(ondra_statistics_sport)
number_of_ascents_sport = json.loads(webdriver.find_elements(By.TAG_NAME, "pre")[0].text)['ascentStatistics']['totalAscents']

webdriver.get(ondra_statistics_boulder)
number_of_ascents_boulder = json.loads(webdriver.find_elements(By.TAG_NAME, "pre")[0].text)['ascentStatistics']['totalAscents']


sport = "https://www.8a.nu/unificationAPI/ascent/v1/web/users/adam-ondra/ascents?category=sportclimbing&pageIndex=0&pageSize=" + str(number_of_ascents_sport) + "&sortField=grade_desc&timeFilter=0&gradeFilter=0&typeFilter=&includeProjects=false&searchQuery=&showRepeats=false&showDuplicates=false"
webdriver.get(sport)
ascents_sport = json.loads(webdriver.find_elements(By.TAG_NAME, "pre")[0].text)

boulder = "https://www.8a.nu/unificationAPI/ascent/v1/web/users/adam-ondra/ascents?category=bouldering&pageIndex=0&pageSize=" + str(number_of_ascents_boulder) + "&sortField=grade_desc&timeFilter=0&gradeFilter=0&typeFilter=&includeProjects=false&searchQuery=&showRepeats=false&showDuplicates=false"
webdriver.get(boulder)
ascents_boulder = json.loads(webdriver.find_elements(By.TAG_NAME, "pre")[0].text)


# Filter the data
filtered_ascents_sport = [
    {
        'ascentId': ascent['ascentId'],
        'zlaggableName': ascent['zlaggableName'],
        'difficulty': ascent['difficulty'],
        'secondGo': ascent['secondGo'],
        'type': ascent['type']
    }
    for ascent in ascents_sport['ascents']
]

filtered_ascents_boulder = [
    {
        'ascentId': ascent['ascentId'],
        'zlaggableName': ascent['zlaggableName'],
        'difficulty': ascent['difficulty'],
        'secondGo': ascent['secondGo'],
        'type': ascent['type']
    }
    for ascent in ascents_boulder['ascents']
]

# Combine the filtered data
combined_ascents = {
    'sport': filtered_ascents_sport,
    'boulder': filtered_ascents_boulder
}

# Write the combined data to a new JSON file
with open('ascents.json', 'w') as f:
    json.dump(combined_ascents, f)
    


