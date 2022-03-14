### FUNCIONES ### 

# Importar librerias necesarias #REQUIREMENTS#
import pandas as pd
# import numpy as np
# import matplotlib as plt
# import seaborn as sns

from alumno.Entregas.EDA.NIC_ENTREGABLE_EDA.Nic_Data.Nic_CreatedData.nic_variables import EU_countries
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import folium
import json
from Nic_Data.Nic_CreatedData.nic_variables import EU_european_dec_countries, european_countries, EU_countries
from nic_classes import Drugs 

################################################################################################################################

def drug_list():
    drug_list = []
    alcohol = Drugs.add_drug_list('alcohol', drug_list)
    amphetamines = Drugs.add_drug_list('amphetamines', drug_list)
    ecstasy = Drugs.add_drug_list('ecstasy', drug_list)
    cannabis = Drugs.add_drug_list('cannabis', drug_list)
    cocaine = Drugs.add_drug_list('cocaine', drug_list)
    lsd = Drugs.add_drug_list('lsd', drug_list)
    return drug_list

# 1er paso para conseguir tabla de paises decriminalizados, tipo de decriminalizacion, año de decriminalizacion, que drogas
# que actividades, que cantidades, quien decide, que consecuencias puede haber

# WEBSRAPPING
def datos_decrim_web():

    url = "https://www.talkingdrugs.org/drug-decriminalisation"
    response = requests.get(url)
    soup = bs(response.content, "lxml")
    all_countries = soup.find_all('h2',class_="field-content")
    countries = [country.get_text() for country in all_countries]

    dec_year = soup.div(class_="views-field views-field-field-dc-decrim-date-year")
    decrim_year = [elem.get_text() for elem in dec_year]
    decrim_year = [elem[23:-1:] for elem in decrim_year]
    for pos, country in enumerate(countries):
        if country == 'Uruguay':
            decrim_year.insert(pos, None)

    legal_type = soup.find_all('span', class_="field-content legal-model-tid-legal-model-5201")
    legal_type = [elem.get_text() for elem in legal_type]
    for pos, country in enumerate(countries):
        if country == 'Netherlands':
            legal_type.insert(pos, 'De Facto')
        if country == 'Argentina' or (country == 'Colombia') or (country == 'South Africa'):
            legal_type.insert(pos,'Court Decision')

    activities = soup.find_all('span', class_="views-field-field-dc-activity")
    activity = [elem.get_text() for elem in activities]
    activity = [elem[12::] for elem in activity]

    substances = soup.find_all('span', class_="views-field views-field-field-dc-substances substances--field_dc_substances-tid")
    substance = [elem.get_text() for elem in substances]
    substance = [elem[14:-1:] for elem in substance]
    for pos, country in enumerate(countries):
        if country == 'South Australia':
            substance.insert(pos, None)

    thresholds = soup.find_all('span', class_="views-field views-field-field-dc-thresholds" )
    threshold = [elem.get_text() for elem in thresholds]
    threshold = [elem[14:-1:] for elem in threshold]

    decisions = soup.find_all('span', class_="views-field views-field-field-dc-decision-maker" )
    decision = [elem.get_text() for elem in decisions]
    decision = [elem[18:-1:] for elem in decision]

    outcomes = soup.find_all('span', class_="views-field views-field-field-dc-outcome" )
    outcome = [elem.get_text() for elem in outcomes]
    outcome = [elem[11:-1:] for elem in outcome]

    countries = [country.get_text() for country in all_countries]

    data = {"country": countries,
            "legal model": legal_type,
            "decrim_date": decrim_year,
            "activity": activity,
            "substance": substance,
            "threshold": threshold,
            "decision_maker": decision,
            "outcome": outcome}
            
    country_decriminalisation = pd.DataFrame(data)

    return country_decriminalisation, countries

def EU_dec_countries():
    countries = datos_decrim_web[1]
    EU_dec_countries = []
    for country in countries:
        if country in EU_countries:
            EU_dec_countries.append(country)
    return EU_dec_countries

def european_dec_countries():
    countries = datos_decrim_web[1]
    european_dec_countries = []
    for country in countries:
        if country in european_countries:
            european_dec_countries.append(country)
    return european_dec_countries

# Crear mapa para mostrar donde se han decriminalizado las drogas en europa

def decriminalisation_country_map():
    # Crear mapa con JSON y FOLIUM

    # JSON obtenido de GITHUB -- https://github.com/python-visualization/folium
    with open('../world-countries.json') as f:
        geo_json_counties = json.load(f)

    # open and clean json file, filtering through countries, keeping those of interes from EU/europe with decriminalised drugs
    list_d = []
    for i in range(0,(len(geo_json_counties['features'])-1)):
        if geo_json_counties['features'][i]['properties']['name'] in EU_european_dec_countries:
            list_d.append(geo_json_counties['features'][i])

    geo_json_counties['features'] = list_d

    # Map with folium.Choropleth
    the_map = folium.Map(tiles="cartodbpositron", location=[54,15], zoom_start=4)
    df = datos_decrim_web[0]
    folium.Choropleth(
        geo_data= geo_json_counties,
        name='choropleth',
        # color='blue',
        data=df,
        columns=['country', 'legal model']).add_to(the_map)

    folium.CircleMarker(location = [35.9375, 14.3754],
                    radius=2,
                    color = 'black').add_to(the_map)
    return the_map

    # PD: AL FINAL DIMOS TABLEAU Y ACABE UTILIZANDO ESE MAPA

################################################################################################################################
