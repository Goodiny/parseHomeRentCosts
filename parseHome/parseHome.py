import time
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class ParseHome:
    def __init__(self, url: str = "https://home.ss.ge/ru/%D0%BD%D0%B5%D0%B4%D0%B2%D0%B8%D0%B6%D0%B8%D0%BC%D0%BE%D1"
                                  "%81%D1%82%D1%8C/l/%D0%9A%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D0%B0/%D0%90%D1%80"
                                  "s%D0%B5%D0%BD%D0%B4%D0%B0?cityIdList=95&subdistrictIds=3&streetIds=1093%2C1099&"
                                  "areaFrom=40&areaTo=60&currencyId=1"):
        options = webdriver.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/78.0")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")

        service = Service(ChromeDriverManager().install())
        self.URI = url
        self.driver = webdriver.Chrome(service=service, options=options)
        self.data = []

    def get_source_code(self, url: str = None) -> None:
        self.driver.get(url or self.URI)
        time.sleep(1)

        while True:
            try:
                element = WebDriverWait(driver=self.driver, timeout=2).until(
                        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".top-grid-lard"))
                )
                data_temp = {}
                for elem in element.text.replace("реклама", "").split('\n'):
                    if elem.endswith("2024") or elem.endswith("назад"):
                        self.data.append(data_temp) if data_temp else None
                        data_temp = {}
                        data_temp["date"] = elem
                    elif elem.endswith("$"):
                        data_temp["price"] = elem
                    elif elem.startswith("ул."):
                        data_temp["address"] = elem
                    elif elem.endswith("m²"):
                        data_temp["area"] = elem
                    elif elem.isdigit():
                        data_temp["rooms"] = elem
                    elif "/" in elem and len(elem) <= 5:
                        data_temp["floors"] = elem
                    elif (((elem.startswith("Аренда") or elem.startswith("Продается") or elem.startswith("Сдается"))
                          and len(elem) <= 45) and "date" in data_temp and "price" not in data_temp):
                        data_temp["title"] = elem
                    else:
                        data_temp["description"] = elem

                with open("source_code.txt", "w") as f:
                    f.write(element.text.replace("реклама", ""))
                break
            except TimeoutException as _ex:
                print(_ex)
            finally:
                self.driver.close()
                self.driver.quit()
                break


def main() -> None:
    parse_home = ParseHome()
    parse_home.get_source_code()


if __name__ == "__main__":
    main()
