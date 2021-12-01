import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, request
import os


engine = create_engine("sqlite:///activation.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)


# Save reference to the table
Activations = Base.classes.activations


app = Flask(__name__)


@app.route("/")
def welcome():
    with open('resources/index.html') as f:
        return f.read()


@app.route("/static/<filename>")
def get_static(filename):
    with open(f'static/{filename}') as f:
        return f.read()
    
@app.route('/data/<activation>')
def get_data(activation):  
    print(f'Activation={activation}')
    x_lower = request.args.get('from', type=float)
    x_upper = request.args.get('to', type=float)
    
    if activation == 'sigmoid': 
        feature = Activations.sigmoid
    elif activation == 'tanh':
        feature = Activations.tanh
    elif activation == 'relu':
        feature = Activations.relu
    else:
        raise Exception(f"Invalid request. Activation:[{activation}] not found")
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    query = session.query(Activations.x, feature)
    if x_lower:
        query = query.filter(Activations.x >= x_lower)
    if x_upper:
        query = query.filter(Activations.x <= x_upper)

    """Return a list of all passenger names"""
    # Query all passengers
    results = query.all()

    session.close()
    x = [x for x, _ in results]
    y = [y for _, y in results]
    return jsonify({'x': x, 'y': y})


if __name__ == '__main__':
    app.run(debug=True)
