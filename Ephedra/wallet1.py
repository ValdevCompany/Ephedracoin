from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Инициализация веб-драйвера
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Запуск без графического интерфейса
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Открытие страницы
url = "https://www.coingecko.com/en"
driver.get(url)
time.sleep(5)  # Даем время для загрузки JavaScript

# Находим все строки с криптовалютами
rows = driver.find_elements(By.CSS_SELECTOR, 'tr.table-hover')

polygon_tokens = []

# Проходим по всем строкам и ищем токены с ростом < 5% и которые относятся к Polygon
for row in rows:
    try:
        # Извлекаем название токена
        name = row.find_element(By.CSS_SELECTOR, 'td.coin-name a').text.strip()

        # Извлекаем процент изменения за 24 часа
        growth_24h = row.find_element(By.CSS_SELECTOR, 'td.td-change24h').text.strip().replace('%', '')
        growth_24h = float(growth_24h)

        # Фильтруем токены, чье название содержит 'Polygon' и процент роста < 5%
        if growth_24h < 5 and 'Polygon' in name:
            polygon_tokens.append({
                "name": name,
                "24h_growth": growth_24h
            })
    except Exception as e:
        continue

# Закрываем браузер
driver.quit()

# Выводим результаты
if polygon_tokens:
    for token in polygon_tokens:
        print(f"Token: {token['name']}, 24h Growth: {token['24h_growth']}%")
else:
    print("No Polygon-based tokens with < 5% growth found.")
