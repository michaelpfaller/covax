import datetime
#import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlalchemy

import streamlit as st
st.set_page_config(layout="wide")
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

week = 34
@st.cache()
def loadWeek(week):
    df = sql("SELECT * from covax WHERE Week = " + str(week), con())
    return(df)
# -------------------------------------------------------------

df_states = loadWeek(week)
st.title('Covax')

with st.sidebar:
    pages = st.radio("Pages", ("Single Correlations", "Correlation over Time", "Info"))

# main
if pages=="Single Correlations":

    week = st.slider("Week: ", min_value=25, max_value=34, value=34, step=1)

    xData, yData, misc = st.columns((1,1,1))

    with xData:
        xColumns = ['PropVaccinated','PropVaccinated12','PropVaccinated18','PropVaccinated65']
        xData = st.selectbox("x-Axis", xColumns)

    with yData:
        yColumns = ['AdultHospitalized','ChildrenHospitalized','Deaths']
        yData = st.selectbox("y-Axis", yColumns)       

    with misc:
        st.write("TBD")

    sns.regplot(x=xData, y=yData, data=df_states)
    #plt.ylim(-10, None)
    st.pyplot()

elif pages=="Correlations over Time":

    st.write("More to come")

elif pages=="Info":

    info1 = st.expander("Interpretation", expanded=False)
    with info1:
        st.write("Info 1")
    info2 = st.expander("Data Processing", expanded=False)
    with info2:
        st.write("Info 2")
    info3 = st.expander("Info 3", expanded=False)
    with info3:
        st.write("Info 3")