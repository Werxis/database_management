import requests

s = requests.session()

json = {
    'username': 'test',
    'password': 'password'
}

# register
resp = s.post('http://localhost:5000/login',
    json=json
)

print('Status code: ' + str(resp.status_code))
print(resp.json())

resp = s.put('http://localhost:5000/login',
    json=json
)

print('Status code: ' + str(resp.status_code))
print(resp.json())

resp = s.get('http://localhost:5000/login')

print('Status code: ' + str(resp.status_code))
print(resp.json())

resp = s.delete('http://localhost:5000/logout'
)

print('Status code: ' + str(resp.status_code))
print(resp.json())

resp = s.get('http://localhost:5000/login')

print('Status code: ' + str(resp.status_code))
print(resp.json())