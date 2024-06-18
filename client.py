import requests

# response = requests.post(
#     'http://127.0.0.1:5000/user/',
#     json={"name": "user_2", "password": "aaaaaaaa"},
# )
# print(response.status_code)
# print(response.text)

# response = requests.get(
#     'http://127.0.0.1:5000/user/1/',
# )
# print(response.status_code)
# print(response.text)

# response = requests.patch(
#     'http://127.0.0.1:5000/user/1/',
#     json={"name": "new_user_2", "password": "Rrrrrrrrrrrrr"}
# )
# print(response.status_code)
# print(response.text)

# response = requests.post(
#     'http://127.0.0.1:5000/ad/',
#     json={
#         "header": "Ads #1",
#         "description": "I want to buy a house",
#         "user_id": 1},
# )
# print(response.status_code)
# print(response.text)


# response = requests.patch(
#     'http://127.0.0.1:5000/ads/1',
#     json={
#         "header": "Ads #111",
#         "description": "I don't want to buy a house",
#         "user_id": 1},
# )
# print(response.status_code)
# print(response.text)


response = requests.get(
    'http://127.0.0.1:5000/ads/1',
)
print(response.status_code)
print(response.text)

# response = requests.delete(
#     "http://127.0.0.1:5000/ads/2/",
# )
# print(response.status_code)
# print(response.text)

# response = requests.delete(
#     "http://127.0.0.1:5000/user/1/",
# )
# print(response.status_code)
# print(response.text)