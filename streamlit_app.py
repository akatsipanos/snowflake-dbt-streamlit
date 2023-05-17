# Snowpark
from snowflake.snowpark.session import Session
import snowflake.snowpark.functions as F
# Misc
import pandas as pd
import json
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import sys
from joblib import load

import streamlit as st
st.set_page_config(
     page_title="Data Scientist Salary",
     page_icon="💸",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://developers.snowflake.com',
         'About': "This is an *extremely* cool app powered by Snowpark for Python, Snowflake Data Marketplace and Streamlit"
     }
)

def create_session():
    if "snowpark_session" not in st.session_state:
        connection_parameters = json.load(open('../connection1.json'))
        session = Session.builder.configs(connection_parameters).create()
        st.session_state['snowpark_session'] = session
    else:
        session = st.session_state['snowpark_session']
    return session

@st.cache_data()
def load_data():
    salary_df = session.table('SALARIES_FINAL')
    encoded_df = session.table('ENCODED_SALARIES_FINAL')
    return salary_df.to_pandas(), encoded_df.to_pandas()

st.markdown("<h1 style='margin-top:-80px;'>Data Scientist Salary Dataset</h1>", unsafe_allow_html=True)
session = create_session()
salary_df, encoded_df = load_data()

def main_page():
    st.subheader("Exploratory Data Analysis")
    st.write(salary_df[:10])

def page_two():
    st.subheader("Feature Importance")
    feature_cols = encoded_df.drop(['SALARY'], axis=1).columns
    model_file = session.file.get('@ml_models/xgb_hp_model.sav', 'tmp')
    model = joblib.load(f'tmp/{model_file[0].file}')

    feature_importance = pd.DataFrame(data = model.feature_importances_, 
                                      index = feature_cols, 
                                      columns=['Feature_importance'])
    feature_importance = feature_importance.sort_values('Feature_importance', ascending=False)

    selected_features = st.multiselect('',feature_cols)
    st.markdown('___')

    with st.container():
        st.write('Select features to display their feature importance on the bar chart. The top 10 features are shown if none are selected.')
        feature_list = feature_importance.index[:10] if len(selected_features) == 0 else selected_features

        feature_importance_filtered = feature_importance[feature_importance.index.isin(feature_list)]

        fig,ax = plt.subplots()
        sns.barplot(data = feature_importance_filtered,x = 'Feature_importance', y=feature_importance_filtered.index, ax=ax)
        st.pyplot(fig, use_container_width=True)

def page_three():
    st.subheader("Predictor Tool")
    st.write('Enter your details and see your predicted salary')
    year = '2023'
    experience_select = st.selectbox('Experience level', ['Executive','Senior','Intermediate','Entry-level'])
    experience_dict = {'Executive':'EX', 'Entry-level':'EN','Senior':'SE', 'Intermediate':'MI'}
    experience = experience_dict[experience_select]

    employment_select = st.selectbox('Employment type', ['Full-time','Part-time','Contractor','Freelance'])
    employment_dict = {'Full-time':'FT', 'Part-time':'PT','Contractor':'CT', 'Freelance':'FL'}
    employment = employment_dict[employment_select]

    job = st.selectbox('Job title', salary_df['JOB'].unique())
    res = st.selectbox('Residence', salary_df['EMPLOYEE_RESIDENCE'].unique())
    rr = st.select_slider('Remote ratio (%)', np.arange(0,101,1))
    loc = st.selectbox('Company location', salary_df['COMPANY_LOCATION'].unique())
    size = st.selectbox('Company size', ['S','M','L'])
    input = {'YEAR':year,
             'EXPERIENCE':experience,
             'EMPLOYMENT':employment,
             'JOB':job,
             'EMPLOYEE_RESIDENCE':res,
             'REMOTE_RATIO':rr,
             'COMPANY_LOCATION':loc,
             'COMPANY_SIZE':size}
    input_df = pd.DataFrame(input.values(), input.keys()).T
    # st.write(input_df)

    transformer_file = session.file.get('@ml_models/transformer.sav', 'tmp')
    model_file = session.file.get(f'@ml_models/xgb_hp_model.sav','tmp')
    transformer = load(f'tmp/{transformer_file[0].file}')
    model = load(f'tmp/{model_file[0].file}')
    df =  transformer.transform(input_df)
    pred = model.predict(df)
    st.markdown("#")
    st.markdown('# ')
    st.markdown(f"<h1 style='margin-top:-80px;'>Predicted salary: ${pred[0]:.2f}</h1>", unsafe_allow_html=True)

page_names_to_funcs = {
    "Exploratory Data Anlaysis": main_page,
    "Feature Importance":page_two,
    "Predictor Tool":page_three}

selected_page = st.sidebar.selectbox("Select", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
