from flask import Flask, jsonify
from sklearn.neighbors import BallTree
# import numpy as np
import pandas as pd
from math import radians
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
import json 


app = Flask(__name__)

engine = create_engine("postgresql+psycopg2://postgres:''@localhost:5432/kmfl")
metadata = MetaData()
metadata.create_all(engine)
Session = sessionmaker(engine)
session = Session()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/init/<float:lat>/<float:long>")
def init_load(lat, long):
    kmfl = Table('kmfl', metadata, autoload_with=engine)
    res = session.execute(select(kmfl).where(kmfl.c.id < 10))

    dataDict=[]
    for row in res:
        dataDict.append(row._mapping)

    

# def nearestFacility(lat, long):

#     df = pd.DataFrame(cities_np, columns=['City', 'Latitude', 'Longitude'])
