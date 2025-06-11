# Multi-agent AI CV Advisor

Welcome to the Multi-agent AI CV Advisor Crew project, powered by [crewAI](https://crewai.com). 
This coach help tailoring the user's CV for your suitabale career role. The Multi-agent AI CV Advisor analyze the user's CV and repository (if the link is provided) and suggest imrpovement for the CV and a suitable job role by searching current job market demand. 


**Input:**
- CV in a PDF format

    - You can also find sample CV (long and short version) under ./cv_advisor/src/ai_cv_advisor_data

**Output:**
- A Markdown file contains the quality of the CV with scores, alignment of the CV wih current job market, and CV tailoring and job role recommendations

## Running app

Create an environment and install the dependencies:

```
pip install -r requirements.txt
```

Add your `OPENAI_API_KEY` and `SERPER_API_KEY`into the `.env` file:

Go to https://serper.dev if you don't have `SERPER_API_KEY`.

```
export OPENAI_API_KEY=<your-openai-api-key>
```
```
export SERPER_API_KEY=<your-serper-api-key>
```

Start application by running this from ./cv_advisor/src/ai_cv_advisor:
```bash
$ uvicorn app.api:app --reload
```
