import requests

url = "http://127.0.0.1:8000/create/user/van laere/pierric"

response = requests.post(url)

if response.status_code == 200:
    print("Utilisateur créé avec succès : ", response.json())
else:
    print("Erreur : ", response.status_code, response.text)