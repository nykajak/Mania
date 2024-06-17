import json

content = None
with open("UserSettings.json","r") as f:
    content = f.read()

content = json.loads(content)

API_KEY = content["API_KEY"]
PATHS =  content["PATHS"]