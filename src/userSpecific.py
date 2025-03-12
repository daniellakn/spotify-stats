import requests
from auth import writeTokens, readTokens
accessToken = None

def usersCurrentProfile():
    readTokens()

    headers = {
        'Authorization': f'Bearer {accessToken}'
    }
    response = requests.get( "https://api.spotify.com/v1/me", headers=headers)
    if (response.status_code != 200):
        writeTokens()
    response = requests.get( "https://api.spotify.com/v1/me", headers=headers)
    print(response.json())

usersCurrentProfile()


def whatever():
    pass



