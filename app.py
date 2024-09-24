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
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-white flex items-center justify-center min-h-screen">
    <div class="container mx-auto p-6 bg-gray-800 shadow-md rounded-lg w-full max-w-4xl">
        <div class="flex justify-between items-start">
            <!-- Input Section -->
            <div class="w-full">
                <form action="/generate" method="post" class="flex flex-col">
                    <textarea name="prompt" placeholder="Enter the prompt" required
                        class="w-full p-3 rounded-lg border border-gray-600 bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 h-32 mb-4"></textarea>
                    <button type="submit"
                        class="bg-blue-500 hover:bg-blue-600 text-white p-3 rounded-lg w-full">
                        Generate Image
                    </button>
                </form>
            </div>

            <!-- Image Section -->
            <div class="ml-6 flex flex-col items-center">
                {% if image_url %}
                    <img src="{{ image_url }}" alt="Generated Image" class="max-w-sm h-auto rounded-lg mb-4">
                    <a href="{{ image_url }}" download class="text-blue-400 hover:text-blue-600">Download Image</a>
                {% endif %}
            </div>
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
    # Fetch the user input
    user_prompt = request.form["prompt"]

    # Define the prefix
    prefix = "No colors, just black outlines on a white background. "

    # Modify the prompt to remove any mention of colors
    prompt = user_prompt.replace("vibrant colors", "").replace("colors", "").strip()

    # Ensure the prefix is added to the processed prompt
    final_prompt = prefix + prompt

    # Correct the input dictionary format
    input_data = {
        "prompt": final_prompt,
        "num_outputs": 1,
        "aspect_ratio": "4:3",
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