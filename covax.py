import datetime
#import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlalchemy

import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)

def con(db_schema = st.secrets["db_schema"], db_typ = 'mysql+mysqlconnector', db_user = st.secrets["db_user"]+":"+st.secrets["db_pass"], db_adr = st.secrets["db_server"]+":3306", echo=1):
    try:
        str_connection = f'{db_typ}://{db_user}@{db_adr}/{db_schema}'    
        if echo == 1:
            print(f'This connection string has been created: {str_connection}')
        return str_connection
    except:
        print('Invalid values given.')
        return ''  

@st.cache()    
def sql(str_sql,str_con):
    '''Dies ist eine eigene Funktion, um jedes denkbare SQL-Statement auszuführen.'''
    try:
        f_engine  = sqlalchemy.create_engine(str_con)
        df_return = pd.read_sql(str_sql, f_engine)
        print("Die Aktion wurde erfolgreich ausgeführt.")
        return df_return        
    except sqlalchemy.exc.ProgrammingError as pre:
        print(f'Es ist ein Fehler aufgetreten! \n Das Statement {str_sql} war fehlerhaft.\n')
        print(pre)        
        return pd.DataFrame()
    except sqlalchemy.exc.ResourceClosedError as rce:
        print('Die Aktion wurde ausgeführt. Es wurden keine Daten zurückgeliefert.')
        return pd.DataFrame()
    except sqlalchemy.exc.IntegrityError as ie:
        print('Das SQL-Statement ist NICHT fehlerhaft, kann aber nicht ausgeführt werden. \n')
        print(ie)
        return pd.DataFrame()
    except:
        raise

week = str(st.slider ("Week: ", min_value=25, max_value=34, value=34, step=1))

df_states = sql("SELECT * from covax WHERE Week = " + week, con())

# -------------------------------------------------------------

st.set_page_config(layout="wide")st.title('Covax')

st.write(df_states.columns) 

xData, yData = st.columns((1,1))

with xData:
    xData = st.radio("x-Axis", ('PropVaccinated','PropVaccinated12','PropVaccinated18','PropVaccinated65'))

with yData:
    yData = st.radio("y-Axis", ('AdultHospitalized','ChildrenHospitalized','Deaths'))       

sns.regplot(x=xData, y=yData, data=df_states)
st.pyplot()

info1 = st.beta_expander("Info 1", expanded=False)
with info1:
    st.write("Info 1")
info2 = st.beta_expander("Info 2", expanded=False)
with info2:
    st.write("Info 2")