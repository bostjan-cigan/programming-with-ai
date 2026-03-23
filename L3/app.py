# Import Flask and the tools we need:
# - Flask: the web framework
# - request: access incoming HTTP request data (e.g. JSON body)
# - jsonify: turn Python dicts into JSON responses
# - render_template: render HTML templates
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

# Create the Flask application. Use "public" folder for static files (CSS, JS, images).
app = Flask(__name__, static_folder="public", static_url_path="/public")

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

def generate_with_ai(ingredients, cuisine=None, diet=None, max_time=None):
    prompt = f"""
Create 3 simple recipes using these ingredients: {ingredients}.
"""

    if cuisine:
        prompt += f"\nPreferred cuisine: {cuisine}"
    if diet:
        prompt += f"\nDietary preference: {diet}"
    if max_time:
        prompt += f"\nMaximum cooking time: {max_time} minutes"

    prompt += """

For each recipe include:
- title
- short description
- cooking time
- missing ingredients
- steps

Keep the output clear and easy to read.
"""

    response = client.chat.completions.create(
        model="liquid/lfm2.5-1.2b",
        messages=[
            {"role": "system", "content": "You are a helpful recipe generator."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

@app.route("/")
def index():
    """Render the main page when visiting the root URL."""
    return render_template("index.html")


# @app.route defines a URL endpoint. "/generate" is the path clients will call.
# methods=["POST"] means this endpoint only accepts POST requests (not GET).
@app.route("/generate", methods=["POST"])
def generate_recipe():
    data = request.json
    ingredients = data["ingredients"]
    cuisine = data.get("cuisine") or None
    diet = data.get("diet") or None
    max_time = data.get("max_time") or None

    recipe_text = generate_with_ai(ingredients, cuisine=cuisine, diet=diet, max_time=max_time)

    return jsonify({
        "recipe": recipe_text
    })


# Start the development server. debug=True enables auto-reload on code changes
# and shows detailed error pages. Use only in development!
if __name__ == "__main__":
    app.run(debug=True, port=5001)