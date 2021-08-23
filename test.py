import pandas as pd
import streamlit as st

df_states = pd.read_csv("states.csv")


# give a title to our app
st.title('Covax')
 
# 
status = st.radio('Select column: ',
                  ('Name', 'Code'))
 
if(status == 'Name'):

    st.text(df_states['Name'])

elif(status == 'Code'):

    st.text(df_states['Code'])
else:
    st.text("Please choose")