from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import markdown

app = Flask(__name__)

# Allow requests from frontend (Update with your frontend URL if needed)
CORS(app, resources={r"/generate_meal_plan": {"origins": "http://127.0.0.1:5500"}})

# Configure Gemini API
genai.configure(api_key="AIzaSyA1LpSjATRhpedvCKgtWU1XZ3sxUfJP7a4")  # Replace with your actual API key

# Create Gemini model instance
model = genai.GenerativeModel("tunedModels/personalizeddietrecommendation-1h9ouyrco")

# Function to generate a meal plan
def generate_meal_plan(data):
    try:
        prompt = (
            f"Create a personalized 7-day meal plan for a {data.get('diet', 'balanced')} diet. "
            f"User details: Age {data.get('age', 'N/A')}, Gender {data.get('gender', 'N/A')}, "
            f"Height {data.get('height', 'N/A')} cm, Weight {data.get('weight', 'N/A')} kg. "
            f"Consider allergies: {data.get('allergies', 'None')}. "
            f"Health goal: {data.get('healthGoals', 'General Health')}. "
            f"Activity level: {data.get('activityLevel', 'Moderate')}. "
            f"Preferred cuisine: {data.get('cuisine', 'No Preference')}. "
            f"Include breakfast, lunch, and dinner for each day."
            f"Include number of calories provided by each meal."
        )

        response = model.generate_content(prompt)
        return response.text if response else "No response from AI."
    
    except Exception as e:
        return f"Error: {str(e)}"

# Define API route
@app.route('/generate_meal_plan', methods=['POST', 'OPTIONS'])
def generate_meal():
    if request.method == "OPTIONS":  # Handle CORS preflight request
        response = jsonify({"message": "CORS preflight successful"})
        response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:5500")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response, 200

    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["diet", "healthGoals", "activityLevel"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Generate meal plan
        meal_plan = generate_meal_plan(data)
        formatted_plan = markdown.markdown(meal_plan)
        response = jsonify({"meal_plan": formatted_plan})
        response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:5500")  # Allow frontend
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle server errors

if __name__ == '__main__':
    app.run(debug=True)