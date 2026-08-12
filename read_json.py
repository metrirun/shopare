import json

with open('check.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('📄 Content of check.json:')
print(f"Name: {data.get('name')}")
print(f"Status: {data.get('status')}")
print(f"Version: {data.get('version')}")
