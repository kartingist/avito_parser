import json
import time
from pprint import pprint
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions

chromedriver_autoinstaller.install()
url = 'https://www.avito.ru/krasnodar/noutbuki/'
options = ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.headless = True
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)

x = {}


def open_item_page():
    result.click()
    windows = driver.window_handles
    driver.switch_to.window(windows[1])


def close_window():
    driver.close()
    windows = driver.window_handles
    driver.switch_to.window(windows[0])


def get_info(count):
    title = driver.find_element(By.CSS_SELECTOR, '[class="title-info-title-text"]').text
    price = driver.find_element(By.CSS_SELECTOR, '[class="item-price"]').text
    time_publ = driver.find_element(By.CSS_SELECTOR, '[class="title-info-metadata-item-redesign"]').text
    seller_name = driver.find_element(By.CSS_SELECTOR, '[data-marker="seller-info/name"]').text.strip()
    link = driver.current_url

    data = {
        'title': title.replace(' ', '_'),
        'time': time_publ,
        'price': price.replace('\n', ' '),
        'seller_name': seller_name.replace(' ', '_'),
        'link': link.replace(' ', '')
    }
    x[f'item_{count}'] = data

def get_count_pages():
    pages_block = driver.find_element(By.CSS_SELECTOR, '[data-marker="pagination-button"]').find_elements(By.CSS_SELECTOR, 'span')
    pages_count = pages_block[-2].text
    return pages_count




try:
    driver.maximize_window()
    driver.get(url)
    print('открывается браузер')
    driver.find_element(By.CSS_SELECTOR, '[data-marker="search-form/suggest"]').send_keys('msi')
    driver.find_element(By.CSS_SELECTOR, '[data-marker="search-form/submit-button"]').click()

    pages_count = int(get_count_pages())
    count_results = int(driver.find_element(By.CSS_SELECTOR, '[data-marker="page-title/count"]').text)
    count = 0
    for i in range(pages_count):
        print(f'открыта страница {i+1} из {pages_count}')
        time.sleep(1)


        print('загружаются результаты')
        results = driver.find_element(By.CSS_SELECTOR, '[data-marker="catalog-serp"]').find_elements(By.CSS_SELECTOR, '[data-marker="item-title"]')
        print(f'на данной странице {len(results)} товаров, начинается сбор данных')

        for result in results:
            open_item_page()
            get_info(count)
            close_window()
            count += 1
            print(f'товаров обработано: {count} из {count_results}')
        if count == count_results:
            break
        else:
            driver.find_element(By.CSS_SELECTOR, '[data-marker="pagination-button/next"]').click()





except Exception as ex:
    raise ex

finally:
    # pprint(output)
    # json_string = json.dumps(output, ensure_ascii=False)

    with open('result.json', 'w') as file:
        json.dump(x, file, indent=4, ensure_ascii=False)

    driver.quit()
