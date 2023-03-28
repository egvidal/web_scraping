'''
1)  Go to the game website and familiarise yourself with how it works: http://orteil.dashnet.org/experiments/cookie/ (classic version)
2)  Create a bot using Selenium and Python to click on the cookie as fast as possible
3)  Every 5 seconds, check the right-hand pane to see which upgrades are affordable and purchase the most expensive one.
    You'll need to check how much money (cookies) you have against the price of each upgrade.
'''


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

WAIT_TIME = 0.1

class Element():
  def __init__(self, value):
    self.value = value

  def web_element(self):
    return browser.find_element(by=By.ID, value=self.value)

class Upgrade(Element):
  total_count = 0
  def __init__(self, value):
    self.value = value
    self.count = 0
    Element(self).__init__(self.value)

  def get_text(self):
    text = self.web_element().find_element(by=By.CSS_SELECTOR, value="b").text
    return text

  def get_price(self):
    price = self.get_text().split(' -  ')[1].replace(',', '')
    return int(price)

  def buy_item(self):
    self.web_element().click()
    self.count += 1
    Upgrade.total_count += 1

  def __str__(self):
    return self.get_text()

browser = webdriver.Safari()
browser.get("http://orteil.dashnet.org/experiments/cookie/")
browser.set_window_size(1400, 550)

cookie = Element("cookie")
money = Element("money")
cps = Element("cps")
time_machine = Upgrade("buyTime machine")
portal = Upgrade("buyPortal")
alchemy_lab = Upgrade("buyAlchemy lab")
shipment = Upgrade("buyShipment")
mine = Upgrade("buyMine")
factory = Upgrade("buyFactory")
grandma = Upgrade("buyGrandma")
cursor = Upgrade("buyCursor")

upgrades = [time_machine, portal, alchemy_lab, shipment, mine, factory, grandma, cursor]
purchased_items = {}

start = time.time()

while True:
  cookie.web_element().click()
  new_time = time.time()
  if new_time >= (start + 5):
    available_money = int(money.web_element().text.replace(',', ''))
    print("\n----------------------------------------------------------------------------------------------------")
    print("Money(cookies) :", available_money, "\t", cps.web_element().text, "\tTotal upgrades :", Upgrade.total_count)
    print("\nPrices:", end='')
    for upgrade in upgrades:
      print("\n", upgrade, end='')
      current_price = upgrade.get_price()
      while available_money >= current_price:
        upgrade.buy_item()
        print("  -> Purchased!", end='')
        time.sleep(WAIT_TIME)
        purchased_items[upgrade.value] = upgrade.count
        available_money -= current_price
        current_price = upgrade.get_price()
    print("\n\nPurchased items :", purchased_items)

    start = time.time()
