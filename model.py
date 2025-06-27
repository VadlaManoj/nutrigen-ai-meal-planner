import google.generativeai as genai

genai.configure(api_key="AIzaSyBjOXRIO3eEHPftE0TjnM5hJpU4S0eELxY")

for model in genai.list_models():
    print(model.name)
