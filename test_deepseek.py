import os
import requests

API_KEY = "sk-e6a59cd4626d432593a159e7b7227672"
BASE_URL = "https://api.deepseek.com"

url = f"{BASE_URL}/chat/completions"

payload = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "user", "content": "Hola, ¿puedes confirmar que la API funciona?"}
    ]
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}

resp = requests.post(url, json=payload, headers=headers)

print("Status code:", resp.status_code)
print("Respuesta:")
print(resp.text)
