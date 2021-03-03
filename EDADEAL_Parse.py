import sqlite3
import sys
import traceback
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def auth_start():

    url_start_page = "https://edadeal.ru/tomsk/offers"
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url_start_page)
    driver.implicitly_wait(5)
    last_page = 1#int(driver.find_element_by_xpath("//div[9]/a[@class='b-button__root']").get_attribute('textContent'))
    page_num = 1
    #print("Всего страниц найдено: " + str(last_page))

    sqlite_connection = sqlite3.connect('edadeal_db.db')
    cursor = sqlite_connection.cursor()

    while page_num <= last_page:
        url_start = "https://edadeal.ru/tomsk/offers" + "?page=" + str(page_num)
        driver.get(url_start)
        driver.implicitly_wait(5)
        goods_card = driver.find_elements_by_class_name("b-offer__root")
        for gcard in goods_card:
            gname = gcard.find_element_by_class_name("b-offer__description").text
            gprice_dis = gcard.find_element_by_class_name("b-offer__price-new").text
            gprice_old = gcard.find_element_by_class_name("b-offer__price-old").text
            gmarket = gcard.find_element_by_class_name("b-image.b-image_disabled_false.b-image_cap_f.b-image_img_vert.b-image_loaded_true.b-offer__retailer-icon").get_attribute("title")
            page_num += 1
            #a.p-offers__offer:nth-child(1) > div.b-offer.b-offer_disabled_false.b-offer_view_default.b-offer_is-outdated_false.b-offer_is-added-to-cart_false:nth-child(1) > div.b-offer__root:nth-child(1) > div.b-offer__header:nth-child(1) > div.b-offer__offer-info:nth-child(2) > div.b-offer__dates:nth-child(2) > div.b-image.b-image_disabled_false.b-image_cap_f.b-image_img_vert.b-image_loaded_true.b-offer__retailer-icon:nth-child(1) > div.b-image__root:nth-child(1) > img
            ##v<div title="Лента Гипермаркет" class=""><div class="b-image__root"><div class="b-image__cap b-image__cap_loading_false"
            #print(gname)
            #print(gprice_old)
            #print(gprice_dis)
            #print(gmarket)
            try:
                #ДБАВИТЬ ПРОПКУСК ОШИБОК ЕЛСИ ЭЛЕМЕНТ НЕ НАЙДЕН!!!!
                cursor.execute('INSERT INTO EDADEAL_GOODS (name,price_old,price_dis,market) VALUES (?,?,?,?)', (gname, gprice_old, gprice_dis, gmarket))
                sqlite_connection.commit()
                print("Запись успешно вставлена в таблицу edadeal_db ", cursor.rowcount)
            except sqlite3.Error as error:
                print("Не удалось вставить данные в таблицу sqlite")
                print("Класс исключения: ", error.__class__)
                print("Исключение", error.args)
                print("Печать подробноcтей исключения SQLite: ")
                exc_type, exc_value, exc_tb = sys.exc_info()
                print(traceback.format_exception(exc_type, exc_value, exc_tb))
            except NoSuchElementException as err:
                print("Не могу найти элемент")
                print("Класс исключения: ", err.__class__)
                print("Исключение", err.args)
                print("Печать подробноcтей исключения: ")
                exc_type, exc_value, exc_tb = sys.exc_info()
                print(traceback.format_exception(exc_type, exc_value, exc_tb))

    cursor.close()
    sqlite_connection.close()
# ---------------------------------------------
#user_choice = input('Please click ENTER button to close application')
#if not user_choice:
#    print("ABORTED")
#driver.close()
    driver.quit()
auth_start()




