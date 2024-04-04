import typer
import jsonschema
import json

app = typer.Typer()



def get_id_and_name():
    with open("schema.json") as schema_file:
                schema_name = json.load(schema_file)["title"]
    try:
        with open("db.json") as file:
            return json.load(file)[schema_name][-1]["id"], schema_name
    except:
        return 1, schema_name

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
    id, schema_name = get_id_and_name()
    data["id"] = id
    validate(data)
    try:
        with open("db.json", 'r') as file:
            db = json.load(file)
            db[schema_name].append(data)
    except FileNotFoundError:
        pass
    

if __name__ == '__main__':
    app()