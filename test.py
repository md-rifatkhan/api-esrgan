
import requests
api_url = 'https://evolved-awaited-herring.ngrok-free.app/upscale'  # Replace with your API URL
files = {
    'input_image': open('xd.jpg', 'rb')  # Replace with the path to your image file
}
data = {
    's': '2'  # Optional scale factor (default is 2)
}

response = requests.post(api_url, files=files, data=data)
if response.status_code == 200:
    with open('output_image.png', 'wb') as output_file:
        output_file.write(response.content)
    print('Image processed and saved as output_image.png')
else:
    print('Error:', response.json())