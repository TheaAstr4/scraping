import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from pyairtable import Api
import agentql

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
os.environ["AGENTQL_API_KEY"] = os.getenv("AGENTQL_API_KEY")

EMAIL_INPUT_QUERY = """
{
    login_form{
        email_input
        password_input
        signin_btn
    }
}
"""


INITIAL_URL = "https://www.linkedin.com/checkpoint/lg/sign-in-another-account"
JOBS_URL = "https://www.linkedin.com/jobs/"

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
    job_list[]{
        title
        comapany_name
        location
    }
}
"""

with sync_playwright() as playwright, playwright.firefox.launch(headless=False) as browser:
    page = agentql.wrap(browser.new_page())
    page.goto(INITIAL_URL)

    response = page.query_elements(EMAIL_INPUT_QUERY)
    response.login_form.email_input.fill(EMAIL)
    page.wait_for_timeout(1000)
    response.login_form.password_input.fill(PASSWORD)
    page.wait_for_timeout(1000)
    response.login_form.signin_btn.click()
    page.wait_for_timeout(10000)

    page.goto(JOBS_URL)
    page.wait_for_timeout(10000)
    
    response = page.query_elements(JOB_QUERY)
    
    # Interacting with the correct elements
    position_input = response.job_form.position_input
    location_input = response.job_form.location_input

    # Filling in the job search fields
    position_input.fill("TI")
    page.wait_for_timeout(1000)
    location_input.fill("Brasil")
    page.wait_for_timeout(1000)

    location_input.press("Enter")
    page.wait_for_timeout(10000)

    response = page.query_elements(JOB_LIST_QUERY)
    job_posts = response.job_list
    job_posts = job_posts.to_data()
    print(job_posts)





    



