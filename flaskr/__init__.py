#!/usr/bin/python3
# -*- coding: latin-1 -*-
import os
import sys
# import psycopg2
import json
from bson import json_util
from pymongo import MongoClient
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from datetime import datetime


def create_app():
    app = Flask(__name__)
    return app

app = create_app()

# REPLACE WITH YOUR DATABASE NAME
MONGODATABASE = "dbName"
MONGOSERVER = "localhost"
MONGOPORT = 27017
client = MongoClient(MONGOSERVER, MONGOPORT)
mongodb = client[MONGODATABASE]

'''# Uncomment for postgres connection
# REPLACE WITH YOUR DATABASE NAME, USER AND PASS
POSTGRESDATABASE = "grupo6"
POSTGRESUSER = "grupo6"
POSTGRESPASS = "grupo6"
postgresdb = psycopg2.connect(
    database=POSTGRESDATABASE,
    user=POSTGRESUSER,
    password=POSTGRESPASS,
    host = '146.155.13.141',
    port = 5432)
'''

#Cambiar por Path Absoluto en el servidor
QUERIES_FILENAME = '/var/www/flaskr/queries'


@app.route("/")
def home():
    with open(QUERIES_FILENAME, 'r', encoding='utf-8') as queries_file:
        json_file = json.load(queries_file)
        pairs = [(x["name"],
                  x["database"],
                  x["description"],
                  x["query"]) for x in json_file]
        return render_template('file.html', results=pairs)


@app.route("/mongo")
def mongo():
    query = request.args.get("query")

    results = eval('mongodb.'+query)
    #results = mongodb.collectionName.find()
    results = json_util.dumps(results, sort_keys=True, indent=4)
    if "find" in query:
        return render_template('mongo.html', results=results)
    else:
        return "ok"

@app.route("/palabra")
def palabra():
    palabra = request.args.get("key")

    
    results = eval("mongodb.collectionName.find()")
    nuevo = json_util.dumps(results, sort_keys=True, indent=4)
    nuevo2 = json.loads(nuevo)
    
    resultado_final = []
    for subdic in nuevo2:
        
        if 'contenido' in subdic.keys():
            if palabra in subdic['contenido']:

                resultado_final.append(subdic)
                
    resultado_final = json_util.dumps(resultado_final, sort_keys=True, indent=4)
    
    return render_template('mongo.html', results=resultado_final)


@app.route("/numero")
def numero():
    numero= request.args.get("numero")
    #return numero
    entero= request.args.get("entero")

    
    results = eval("mongodb.collectionName.find()")
    nuevo = json_util.dumps(results, sort_keys=True, indent=4)
    nuevo2 = json.loads(nuevo)
    
    resultado_final = []
    for subdic in nuevo2:
        
        if 'numero' in subdic.keys():
            if numero == subdic['numero']:

                resultado_final.append(subdic)
    return '2'
    resultado_final.sort(key = lambda x: datetime.strptime(x['fecha'], "%d-%m-%y"), reverse = True)
                
    resultado_final = json_util.dumps(resultado_final[:entero], sort_keys=True, indent=4)
    
    return render_template('mongo.html', results=resultado_final)






#"query": "collectionName.find({'numero':'42638939'},{})"



@app.route("/postgres")
def postgres():
    query = request.args.get("query")
    cursor = postgresdb.cursor()
    cursor.execute(query)
    results = [[a for a in result] for result in cursor]
    print(results)
    return render_template('postgres.html', results=results)


@app.route("/example")
def example():
    return render_template('example.html')


if __name__ == "__main__":
    app.run()
