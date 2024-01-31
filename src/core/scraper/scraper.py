import locale
import re
import time as system_time

from datetime import date
from selenium import webdriver
from selenium.common.exceptions import (
    ElementNotVisibleException, NoSuchElementException, TimeoutException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing import Optional

from src.core.scraper.utils import (
    add_n_days_to_input_dates, combine_input_dates_and_scraped_timestr
)


class EdreamsScraper:

    @classmethod
    def _set_locale(self, locale_str: str = 'it_IT'):
        locale.setlocale(locale.LC_ALL, locale_str)

    def __init__(self):
        self._options = Options()
        self._options.add_argument("--headless")
        self._options.add_argument("--window-size=1400,600")
        self._options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        self._options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self._options.add_experimental_option("detach", True)
        self._url = "https://www.edreams.it/"
        self._driver = webdriver.Chrome(options=self._options)
        self._init_xpaths()
        self._locale = self._set_locale()

    def _init_xpaths(self):
        self._xpath_cookies_button = "//button[@id='didomi-notice-agree-button']"
        self._xpath_ow_trip_radio_button = "//label[@for='tripTypeSwitcher_oneWayTrip']"
        self._xpath_tw_trip_radio_button = "//label[@for='tripTypeSwitcher_multipleTrip']"
        self._xpath_dep_location_boxes = "//input[(@test-id='input-airport') and contains(@class, 'first')]"
        self._xpath_arr_location_boxes = "//input[(@test-id='input-airport') and not(contains(@class, 'first'))]"
        self._xpath_dep_date_boxes = "//div[contains(@class, 'datepicker')]//input[contains(@class, 'odf-clickable')]"
        self._xpath_month_selector = "//div[contains(@class, 'odf-calendar')]"
        self._day_to_select = None
        self._xpath_day_selector = ""
        self._xpath_arrows_date_box = "//div[contains(@class, 'odf-col-nogutter')]"
        self._xpath_submit_button = "//button[@test-id='search-flights-btn']"
        self._xpath_flight_cards = "//div[contains(@data-testid, 'itinerary') and contains(@class, 'css-1xi4blx')]"
        self._xpath_line_splitting_subboxes = ".//div[@class='css-pfehrt-Box e17fzqxg0']"
        self._xpath_flight_times = ".//div[contains(@class, 'css-1fgaoh1')]"
        self._xpath_flight_times_next_days = ".//div[contains(@class, 'css-18cpgt')]"
        self._xpath_flight_locations = ".//div[contains(@class, 'css-1aklsay')]"
        self._xpath_airlines = ".//div[contains(@class, 'css-16ig7wx')]"
        self._xpath_flight_lengths = ".//span[contains(@class, 'css-frp1wa')]"
        self._xpath_flight_types = ".//span[contains(@class, 'css-vbzcfl')]"
        self._xpath_unchecked_luggage = ".//div[contains(@class, 'css-wa1si')]"
        self._xpath_checked_luggage = ".//div[contains(@class, 'css-1u8kibv')]"
        self._xpath_prices = ".//span[contains(@class, 'money-integer')]"
        self._xpath_currencies = ".//span[contains(@class, 'money-currency')]"
        self._xpath_load_further_results = "//div[contains(@class, 'css-5ve9sa')]//button[@class='e6ygnnq0 css-40dyis e3hopz80']"

    def _construct_day_xpath(self):
        return f"//div[contains(@class, 'odf-calendar-row')]//div[contains(@class, 'odf-calendar-day') and text()='{self._day_to_select}']"

    def _setup_cookies(self):
        self._driver.get(self._url)
        try:
            cookies_button = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self._xpath_cookies_button))
            )
            cookies_button.click()
        except (ElementNotVisibleException, TimeoutException):
            pass

    def _click_trip_type_radio_button(
        self,
        is_two_way_trip: bool
    ):
        if is_two_way_trip:
            trip_type_button = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self._xpath_tw_trip_radio_button))
            )
        else:
            trip_type_button = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self._xpath_ow_trip_radio_button))
            )
        trip_type_button.click()

    def _fill_location_box(
        self,
        location_xpath: str,
        location_input: str,
        index: int
    ):
        location_box = WebDriverWait(self._driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, location_xpath))
        )[index]
        location_box.send_keys(Keys.CONTROL, 'a')
        location_box.send_keys(Keys.DELETE)
        location_box.send_keys(location_input)

    def _fill_date_box(
        self,
        month_to_select: str,
        day_to_select: int,
        index: int,
        arrow_index: int
    ):
        date_box = WebDriverWait(self._driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, self._xpath_dep_date_boxes))
        )[index]
        date_box.click()
        month_selector = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self._xpath_month_selector))
        )
        while not month_selector.text.startswith(month_to_select):
            arrows_date_box = self._driver.find_elements(
                By.XPATH, self._xpath_arrows_date_box
            )
            right_arrow_date_box = arrows_date_box[arrow_index]
            right_arrow_date_box.click()

        self._day_to_select = day_to_select
        self._xpath_day_selector = self._construct_day_xpath()
        day = self._driver.find_element(By.XPATH, self._xpath_day_selector)
        day.click()

    def _click_submit_button(self):
        submit_button = self._driver.find_element(By.XPATH, self._xpath_submit_button)
        submit_button.click()

    def _fill_trip_details(
        self,
        departure_location: str,
        arrival_location: str,
        departure_date: date,
        is_outbound: bool
    ):
        pos_index = 0 if is_outbound else 1
        self._fill_location_box(self._xpath_dep_location_boxes, departure_location, pos_index)
        self._fill_location_box(self._xpath_arr_location_boxes, arrival_location, pos_index)
        system_time.sleep(3)
        month_to_select = departure_date.strftime('%B').capitalize()
        day_to_select = departure_date.day
        self._fill_date_box(month_to_select, day_to_select, pos_index, 1)

    def search_flights(
        self,
        is_two_way_trip: bool,
        departure_location: str,
        arrival_location: str,
        departure_date: date,
        departure_location_comeback: Optional[str] = None,
        arrival_location_comeback: Optional[str] = None,
        departure_date_comeback: Optional[date] = None
    ):
        self._setup_cookies()
        self._click_trip_type_radio_button(is_two_way_trip)
        self._fill_trip_details(
            departure_location,
            arrival_location,
            departure_date,
            is_outbound=True
        )
        if is_two_way_trip:
            self._fill_trip_details(
                departure_location_comeback,
                arrival_location_comeback,
                departure_date_comeback,
                is_outbound=False
            )
        self._click_submit_button()

    def _click_load_additional_cards_button(self):
        try:
            load_add_elements_button = self._driver.find_element(
                By.XPATH, self._xpath_load_further_results
            )
        except NoSuchElementException:
            pass
        else:
            load_add_elements_button.click()

    def _scroll_to_load_all_flight_cards(self):
        prev_page_height = self._driver.execute_script("return document.body.scrollHeight")
        while True:
            self._driver.execute_script("window.scrollBy(0, 600)")
            system_time.sleep(1)
            curr_page_height = self._driver.execute_script("return document.body.scrollHeight")
            if curr_page_height == prev_page_height:
                self._click_load_additional_cards_button()
                curr_page_height = self._driver.execute_script("return document.body.scrollHeight")
                if curr_page_height == prev_page_height:
                    break
            prev_page_height = curr_page_height

    def _determine_arrival_date(
        self,
        departure_date: date,
        arrival_time: str,
        web_element: WebElement,
        index: int
    ):
        days_to_add = 0
        delta_days = web_element.find_elements(By.XPATH, self._xpath_flight_times_next_days)
        days_to_add += int(delta_days[index].text[-1]) if delta_days[index].text != "" else 0
        arrival_date = add_n_days_to_input_dates(departure_date, days_to_add)
        return combine_input_dates_and_scraped_timestr(arrival_date, arrival_time)

    def _localize_outbound_or_return_trip_box(
        self,
        web_element: WebElement,
        is_outbound: bool
    ):
        xpath_outbound_trip_box = self._xpath_line_splitting_subboxes + "/preceding-sibling::div[1]"
        xpath_return_trip_box = self._xpath_line_splitting_subboxes + "/following-sibling::div[1]"
        if is_outbound:
            return web_element.find_element(By.XPATH, xpath_outbound_trip_box)
        else:
            return web_element.find_element(By.XPATH, xpath_return_trip_box)

    def _determine_luggage_type(
        self,
        web_element: WebElement,
        is_outbound: bool
    ):
        try:
            single_trip_box = self._localize_outbound_or_return_trip_box(web_element, is_outbound)
        except NoSuchElementException:
            unchecked_luggage_ow_trip = web_element.find_elements(
                By.XPATH, self._xpath_unchecked_luggage
            )
            checked_luggage_ow_trip = web_element.find_elements(
                By.XPATH, self._xpath_checked_luggage
            )
            if unchecked_luggage_ow_trip != []:
                return unchecked_luggage_ow_trip[0].text
            else:
                return checked_luggage_ow_trip[0].text
        else:
            unchecked_luggage_tw_trip = single_trip_box.find_elements(
                By.XPATH, self._xpath_unchecked_luggage
            )
            checked_luggage_tw_trip = single_trip_box.find_elements(
                By.XPATH, self._xpath_checked_luggage
            )
            if unchecked_luggage_tw_trip != []:
                return unchecked_luggage_tw_trip[0].text
            else:
                return checked_luggage_tw_trip[0].text

    def _extract_date_details(
        self,
        web_element: WebElement,
        date: date,
        is_outbound: bool
    ):
        pos_index = 0 if is_outbound else 1
        flight_times = web_element.find_elements(By.XPATH, self._xpath_flight_times)
        departure_dates = combine_input_dates_and_scraped_timestr(
            date, flight_times[pos_index * 2].text
        )
        arrival_dates = self._determine_arrival_date(
            date, flight_times[pos_index * 2 + 1].text, web_element, pos_index
        )
        return departure_dates, arrival_dates

    def _extract_location_details(
        self,
        web_element: WebElement,
        is_outbound: bool
    ):
        pos_index = 0 if is_outbound else 1
        locations = web_element.find_elements(By.XPATH, self._xpath_flight_locations)
        departure_locations = locations[pos_index * 2].text
        arrival_locations = locations[pos_index * 2 + 1].text
        return departure_locations, arrival_locations

    def _extract_airline_details(
        self,
        web_element: WebElement,
        is_outbound: bool
    ):
        pos_index = 0 if is_outbound else 1
        airlines = web_element.find_elements(By.XPATH, self._xpath_airlines)
        return re.sub("·", "", airlines[pos_index].text).strip()

    def _extract_flight_length_details(
        self,
        web_element: WebElement,
        is_outbound: bool
    ):
        pos_index = 0 if is_outbound else 1
        flight_lengths = web_element.find_elements(By.XPATH, self._xpath_flight_lengths)
        return flight_lengths[pos_index].text

    def _extract_flight_type_details(
        self,
        web_element: WebElement,
        is_outbound: bool
    ):
        pos_index = 0 if is_outbound else 1
        flight_types = web_element.find_elements(By.XPATH, self._xpath_flight_types)
        return flight_types[pos_index].text

    def _extract_luggage_type_details(
        self,
        web_element: WebElement,
        is_outbound: bool
    ):
        return self._determine_luggage_type(web_element, is_outbound)

    def _extract_price_details(
        self,
        web_element: WebElement
    ):
        prices = web_element.find_elements(By.XPATH, self._xpath_prices)
        return float(prices[0].text)

    def _extract_currency_details(
        self,
        web_element: WebElement
    ):
        currencies = web_element.find_elements(By.XPATH, self._xpath_currencies)
        return currencies[0].text[-1]

    def _extract_single_trip_details(
        self,
        web_element: WebElement,
        departure_date: date,
        is_outbound: bool
    ):
        departure_date, arrival_date = self._extract_date_details(
            web_element, departure_date, is_outbound
        )
        departure_location, arrival_location = self._extract_location_details(
            web_element, is_outbound
        )
        airline = self._extract_airline_details(web_element, is_outbound)
        trip_length = self._extract_flight_length_details(web_element, is_outbound)
        trip_type = self._extract_flight_type_details(web_element, is_outbound)
        luggage_type = self._extract_luggage_type_details(web_element, is_outbound)
        price = self._extract_price_details(web_element)
        currency = self._extract_currency_details(web_element)
        trip_data = {
            "departure_date" if is_outbound else "departure_date_comeback": departure_date,
            "arrival_date" if is_outbound else "arrival_date_comeback": arrival_date,
            "departure_location" if is_outbound else "departure_location_comeback": departure_location,
            "arrival_location" if is_outbound else "arrival_location_comeback": arrival_location,
            "airline" if is_outbound else "airline_comeback": airline,
            "flight_length" if is_outbound else "flight_length_comeback": trip_length,
            "trip_type" if is_outbound else "trip_type_comeback": trip_type,
            "luggage_type" if is_outbound else "luggage_type_comeback": luggage_type,
            "price": price,
            "currency": currency
        }
        return trip_data

    def scrape_flight_data(
        self,
        is_two_way_trip: bool,
        departure_date: date,
        departure_date_comeback: Optional[date] = None
    ):
        self._scroll_to_load_all_flight_cards()
        flight_cards = WebDriverWait(self._driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, self._xpath_flight_cards))
        )
        flight_data_list = []
        for card in flight_cards:
            flight_data = dict()
            flight_data["is_two_way_trip"] = is_two_way_trip
            flight_data.update(self._extract_single_trip_details(
                card, departure_date, is_outbound=True)
            )
            if is_two_way_trip:
                flight_data.update(self._extract_single_trip_details(
                    card, departure_date_comeback, is_outbound=False)
                )
            flight_data_list.append(flight_data)
        return flight_data_list

    def close(self):
        self._driver.quit()


def scrape_data(
    is_two_way_trip: bool,
    departure_location: str,
    arrival_location: str,
    departure_date: date,
    departure_location_comeback: Optional[str] = None,
    arrival_location_comeback: Optional[str] = None,
    departure_date_comeback: Optional[date] = None
):
    scraper = EdreamsScraper()
    scraper.search_flights(
        is_two_way_trip,
        departure_location,
        arrival_location,
        departure_date,
        departure_location_comeback,
        arrival_location_comeback,
        departure_date_comeback
    )
    system_time.sleep(3)
    data = scraper.scrape_flight_data(
        is_two_way_trip,
        departure_date,
        departure_date_comeback
    )
    scraper.close()
    return data
