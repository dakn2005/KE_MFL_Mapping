from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

from sklearn.neighbors import BallTree
import numpy as np
import pandas as pd
from math import radians
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app)    
engine = create_engine("postgresql+psycopg2://postgres:123@Team@localhost:5432/kmfl")
#https://stackoverflow.com/questions/38332787/pandas-to-sql-to-sqlite-returns-engine-object-has-no-attribute-cursor
engine = engine.raw_connection() 

@app.route("/")
def hello_world():
    return "<p>Hello, World, test!</p>"


@app.route("/init/<coords>")
@cross_origin()
def init_load(coords):

    coordArr = coords.split(',')
    lat_q = float(coordArr[0]) #-1.13481782999
    long_q = float(coordArr[1]) #37.02479170999999


    dfFacilities = pd.read_sql("""select 
        id, name, officialname, keph_level_name, facility_type_name, county_name, 
        sub_county_name, owner_type_name, admission_status_name, 
        operation_status_name, 
        open_whole_day, open_public_holidays, open_weekends, open_late_night,
        service_names, categories,
        lat,long, 
        '' as distance 
        from tbl_kmfl where lat is not null""", con=engine)
    

    tree2 = BallTree(np.deg2rad(dfFacilities[['lat', 'long']].values.astype(float)), metric='haversine') #minkowski

    distances2, indices2 = tree2.query(np.deg2rad(np.c_[lat_q, long_q]), k = 100)

    r_km = 6371 # multiplier to convert to km (from unit distance)

    for d, ind in zip(distances2, indices2):
        # print(d, ind)
        for i,index in enumerate(ind):
            dfFacilities['distance'][index] = d[i] * r_km
            # print("\n\t{} with distance of approx {} kms".format(df2['name'][index], d[i] * r_km) )

    # print(indices2[0])

    outDf = dfFacilities.iloc[indices2[0]]

    #load services
    dfServices = pd.read_sql("select * from service", con=engine)

    #load service categories
    dfCategories = pd.read_sql("select * from service_category", con=engine)

    return {
        "data": outDf.to_json(orient="records"),
        "services": dfServices.to_json(orient="records"),
        "service_categories": dfCategories.to_json(orient="records")
    }