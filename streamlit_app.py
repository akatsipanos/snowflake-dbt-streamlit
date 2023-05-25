
from snowflake.snowpark.session import Session
import pandas as pd
import json
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from joblib import load
import streamlit as st

# Page configuration
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

# This creates the session, however, if a session is already created, then the connection doesn't need to be made
# again to snowflake and instead the session variable points to the sesssion object within the st.session_state 
# dictionary. The benefit of this is that the code runs quicker, making the 'always run' feature on streamlit very handy
def create_session():
    if "snowpark_session" not in st.session_state:
        connection_parameters = json.load(open('../connection1.json'))
        session = Session.builder.configs(connection_parameters).create()
        st.session_state['snowpark_session'] = session
    else:
        session = st.session_state['snowpark_session']
    return session

# Load the data in and convert to pandas, and cache the data so this potentially lengthy process doesn't need to be 
# constantly repeated
@st.cache_data()
def load_data():
    salary_df = session.table('SALARIES_FINAL')
    encoded_df = session.table('ENCODED_SALARIES_FINAL')
    return salary_df.to_pandas(), encoded_df.to_pandas()

# Put a title on the page and run the create session function above to connect to Snowpark and load in the data.
st.markdown("<h1 style='margin-top:-80px;'>Data Scientist Salary Dataset</h1>", unsafe_allow_html=True)
session = create_session()
salary_df, encoded_df = load_data()


# Now we start creating each page in our app
def main_page():
    # Not much here, it's just acting as a place holder to where some EDA could go
    st.subheader("Exploratory Data Analysis")
    st.write(salary_df[:10])


def page_two():
    # A section on the model feature importance
    st.subheader("Feature Importance")

    feature_cols = encoded_df.drop(['SALARY'], axis=1).columns

    # Access the model that was saved in the stored procedure which was run in the dbt_project.ipynb file. This is saved to a local directory 'tmp'
    model_file = session.file.get('@ml_models/xgb_hp_model.sav', 'tmp')
    # Load the model in with joblib
    model = load(f'tmp/{model_file[0].file}')

    # Create the feature importances dataframe  and sort into descending order. The point of sorting is so that I can show the top 10 features by default below
    feature_importance = pd.DataFrame(data = model.feature_importances_, 
                                      index = feature_cols, 
                                      columns=['Feature_importance'])
    feature_importance = feature_importance.sort_values('Feature_importance', ascending=False)

    # Create a dropdown menu where features can be selected from
    selected_features = st.multiselect('',feature_cols)
    st.markdown('___')

    # This 'with' statement allows us to put multiple elements into a streamlit container
    with st.container():
        st.write('Select features to display their feature importance on the bar chart. The top 10 features are shown if none are selected.')

        # If selected features is empty (none are selected from the dropdown) then the top 10 features will be shown 
        feature_list = feature_importance.index[:10] if len(selected_features) == 0 else selected_features
        feature_importance_filtered = feature_importance[feature_importance.index.isin(feature_list)]

        # Plot the bar chart and show the results on streamlit
        fig,ax = plt.subplots()
        sns.barplot(data = feature_importance_filtered,x = 'Feature_importance', y=feature_importance_filtered.index, ax=ax)
        st.pyplot(fig, use_container_width=True)

def page_three():
    # Creating a prediction tool to make a live prediciton
    st.subheader("Predictor Tool")

    # Get the feature information from the user and map it into the correct inputs to the model
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

    # Access the transformer file and model file as was shown on page 2
    transformer_file = session.file.get('@ml_models/transformer.sav', 'tmp')
    model_file = session.file.get(f'@ml_models/xgb_hp_model.sav','tmp')
    transformer = load(f'tmp/{transformer_file[0].file}')
    model = load(f'tmp/{model_file[0].file}')
    df =  transformer.transform(input_df)
    pred = model.predict(df)
    st.markdown("#")
    st.markdown('#')
    st.markdown(f"<h1 style='margin-top:-80px;'>Predicted salary: ${pred[0]:.2f}</h1>", unsafe_allow_html=True)

# This code puts headings on the different pages in streamlit and maps them to the create page function in this code
page_names_to_funcs = {
    "Exploratory Data Anlaysis": main_page,
    "Feature Importance":page_two,
    "Predictor Tool":page_three}

selected_page = st.sidebar.selectbox("Select", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
