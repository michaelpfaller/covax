import pandas as pd
import streamlit as st

df_states = pd.read_csv("states.csv")


# give a title to our app
st.title('Covax')
 
# 
status = st.radio('Select column: ',
                  ('Name', 'Code','Save CSV'))
 
if(status == 'Name'):

    st.text(df_states['StateName'])

elif(status == 'Code'):

    st.text(df_states['StateCode'])
    
elif(status == 'Save CSV'):

    df_states.to_csv('states.csv', mode='a')
else:
    st.text("Please choose")