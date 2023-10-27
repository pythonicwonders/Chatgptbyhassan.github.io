from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "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"

# Initialize discussions with a system message
discussions = [{"role": "system", "content": "You are a helpful assistant."}]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form["user_input"]

    # Append the user's input to the discussions
    discussions.append({"role": "user", "content": user_input})

    try:
        # Create a message for GPT-3
        message = {
            "role": "user",
            "content": user_input
        }

        # Append the user's message to the discussions
        discussions.append(message)

        # Make an API call to GPT-3
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=discussions
        )

        assistant_response = response['choices'][0]['message']['content']

        # Append the assistant's response to the discussions
        discussions.append({"role": "assistant", "content": assistant_response})

        return jsonify({"response": assistant_response})

    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500  # Return a 500 Internal Server Error with the error message

if __name__ == "__main__":
    app.run(debug=True)