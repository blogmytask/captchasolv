from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# API details
api_url = 'https://api.api-ninjas.com/v1/imagetotext'
api_key = '8ZnF+dyEbD6MBMrmxcWjpA==wXpVZXZuaagp6tfE'

# HTML template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image to Text</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f9;
        }
        form {
            margin-top: 20px;
        }
        input[type="text"] {
            width: 60%;
            padding: 10px;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #007BFF;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .result {
            margin-top: 20px;
            font-size: 18px;
            color: #333;
        }
    </style>
</head>
<body>
    <h1>Image to Text Converter</h1>
    <form method="POST">
        <input type="text" name="image_url" placeholder="Enter Image URL" required>
        <button type="submit">Convert</button>
    </form>
    {% if result %}
    <div class="result">
        <h2>Extracted Text:</h2>
        <p>{{ result }}</p>
    </div>
    {% else %}
    <div class="result">
        <p>No text was extracted. Please try a different image.</p>
    </div>
    {% endif %}
</body>
</html>
"""

# Function to handle API calls
def extract_text_from_image(image_url):
    try:
        print(f"Fetching image from URL: {image_url}")  # Debug log
        response = requests.get(image_url)
        response.raise_for_status()

        print("Image fetched successfully, sending to OCR API...")  # Debug log
        files = {'image': ('image.jpg', response.content)}
        headers = {'X-Api-Key': api_key}
        r = requests.post(api_url, files=files, headers=headers)
        r.raise_for_status()

        print(f"API Response: {r.json()}")  # Debug log
        response_data = r.json()
        combined_text = ''.join([item['text'] for item in response_data])
        return combined_text
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Debug log
        return f"Error: {str(e)}"

# Route for the main page
@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        image_url = request.form.get("image_url")
        result = extract_text_from_image(image_url)
    return render_template_string(html_template, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
