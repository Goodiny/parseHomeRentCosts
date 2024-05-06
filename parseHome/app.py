import time
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/78.0")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless")

service = Service(ChromeDriverManager().install())
URI = ("https://home.ss.ge/ru/%D0%BD%D0%B5%D0%B4%D0%B2%D0%B8%D0%B6%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D1%8C/l/"
       "%D0%9A%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D0%B0/%D0%90%D1%80s%D0%B5%D0%BD%D0%B4%D0%B0?cityIdList="
       "95&subdistrictIds=3&streetIds=1093%2C1099&areaFrom=40&areaTo=60&currencyId=1")
driver = webdriver.Chrome(service=service, options=options)


def get_source_code(url: str, driver: webdriver = driver) -> None:
    driver.get(url)
    time.sleep(1)

    while True:
        try:
            element = WebDriverWait(driver=driver, timeout=2).until(
                    expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".top-grid-lard"))
            )
            with open("source_code.txt", "w") as f:
                f.write(element.text.replace("реклама", ""))
            break
        except TimeoutException as _ex:
            print(_ex)
        finally:
            driver.close()
            driver.quit()
            break


def main() -> None:
    get_source_code(URI)


if __name__ == "__main__":
    main()
