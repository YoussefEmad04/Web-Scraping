import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import streamlit as st

# Set page layout and title
st.set_page_config(layout="wide", page_title="FilGoal Match Data")

# Custom CSS for better contrast and readability
st.markdown("""
    <style>
    .main {
        background-color: #1c1c1c;
        color: #f0f2f6;
        padding: 20px;
    }
    .stTextInput label {
        color: #f0f2f6;
        font-size: 18px;
    }
    .stButton button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
    }
    .stDataFrame {
        background-color: #2c2c2c;
        border: 2px solid #e6e6e6;
        border-radius: 8px;
        color: #f0f2f6;
    }
    .stMarkdown {
        color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit app title
st.title("⚽ FilGoal Match Data")

# User input for date
date = st.text_input('Enter a date (yyyy-mm-dd):', '')

if date:
    # Fetch and parse the webpage
    page = requests.get(f'https://www.filgoal.com/matches/?date={date}', verify=True)
    source = page.content
    soup = BeautifulSoup(source, 'html.parser')

    # Championship Name
    new_list = [tag.a.get('href') for tag in soup.find_all('div', 'm')]
    champion_name = [list[list.find("في")+2:].replace('-', ' ').strip() for list in new_list]

    # Teams
    Team_A = [i.get_text().strip() for i in soup.select('.f strong')]
    Team_B = [i.get_text().strip() for i in soup.select('.s strong')]

    # Time of the Match
    Time_of_match = [i.get_text().strip() for i in soup.select('.match-aux span')]
    pattern = re.compile(r'\d{2}-\d{2}-\d{4} - \d{2}:\d{2}')
    Date_Time_Match = [match.group() for item in Time_of_match for match in [re.search(r'\d{2}-\d{2}-\d{4} - \d{2}:\d{2}', item)] if match]

    # Results
    Team_A_Result = [i.get_text().strip() for i in soup.select('.f b')]
    Team_B_Result = [i.get_text().strip() for i in soup.select('.s b')]

    # Create DataFrame
    match_details = pd.DataFrame({
        'البطولة': champion_name,
        'الفريق الأول': Team_A,
        'الفريق التانى': Team_B,
        'ميعاد المباراة': Date_Time_Match,
        'نتيجة المباراة': [f'{i}-{x}'.strip() for i, x in zip(Team_B_Result, Team_A_Result)]
    })

    # Display DataFrame
    st.dataframe(match_details, use_container_width=True)

    # Download button for CSV
    csv = match_details.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download data as CSV", data=csv, file_name='match_details.csv', mime='text/csv')

else:
    st.info("Please enter a valid date to see the match data.")
