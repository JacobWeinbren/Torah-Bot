import requests


def get_sefaria_data(text):
    url = "https://www.sefaria.org/api/find-refs?with_text=1"
    response = requests.post(url, json={"text": text})
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}\n{response.text}")
    return response.json()
