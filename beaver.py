#!/usr/bin/env python3

import typer
import jsonschema
import json
from rich.progress import track

app = typer.Typer()

def get_id():
    try:
        with open("db.json") as file:
            return json.load(file)[-1]["id"] + 1
    except:
        return 1

@app.command()
def validate(data):
    with open("schema.json") as file:
        schema = json.load(file)
    try:
        jsonschema.validate(data, schema)
        print("JSON data is valid.")
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"JSON data is invalid: {e.message}")
        return False

@app.command()
def create(data: str):
    data = json.loads(data)
    id = get_id()
    data["id"] = id
    if not validate(data):
        exit()

    try:
        with open("db.json", 'r+') as file:
            file_data = json.load(file)
            file_data.append(data)
            file.seek(0)
            json.dump(file_data, file, indent=4)   
    except FileNotFoundError:
        pass
    
@app.command()
def create_database():

    data = []
    db_file = open('db.json', 'w')
    json.dump(data, db_file)

@app.command()
def read(all:bool = False, id:int = False):
    if all:
        with open('db.json', 'r') as file:
            db = json.load(file)
            print(db)
    elif id:
        with open('db.json', 'r') as file:
            db = json.load(file)
        print(db[id-1])
    else:
        print("ERROR")

@app.command()
def search(value:str = typer.Option(), keyword: str=None, update:int=0):
    with open("db.json") as file:
        db = json.load(file)
    if update:
        for record in db:
            if record["id"] == update:
                record = json.loads(value)
                record["id"] = update
                if not validate(record):
                    exit()
                db[update-1] = record
                break

        with open('db.json', 'w') as file:
            json.dump(db, file, indent=4)
    else:
        for record in track(db, description="Searching..."):
            if keyword:
                if str(record[keyword]) == value or (type(record[keyword]) == list and value in record[keyword]) or (type(record[keyword]) == str and record[keyword].find(value) != -1):
                    print(record)
            else:
                for val in record.values():
                    if val == value or (type(val) == list and value in val):
                        print(record)
            
@app.command()
def delete(id:int = False, all:bool = False):
    delete = typer.confirm("Are you sure you want to delete this")
    if not delete:
        raise typer.Abort()
    if all:
        try:
            with open("db.json", 'r+') as file:
                file_data = json.load(file)
                file_data = []
                file.seek(0)
                open('db.json', 'w').close()
                json.dump(file_data, file, indent=4)
        except FileNotFoundError:
            pass
    elif id:
        try:
            with open("db.json", 'r+') as file:
                file_data = json.load(file)
                found = False
                for key, item in enumerate(file_data):
                    if item['id'] == id:
                        file_data = file_data[:key] + file_data[key+1:]
                        print(file_data)
                        found = True
                        break

                if found:
                    file.seek(0)
                    open('db.json', 'w').close()
                    json.dump(file_data, file, indent=4)
                else:
                    print("ID not found")
                    raise typer.Abort()
        except FileNotFoundError:
            pass
    else:
        print("ERROR")

if __name__ == '__main__':
    app()