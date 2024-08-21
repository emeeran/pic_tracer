from flask import Flask, request, render_template_string
import replicate
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress only the single InsecureRequestWarning from urllib3 needed
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

app = Flask(__name__)

# HTML template for the chat-like UI
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Generator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            height: 100vh;
        }
        .container {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 20px;
        }
        .image-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 20px;
        }
        .image-container img {
            max-width: 100%;
            height: auto;
        }
        .download-link {
            margin-top: 10px;
        }
        .input-container {
            display: flex;
            align-items: center;
        }
        .input-container {
            position: relative;
            width: 160%; /* Adjust the width as needed */
        }
        
        .input-container input[type="text"] {
            width: 100%;
            padding: 10px;
            font-size: 16px;
            box-sizing: border-box; /* Ensure padding is included in the width */
        }
        
        .input-container .generate-button {
            position: absolute;
            right: 0;
            top: 0;
            bottom: 0;
            padding: 0 20px;
            font-size: 16px;
            cursor: pointer;
            border: none;
            background-color: #007BFF; /* Adjust the background color as needed */
            color: white;
        }
        
        .input-container button {
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            margin-left: 10px;
        }
        
    </style>
</head>
<body>
    <div class="container">
        <div class="image-container">
            {% if image_url %}
                <img src="{{ image_url }}" alt="Generated Image" style="max-width: 100%; height: auto;">
                <a href="{{ image_url }}" download class="download-link">Download Image</a>
            {% endif %}
        </div>
        <div class="input-container">
            <form action="/generate" method="post">
                <input type="text" name="prompt" placeholder="Enter the prompt" required>
                <button type="submit">Generate Image</button>
            </form>
        </div>
    </div>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(html_template, image_url=None)


@app.route("/generate", methods=["POST"])
def generate_image():
    prompt = request.form["prompt"]

    # Correct the input dictionary format
    input_data = {
        "prompt": prompt,
        "num_outputs": 1,
        "aspect_ratio": "1:1",
        "output_format": "webp",
        "output_quality": 80,
    }

    output = replicate.run("black-forest-labs/flux-schnell", input=input_data)
    print(output)

    # Assuming the output is a list with a single URL
    image_url = output[0]

    return render_template_string(html_template, image_url=image_url)


if __name__ == "__main__":
    app.run(debug=True)