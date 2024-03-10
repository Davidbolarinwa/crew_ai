import os
from crewai import Agent, Task, Crew, Process
from textwrap import dedent
from crewai_tools import WebsiteSearchTool
import requests
from requests.exceptions import RequestException

os.environ["OPENAI_API_KEY"] = "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"


# Define your agents with roles and goals
class NewsletterCrew:
    def __init__(self, urls):
        self.urls = urls

    def run(self):
        scraper = Agent(
            role='Summarizer of Websites',
            goal='Ask the user for a list of URLs, then use the WebsiteSearchTool to then scrape the content, and provide the full content to the writer agent so it can then be summarized',
            backstory="""You work at a leading tech think tank.
            Your expertise is taking URLs and getting just the text-based content of them.""",
            verbose=True,  # Ensures detailed logging for the scraper, adjust as needed.
            allow_delegation=False,  # Scraper cannot delegate tasks.
            tool=WebsiteSearchTool()
        )
        writer = Agent(
            role='Tech Content Summarizer and Writer',
            goal='Craft compelling short-form content on AI advancements based on long-form text passed to you',
            backstory="""You are a renowned Content Creator, known for your insightful and engaging articles.
            You transform complex concepts into compelling narratives.""",
            verbose=False,  # Set to False if you prefer less logging for the writer, adjust as needed.
            allow_delegation=True,  # Writer can delegate tasks if necessary.
        )

        # Create tasks for your agents
        task1 = Task(
            description=f"""Take a list of websites that contain AI content, read/scrape the content and then pass it to the writer agent
            
            here are the URLs from the user that you need to scrape: {self.urls}""",
            agent=scraper,
            expected_output="A comprehensive text summary of the specified URLs, highlighting key points, findings, and themes related to AI advancements. The summary should include important details such as major technological breakthroughs, research findings, industry trends, and expert opinions extracted from the content. This detailed summary will enable the writer agent in task2 to develop insightful and engaging short-form content."
        )

        task2 = Task(
            description="""Using the text provided by the scraper agent, develop a short and compelling/interesting short-form summary of the 
            text provided to you about AI""",
            agent=writer,
            expected_output="A concise, engaging summary that distills the key points from the comprehensive AI content analysis provided by the first task. This summary should capture the essence of the AI advancements, trends, and significant insights in a manner that is both entertaining and enlightening. It should weave the complex ideas and technical concepts into a narrative that is accessible to readers with varying levels of expertise in AI, making the content not only informative but also enjoyable to read. The final piece should inspire curiosity about AI, encouraging further exploration of the subject matter."
        )

        # Instantiate your crew with a sequential process
        newsletter_crew = Crew(
            agents=[scraper, writer],
            tasks=[task1, task2],
            verbose=2,  # You can set it to 1 or 2 for different logging levels
        )

        try:
            newsletter_crew.kickoff()
        except RequestException as e:
            print(f"An error occurred during web scraping: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("## Welcome to Newsletter Writer")
    print('-------------------------------')
    urls = input(
        dedent("""
        What is the URL you want to summarize?
        """)
    )

    newsletter_crew = NewsletterCrew(urls)

    result = newsletter_crew.run()

    print("\n\n########################")
    print("## Here is the Result")
    print("########################\n")
    print(result)
