from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Parameter

app = Flask(__name__)

engine = create_engine('sqlite:///partool.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/params/<string:tagname_id>')
def parameterList(tagname_id):
    parameters = session.query(Parameter).filter_by(tagname=tagname_id)
    return render_template('parameters.html', parameters=parameters)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
