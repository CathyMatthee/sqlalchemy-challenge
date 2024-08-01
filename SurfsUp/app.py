# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Welcome to the Hawaii Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and precipitation measurements"""
    # Query last year dates and precipitations
    prec_results = session.query(Measurement.date, Measurement.prcp).\
                    filter(Measurement.date >= '2016-08-23').all()

    session.close()

    # Create a dictionary from the tuple row data, where date is key and prcp is value    all_prec = []
    for date, prcp in prec_results:
        prec_dict = {}
        prec_dict[date] = prcp
        all_prec.append(prec_dict) 
    
    return jsonify(all_prec)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all unique station names"""
    # Query all stations
    station_names = session.query(Station.station).distinct().all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(station_names))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of dates and temps of last year data of most active station"""
    # Query all dates and temperatures
    tobs_results = session.query(Measurement.date, Measurement.tobs).\
                    filter(Measurement.date >= '2016-08-23').\
                    filter(Measurement.station == "USC00519281").all()

    session.close()

    # Create a dictionary from the tuple row data, where date is key and temp observations is value
    all_tobs = []
    for date, tobs in tobs_results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        all_tobs.append(tobs_dict) 
    
    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

     # Need to clean data inputed by user but I ran out of time and didn't know how to
    """Fetch the start date from DB where it matches the path variable date supplied by the user in URL, or a 404 if not found."""

    # Query the min, avg and max temps using variable user input dates
    calcs = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
    
    session.close()

    # Convert list of tuples into min, avg and max temps variables
    min, avg, max = np.ravel(calcs)

    # Create dictionary
    temps = {
        "TMIN": min,
        "TAVG": avg,
        "TMAX": max
    }

    return jsonify(temps)
    

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Need to clean data inputed by user but I ran out of time and didn't know how to
    """Fetch the start and end date from DB where it matches the path variable date supplied by the user in URL, or a 404 if not found."""
    
    calc = session.query(Measurement.station, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            group_by(Measurement.station).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
    session.close()

    # Convert list of tuples into min, avg and max temps variables
    min, avg, max = np.ravel(calc)

    # Create dictionary
    temp = {
        "TMIN": min,
        "TAVG": avg,
        "TMAX": max
    }

    return jsonify(temp)


if __name__ == "__main__":
    app.run(debug=True)






















