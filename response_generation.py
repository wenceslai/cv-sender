import re

from gpt_calls import *

import requests
from bs4 import BeautifulSoup


def respond(url, category):
    response = requests.get(url)

    # we cannot send cvs through websites of the employer, only through the standardised jobs.cz one
    if "www.jobs.cz" not in response.url:
        print("offer is on the website of employer, not jobs.cz")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    web_text = soup.get_text()

    start_search_i = web_text.find("Pracovní nabídka")

    if start_search_i == -1:
        print("error, the description of the job is not there")
        return

    job_desc = re.sub(r'\s{2,}', ' ', web_text[start_search_i + 16: start_search_i + 1000])

    if category == "low_income":
        # if it's a white or blue collar position
        blue_or_white_collar = classify_blue_white_collar(job_desc)
        category += "_" + blue_or_white_collar

        # if white collar position further classify if it's in contact with customers
        if blue_or_white_collar == "white":
            customer_or_internal_facing = classify_is_client_facing(job_desc)
            category += "_" + customer_or_internal_facing

    generate_pdfs(category)


def generate_pdfs():
    pass
