import json
import time
from pprint import pprint
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from undetected_chromedriver import ChromeOptions

url = 'https://www.avito.ru/krasnodar/noutbuki/'
options = ChromeOptions()
options.headless = True
driver = uc.Chrome(options=options)

output = []
x={}


def open_item_page():
    result.click()
    windows = driver.window_handles
    driver.switch_to.window(windows[1])


def close_window():
    driver.close()
    windows = driver.window_handles
    # print(windows)
    driver.switch_to.window(windows[0])


def get_info():

    title = driver.find_element(By.CSS_SELECTOR, '[class="title-info-title-text"]').text
    price = driver.find_element(By.CSS_SELECTOR, '[id="price-value"]').text
    time_publ = driver.find_element(By.CSS_SELECTOR, '[class="title-info-metadata-item-redesign"]').text
    seller_name = driver.find_element(By.CSS_SELECTOR, '[data-marker="seller-info/name"]').text.strip()
    link = driver.current_url
    title = title.replace(' ', '_')
    data = {
                # 'title': title.replace(' ', '_'),
                'time': time_publ,
                'price': price.replace(' ', '').replace('\n', ' '),
                'seller_name': seller_name.replace(' ', '_'),
                'link': link.replace(' ', '')
            }
    x[title] = data
    return x


try:
    driver.get(url)
    print('открывается браузер')
    driver.find_element(By.CSS_SELECTOR, '[data-marker="search-form/suggest"]').send_keys('msi')
    driver.find_element(By.CSS_SELECTOR, '[data-marker="search-form/submit-button"]').click()
    print('загружаются результаты')
    results = driver.find_elements(By.CSS_SELECTOR, '[data-marker="item"]')
    print('начинается сбор данных')
    count = 0
    for result in results:
        open_item_page()
        get_info()
        close_window()
        count += 1
        print(f'товаров обработано: {count}')




except Exception as ex:
    pprint(ex)

finally:
    # pprint(output)
    # json_string = json.dumps(output, ensure_ascii=False)

    with open('result.json', 'w') as file:
        json.dump(x, file, indent=4, ensure_ascii=False)

    driver.quit()

