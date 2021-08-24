import datetime
#import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlalchemy

currentWeek = 34

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
        
@st.cache(suppress_st_warning=True)
def loadWeek(week):
    st.write("fetching data from database")
    df = sql("SELECT * from covax WHERE Week = " + str(week), con())
    return(df)

@st.cache(suppress_st_warning=True)    
def loadState(StateName):
    st.write("fetching data from database")
    df = sql("SELECT * from covax WHERE StateName = '" + StateName + "'", con())
    return(df)

if 'week' not in locals():
    # todo: set to current week
    week = currentWeek
    df_week = loadWeek(week)

    if 'df_states' not in locals():
        df_states = df_week[['StateName','StateCode']]

# -------------------------------------------------------------

st.title('Covax')

with st.sidebar:
    pages = st.radio("", ("Single Correlations", "Single States over Time", "Correlation over Time", "Info"))

# main
if pages=="Single Correlations":

    week = st.slider("Week: ", min_value=1, max_value=currentWeek, value=currentWeek, step=1)
    df_week = loadWeek(week)
        
    xData, yData, misc = st.columns((1,1,1))

    with xData:
        xColumns = ['PropVaccinated','PropVaccinated12','PropVaccinated18','PropVaccinated65']
        xData = st.selectbox("x-Axis", xColumns)

    with yData:
        yColumns = ['AdultHospitalized','ChildrenHospitalized','Deaths']
        yData = st.selectbox("y-Axis", yColumns)     

    with misc:
        pointOptions = ['Default','Code','Number']
        pointOption = st.selectbox("Data Points", pointOptions)

    #plt.figure(figsize=(4,4)) 
    sns.regplot(x=xData, y=yData, data=df_week)
    plt.ylim(0, None)
    
    if pointOption=='Code':
        for i in range(0, df_week.shape[0]):
            plt.text(x=df_week[xData][i], y=df_week[yData][i], s=df_week['StateCode'][i])
    
    st.pyplot()

    dataTable = st.expander("Data Table", expanded=False)
    with dataTable:
        st.write(df_week)

elif pages=="Single States over Time":
    
    currentState = st.selectbox("", df_states['StateName'])
    
    df_state = loadState(currentState)
    st.write(df_state)
    
    yData = st.selectbox("", list(df_state.columns.drop(["StateName","StateCode","Year","Week","Population100K"])))
    
    sns.lineplot(x="Week", y=yData, data=df_state)
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