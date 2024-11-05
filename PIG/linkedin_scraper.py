from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

# Demander les identifiants à l'utilisateur
email = input("Entrez votre adresse e-mail LinkedIn : ")
password = input("Entrez votre mot de passe LinkedIn : ")

# Démarrer le navigateur
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
driver.get("https://www.linkedin.com/login")

# Entrer les identifiants
driver.find_element_by_id('username').send_keys(email)
driver.find_element_by_id('password').send_keys(password)

# Soumettre le formulaire de connexion
driver.find_element_by_css_selector('.login__form_action_container button').click()

profile_url = 'https://www.linkedin.com/in/florian-andre-a636b12ab/'
driver.get(profile_url)


# Get the page source
page_source = driver.page_source# Parse the HTML using Beautiful Soup
soup = BeautifulSoup(page_source, 'html.parser')# Extract the name and headline
name = soup.find('li', {'class': 'inline t-24 t-black t-normal break-words'}).text.strip()
headline = soup.find('h2', {'class': 'mt1 t-18 t-black t-normal break-words'}).text.strip()# Print the extracted data
print('Name:', name)
print('Headline:', headline)