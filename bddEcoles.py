# bddEcoles.py

import pymongo
import csv

DATABASE = "LOL"
client = pymongo.MongoClient(DATABASE)
db = client.Faidherbe

path = "./ressources/ecolestest.csv"
with open( path, 'r', encoding='utf-8') as theFile:
    reader = csv.DictReader(theFile, delimiter=";")
    for line in reader:
        # line is { 'workers': 'w0', 'constant': 7.334, 'age': -1.406, ... }
        # e.g. print( line[ 'workers' ] ) yields 'w0'
        nom = line['nom']
        sigle = line['sigle']
        commune = line['commune']
        insert = {'nom': nom, 'sigle': sigle, 'commune': commune}
        if db.Ecoles.find_one({"nom": nom}) is None:
            db.Ecoles.insert_one(insert)

# f = open(path, 'rt')
# reader = csv.reader(f)
# headers = next(reader, None)
# print(headers)

