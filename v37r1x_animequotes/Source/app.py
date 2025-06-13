from flask import Flask, request, render_template_string
import json
import random
import os
import logging
import requests
from functools import lru_cache

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load anime quotes
with open('quotes.json', 'r') as f:
    quotes = json.load(f)

# Cache Kitsu API calls to avoid rate limits
@lru_cache(maxsize=100)
def get_character_image(character_name):
    try:
        url = f"https://kitsu.io/api/edge/characters?filter[name]={character_name}"
        headers = {'Accept': 'application/vnd.api+json'}
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data["data"]:
            return data["data"][0]["attributes"]["image"]["original"]
        logger.warning(f"No image found for {character_name}")
        return "https://placehold.co/150x150?text=Unknown"
    except Exception as e:
        logger.error(f"Error fetching image for {character_name}: {str(e)}")
        return "https://placehold.co/150x150?text=Unknown"

# Custom Jinja2 filter to evaluate expressions (vulnerable)
def eval_filter(value):
    try:
        safe_builtins = {'__builtins__': {'int': int, 'str': str}}
        result = eval(value, safe_builtins, {'os': os, 'config': app.config})
        logger.debug(f"Evaluated '{value}' to '{result}'")
        return result
    except Exception as e:
        logger.error(f"Error evaluating '{value}': {str(e)}")
        if '__subclasses__' in value:
            try:
                subclasses = [x.__name__ for x in ''.__class__.__mro__[1].__subclasses__()]
                logger.debug(f"Subclasses: {subclasses[180:190]} (indices 180-189)")
            except Exception as sub_e:
                logger.error(f"Failed to log subclasses: {sub_e}")
        return f'Invalid expression: {str(e)}'

app.jinja_env.filters['eval'] = eval_filter

# Custom rendering function to obscure Jinja2
def render_content(template_path, **data):
    with open(template_path, 'r') as f:
        template_str = f.read()
    return render_template_string(template_str, **data)

@app.route('/')
def home():
    return render_content('views/home.tmpl')

@app.route('/quote', methods=['POST'])
def quote():
    username = request.form.get('username', 'Guest')
    # Check if username is a code expression (wrapped in {})
    is_code = username.startswith('{') and username.endswith('}')
    processed_username = username[1:-1] if is_code else username
    random_quote = random.choice(quotes)
    image_url = get_character_image(random_quote['name'])
    data = {
        'username': processed_username,
        'is_code': is_code,
        'quote': random_quote['quote'],
        'name': random_quote['name'],
        'anime': random_quote['anime'],
        'image_url': image_url
    }
    return render_content('views/quote.tmpl', **data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)