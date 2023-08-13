import openai
from flask import Flask, render_template, request
from dotenv import dotenv_values
import json

config = dotenv_values("../.env")
print(config)

openai.api_key = config["OPENAI_API_KEY"]

def get_colors(msg):
    print("what is the value of msg? ", msg)
    prompt = f"""
    you are a color palette generating assistant that responds to text prompts for color palettes
    you should generate color palettes that fit the theme, mood, or instructions in the prompt. the palettes should be between 2 and 8 colors.
    
    Q: Convert the following verbal description of a color palette into a list of colors: The Mediterranean Sea
    A: ["#006699", "#66CCCC", "#F0E68C", "#008000", "#F08080"]
    
    Q: Convert the following verbal description of a color palette into a list of colors: A beautiful sunset
    A: ["#F08080", "#FFA500", "#fcede0", "#f7bb5f", "#ec6607"]
    
    Desired format: a JSON array of hexadecimal color codes without Answer or A in the beginning
    Q: Convert the following verbal description of a color palette into a list of colors: {msg}
    A:
    """

    response = openai.Completion.create(
        prompt=prompt,
        model="text-davinci-003",
        max_tokens=200
    )
    print("what is the value of response? ", response)
    colors = response["choices"][0]["text"]
    print('what is the value of colors? ', colors)
    return json.loads(colors);

app = Flask(__name__,
            template_folder='templates',
            static_url_path='',
            static_folder='static'
            )

@app.route("/palette", methods=["POST"])
def prompt_to_palette():
    query = request.form.get("query")
    colors = get_colors(query)
    return {"colors": colors}

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(port=8000, debug=True)

