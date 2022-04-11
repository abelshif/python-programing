
import pandas as pd
import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt

class Data_managing:
    def __init__(self):
        """ This initial method(constractor) reads the vaccin_covid.csv file  from the root 
        source and displays it as a dataframe table called df_vaccin.
        """

        self.df_vaccin =pd.read_csv('vaccin_covid.csv') #read data in dataframe from "vaccin_covid.csv" 

    def create_database(self):
        """ This method creats a connection to the database and open the vaccin_covid.csv file as
        vacccin_covid.db file where all the values in the vaccin_covid.csv table(vaccin)
        are copied in to the vaccin_covid.db table(vaccination). 

        Returns:
            The vaccin_covid.db table called vaccination. 

        """

        self.db_conn = sqlite3.connect('vaccin_covid.db') # connects to vaccin_covid.db and opens it as a database
        self.cur = self.db_conn.cursor()
        vaccination = self.df_vaccin.to_sql('vaccination', self.db_conn) # creates the table "vaccination" in the database "vaccin_covid.db" and fill it with the csv data
                                                                  
        return vaccination
    
    def seed_database(self, path_to_file):
        """ This method returns path to vaccin_covid.db. 
        """

        print("------------------------------------------------")
        print("Path to vaccin_covid.db file:- ", path_to_file)
        print("------------------------------------------------")

    def normalization(self):
        """ This method reads the table vaccination in vaccin_covid.bd as dataframe table(df_vaccination) and  
        clean it. Moreover, it clarifis the concept of normaliztion(1st, 2nd & 3rd) in the relational database tables.
        """

        self.df_vaccination =  pd.read_sql("SELECT * FROM vaccination ", self.db_conn) #reads data in dataframe from "vaccin_covid.db" 

        print("Number of NaN värder in df_vaccination:",'\n',self.df_vaccination.isna().sum())
        print("------------------------------------------------")
        print("length of df_vaccination: ",len(self.df_vaccination)) 
        print("------------------------------------------------")

        #Cleaning df_vaccination.
        self.df_vaccination_cleaned = self.df_vaccination.dropna() # removes all NaN values from df_vaccination

        print("Number of NaN värder in cleaned df_vaccination:",'\n',self.df_vaccination_cleaned.isna().sum())
        print("------------------------------------------------")
        print("length of cleaned df_vaccination: ",len(self.df_vaccination_cleaned))
        print("------------------------------------------------")
       
        #Check for 1st normal form in df_vaccination.
        print("df_vaccination:",'\n',self.df_vaccination_cleaned.head())
        print("No rereating groups in cleaned df_vaccination, meaning every raw has only one corresponding value.")
        print("Hence, the relational database table fullfils first normal form.")
        print("------------------------------------------------")
        print("------------------------------------------------")

        #.....Two relational tables that fullfills 2nd & 3rd normal form.......
        # All non-key attributes are functionally dependent on the entire primary key(2nd normal form)
        #There are no transitive dependencies(3rd normal form)

        #Create
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Country(
        id integer PRIMARY KEY,
        name text, 
        country_code text) """)
        self.db_conn.commit()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS People(
        person_id integer PRIMARY KEY,
        country_id integer,
        FOREIGN KEY (country_id) REFERENCES Country (id))""")
        self.db_conn.commit()

        #Inserting values
        self.cur.execute('''INSERT INTO Country VALUES(1, 'Ethiopia', 'ETH')''')
        self.cur.execute('''INSERT INTO Country VALUES(2, 'Sweden', 'SWE')''')
        self.db_conn.commit()

        self.cur.execute('''INSERT INTO People VALUES(1, 1)''')
        self.cur.execute('''INSERT INTO People VALUES(2, 1)''')
        self.db_conn.commit()

    def _extract_country_data(self, country):
        """ This method extracts covid vaccination data of a specific country  
        from table vaccination in vaccin_covid.db

        Args:
            country: country data related to covid vaccination to be extracted

        Returns:
            country: a vaccination table to a specified country 
        """
        country = pd.read_sql("SELECT * FROM vaccination WHERE country = 'Sweden'", self.db_conn)
        
        return country.head()
        

    def plot_daily_vaccinations(self):
        """ This method gives histogram plot of daily_vaccination from 
        table vaccination in vaccin_covid.db
        """
        
        sns.histplot(self.df_vaccination_cleaned['daily_vaccinations'])
        plt.show()


        

        

