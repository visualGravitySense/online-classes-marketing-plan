import requests; print('Testing API...'); response = requests.get('http://127.0.0.1:5001/'); print(f'Status: {response.status_code}')
