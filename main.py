
#from pathlib import Path
from  Vaccin_Data import Data_managing

def main():
    """ Creats an object of the "Data_managing" class and implement the 
    methods witn in this class when they are called.
    """
    data_manage = Data_managing() #create an object of class "Data_managing"
    data_manage.create_database()
    #data_manage.seed_database(Path('vaccin_covid.db'))
    data_manage.seed_database()
    data_manage.normalization()
    print(data_manage._extract_country_data('Sweden'))
    data_manage.plot_daily_vaccinations()
    
if __name__ == "__main__":
    main() # call on the main function