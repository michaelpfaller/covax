import datetime
#import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import sqlalchemy

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

df_states = sql("SELECT * from covax WHERE Week = 33", con())

# give a title to our app
st.title('Covax')
 

status = st.radio('Select column: ',
                  ('Name', 'Code','Population100K'))
 
if(status == 'Name'):

    st.text(df_states['StateName'])

elif(status == 'Code'):

    st.text(df_states['StateCode'])
    
elif(status == 'Save CSV'):

    st.text(df_states['Population100K'])

else:
    st.text("Please choose")