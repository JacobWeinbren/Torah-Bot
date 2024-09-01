import requests


def get_sefaria_data(body):
    url = "https://www.sefaria.org/api/find-refs"
    params = {"with_text": 1}
    data = {"text": {"title": "", "body": body}}
    try:
        response = requests.post(url, params=params, json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_message = f"Error accessing Sefaria API: {str(e)}"
        if hasattr(e, "response") and e.response is not None:
            error_message += f"\nStatus code: {e.response.status_code}"
            error_message += f"\nResponse text: {e.response.text[:200]}..."
        raise Exception(error_message)
