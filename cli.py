import typer
import jsonschema
import json

app = typer.Typer()

def get_id():
    try:
        with open("db.json") as file:
            return json.load(file)["counter"]
    except:
        return 1

@app.command()
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

if __name__ == '__main__':
    app()