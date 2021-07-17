from datetime import datetime
from time import sleep

from selenium import webdriver

import csv

header = ['pt', 'en']
csv_file = open('translated_sentences_google_v2.csv', 'a', encoding='UTF8')
writer = csv.writer(csv_file, delimiter='\t')
# write the header
writer.writerow(header)

current_index = 0


def do_work(driver, sentences, cur_index):

    global current_index

    driver.get("https://translate.google.com/?hl=en&tab=TT&sl=pt&tl=en")

    for i, s in enumerate(sentences):

        current_index = cur_index + i

        driver.find_element_by_xpath("//body[@id='yDmH0d']/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div/div[2]/div[2]/c-wiz/span/span/div/textarea").clear()
        driver.find_element_by_xpath("//body[@id='yDmH0d']/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div/div[2]/div[2]/c-wiz/span/span/div/textarea").send_keys(s)
        sleep(3)
        output = driver.find_element_by_xpath("//body[@id='yDmH0d']/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div/div[2]/div[2]/c-wiz[2]/div[5]/div/div/span/span/span").text
        # print(output)
        writer.writerow([s, output])
        # sleep(0.5)


if __name__ == "__main__":

    with open('./problematic_df.txt', encoding='UTF8') as f:
        content = f.readlines()

    list_sentences = [x.strip() for x in content]
    list_sentences.sort(key=len, reverse=True)
    # list_sentences.reverse()

    while current_index < len(list_sentences):

        # firefox_profile = webdriver.FirefoxProfile()
        # firefox_profile.set_preference("browser.privatebrowsing.autostart", True)

        web_driver = webdriver.Firefox(executable_path=r'C:\Users\Navaneeth Sen\Downloads\geckodriver-v0.29.1-win64\geckodriver.exe')
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
