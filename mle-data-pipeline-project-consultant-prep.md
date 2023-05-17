# Practical mini-project: data pipeline with modern data stack

## Aim

Demand for skills in modern data stack (MDS) and analytics engineering is growing, as more organisations become mature in their data roadmap. Junior Consultants going through placement allocation process should feel prepared **to talk about their experience and/ or understanding of the typical MDS tools**, what they do, what problem they solve and where in the data process they fit.

To develop understanding of and experience with the data processing journey using MDS, consultants are tasked with completing a mini-project on a dataset of their choice, or a dataset relevant to the industry sector for the potential client.

The completion of the end-to-end mini-project provides basis to prepare for interview questions and talk about previous experience. See final **"After the project"** section in this document for next steps.

## Project statement

To validate your understanding of the data processing journey, you are tasked with building a Snowflake-dbt-Power BI data pipeline using datasets of your choice.

### Data sources:
You can pick a dataset of interest from, e.g.:
- [Kaggle datasets](https://www.kaggle.com/datasets)

Topics vary from NYC taxi data, to emissions, food, music, mental health and other topics. Think of your interests and pick a dataset that is interesting to you. Your analytics on dbt shouldn't be complicated, the point of this exercise is to build an end-to-end pipeline, so don't overthink the dataset choice too much.

An example could be to choose a chocolate dataset and analyse consumption per country, etc.



### Pipeline steps:

On a higher level, your data pipeline should include the following steps:
1. Load the chosen data from local storage to a raw table in Snowflake
2. Run dbt job to trigger data transformations, running a testing suite and documentation for your models via dbt 
3. Display a dashboard connecting final data transformations on Snowflake to Power BI
4. For MLE consultants: Build a machine learning model and demonstrate any inferences and/ or predictions you manage to generate with the dataset you chose.
*5. Deploy to Snowflake following x...
 

### Success criteria:
- [ ] Final data product is available on Snowflake
- [ ] Dashboard exists and connects Power BI to final data product(s) on Snowflake
- [ ] Individual repository on Azure DevOps contains your dbt project as a codebase
- [ ] 

---

## Project pre-requisites:

Before you begin working on your data pipeline, make sure you have the following:

- [ ] Snowflake account
  - [ ] `raw` database
  - [ ] dedicated schema in `raw` database for your raw dataset(s)
- [ ] [SnowSQL CLI](https://developers.snowflake.com/snowsql/) to upload data from local to snowflake
  - [ ] SnowSQL allows to upload data form local storage to Snwoflake stage using PUT command, e.g. `put file://<path_to_file_locally> @%table_name`
- [ ] dbt Cloud 
  - [ ] dedicated "account" on dbt for this project (remember how we created 2 accounts for training?)
- [ ] Azure DevOps repository for this project to link your dbt Cloud repository

## Detailed pipeline steps:

### Step 1: Load data from kaggle to Snowflake
Once you've chosen the data for modelling, make sure your explore it:
- what format if your data in? Is it tabular or semi-structured?
- what questions can you answer with this data? What models will you build on dbt? What data product(s) you will be able to create? What predictions could you generate from the data?

Once you are happy with your dataset, land it to a stage in Snowflake.

- Do you remember a command line utility you can use to upload a local file to Snowflake account? What command does the upload?
- What command loads data from files to a table in Snowflake?
- You are encouraged to use database `raw` as this follows best practice. But make sure you create appropriate schema for your source table


### 2. Build your dbt project for data transformations, creating a testing suite and documentation for your models via dbt 

- Create a new "account" on dbt Cloud dedicated for this project (same email, just new "account" for a new project from top-right corner).
- Make sure you have source(s) and staging model(s) defined
- Make sure you build a testing suite for your data, using both generic and singular tests, where required
- Make sure you document your source, staging and mart models.
- Once you are happy with your dbt project, you need to deploy it. 

### 3. Create analytical dashboards with a tool of your choice (Power BI is highly suggested)
Once you are happy you've derived transformations on dbt and produced analytical views/ tables that got landed to Snowflake, build a dashboard with KPIs and metrics you've produced.

- Connect Power BI to Snowflake
- Build dashboards on final models you've produced via dbt to display your analytics

### 4. Build predictive models with the transformed data
- Once you have persisted your transformed data in Snowflake via dbt, it's time to get creative and build your predictions.
- Where would you experiment and build your models on? How would you access the transformed data models from Snowflake? Is there a snowflake-python connector you could use?

### 4. Build predictive model with the transformed data using Snowpark
- Once you have persisted your transformed data in Snowflake via dbt, it's time to get creative and build your predictions
- With the snowpark python connector, create a machine learning model using snowpark. This can be completed within vscode
- To get you started, follow the Snowpark quickstarter guide (help regarding the setup of the python environment can be seen below) - https://quickstarts.snowflake.com/guide/getting_started_snowpark_machine_learning/?index=..%2F..index#0

### 5. Integrate Snowflake into Streamlit
- Create an interactive dashboard using Streamlit, hosted on a local server
- Get creative! What could be useful to show on this dashboard and what purpose does it have
- To begin with, checkout the quickstarter guide, which should give you everything you need to get the ball rolling - https://quickstarts.snowflake.com/guide/getting_started_with_snowpark_for_python_streamlit/index.html#5

---

## A successful pipeline

In the end, your pipeline will load file from kaggle to a stage in Snowflake, from the staged file to a raw table in Snowflake, run transformation jobs on dbt based on the data transformations that you will build and the transformations manifest as a dashboard in Power BI. Additionally, you will be able to consume the transformed data to create predictive models from it too.

## Useful resources:
- [Kaggle - datasets](https://www.kaggle.com/datasets)
- [Snowflake Quickstarts on ML with Snowpark](#TODO)

---

## Snowpark and Streamlit setup help

### Snowpark python environment

### Streamlit
If the virtual environment has been setup correctly, then the only install that is required is the streamlit python package, installed with:
```bash 
pip install streamlit
```
This will allow you to start the guide on step 3. The connection to snowflake is established as was done in the snowpark guide, however, in step 8, the guide instead puts the account credentials in a json file and loads them into the streamlit app file.

---

## After the project
Once you've completed the project, you want to make sure you can talk about your experience in an interview. Please find below some guidelines.

### What was your experience using x?
When preparing for the interview, always plan for a "previous experience" question, e.g.:
- Tell me how have you used x before?
- What is your previous experience with Snowflake?

You can navigate how the interview will go based on what you will answer to this question. So make sure you structure your answer well and highlight in your answer the parts of the technology you are most comfortable talking about, based on your previous experience (training, this project, final 2-week project, etc.).

When structuring your answer, have a clean beginning-middle-end. Introduce the setting for the project, why were you doing it, what was your role in it. What did you deliver exactly? Was it a pipeline that feeds a dashboard? Does it run on a schedule or a trigger? What business questions have your tech skills helped to solve? Compare the "before" and the "after".

Even if this question won't be asked, this interview preparation trick ensures you have consolidated your understanding of the technologies you have used and why, as well as experience and clearly. 

### Using chatbots to help with interview preparation
Now that you have completed an applied project, you can leverage chatbots, e.g. [ChatGPT](https://chat.openai.com/), to generate potential interview questions and bullet point answers that you'd then use to adjust to your personal learning and project experience.

Two simple prompts to get you going could be:
- give me 10 example interview questions asked for analytics engineering position
- For each question, give me example answer bullet points

Please note, these are not extensive or guaranteed questions, but you can leverage this technology to consolidate your understanding and prepare to talk around your experience.

![Alt text](ae-gpt-questions1.png)
![Alt text](ae-gpt-answers1.png)