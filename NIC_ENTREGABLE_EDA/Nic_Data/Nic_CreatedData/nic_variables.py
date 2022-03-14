# variables
import numpy as np
from Nic_EDA_funciones import datos_decrim_web
from Nic_EDA_funciones import EU_dec_countries
from Nic_EDA_funciones import european_dec_countries
from Nic_EDA_funciones import drug_list

drug_list = drug_list()
EU_countries = ["Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Denmark","Estonia", "Finland", "France", "Germany", "Greece", "Hungary","Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden", "United_Kingdom"]
european_countries = ["Austria", "Albania","Andorra","Armenia","Azerbaijan","Belarus", "Belgium", "Bulgaria", "Bosnia_Herzegovina", "Croatia", "Cyprus", "Czechia", "Denmark","Estonia", "Finland", "France", "Germany","Georgia", "Greece", "Hungary","Iceland","Ireland", "Italy", "Kosovo","Latvia", "Lithuania", "Liechtenstein","Luxembourg", "Malta","Moldova","Montenegro", "Monaco" "Netherlands","North_Macedonia","Norway","Poland", "Portugal", "Romania","Russia","San_Marino","Serbia","Switzerland","Slovakia", "Slovenia", "Spain", "Sweden","Turkey","Ukraine","United_Kingdom","Vatican_City"]
EU_dec_countries = EU_dec_countries()
european_dec_countries = european_dec_countries()

EU_european_dec_countries = np.unique(EU_dec_countries + european_dec_countries)

country_decriminalisaton_data = datos_decrim_web()
