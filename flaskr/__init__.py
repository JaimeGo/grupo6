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

@app.route('/', methods=['POST'])
def my_form_post():

    tipo = request.form['tipo']
    tipo_processed = tipo.lower()
    if tipo_processed == 'fecha':
        text = request.form['Input']
        return redirect("http://query17-6.ing.puc.cl/fecha?fecha={}".format(text))
    elif tipo_processed == 'palabra':
        text = request.form['Input']
        return redirect("http://query17-6.ing.puc.cl/palabra?key={}".format(text))
    elif tipo_processed == 'numero':
        text = request.form['Input']
        text2 = request.form['Input2']
        return redirect("http://query17-6.ing.puc.cl/numero?numero={}&entero={}".format(text, text2))
    else:
        return redirect("http://query17-6.ing.puc.cl/mongo?query=collectionName.find()")
        

    

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
    #return palabra.lower()
    #return '1'
    results = eval("mongodb.collectionName.find()")
    nuevo = json_util.dumps(results, sort_keys=True, indent=4)
    nuevo2 = json.loads(nuevo)
    
    resultado_final = []
    for subdic in nuevo2:
        
        if 'contenido' in subdic.keys():
            if palabra.lower() in subdic['contenido'].lower():

                resultado_final.append(subdic)
                
    resultado_final = json_util.dumps(resultado_final, sort_keys=True, indent=4)
    #return '1'
    return resultado_final


@app.route("/numero")
def numero():
    numero= request.args.get("numero")
    
    entero= request.args.get("entero")

    results = eval("mongodb.collectionName.find()")
    nuevo = json_util.dumps(results, sort_keys=True, indent=4)
    nuevo2 = json.loads(nuevo)
    
    resultado_final = []
    for subdic in nuevo2:
        
        if 'numero' in subdic.keys():
            if numero == subdic['numero']:

                resultado_final.append(subdic)
    resultado_final.sort(key = lambda x: x['fecha'], reverse = True)
    resultado_final = json_util.dumps(resultado_final[:int(entero)], sort_keys=True, indent=4)
    return resultado_final


@app.route("/fecha")
def fecha():
    fecha= request.args.get("fecha")
    
    results = eval("mongodb.collectionName.find()")
    nuevo = json_util.dumps(results, sort_keys=True, indent=4)
    nuevo2 = json.loads(nuevo)
    
    resultado_final = []
    for subdic in nuevo2:
        
        if 'fecha' in subdic.keys():
            if fecha == subdic['fecha']:

                resultado_final.append(subdic['numero'])
    resultado_final = json_util.dumps(resultado_final, sort_keys=True, indent=4)
    return resultado_final




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
