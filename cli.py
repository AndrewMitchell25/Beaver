import typer
import jsonschema
import json

app = typer.Typer()


@app.command()
def validate(data):
    with open("schema.json") as file:
        schema = json.load(file)
    try:
        jsonschema.validate(data, schema)
        print("JSON data is valid.")
    except jsonschema.exceptions.ValidationError as e:
        print(f"JSON data is invalid: {e.message}")

if __name__ == '__main__':
    app()