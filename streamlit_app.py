import streamlit as st
from transformers import pipeline
from openai import OpenAI 

from flask import Flask, render_template, request

# Initialize the app
app = Flask(__name__)

# Set up your OpenAI API key (make sure to replace with your actual API key)
openai.api_key = 'your-openai-api-key'

# Define the route for the main page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the user input from the form
        prompt = request.form["prompt"]
        max_tokens = int(request.form["max_tokens"])

        # Create two responses: one creative (high temperature) and one predictable (low temperature)
        creative_response = openai.Completion.create(
            engine="text-davinci-003",  # You can also use 'gpt-3.5-turbo' or 'gpt-4'
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.9  # High temperature for creative response
        )
        
        predictable_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.2  # Low temperature for predictable response
        )

        # Extract the responses
        creative_text = creative_response.choices[0].text.strip()
        predictable_text = predictable_response.choices[0].text.strip()

        # Return the results to the template
        return render_template("index.html", creative_response=creative_text, predictable_response=predictable_text)

    # If the request is a GET, just render the default form
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

