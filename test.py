pip install -r requirements.txt

import datetime
#import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st

import sqlalchemy

import functions

df_states = sql("SELECT * from covax WHERE Week = 33", con())

# give a title to our app
st.title('Covax')
 

status = st.radio('Select column: ',
                  ('Name', 'Code','Save CSV'))
 
if(status == 'Name'):

    st.text(df_states['StateName'])

elif(status == 'Code'):

    st.text(df_states['StateCode'])
    
elif(status == 'Save CSV'):

    df_states.to_csv('states.csv', mode='a', index=False)
else:
    st.text("Please choose")