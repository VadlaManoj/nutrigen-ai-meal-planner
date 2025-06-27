import streamlit as st
import requests

# Set your OpenRouter API Key
OPENROUTER_API_KEY = "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"  # Replace with your real key

# App Title
st.title("NutriGen 🍽️ - Personalized AI Meal Planner")
st.write("Get a customized, healthy meal plan based on your dietary needs!")

# User Inputs
st.subheader("Tell us about your dietary preferences:")

col1, col2 = st.columns(2)

with col1:
    dietary_restrictions = st.text_input("Dietary Restrictions (e.g., vegan, keto, gluten-free):")
    allergies = st.text_input("Allergies (e.g., nuts, dairy, seafood):")

with col2:
    health_conditions = st.text_input("Health Conditions (e.g., diabetes, heart health):")
    activity_level = st.selectbox("Activity Level:", ["Sedentary", "Lightly active", "Moderately active", "Very active"])

taste_preferences = st.text_area("Taste Preferences (e.g., spicy food, Mediterranean cuisine, dislike broccoli):")
day_selected = st.selectbox("Select Day", ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"])

# Function to query OpenRouter
def get_meal_plan_from_ai(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/mistral-7b-instruct",  # Fast, free model
        "messages": [
            {"role": "system", "content": "You are a professional nutritionist."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1024
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"❌ Error {response.status_code}: {response.text}"

# Button to generate plan
if st.button("Generate Meal Plan"):
    st.subheader(f"{day_selected} Meal Plan 🍱")
    with st.spinner("AI is cooking up your plan..."):
        prompt = f"""
        Create a detailed {day_selected} personalized meal plan with ingredients and recipes.
        - Dietary Restrictions: {dietary_restrictions}
        - Allergies: {allergies}
        - Health Conditions: {health_conditions}
        - Activity Level: {activity_level}
        - Taste Preferences: {taste_preferences}

        Include breakfast, lunch, dinner, and a snack if suitable.
        """
        result = get_meal_plan_from_ai(prompt)
        st.write(result)
