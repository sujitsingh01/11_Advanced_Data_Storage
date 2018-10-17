#Flask API  
import numpy as np 
import datetime as dt 
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base 
from sqlalchemy.orm import Session 
from sqlalchemy import create_engine, func 
 
 
from flask import Flask, jsonify 
 
 
engine = create_engine("sqlite:///Resources/hawaii.sqlite") 
 
 
# reflect an existing database into a new model 
Base = automap_base() 
# reflect the tables 
Base.prepare(engine, reflect=True) 

 
# Save reference to the table 
Measurement = Base.classes.measurement 
Station = Base.classes.station 

 
# Create our session (link) from Python to the DB 
session = Session(engine) 

 
app = Flask(__name__) 
 
 
@app.route("/api/v1.0/precipitation") 
def temperature(): 
     #Query for the dates and precipitation from 3 years to 2 years ago. 
    
    today = dt.date.today() 
    search_end_date = today - dt.timedelta(days = 365) 
    search_start_date = search_end_date -dt.timedelta(days = 365) 
     
      #convert datetime objects to strings 
    search_start_date = search_start_date.strftime("%Y-%m-%d") 
    search_end_date = search_end_date.strftime("%Y-%m-%d") 
       
    query_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>search_start_date,Measurement.date <= search_end_date).all() 
       
      #Convert the query results to a Dictionary using date as the key and prcp as the value. 
    prcp_measurements = [] 
    for result in query_results:
        date_precipitation = {} 
        date_precipitation[result.date] = result.prcp 
        prcp_measurements.append(date_precipitation) 
  
 
      #Return the JSON representation of your dictionary. 
    return jsonify(prcp_measurements) 
  
 
  
 
  #Return a JSON list of stations from the dataset. 
    @app.route("/api/v1.0/stations") 
    def stations(): 
      results = session.query(Station.id, Station.name, Station.station).all() 
       
      stations_list = [] 
      for result in results: 
          station_dict = {} 
          station_dict[result.id]=(result.name, result.station) 
          stations_list.append(station_dict) 
  
 
      return jsonify(stations_list) 
  
 
  
 
@app.route("/api/v1.0/tobs") 
  #Return a JSON list of Temperature Observations (tobs) for the previous year. 
def tobs(): 
    today = dt.date.today() 
    search_end_date = today - dt.timedelta(days = 365) 
    search_start_date = search_end_date -dt.timedelta(days = 365) 
       
      #convert datetime objects to strings 
    search_start_date = search_start_date.strftime("%Y-%m-%d") 
    search_end_date = search_end_date.strftime("%Y-%m-%d") 
       
    query_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>search_start_date,Measurement.date <= search_end_date).all() 
  
 
      #Convert the query results to a Dictionary using date as the key and tobs as the value. 
    tobs_measurements = [] 
    for result in query_results: 
        date_tobs = {} 
        date_tobs[result.date] = result.tobs 
        tobs_measurements.append(date_tobs) 
  
 
      #Return the JSON representation of your dictionary. 
    return jsonify(tobs_measurements) 
  
 
if __name__ == '__main__': 
      app.run(debug=True) 
  
