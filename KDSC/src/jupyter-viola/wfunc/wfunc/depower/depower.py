import pandas as pd
# import numpy as np
from shapely.geometry import Point, Polygon
from geopy.geocoders import Nominatim
import geopandas as gpd
import json
import csv
import requests



def fill_missing_data(conventional_plants):
    """
    fil missing lat, lot and capacity_net_bnetza data points
    """
    dfc = pd.read_csv(conventional_plants)
    # this block is for filling missing lon and lat
    nom =  Nominatim(user_agent="depower")
    mask = dfc['lat'].isnull() | dfc['lon'].isnull()
    for i in dfc.loc[mask.values].index:
        n = nom.geocode(dfc.at[i, 'city'] +' '+ dfc.at[i, 'city'])
        dfc.at[i, 'lat'] = n.latitude
        dfc.at[i, 'lon'] = n.longitude 
    # this block is for filling missing capacity_net_bnetza, estimating it with 0.75*'capacity_gross_uba'
    potato = dfc.loc[(dfc['capacity_net_bnetza'].isna()) & (dfc['capacity_gross_uba'].notnull())]
    total_gross_to_net = 0
    count_gross_to_net = 0
    for i3, nan_ele in potato.iterrows():
        print(' potato')
        dfc.at[i3, 'capacity_net_bnetza'] = nan_ele['capacity_gross_uba']*0.75
        total_gross_to_net += nan_ele['capacity_gross_uba']*0.75
        count_gross_to_net += 1
    dfc.loc[(dfc['capacity_net_bnetza'].isna()),'capacity_net_bnetza'] = total_gross_to_net/count_gross_to_net
    return dfc


def powersetter(dfc, geo_data1): 
    """
     assign power of the plant to the polygon-location(german counties)
    """
    de = gpd.read_file(geo_data1)
    dfc['location_found'] = None
    dfc['location_found'] = dfc['location_found'].astype(bool)

    
    # sum total power from each energy_source and assigan to polygon-location
    ess = dfc['energy_source_level_1'].value_counts().index
    for es in ess:
        de[es] = 0
        for i1, row1 in dfc.loc[(dfc['energy_source_level_1']==es)].iterrows():
            p = Point(row1[['lon','lat']].tolist())
            for i2, row2 in de.iterrows():
                if row2['geometry'].contains(p) is True:
                    de.at[i2, es] = de.at[i2, es] + row1['capacity_net_bnetza']
                    dfc.at[i1,'location_found'] = True
                    break
    print(type(de))
    de['other'] = de.apply(lambda row: row['Other'] +
                           row['Other or unspecified energy sources'], axis=1)
    de = de.drop(['Other or unspecified energy sources','Other'], axis=1)
    de['total'] =  de.apply(lambda row: row['other'] + row['Nuclear'] +
                           row['Fossil fuels'] + row['Renewable energy'], axis=1)
    # print(type(de))
    # de1 = de.copy()
    # de1 = de1.astype(str)
    
    de.to_file("./output.geojson", driver='GeoJSON', encoding='utf-8')
    return de















##########################################################################
#geo_data1 = './germany/germany.json'



# def main()
#     color = 'YlOrRd'
#     columns1 = ['NAME_3', 'total']

#     #%memit mask = dfc['energy_source_level_1']=='Other'
#     by2 = 'capacity_net_bnetza'

#     geo_data1 ='./germany/germany.json'
#     de = powersetter(dfc, geo_data1)