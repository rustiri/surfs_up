#import dependencies
import datetime as dt
import numpy as np
import pandas as pd

#get the dependencies we need for SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#import dependencies for flask
from flask import Flask, jsonify

#setup database
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect the database into our classes.
Base = automap_base()
#to reflect the database
Base.prepare(engine, reflect=True)
#save our references to each table.
Measurement = Base.classes.measurement
Station = Base.classes.station
#create session link from python to database
session = Session(engine)

#create a new Flask app instance
app = Flask(__name__)

#Create Flask Routes
@app.route('/')

#create function 
#def hello_world():
#    return 'Hello World'


#create welcome function with return statement, use f-string 
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:\n
    /api/v1.0/precipitation\n
    /api/v1.0/stations\n
    /api/v1.0/tobs\n
    /api/v1.0/temp/start/end
    '''
    )

#create route for the precipitation analysis
@app.route("/api/v1.0/precipitation")

#create precipitation function
def precipitation():
    #calculates the date one year ago from the most recent date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #write a query to get the date and precipitation for the previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    #create a dictionary with the date as the key and the precipitation as the value.
    #use Jsonify() function that converts the dictionaly to JSON file
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#create route for stations analysis
@app.route("/api/v1.0/stations")

#create function for stations
def stations():
    #create a query that will allow us to get all of the stations in our database.
    results = session.query(Station.station).all()
    #results into a one-dimensional array, use function np.ravel()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#create route for montly temperature: 
#to return the temperature observations for the previous year.
@app.route("/api/v1.0/tobs")

#create function temp_monthly
def temp_monthly():
    #calculate the date one year ago from the last date in the database.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #query the primary station for all the temperature observations from the previous year. 
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    #unravel the results into a one-dimensional array and convert that array into a list.
    temps = list(np.ravel(results))
    #return jsonify
    return jsonify(temps=temps)

#create route for statistic analysis
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

#create function stats with two parameter start and end
def stats(start=None, end=None):
    #create a query to select the minimum, average, and maximum temperatures from our SQLite database.
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    #determine the starting and ending date, add if-not
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()

    #calculate the temperature minimum, average, and maximum with the start and end dates.
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)





