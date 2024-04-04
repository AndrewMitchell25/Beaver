import typer
import jsonschema
import json
from rich.progress import track

app = typer.Typer()
        
def get_id():
    try:
        with open("db.json") as file:
            return json.load(file)[-1]["id"]
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
    data["id"] = id
    validate(data)
    try:
        with open("db.json", 'r') as file:
            db = json.load(file)
            db.append(data)
    except FileNotFoundError:
        pass
    
@app.command()
def read(all:bool = False, id:int = False):
    if all:
       with open("db.json") as file:
           db = json.load(file)
           print(db)
    elif id:
        with open("db.json") as file:
           db = json.load(file)
        print(db[id - 1])
    else:
        print("ERROR")

@app.command()
def search(value:str = typer.Option(), keyword:str = False, update:int = False):
    with open("db.json") as file:
        db = json.load(file)
        #NEED TO TEST
        if update:
            for record in db:
                if record["id"] == update:
                    record["id"] = json.loads(value)
                    break
            file.seek(0)
            json.dump(db, file, indent=4)
        else:
            for record in db:
                if keyword and (record[keyword] == value or value in record[keyword]):
                    print(record)
                

if __name__ == '__main__':
    app()