from crewai import Agent, Crew, Process, Task
# from crewai.project import CrewBase, agent, crew, task
import yaml
from tools.my_custom_tool import PDFReaderTool
from crewai_tools import SerperDevTool, ScrapeWebsiteTool


# @CrewBase
class CareerSupportCrew:
  
    def __init__(self, inputs):
        
        self.inputs = inputs
        self.pdf_reader_tool = PDFReaderTool(pdf_path=inputs["pdf_path"])
        self.search_tool = SerperDevTool(n_results=1)
        self.scrape_tool = ScrapeWebsiteTool()
        
        with open('config/agents.yaml', 'r') as agents_file:
            self.agents_config = yaml.safe_load(agents_file)
        with open('config/tasks.yaml', 'r') as tasks_file:
            self.tasks_config = yaml.safe_load(tasks_file)

        self.cv_reviewer = Agent(
            config=self.agents_config['cv_reviewer'],
            verbose=True,
            allow_deligation=False,
            tools=[self.pdf_reader_tool],
            llm="gpt-3.5-turbo"
        )

        self.repo_reviewer = Agent(
            config=self.agents_config['repo_reviewer'],
            verbose=True,
            allow_deligation=True,
            llm="gpt-3.5-turbo"
        )
    
        self.career_advisor = Agent(
            config=self.agents_config['career_advisor'],
            verbose=True,
            allow_deligation=True,
            llm="gpt-3.5-turbo"
        )

        self.review_cv = Task(
        config=self.tasks_config['review_cv'],
        agent=self.cv_reviewer,
        tools=[self.pdf_reader_tool]
        )
        
        self.review_repo = Task(
        config=self.tasks_config['review_repo'],
        agent=self.repo_reviewer,
        context=[self.review_cv]
        )
        
        self.research_job_market = Task(
        config=self.tasks_config['research_job_market'],
        agent=self.career_advisor,
        tools=[self.search_tool, self.scrape_tool],
        context=[self.review_cv]
        )
        
        self.match_career = Task(
        config=self.tasks_config['match_career'],
        agent=self.career_advisor,
        context=[self.review_cv, self.review_repo, self.research_job_market],
        output_file="output/result.md"
        )
        
    # @crew
    def crew(self) -> Crew:
        """Creates cv tailor crew"""
        
        return Crew(
            agents=[self.cv_reviewer, self.repo_reviewer, self.career_advisor],
            tasks=[self.review_cv, self.review_repo, self.research_job_market, self.match_career],   
            process=Process.sequential,
            verbose=True
            # process=Process.hierarchical,  # In case you want to use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
    
