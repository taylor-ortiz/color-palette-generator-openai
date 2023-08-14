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
            "content": "You are a color palette generating assistant that responds to text promps and returns color paletters."
        },
        {
            "role": "system",
            "content": "Your resposne should only be one JSON array containing hexadecimals and contain 0 text. The array should have a length between 2 and 8 values. Do not add any text before or after you provide the array"
        },
        {
            "role": "assistant",
            "content": "Of course, I'd be happy to help you generate color palettes! "
        },
        {
            "role": "user",
            "content": msg
        }
    ]

    response = openai.ChatCompletion.create(
        messages=messages,
        model="gpt-3.5-turbo",
        temperature=0
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
    colors_json = {
        'colors': colors
    }
    return colors_json;

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

