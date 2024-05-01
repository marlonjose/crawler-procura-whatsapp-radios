from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Configuração do ChromeDriver, substitua o caminho pelo local onde você baixou o ChromeDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Executar em modo headless, sem abrir a janela do navegador
driver = webdriver.Chrome(executable_path='/caminho/para/chromedriver', options=chrome_options)

# Número de telefone para enviar a mensagem (incluindo o código do país, sem símbolos)
numero_whatsapp = "551234567890"

# Mensagem a ser enviada
mensagem = "teste"

# URL para acessar o WhatsApp Web
url_whatsapp = "https://web.whatsapp.com/send?phone=" + numero_whatsapp + "&text=" + mensagem

# Abre a página do WhatsApp Web
driver.get(url_whatsapp)

# Espera alguns segundos para a página carregar completamente
time.sleep(10)

# Envia a mensagem pressionando Enter
driver.find_element_by_css_selector('footer div._13mgZ').send_keys(Keys.ENTER)

# Aguarda 5 segundos antes de fechar o navegador
time.sleep(5)

# Fecha o navegador
driver.quit()
