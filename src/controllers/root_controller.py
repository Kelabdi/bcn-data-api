from app import app
from flask import request
from utils.json_response import json_response
from utils.handle_error import handle_error
from utils.mongo_connection import mongo_read

# API ENDPOINTS #
#################

@app.route("/")
@handle_error
def home():
    print(request.args)
    name = request.args.get("name","")
    surname = request.args.get("surname")
    return {
        "name":name,
        "surname": surname
    }

# Read selected collection plus requested parameters
@app.route("/read/<collection>")
@handle_error
def read_mongo(collection):
    q = dict(request.args)
    print(q)
    return json_response(list(mongo_read("bdmlpt0521midproject",f"{collection}", q)))


# POPULATION DATASET #

# Total Population by year
@app.route("/bcn-population-by-year/<year>")
@handle_error
def pop_year(year):
    q = {"Year":f"{year}"}
    data = list(mongo_read("bdmlpt0521midproject","population", query=q))
    val = sum([int(x["Total"]) for x in data])
    return {"Description":"Total population in BCN",
            "Year":f"{year}",
            "Total": f"{val}"}

# Population by district name
@app.route("/bcn-population-by-district/<name>")
@handle_error
def pop_district(name):
    q = {"District.Name":{"$regex":f"({name})+"}}
    return json_response(list(mongo_read("bdmlpt0521midproject","population", query=q)))

# Population by neighborhood name
@app.route("/bcn-population-by-neighborhood/<name>")
@handle_error
def pop_neighborhood(name):
    q = {"Neighborhood.Name":{"$regex":f"({name})+"}}
    return json_response(list(mongo_read("bdmlpt0521midproject","population", query=q)))

#--------------------------------------------

# UNEMPLOYMENT DATASET #

# Total Unemployment by year
@app.route("/bcn-unemployment-by-year/<year>")
@handle_error
def unem_year(year):
    q = {"Year":f"{year}"}
    data = list(mongo_read("bdmlpt0521midproject","unemployed", query=q))
    val = sum([int(x["Total"]) for x in data])
    return {"Description":"Total registered unemployeds in BCN",
            "Year":f"{year}",
            "Total": f"{val}"}
    
# Registered unemployees by district name
@app.route("/bcn-unemployed-by-district/<name>")
@handle_error
def unem_district(name):
    q = {"District.Name":{"$regex":f"({name})+"}}
    return json_response(list(mongo_read("bdmlpt0521midproject","unemployed", query=q)))


# Registered unemployees by neighborhood name
@app.route("/bcn-unemployed-by-neighborhood/<name>")
@handle_error
def unem_neighborhood(name):
    q = {"Neighborhood.Name":{"$regex":f"({name})+"}}
    return json_response(list(mongo_read("bdmlpt0521midproject","unemployed", query=q)))



