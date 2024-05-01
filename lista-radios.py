import requests
from bs4 import BeautifulSoup

# Função para verificar se a página contém um link para o WhatsApp
def verifica_whatsapp(url):
    try:
        # Fazendo a requisição para a página
        response = requests.get(url)
        
        # Analisando o HTML da página
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Procurando por elementos que contenham "whatsapp" no atributo href
        whatsapp_links = soup.find_all('a', href=lambda href: href and 'whatsapp' in href.lower())
        
        # Verificando se há algum link encontrado
        if whatsapp_links:
            print(f'O site {url} contém um link para o WhatsApp.')
            return url  # Retorna a URL se um link para o WhatsApp for encontrado
        else:
            print(f'O site {url} não contém um link para o WhatsApp.')
            return None
    
    except Exception as e:
        print(f"Ocorreu um erro ao acessar o site {url}: {e}")
        return None

# URL da página que lista as rádios de Minas Gerais
url = 'https://www.radios.com.br/radio/uf/minas-gerais/13'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}

# Lista para armazenar URLs com links para o WhatsApp
urls_com_whatsapp = []

# Fazendo a requisição para a página
response = requests.get(url, headers=headers)

# Verificando se a requisição foi bem-sucedida
if response.status_code == 200:
    # Analisando o HTML da página
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontrando todos os itens da lista de rádios
    radio_items = soup.find_all('a', href=lambda href: href.startswith('https://www.radios.com.br/aovivo'))
    # radio_items = soup.find_all('div', class_='c-radio')

    # Iterando sobre cada item da lista
    for item in radio_items:
        # Obtendo a URL da rádio
        print(type(item))
        radio_url = item.get('href')
        print("URL da rádio:", radio_url)
        
        # Acessando a página da rádio
        radio_response = requests.get(radio_url, headers=headers)
        
        if radio_response.status_code == 200:
            radio_soup = BeautifulSoup(radio_response.content, 'html.parser')
            
            # Encontrando o link do site
            site_link = radio_soup.get('a')
            
            if site_link:
                site_url = site_link['href']
                print("Link do site:", site_url)
                
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

# Salvando as URLs com links para o WhatsApp em um arquivo
with open('urls_whatsapp.txt', 'w') as file:
    for url in urls_com_whatsapp:
        file.write(url + '\n')
