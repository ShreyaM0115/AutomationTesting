from time import sleep
from time import time
from selenium.webdriver.common.by import By 
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

edge_options = Options()
edge_options.add_argument("--log-level=3")
edge_options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Edge(options=edge_options)

driver.maximize_window()

driver.implicitly_wait(15)

start_time = time()
driver.get("https://www.amazon.in/")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
end_time = time()

f = f"f:\nPage Load Time: {end_time - start_time:.2f} seconds"

# a

searchbox = driver.find_element(By.ID, "twotabsearchtextbox")
searchbox.click()
searchbox.clear()
searchbox.send_keys("wireless headphones")

start_time = time()
searchbox.submit()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
end_time = time()
print(f"a:\nSearched for 'wireless headphones'")
e1 = f"e:\nPage Load Time after submit: {end_time - start_time:.2f} seconds"

# b

dropdown = driver.find_element(By.ID, "s-result-sort-select")
select = Select(dropdown)

start_time = time()
select.select_by_visible_text("Price: Low to High")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
end_time = time()
e2 = f"Page Load Time after sorting by price: {end_time - start_time:.2f} seconds"

product_name = driver.find_element(By.CSS_SELECTOR, 'h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal span').text
print("b:\nProduct Name:", product_name)

product_price = driver.find_element(By.CSS_SELECTOR, 'span.a-price-whole').text
print("Product Price:", product_price)

# c

dropdown = driver.find_element(By.ID, "s-result-sort-select")
select = Select(dropdown)

start_time = time()
select.select_by_visible_text("Avg. Customer Review")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
end_time = time()
e3 = f"Page Load Time after sorting by user rating: {end_time - start_time:.2f} seconds"

product_name = driver.find_element(By.CSS_SELECTOR, "h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal span").text
print("c:\nProduct Name:", product_name)

product_price = driver.find_element(By.CSS_SELECTOR, 'span.a-price-whole').text
print("Product Price:", product_price)

# d

add_to_card_button = driver.find_element(By.CSS_SELECTOR, "button.a-button-text")

start_time = time()
add_to_card_button.click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
end_time = time()
e4 = f"Page Load Time after clicking 'Add to Cart' button: {end_time - start_time:.2f} seconds"

print(f"d:\nAdd to Cart button clicked")

# e

print(e1,e2,e3,e4,sep="\n")

# f

print(f)

sleep(10)



