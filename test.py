from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

if __name__ == '__main__':
    response = client.get("/country?continent=south%20america")
    list_of_temp = []
    for country in response.json()["List of countries"]:
        list_of_temp.append((client.get(f"/country/{country}/temperature").json()["Temperature"], country))
    warmest_country = max(list_of_temp)
    print(warmest_country[1])
