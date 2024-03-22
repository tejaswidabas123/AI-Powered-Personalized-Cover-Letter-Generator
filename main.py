from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from website_url_fetcher import lookup as company_lookup_agent
from scraper import company_scraper
from constant_templates import Task_Description_Template
from datetime import date

def create_cover_letter(company: str, role: str, resume: str, name: str, hr_name: str, email: str):
    openai_api_key = 'YOUR_API_KEY'

    company_url_text = company_lookup_agent(company=company, role=role)
    print('company_url_text', company_url_text)
    # Extracting the URL from the text
    company_url = company_url_text.split("is ")[-1].strip()
    print("company_url:", company_url)

    job_desc = company_scraper(company_url=company_url)

    current_date = date.today().strftime("%B %d, %Y")

    summary_prompt_template = PromptTemplate(
        input_variables=["job_information", "resume", "name_of_company", "role", "name_of_candidate", "hr_name",
                         "email", "today_date"],
        template=Task_Description_Template)

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    return chain.run(job_information=job_desc, resume=resume, name_of_company=company, role=role,
                     name_of_candidate=name, hr_name=hr_name, email=email, today_date=current_date)
