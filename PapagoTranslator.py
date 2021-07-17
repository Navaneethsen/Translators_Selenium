from datetime import datetime
import re
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv

header = ['pt', 'en']
csv_file = open('translated_sentences_papago.csv', 'a', encoding='UTF8')
writer = csv.writer(csv_file, delimiter='\t')
# write the header
writer.writerow(header)

current_index = 0


def do_work(driver, sentences, cur_index):

    global current_index

    driver.get("https://papago.naver.com/?sk=pt&tk=en")
    driver.find_element_by_id("sourceEditArea").click()
    driver.find_element_by_id("txtSource").click()

    for i, s in enumerate(sentences):
        sen = s
        if s.endswith('...') or s.endswith('...!') or s.endswith('...?') or s.endswith('..."') or s.endswith('...\''):
            sen = re.sub('(\.\.+)([."\'?!])$', '.\\2', s)

        current_index = cur_index + i
        driver.find_element_by_id("txtSource").clear()
        driver.find_element_by_id("txtSource").send_keys(sen)
        driver.find_element_by_xpath("//button[@id='btnTranslate']/span").click()
        # driver.find_element_by_xpath("//div[@id='root']/div/div[2]/section/div/div/div[2]/div/div[7]/span[2]/span/span/button").click()

        translated_text_xpath = "//div[@id='root']/div/div[2]/section/div/div/div[2]/div/div[5]/div/span"
        element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, translated_text_xpath)))

        output = ""
        while output == '' or output == '...':
            output = driver.find_element_by_xpath(translated_text_xpath).text
            # print(output)
            sleep(3)

        if s.endswith('...') or s.endswith('...!') or s.endswith('...?') or s.endswith('..."') or s.endswith('...\''):
            writer.writerow([s, re.sub('\.\.\.$', '..', output)])
        else:
            writer.writerow([s, output])

        # sleep(0.5)


if __name__ == "__main__":

    with open('./problematic_df.txt', encoding='UTF8') as f:
        content = f.readlines()

    list_sentences = [x.strip() for x in content]
    # list_sentences.reverse()

    while current_index < len(list_sentences):

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")

        caps = chrome_options.to_capabilities()

        # web_driver = webdriver.Firefox(executable_path=r'C:\Users\Navaneeth Sen\Downloads\geckodriver-v0.29.1-win64\geckodriver.exe')
        web_driver = webdriver.Chrome(
            executable_path=r'C:\Users\Navaneeth Sen\Downloads\chromedriver_win32\chromedriver.exe',
            desired_capabilities=caps)

        # firefox_profile = webdriver.FirefoxProfile()
        # firefox_profile.set_preference("browser.privatebrowsing.autostart", True)

        # web_driver = webdriver.Firefox(executable_path=r'C:\Users\Navaneeth Sen\Downloads\geckodriver-v0.29.1-win64\geckodriver.exe')
        # web_driver = webdriver.Firefox()
        web_driver.implicitly_wait(30)
        try:
            print("Doing work from " + str(current_index) + " -- " + str(datetime.now()))
            do_work(web_driver, list_sentences[current_index:], current_index)
        except:
            print("Failed work at " + str(current_index))
            current_index = current_index + 1
            web_driver.quit()
            sleep(10)

    csv_file.close()
