import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from pyairtable import Api
import agentql
import time

# Carregar variáveis de ambiente
load_dotenv()

# Variáveis de configuração
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
AGENTQL_API_KEY = os.getenv("AGENTQL_API_KEY")
os.environ["AGENTQL_API_KEY"] = AGENTQL_API_KEY

# Consultas GraphQL
EMAIL_INPUT_QUERY = """
{
    login_form {
        email_input
        password_input
        signin_btn
    }
}
"""

JOB_QUERY = """
{
    job_form {
        position_input
        location_input
    }
}
"""

JOB_LIST_QUERY = """
{
    job_list[] {
        title
        company_name
        location
        type
    }
}
"""

# URLs
INITIAL_URL = "https://www.linkedin.com/checkpoint/lg/sign-in-another-account"
JOBS_URL = "https://www.linkedin.com/jobs/"

def login_to_linkedin(page):
    """Função para realizar login no LinkedIn."""
    print("Realizando login...")
    response = page.query_elements(EMAIL_INPUT_QUERY)
    response.login_form.email_input.fill(EMAIL)
    time.sleep(1)  # Aguardar para garantir a interação
    response.login_form.password_input.fill(PASSWORD)
    time.sleep(1)
    response.login_form.signin_btn.click()
    time.sleep(5)  # Aguardar o carregamento da página após o login

def search_jobs(page):
    """Função para realizar busca de vagas no LinkedIn."""
    print("Buscando vagas de TI no Brasil...")
    response = page.query_elements(JOB_QUERY)
    
    # Preenchendo os campos de busca
    position_input = response.job_form.position_input
    location_input = response.job_form.location_input

    position_input.fill("TI")
    time.sleep(1)
    location_input.fill("Brasil")
    time.sleep(1)

    location_input.press("Enter")
    time.sleep(5)  # Aguardar o carregamento dos resultados

    return page.query_elements(JOB_LIST_QUERY)

def extract_job_posts(response):
    """Função para extrair e exibir as informações das vagas."""
    print("Extraindo vagas...")
    job_posts = response.job_list
    job_posts = job_posts.to_data()
    
    for job in job_posts:
        print(f"Título: {job['title']}")
        print(f"Empresa: {job['company_name']}")
        print(f"Localização: {job['location']}")
        print(f"Tipo de Vaga: {job['type']}")
        print("-" * 50)

def main():
    """Função principal que orquestra o fluxo de scraping."""
    with sync_playwright() as playwright:
        with playwright.firefox.launch(headless=False) as browser:
            page = agentql.wrap(browser.new_page())
            
            # Acessando a página inicial de login
            page.goto(INITIAL_URL)
            login_to_linkedin(page)

            # Acessando a página de vagas de emprego
            page.goto(JOBS_URL)
            time.sleep(5)

            # Buscando vagas e extraindo as informações
            response = search_jobs(page)
            extract_job_posts(response)

if __name__ == "__main__":
    main()
