import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template

# Initialize Flask App
app = Flask(_name_)

# Configure Google Gemini AI API
GENAI_API_KEY = "AIzaSyA_JVcNpZLDepTRiAz2y_f0pHY6AnwUkqs"
genai.configure(api_key=GENAI_API_KEY)

# Function to get nutrition info from Gemini AI
def get_nutrition(food_item):
    prompt = f"Provide a detailed nutritional breakdown of {food_item}, including calories, protein, carbs, fats, vitamins, and minerals."
    response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
    return response.text if response else "No data available."

# Function to generate personalized diet plan
def generate_diet_plan(age, weight, height, activity_level, goal):
    prompt = f"""
    Generate a 7-day meal plan for a {age}-year-old person who weighs {weight} kg, is {height} cm tall, has an {activity_level} activity level, and aims for {goal}.
    The plan should include breakfast, lunch, dinner, and snacks, along with macronutrients.
    """
    response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
    return response.text if response else "No meal plan available."

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# API to Get Nutrition Info
@app.route('/nutrition', methods=['POST'])
def nutrition():
    data = request.json
    food_item = data.get("food_item", "")
    if not food_item:
        return jsonify({"error": "Food item required"}), 400
    nutrition_info = get_nutrition(food_item)
    return jsonify({"food_item": food_item, "nutrition_info": nutrition_info})

# API to Generate Diet Plan
@app.route('/diet_plan', methods=['POST'])
def diet_plan():
    data = request.json
    age = data.get("age")
    weight = data.get("weight")
    height = data.get("height")
    activity_level = data.get("activity_level")
    goal = data.get("goal")

    if not all([age, weight, height, activity_level, goal]):
        return jsonify({"error": "All inputs are required"}), 400

    diet_plan = generate_diet_plan(age, weight, height, activity_level, goal)
    return jsonify({"diet_plan": diet_plan})

if _name_ == '_main_':
    app.run(debug=True)