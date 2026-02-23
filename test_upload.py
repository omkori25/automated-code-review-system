import requests

url = "http://localhost:8000/analysis/upload"
files = {'files': ('test_day4.py', open('test_day4.py', 'rb'), 'text/x-python')}

response = requests.post(url, files=files)
print(f"Status Code: {response.status_code}")
print("Response:")
print(response.json())
