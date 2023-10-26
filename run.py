from flask import Flask, request, jsonify
import subprocess
import os
import requests
import uuid
import config
import time


app = Flask(__name__)
app.secret_key = config.SECRET_KEY


@app.route('/upscale', methods=['POST'])
def upscale():
    s_param = request.form.get('s', 2)  # Default scale is 2x

    input_image_url = request.form.get('input_image_url')

    if input_image_url:
        # Check if input_image_url is provided
        response = requests.get(input_image_url)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to download the image'})

        # Process the image in memory (without saving it to local storage)
        input_image_bytes = response.content
    elif 'input_image' in request.files:
        # If the user uploads an image, read it from the request
        uploaded_file = request.files['input_image']
        input_image_bytes = uploaded_file.read()
    else:
        return jsonify({'error': 'No input image provided'})

    # Generate a unique filename for the input and output files
    unique_id = str(uuid.uuid4())
    timestamp = int(time.time())
    input_file_path = f'input_{unique_id}_{timestamp}.jpg'
    output_file_path = f'output_{unique_id}_{timestamp}.png'

    # Save the input image to a file
    with open(input_file_path, 'wb') as f:
        f.write(input_image_bytes)

    # Call the realesrgan-ncnn-vulkan.exe command with specified input and output paths
    command = f'realesrgan-ncnn-vulkan.exe -i {input_file_path} -o {output_file_path} -n realesrgan-x4plus -s {s_param}'

    # Execute the command
    subprocess.run(command, shell=True)

    # Send the processed image as a direct response to the client
    with open(output_file_path, 'rb') as output_file:
        processed_image = output_file.read()

    # Delete the input and output files
    os.remove(input_file_path)
    os.remove(output_file_path)

    return processed_image, 200, {'Content-Type': 'image/png'}

if __name__ == '__main__':
    app.run(debug=False)
