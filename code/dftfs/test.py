import requests

print("Hello")
response = requests.get("http://localhost:5000/")
print("Hello")
print(response.raw)
exit()
