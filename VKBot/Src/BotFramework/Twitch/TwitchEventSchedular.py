import requests



r = requests.get('https://api.twitch.tv/helix/streams/key', json={'client-id': '4dntla256uzceva3kwitjhut8nlord'})

print(r.status_code)
print(r.json())