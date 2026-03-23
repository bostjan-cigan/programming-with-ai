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


def ask_prompt(prompt_text):
    """Send a prompt to the AI and return the response."""
    response = client.chat.completions.create(
        model="liquid/lfm2.5-1.2b",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that gives clear, informative explanations."},
            {"role": "user", "content": prompt_text}
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
    data = request.json or {}
    ingredients = data.get("ingredients", "")
    cuisine = data.get("cuisine") or None
    diet = data.get("diet") or None
    max_time = data.get("max_time") or None

    # Validate ingredients: must be non-empty after stripping whitespace
    ingredients_str = ingredients if isinstance(ingredients, str) else ", ".join(str(i) for i in ingredients)
    if not ingredients_str or not ingredients_str.strip():
        return jsonify({"error": "Please enter at least one ingredient."}), 400

    recipe_text = generate_with_ai(ingredients_str.strip(), cuisine=cuisine, diet=diet, max_time=max_time)

    return jsonify({
        "recipe": recipe_text
    })


@app.route("/api/sample", methods=["GET"])
def sample_data():
    """Return dummy data for testing or prototyping."""
    return jsonify({
        "recipes": [
            {
                "id": 1,
                "title": "Simple Pasta",
                "ingredients": ["pasta", "tomato", "garlic"],
                "cook_time_minutes": 15
            },
            {
                "id": 2,
                "title": "Quick Salad",
                "ingredients": ["lettuce", "tomato", "olive oil"],
                "cook_time_minutes": 5
            }
        ]
    })


@app.route("/api/explain", methods=["GET"])
def explain_tomato():
    """Return an AI-generated explanation of what a tomato is."""
    explanation = ask_prompt("Tell me what a tomato is.")
    return jsonify({"explanation": explanation})


# Start the development server. debug=True enables auto-reload on code changes
# and shows detailed error pages. Use only in development!
if __name__ == "__main__":
    app.run(debug=True, port=5001)