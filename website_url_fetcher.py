from langchain.utilities import SerpAPIWrapper
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
import streamlit as st

# custom serp api wrapper for searching the company's job description page
class CustomSerpAPIWrapperJobSearch(SerpAPIWrapper):
    def __init__(self):
        serpapi_api_key = 'YOUR_API_KEY'
        super(CustomSerpAPIWrapperJobSearch, self).__init__(serpapi_api_key=serpapi_api_key)

    @staticmethod
    def _process_response(res: dict) -> str:
        """Process response from SerpAPI."""
        if "error" in res.keys():
            raise ValueError(f"Got error from SerpAPI: {res['error']}")
        if "answer_box" in res.keys() and "answer" in res["answer_box"].keys():
            toret = res["answer_box"]["answer"]
        elif "answer_box" in res.keys() and "snippet" in res["answer_box"].keys():
            toret = res["answer_box"]["snippet"]
        elif (
                "answer_box" in res.keys()
                and "snippet_highlighted_words" in res["answer_box"].keys()
        ):
            toret = res["answer_box"]["snippet_highlighted_words"][0]
        elif (
                "sports_results" in res.keys()
                and "game_spotlight" in res["sports_results"].keys()
        ):
            toret = res["sports_results"]["game_spotlight"]
        elif (
                "knowledge_graph" in res.keys()
                and "description" in res["knowledge_graph"].keys()
        ):
            toret = res["knowledge_graph"]["description"]
        elif "snippet" in res["organic_results"][0].keys():
            toret = res["organic_results"][0][
                "link"]  # The source code assigns the snippet to toret, but we want the link
        else:
            toret = "No good search result found"
        return toret


def get_job_description(company: str):
    """Searches for the company's job description page"""
    search = CustomSerpAPIWrapperJobSearch()
    resp = search.run(f"{company}")
    print(f"SerAPI response: {resp}")
    return resp


def lookup(company: str, role: str) -> str:
    # openai api key
    openai_api_key = 'YOUR_API_KEY'
    # GPT LLM model
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

    template = """ Given the company name: {name_of_company} I want you to find the URL to their {role} position.
            Your answer should contain only the URL of the page where the job position is posted.
            If you cannot find the URL, please say so, and do not make up an answer.
            """

    # for search run function
    tools_for_agent = [
        Tool(name="Crawl google 4 a company job description page",
             func=get_job_description,
             description="Useful for when you need to get the job description page URL")
    ]
    # initializing the agent
    agent = initialize_agent(tools_for_agent, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    # promptTemplate of langchain makes constructing prompts with dynamic inputs easier
    prompt_template = PromptTemplate(input_variables=['name_of_company', 'role'], template=template)

    company_page = agent.run(prompt_template.format_prompt(name_of_company=company, role=role))
    return company_page
