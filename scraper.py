from langchain.chains import LLMChain, LLMRequestsChain
from constant_templates import Job_Description_Template
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# function to scrape the job description and qualifications from the job website for the company url fetched
def company_scraper(company_url:str):
    openai_api_key = 'YOUR_API_KEY'
    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo', openai_api_key=openai_api_key)

    prompt = PromptTemplate(input_variables=["requests_result"], template=Job_Description_Template)

    chain = LLMRequestsChain(llm_chain=LLMChain(llm=llm, prompt=prompt))

    inputs = {"url": company_url}
    result = chain.run(inputs)
    return result

