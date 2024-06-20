import chromedriver_autoinstaller
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


chromedriver_autoinstaller.install()


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    # Установка неявного ожидания
    driver.implicitly_wait(10)
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    driver.maximize_window()
    yield driver

    driver.quit()


'''Тест: Присутствуют все питомцы'''


def test_show_all_pets(driver):
    # Установка явного ожидания появления поля ввода "email"
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, 'email')))
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('sergejs.bogdanovs.2011@gmail.com')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('BogSer')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Установка явного ожидания появления кнопки "Мои питомцы"
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a')))
    # Переходим в раздел Мои питомцы
    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()

    # Установка явного ожидания появления карточек питомцев
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH,
                                                                    '//table[@class="table table-hover"]/tbody/tr')))
    # Получаем колличество питомцев отображаемое в статистике
    pets_number = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    # Получаем колличество карточек питомцев
    pets_count = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')

    # Проверяем, что эти два параметра равны
    assert int(pets_number) == len(pets_count)


'''Тест: Хотя бы у половины питомцев есть фото'''


def test_half_of_pets_have_photo(driver):
    # Установка явного ожидания появления поля ввода "email"
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, 'email')))
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('sergejs.bogdanovs.2011@gmail.com')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('BogSer')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Установка явного ожидания появления кнопки "Мои питомцы"
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a')))
    # Переходим в раздел Мои питомцы
    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()

    # Установка явного ожидания появления карточек питомцев
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH,
                                                                    '//table[@class="table table-hover"]/tbody/tr')))

    # Получаем путь к фото
    images = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/th/img')
    # Получаем колличество карточек питомцев
    names = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    count_photo = 0

    # Считаем колличество карточек с фото
    for i in range(len(names)):
        if images[i].get_attribute('src') != '':
            count_photo += 1
    # Проверяем, что хотя бы у половины питомцев есть фото
    assert len(names) / 2 <= count_photo


'''Тест: У всех питомцев есть имя, возраст и порода'''


def test_all_pets_have_descriptions(driver):
    # Установка явного ожидания появления поля ввода "email"
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, 'email')))
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('sergejs.bogdanovs.2011@gmail.com')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('BogSer')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Установка явного ожидания появления кнопки "Мои питомцы"
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a')))
    # Переходим в раздел Мои питомцы
    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()

    # Установка явного ожидания появления карточек питомцев
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH,
                                                                    '//table[@class="table table-hover"]/tbody/tr')))

    # Получаем имена
    names = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[1]')
    # Получаем породы
    breed = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[2]')
    # Получаем возраст
    age = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[3]')

    # Проверяем, что у всех питомцев есть имя, возраст и порода
    for i in range(len(names)):
        assert names[i].text != ''
        assert breed[i].text != ''
        assert age[i].text != ''


'''Тест: У всех питомцев разные имена'''


def test_all_pets_have_differents_names(driver):
    # Установка явного ожидания появления поля ввода "email"
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, 'email')))
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('sergejs.bogdanovs.2011@gmail.com')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('BogSer')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Установка явного ожидания появления кнопки "Мои питомцы"
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a')))
    # Переходим в раздел Мои питомцы
    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()

    # Установка явного ожидания появления карточек питомцев
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH,
                                                                    '//table[@class="table table-hover"]/tbody/tr')))

    # Получаем имена
    names = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[1]')

    list_names = [name.text for name in names]  # имена в списке

    # Проверка уникальности имен
    unique_names = set(list_names)
    assert len(unique_names) == len(list_names)


'''Тест: В списке нет повторяющихся питомцев'''


def test_all_pets_is_unique(driver):
    # Установка явного ожидания появления поля ввода "email"
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, 'email')))
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('sergejs.bogdanovs.2011@gmail.com')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('BogSer')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Установка явного ожидания появления кнопки "Мои питомцы"
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a')))
    # Переходим в раздел Мои питомцы
    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()

    # Установка явного ожидания появления карточек питомцев
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH,
                                                                    '//table[@class="table table-hover"]/tbody/tr')))

    # Получем список питомцев
    pet = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')

    # Проверяем, что в списке нет повторяющихся питомцев
    for i in range(len(pet) - 1):
        for j in range(i + 1, len(pet)):
            assert pet[i].text != pet[j].text
