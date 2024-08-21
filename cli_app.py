import replicate
import requests
import os
import uuid
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress only the single InsecureRequestWarning from urllib3 needed
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Ask the user for the prompt
prompt = input("Enter the prompt: ")

# Correct the input dictionary format
input_data = {
    "prompt": prompt
}

output = replicate.run(
  "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
  input=input_data
)
print(output)
# Assuming the output is a list with a single URL
image_url = output[0]

def download_image(url, retries=3):
    session = requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    try:
        response = session.get(url, verify=False)  # Disable SSL verification
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        return None

# Download the image
image_content = download_image(image_url)

if image_content:
    # Save the image locally with a unique name
    unique_id = uuid.uuid4()
    image_extension = os.path.splitext(image_url)[1]
    image_path = f"./pics/image_{unique_id}{image_extension}"
    
    with open(image_path, 'wb') as file:
        file.write(image_content)
        print(f"Image saved successfully as {image_path}!")
else:
    print("Failed to download the image.")