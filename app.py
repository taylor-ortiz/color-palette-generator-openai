import openai
from flask import Flask, render_template, request
from dotenv import dotenv_values
import json

config = dotenv_values("../.env")
print(config)

openai.api_key = config["OPENAI_API_KEY"]

def get_colors(msg):
    print("what is the value of msg? ", msg)

    messages = [
        {
            "role": "system",
            "content": "You are a color palette generating assistant that responds to text promps and returns color paletters. you should generate color palettes that fit the theme, mood, or instructions in the prompt. the palettes should be between 2 and 8 colors."
        },
        {
            "role": "system",
            "content": "The desired response is a JSON array of hexadecimal color codes compatible with python "
        },
        {
            "role": "user",
            "content": "Convert the following verbal description of a color palette into a list of colors: The Mediterranean Sea"
        },
        {
            "role": "assistant",
            "content": "{\"colors\":[\"#F08080\",\"#FFA500\",\"#fcede0\",\"#f7bb5f\",\"#ec6607\"]}"
        },
        {
            "role": "user",
            "content": "Convert the following verbal description of a color palette into a list of colors: A beautiful sunset"
        }
    ]

    response = openai.ChatCompletion.create(
        messages=messages,
        model="gpt-3.5-turbo"
    )
    print("what is the value of response? ", response)
    colors = response["choices"][0]["message"]["content"]
    print('what is the value of colors? ', colors)
    colors_json = json.loads(colors);
    print('what is the value of colors json? ', colors_json)
    return colors_json;

app = Flask(__name__,
            template_folder='templates',
            static_url_path='',
            static_folder='static'
            )

@app.route("/palette", methods=["POST"])
def prompt_to_palette():
    query = request.form.get("query")
    print('what is query? ', query)
    colors = get_colors(query)
    return colors;

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

