from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import details
import pandas as pd


# if __name__ == '__main__':
driver = webdriver.Chrome()
driver.get("https://instagram.com")
sleep(.5)

driver.maximize_window()        # maximizes window
sleep(.5)

# username and password
driver.find_element_by_xpath('//input[@name="username"]').send_keys(details.username)
sleep(1)
driver.find_element_by_xpath('//input[@name="password"]').send_keys(details.password)
sleep(1)
driver.find_element_by_xpath('//button[@type="submit"]').click()
sleep(3)

driver.find_element_by_xpath('//button[contains(text(), "Not Now")]').click()       # save info
sleep(.5)
driver.find_element_by_xpath('//button[contains(text(), "Not Now")]').click()       # notifications
sleep(.5)

driver.find_element_by_xpath('//a[@href= "/{}/"]'.format(details.username)).click()     # profile
sleep(2)


# following
driver.find_element_by_xpath('//a[@href= "/{}/following/"]'.format(details.username)).click()
sleep(2)

scroll_box = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/ul')
last_height, new_height = 0,1
while last_height != new_height:
    last_height = new_height
    sleep(2.5)
    new_height = driver.execute_script("""arguments[0].scrollTo(0, arguments[0].scrollHeight); 
    return arguments[0].scrollHeight;""", scroll_box)
sleep(1)

links = scroll_box.find_elements_by_xpath('//a[@title][@tabindex="0"]')
following = [uname.get_attribute('title') for uname in links if (uname.get_attribute('title') != '')]
print("Following")
print(len(following))
print(following)
sleep(1)
driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button').click()      # close button
sleep(2)


# followers
driver.find_element_by_xpath('//a[@href= "/{}/followers/"]'.format(details.username)).click()
sleep(2)

scroll_box = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/ul')
last_height, new_height = 0,1
while last_height != new_height:
    last_height = new_height
    sleep(2.5)
    new_height = driver.execute_script("""arguments[0].scrollTo(0, arguments[0].scrollHeight); 
    return arguments[0].scrollHeight;""", scroll_box)
sleep(1)

links = scroll_box.find_elements_by_xpath('//a[@title][@tabindex="0"]')
# followers = [uname.text for uname in links if uname.text != '']
followers = [uname.get_attribute('title') for uname in links if (uname.get_attribute('title') != '')]
print("Followers")
print(len(followers))
print(followers)
sleep(1)
driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button').click()      # close button
sleep(2)


# not following me back
not_following_back = [user for user in following if user not in followers]
print("Not Following Back")
print(len(not_following_back))
print(not_following_back)


# i am not following back
not_following = [user for user in followers if user not in following]
print("Not Following")
print(len(not_following))
print(not_following)


# saving as a csv file
data = pd.DataFrame()
data['following'] = following
data['followers'] = pd.Series(followers)
data['not_following_me_back'] = pd.Series(not_following_back)
data['i_not_following_back'] = pd.Series(not_following)
data.to_csv('data.csv', index=False)

sleep(10)
driver.quit()
