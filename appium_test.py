import unittest
import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up basic Appium configuration for the Amazon app
capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    appPackage='in.amazon.mShop.android.shopping',
    appActivity='com.amazon.mShop.splashscreen.StartupActivity',
    language='en',
    locale='US',
    autoGrantPermissions=True,
    fullReset=False,
    noReset=True
)

appium_server_url = 'http://localhost:4723'

class AmazonShoppingTest(unittest.TestCase):
    def setUp(self) -> None:
        """This runs before every test. It opens the app and sets up wait logic."""
        options = UiAutomator2Options().load_capabilities(capabilities)
        self.driver = webdriver.Remote(appium_server_url, options=options)
        self.start_time = time.time()  # Start timing from here
        self.driver.implicitly_wait(10)  # Short wait for finding elements
        self.wait = WebDriverWait(self.driver, 15)  # Explicit wait setup
        self.response_times = {}  # Track all response times here

    def tearDown(self) -> None:
        """This runs after every test. It closes the app."""
        if self.driver:
            self.driver.quit()

    def scroll_vertically(self, start_percent_y, end_percent_y, percent_x=0.5):
        """Scroll down or up using touch gestures from one point to another on screen."""
        screen_size = self.driver.get_window_size()
        start_x = screen_size['width'] * percent_x
        start_y = screen_size['height'] * start_percent_y
        end_x = start_x
        end_y = screen_size['height'] * end_percent_y

        # Create a gesture for the scroll
        actions = ActionChains(self.driver)
        finger = PointerInput(interaction.POINTER_TOUCH, "finger")
        actions.w3c_actions = ActionBuilder(self.driver, mouse=finger)
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    def test_amazon_shopping_with_timing(self):
        """This test covers searching, sorting, selecting and adding to cart on Amazon."""
        try:
            print("\n--- Amazon Shopping Test with Response Time Measurements ---")

            # Wait for app's main search box to appear
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,
                '//android.widget.ImageButton[@resource-id="in.amazon.mShop.android.shopping:id/chrome_search_box"]')))

            # Record time taken for app to load
            search_time = time.time() - self.start_time
            self.response_times['amazonload'] = search_time
            print(f"Response time for amazon load: {search_time:.2f} seconds")

            # a) Start search for "wireless headphones"
            print("\na) Searching for 'wireless headphones'")

            # Click search box
            search_box = self.driver.find_element(by=AppiumBy.XPATH,
                value='//android.widget.ImageButton[@resource-id="in.amazon.mShop.android.shopping:id/chrome_search_box"]')
            search_box.click()

            # Type the search query
            search_input = self.wait.until(EC.presence_of_element_located(
                (AppiumBy.ID, 'in.amazon.mShop.android.shopping:id/rs_search_src_text')))
            search_input.send_keys("wireless headphones")
            self.driver.press_keycode(66)  # Press Enter to search

            # Wait for search results to load
            start_time = time.time()
            self.wait.until(EC.presence_of_element_located(
                (AppiumBy.XPATH, '//android.view.View[@resource-id="s-all-filters"]')))
            search_time = time.time() - start_time
            self.response_times['search'] = search_time
            print(f"Response time for search: {search_time:.2f} seconds")

            # b) Sort by price (low to high)
            print("\nb) Sorting by price (low to high)")

            filters_button = self.driver.find_element(by=AppiumBy.XPATH,
                value='//android.view.View[@resource-id="s-all-filters"]')
            filters_button.click()

            # Wait for filters to load
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.view.View[@text="Prime & Delivery"]')))

            # Scroll to reveal sorting options
            self.scroll_vertically(0.7, 0.1, 0.2)
            self.scroll_vertically(0.7, 0.1, 0.2)

            # Select Sort By -> Price Low to High
            sort_by_button = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.XPATH, '//android.view.View[@text="Sort by"]')))
            sort_by_button.click()

            self.wait.until(EC.presence_of_element_located(
                (AppiumBy.XPATH, '//android.widget.CheckBox[@resource-id="sort/price-asc-rank"]')))
            start_time = time.time()
            price_low_to_high_checkbox = self.driver.find_element(by=AppiumBy.XPATH, 
                value='//android.widget.CheckBox[@resource-id="sort/price-asc-rank"]')
            price_low_to_high_checkbox.click()

            # Wait for and click "Show Results"
            self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.XPATH, '//android.view.View[contains(@content-desc, "Show") or contains(@text, "Show")]')))
            time.sleep(1)
            price_sort_time = time.time() - start_time
            self.response_times['price_sort'] = price_sort_time
            print(f"Response time for price sort: {price_sort_time:.2f} seconds")
            show_results_button = self.driver.find_element(by=AppiumBy.XPATH, 
                value='//android.view.View[contains(@content-desc, "Show") or contains(@text, "Show")]')
            show_results_button.click()

            # Wait for products to load
            self.wait.until(EC.presence_of_all_elements_located(
                (AppiumBy.XPATH, '//android.view.View[@content-desc and contains(@content-desc, "₹")]')))
            self.scroll_vertically(0.6, 0.4)

            # Try to get product name
            try:
                product_name_element = self.wait.until(EC.presence_of_element_located(
                    (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Wired Headphone")')))
                product_name = product_name_element.get_attribute('text')
            except:
                # Fallback to any headphone result
                product_elements = self.driver.find_elements(by=AppiumBy.XPATH, 
                    value='//android.view.View[@content-desc and contains(@content-desc, "headphone") or contains(@content-desc, "Headphone")]')
                product_name = product_elements[0].get_attribute('content-desc') if product_elements else "Product name not found"

            # Extract product price
            product_containers = self.driver.find_elements(by=AppiumBy.XPATH,
                value='//android.view.View[@content-desc and contains(@content-desc, "₹")]')
            product_price = "Price not found"
            if product_containers:
                product_info = product_containers[0].get_attribute('content-desc')
                if "₹" in product_info:
                    price_text = product_info.split("₹")[1].split()[0]
                    product_price = "₹" + price_text
            print(f"   Lowest priced item: {product_name} - {product_price}")

            # c) Now sort by rating
            print("\nc) Sorting by highest rated")

            self.scroll_vertically(0.4, 0.6)
            filters_button = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.XPATH, '//android.view.View[@resource-id="s-all-filters"]')))
            filters_button.click()

            self.wait.until(EC.presence_of_element_located(
                (AppiumBy.XPATH, '//android.widget.CheckBox[@resource-id="sort/review-rank"]')))
            start_time = time.time()
            avg_review_option = self.driver.find_element(by=AppiumBy.XPATH,
                value='//android.widget.CheckBox[@resource-id="sort/review-rank"]')
            avg_review_option.click()

            # Click "Show Results" again
            self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.XPATH, '//android.view.View[contains(@content-desc, "Show") or contains(@text, "Show")]')))
            time.sleep(1)
            rating_sort_time = time.time() - start_time
            self.response_times['rating_sort'] = rating_sort_time
            print(f"Response time for rating sort: {rating_sort_time:.2f} seconds")
            show_results_button.click()

            # Try to get highest rated product
            self.wait.until(EC.presence_of_all_elements_located(
                (AppiumBy.XPATH, '//android.view.View[@content-desc and contains(@content-desc, "₹")]')))
            self.scroll_vertically(0.6, 0.4)
            try:
                product_name_element = self.wait.until(EC.presence_of_element_located(
                    (AppiumBy.ANDROID_UIAUTOMATOR, 
                     'new UiSelector().textContains("Bluetooth Headphones")')))
                product_name = product_name_element.get_attribute('text')
            except:
                product_elements = self.driver.find_elements(by=AppiumBy.XPATH, 
                    value='//android.view.View[@content-desc and contains(@content-desc, "headphone") or contains(@content-desc, "Headphone")]')
                product_name = product_elements[0].get_attribute('content-desc') if product_elements else "Product name not found"
                if product_elements:
                    product_elements[0].click()

            # Try to get price
            price_elements = self.driver.find_elements(by=AppiumBy.XPATH,
                value='//android.view.View[contains(@text, "₹") or contains(@content-desc, "₹")]')
            product_price = "Price not found"
            for price_element in price_elements:
                price_text = price_element.get_attribute('text') or price_element.get_attribute('content-desc')
                if price_text and "₹" in price_text:
                    product_price = "₹" + price_text.split("₹")[1].split()[0]
                    break

            print(f"Highest rated item: {product_name} - {product_price}")

            # d) Add product to cart
            print("\nd) Adding item to cart")

            add_to_cart_button = self.wait.until(EC.element_to_be_clickable(
                (AppiumBy.XPATH, '//android.widget.Button[@text="Add to cart"]')))
            start_time = time.time()
            add_to_cart_button.click()

            # Click on cart icon after adding
            cart_icon = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                value='new UiSelector().resourceId("in.amazon.mShop.android.shopping:id/bottom_tab_button_icon").instance(2)')
            add_to_cart_time = time.time() - start_time
            self.response_times['add_to_cart'] = add_to_cart_time
            print(f"Response time: {add_to_cart_time:.2f} seconds")
            cart_icon.click()

            # e) Show a summary of response times
            print("\ne) Response Time Summary")
            for step, rt in self.response_times.items():
                print(f"   {step.replace('_', ' ').capitalize()}: {rt:.2f} seconds")
            print(f"   Total response time: {sum(self.response_times.values()):.2f} seconds")

        except Exception as e:
            print(f"Test failed with error: {e}")
            raise

if _name_ == '_main_':
    unittest.main()