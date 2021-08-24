def con(db_schema = 'web97_db2', db_typ = 'mysql+mysqlconnector', db_user = 'web97_2:youshallnotpass', db_adr = 'server4.webgo24.de:3306', echo=1):
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
        f_engine  = create_engine(str_con)
        df_return = pd.read_sql(str_sql, f_engine)
        print("Die Aktion wurde erfolgreich ausgeführt.")
        return df_return        
    except exc.ProgrammingError as pre:
        print(f'Es ist ein Fehler aufgetreten! \n Das Statement {str_sql} war fehlerhaft.\n')
        print(pre)        
        return pd.DataFrame()
    except exc.ResourceClosedError as rce:
        print('Die Aktion wurde ausgeführt. Es wurden keine Daten zurückgeliefert.')
        return pd.DataFrame()
    except exc.IntegrityError as ie:
        print('Das SQL-Statement ist NICHT fehlerhaft, kann aber nicht ausgeführt werden. \n')
        print(ie)
        return pd.DataFrame()
    except:
        raise