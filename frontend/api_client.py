import requests

# Define the URL of the REST API endpoint
url = 'http://192.168.15.56:5057/api/noetllm?prompt=What+can+you+do?'

# Make a GET request to the API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    # Print out the 'result' field if present
    if 'result' in data:
        print("Result:", data['result'])
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")