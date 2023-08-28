import re

from gpt_calls import *
from constants import *
from helpers import *

import random
import time
import requests
from bs4 import BeautifulSoup
import pdfkit


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
    print(job_desc)
    if category == "low_income":
        # if it's a white or blue collar position
        blue_or_white_collar = classify_blue_white_collar(job_desc)
        category += "_" + blue_or_white_collar

        # if white collar position further classify if it's in contact with customers
        if blue_or_white_collar == "white":
            customer_or_internal_facing = classify_is_client_facing(job_desc)
            category += "_" + customer_or_internal_facing

    generate_category_pdfs(category, job_desc, url)

    # mine the website


def generate_category_pdfs(category, job_desc, url):
    sex = random.choice(["male", "female"])
    hq_exps = random.randint(*HIGH_QUALIF_EXPS_RANGE)
    lq_exps = random.randint(*LOW_QUALIF_EXPS_RANGE)

    first_name_i = generate_unique_index((0, len(ROMA_FIRST_NAMES[sex]) - 1), [])
    last_name_i = generate_unique_index((0, len(ROMA_LAST_NAMES[sex]) - 1), [])
    roma_hq_name = ROMA_FIRST_NAMES[sex][first_name_i] + " " + ROMA_LAST_NAMES[sex][last_name_i]

    first_name_i = generate_unique_index((0, len(ROMA_FIRST_NAMES[sex]) - 1), [first_name_i])
    last_name_i = generate_unique_index((0, len(ROMA_LAST_NAMES[sex]) - 1), [last_name_i])
    roma_lq_name = random.choice(ROMA_FIRST_NAMES[sex][first_name_i]) + " " + random.choice(ROMA_LAST_NAMES[sex][last_name_i])

    first_name_i = generate_unique_index((0, len(WHITE_FIRST_NAMES[sex]) - 1), [])
    last_name_i = generate_unique_index((0, len(WHITE_LAST_NAMES[sex]) - 1), [])
    white_hq_name = WHITE_FIRST_NAMES[sex][first_name_i] + " " + WHITE_LAST_NAMES[sex][last_name_i]

    # white, low qualf
    first_name_i = generate_unique_index((0, len(WHITE_FIRST_NAMES[sex]) - 1), [first_name_i])
    last_name_i = generate_unique_index((0, len(WHITE_LAST_NAMES[sex]) - 1), [last_name_i])
    white_lq_name = WHITE_FIRST_NAMES[sex][first_name_i] + " " + WHITE_LAST_NAMES[sex][last_name_i]

    if category == "high_income":
        education_type = "vysoké škole"
    else:
        education_type = "střední škole"

    template_nums = [1, 2, 3, 4]
    random.shuffle(template_nums)

    dir_path = f"generated-cvs/{int(time.time())}"
    os.mkdir(dir_path)

    generate_pdf(category + "_roma_high_qualif", roma_hq_name, hq_exps, education_type, job_desc, template_nums[0], url, dir_path)
    generate_pdf(category + "_roma_low_qualif", roma_lq_name, lq_exps, education_type, job_desc, template_nums[1], url, dir_path)
    generate_pdf(category + "_white_high_qualif", white_hq_name, hq_exps, education_type, job_desc, template_nums[2], url, dir_path)
    generate_pdf(category + "_white_low_qualif", white_lq_name, lq_exps, education_type, job_desc, template_nums[3], url, dir_path)


def generate_pdf(tag, name, exps_num, education_type, job_desc, template_number, url, dir_path):
    with open(f'cv-html-templates/template{template_number}.html', 'r') as file:
        html_content = file.read()

        job_exps = generate_job_experiences(job_desc, exps_num)
        education = generate_education(job_desc, education_type)

        filled_html = html_content % {"name": name, "education": education, "job_exps": job_exps}

        # saving file with metadata
        with open(os.path.join(dir_path, "details.txt"), "w") as file:
            file.write(job_desc + "\n" + url)

        # generating the pdf
        pdfkit.from_string(filled_html, f"{dir_path}/{tag}.pdf")
