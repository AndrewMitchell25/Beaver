import typer
import jsonschema
import json
from typing_extensions import Annotated

app = typer.Typer()

def get_name():
    try:
        with open("schema.json") as schema_file:
            return json.load(schema_file)["title"]
    except:
        print("No database found")
        
def get_id():
    schema_name = get_name()
    try:
        with open("db.json") as file:
            return json.load(file)[schema_name][-1]["id"]
    except:
        return 1

def validate(data):
    with open("schema.json") as file:
        schema = json.load(file)
    try:
        jsonschema.validate(data, schema)
        print("JSON data is valid.")
    except jsonschema.exceptions.ValidationError as e:
        print(f"JSON data is invalid: {e.message}")

@app.command()
def create(data):
    id = get_id()
    schema_name = get_name()
    data["id"] = id
    validate(data)
    try:
        with open("db.json", 'r') as file:
            db = json.load(file)
            db[schema_name].append(data)
    except FileNotFoundError:
        pass
    
@app.command()
def read(all:bool = False, id:int = False):
    if all:
       with open("db.json") as file:
           db = json.load(file)
           print(db)
    elif id:
        schema_name = get_name()
        with open("db.json") as file:
           db = json.load(file)
        print(db[schema_name][id - 1])
    else:
        print("ERROR")

if __name__ == '__main__':
    app()