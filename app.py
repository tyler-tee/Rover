import json
import os
from flask import (Flask, render_template, url_for, request)
import openai
from PetfinderClient.petfinder_client import PetfinderClient


app_path = os.path.dirname(__file__)


def create_app():
    app = Flask(__name__)

    config_path = os.path.join(app_path, "config/config.json")
    app.config.from_file(config_path, load=json.load)

    return app


app = create_app()


def get_breed(dog):
    breeds = dog.get('breeds')
    if not breeds:
        return "Unknown"
    primary = breeds.get('primary', 'Unknown')
    secondary = breeds.get('secondary', 'Unknown')
    return f"{primary} / {secondary}"


def get_location(dog):
    address = dog.get("contact", {}).get("address")
    if not address:
        return "Location unknown"
    city = address.get('city', 'Unknown')
    state = address.get('state', 'Unknown')
    return f"{city}, {state}"


def get_photo(dog):
    default_photo = url_for("static", filename="assets/no_photo_avail.jpg")
    return dog.get("photos", [{}])[0].get("small", default_photo) if dog.get('photos') else default_photo


@app.route('/', methods=['GET', 'POST'])
def render_dog_finder():
    if request.method == 'POST':
        openai.api_key = app.config['OPENAI_KEY']
        petfinder_key = app.config['PETFINDER_KEY']
        petfinder_sec = app.config['PETFINDER_SEC']

        # Initialize Petfinder client
        petfinder_api = PetfinderClient(petfinder_key, petfinder_sec)
        petfinder_api.auth()

        # Get the user description from the form
        user_description = request.json.get('description', '')

        # Step 1: Use GPT-4o-mini to process the description
        try:
            gpt_response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """
                        You are an assistant helping users find adoptable dogs using the Petfinder API.
                        Always include the following parameters in the JSON output:
                        - status (always set to 'adoptable')

                        Include the following parameters **only if relevant**:
                        - breed (if mentioned in the description)
                        - size (one of 'small', 'medium', 'large', 'extra-large')
                        - gender (one of 'male', 'female')
                        - age (one of 'baby', 'young', 'adult', 'senior')
                        - color (if mentioned in the description)
                        - coat (one of 'short', 'medium', 'long', 'wire', 'hairless', 'curly')
                        - location (if mentioned in the description)
                        - good_with_children (1 or 0)
                        - good_with_dogs (1 or 0)
                        - good_with_cats (1 or 0)

                        Output valid JSON only, with no extra text or commentary.
                        """
                    },
                    {
                        "role": "user",
                        "content": f"""
                        Translate this description into Petfinder search parameters.
                        Description: "{user_description}"
                        """
                    }
                ],
                max_tokens=150
            )
            ai_response = gpt_response.choices[0].message.content
            ai_response = ai_response.replace('```json', '').replace('```', '')

        except Exception as e:
            return {"error": f"Failed to process input with GPT-4o-mini: {str(e)}"}, 500

        # Step 2: Parse GPT response into parameters
        try:
            params = json.loads(ai_response)
        except json.JSONDecodeError:
            return {"error": "GPT response is not valid JSON. Please refine the prompt."}, 500

        # Step 3: Query Petfinder with parameters from GPT
        try:
            response = petfinder_api.get_animals(type='dog', **params)
            if response['success']:
                dogs = response['data']['animals']
            else:
                dogs = []
        except Exception as e:
            return {"error": f"Failed to query Petfinder: {str(e)}"}, 500

        # Step 4: Format and return results
        if dogs:
            dogs = [
                {
                    "id": dog.get("id"),
                    "name": dog.get("name", "Unknown"),
                    "url": dog.get("url"),
                    "breed": get_breed(dog),
                    "age": dog.get("age", "Unknown"),
                    "gender": dog.get("gender", "Unknown"),
                    "size": dog.get("size", "Unknown"),
                    "photo": get_photo(dog),
                    "description": dog.get("description", "No description available."),
                    "contact_email": dog.get("contact", {}).get("email", "Not provided"),
                    "contact_phone": dog.get("contact", {}).get("phone", "Not provided"),
                    "location": get_location(dog)
                } for dog in dogs
            ]

            return {"success": True, "dogs": dogs}

        return {"error": "No dogs found matching the criteria."}

    # Render the Rover interface for GET requests
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
