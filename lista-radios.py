import requests
import re
from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import Bys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException

# Função para verificar se a página contém um link para o WhatsApp
def verifica_whatsapp(url):
    try:
        # Fazendo a requisição para a página
        response = requests.get(url, headers=headers)

        if response.status_code == 200:

            print("Url acessada:", url)

            # Encontrando todas as ocorrências do texto desejado no conteúdo HTML
            matches = re.findall(r'phone=(\d+)', response.content.decode('utf-8', errors='ignore'))

            # Se não houver correspondências com o primeiro padrão, tentar com o segundo padrão
            if not matches:
                matches = re.findall(r'https://wa\.me/(\d+)', response.content.decode('utf-8', errors='ignore'))

            # Verificando se há pelo menos uma correspondência
            if matches:
                # Pegar apenas o primeiro match encontrado
                phone_number = matches[0]
                print("Número de telefone do WhatsApp:", phone_number)
                print("\n")
                return phone_number
            
            else:
                print("Url com erro:", url)
                print("Erro", response)
                print("HTTP status code", response.status_code)
                print("\n")
                return None
    
    except Exception as e:
        print(f"Ocorreu um erro ao acessar o site {url}: {e}")
        print("\n")
        return None
    
# def esperar_pagina_carregar(url, timeout=10):
#     try:
#         # Inicialize o driver do navegador
#         driver = webdriver.Chrome()
        
#         # Abra a página desejada
#         driver.get(url)
        
#         # Espere até que a página seja completamente carregada
#         WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
#         print("Página completamente carregada!")
        
#         # Retorna o driver para que você possa usá-lo para interagir com a página
#         return driver
    
#     except TimeoutException:
#         print("Tempo limite excedido ao esperar pelo carregamento da página.")
#         return None

# # Exemplo de uso da função
# url = "https://www.atenasfm.com.br/"
# driver = esperar_pagina_carregar(url)

# if driver:
#     # Agora você pode prosseguir com o restante do seu código para interagir com a página
#     # Por exemplo, você pode acessar o HTML da página usando driver.page_source
#     html = driver.page_source
    
#     # Não se esqueça de fechar o navegador quando terminar
#     driver.quit()
    
    
# limite de paginas para a url de MG
limite_paginas_MG = 129

# indice da pagina atual
indice_pagina = 0

# header para a requisição
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}

# Lista para armazenar URLs com links para o WhatsApp
urls_com_whatsapp = []

# verifica_whatsapp('https://www.atenasfm.com.br/')

while indice_pagina <= limite_paginas_MG:

    # URL da página que lista as rádios de Minas Gerais
    url = f'https://www.radios.com.br/radio/uf/minas-gerais/13?pg={indice_pagina}'

    # Fazendo a requisição para a página
    response = requests.get(url, headers=headers)

    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Analisando o HTML da página
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontrando todos os itens da lista de rádios
        radio_items = soup.find_all('a', href=lambda href: href.startswith('https://www.radios.com.br/aovivo'))
        # radio_items = soup.find_all('div', class_='c-radio')

        h3_elements = soup.find_all('h3')

        # Iterando sobre cada elemento <h3>
        for h3_element in h3_elements:
            # Encontrando todos os elementos <a> dentro do <h3> atual
            radio_items = h3_element.find_all('a', href=lambda href: href.startswith('https://www.radios.com.br/aovivo'))

            # Iterando sobre cada item da lista
            for item in radio_items:
                # Obtendo a URL da rádio
                radio_url = item.get('href')

                if radio_url == None:
                    continue
                
                # Acessando a página da rádio
                radio_response = requests.get(radio_url, headers=headers)
                
                if radio_response.status_code == 200:
                    radio_soup = BeautifulSoup(radio_response.content, 'html.parser')
                    
                    # Encontrando o link do site
                    # site_link = radio_soup.get('a')

                    site_labels = radio_soup.find_all('b', text='Site:')

                    if not site_labels:
                        continue

                    site_link = site_labels[0].find_next_sibling('a', href=True)
                    
                    if site_link:
                        site_url = site_link['href']
                        
                        # Verificando se o site contém um link para o WhatsApp
                        whatsapp_url = verifica_whatsapp(site_url)
                        if whatsapp_url:
                            urls_com_whatsapp.append(whatsapp_url)
                        
                    else:
                        print("Nenhum link para o site encontrado.")
                
                else:
                    print("Falha ao acessar a página da rádio:", radio_url)
    else:
        print("Falha ao acessar a página:", url)

    indice_pagina = indice_pagina + 1

# Salvando as URLs com links para o WhatsApp em um arquivo
with open('urls_whatsapp.txt', 'w') as file:
    for url in urls_com_whatsapp:
        file.write(url + '\n')
