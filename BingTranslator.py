from datetime import datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver.support.select import Select

import csv

header = ['pt', 'en']
csv_file = open('./translated_sentences_bing.csv', 'a', encoding='UTF8')
writer = csv.writer(csv_file, delimiter='\t')
# write the header
writer.writerow(header)

current_index = 0 #136


def do_work(driver, sentences, cur_index):

    global current_index

    driver.get("https://www.bing.com/translator")
    driver.find_element_by_id("tta_srcsl").click()
    Select(driver.find_element_by_id("tta_srcsl")).select_by_visible_text("Portuguese (Portugal)")
    driver.find_element_by_id("tta_srcsl").click()
    driver.find_element_by_id("tta_tgtsl").click()
    Select(driver.find_element_by_id("tta_tgtsl")).select_by_visible_text("English")
    driver.find_element_by_id("tta_tgtsl").click()
    driver.find_element_by_id("tta_input_ta").click()

    for i, s in enumerate(sentences):

        current_index = cur_index + i
        driver.find_element_by_id("tta_input_ta").clear()
        driver.find_element_by_id("tta_input_ta").send_keys(s)
        sleep(3)
        output = driver.find_element_by_id('tta_output_ta').get_attribute('value')
        # print(output)
        writer.writerow([s, output])
        sleep(0.5)


if __name__ == "__main__":

    with open('./problematic_df.txt', encoding='UTF8') as f:
        content = f.readlines()

    list_sentences = [x.strip() for x in content]
    list_sentences.sort(key=len, reverse=True)
    # list_sentences.reverse()

    while current_index < len(list_sentences):

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")

        caps = chrome_options.to_capabilities()

        # web_driver = webdriver.Firefox(executable_path=r'C:\Users\Navaneeth Sen\Downloads\geckodriver-v0.29.1-win64\geckodriver.exe')
        web_driver = webdriver.Chrome(executable_path=r'C:\Users\Navaneeth Sen\Downloads\chromedriver_win32\chromedriver.exe', desired_capabilities=caps)
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
