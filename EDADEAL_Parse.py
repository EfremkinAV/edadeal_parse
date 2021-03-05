import sqlite3
import sys
import traceback
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime

def auth_start():
    url_start_page = "https://edadeal.ru/tomsk/offers"
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url_start_page)
    driver.implicitly_wait(5)
    last_page = 1#int(driver.find_element_by_xpath("//div[9]/a[@class='b-button__root']").get_attribute('textContent'))7
    page_num = 1
    sqlite_connection = sqlite3.connect('edadeal_db.db')
    cursor = sqlite_connection.cursor()

    while page_num <= last_page:
        url_start = "https://edadeal.ru/tomsk/offers" + "?page=" + str(page_num)
        driver.get(url_start)
        driver.implicitly_wait(5)
        goods_card = driver.find_elements_by_class_name("b-offer__root")
        for gcard in goods_card:
            gname = gcard.find_element_by_class_name("b-offer__description").text
            try:
                gprice_dis = gcard.find_element_by_class_name("b-offer__price-new").text
            except NoSuchElementException:
                gprice_dis = 0
            try:
                gprice_old = gcard.find_element_by_class_name("b-offer__price-old").text
            except NoSuchElementException:
                gprice_old = 0
            gmarket = gcard.find_element_by_class_name("b-image.b-image_disabled_false.b-image_cap_f.b-image_img_vert.b-image_loaded_true.b-offer__retailer-icon").get_attribute("title")
            g_add_date = datetime.now().date()
            page_num += 1
            #print("НАЗВАНИЕ: ", gname)
            #print("старая цена: ", gprice_old)
            #print("Цена со скидкой: ", gprice_dis)
            #print("Магазин: ", gmarket)
            try:
                cursor.execute('INSERT INTO EDADEAL_GOODS (name,price_old,price_dis,market,add_date)'
                               'VALUES (?,?,?,?,?)', (gname, gprice_old, gprice_dis, gmarket, g_add_date,))
                sqlite_connection.commit()
                print("Запись успешно вставлена в таблицу edadeal_db ", cursor.rowcount)
            except sqlite3.Error as error:
                print("Класс исключения: ", error.__class__)
                print("Исключение", error.args)
                print("Печать подробноcтей исключения SQLite: ")
                exc_type, exc_value, exc_tb = sys.exc_info()
                print(traceback.format_exception(exc_type, exc_value, exc_tb))
    cursor.close()
    sqlite_connection.close()

# ---------------------------------------------
#user_choice = input('Please click ENTER button to close application')
#if not user_choice:
#    print("ABORTED")
#driver.close
    driver.quit()
auth_start()




