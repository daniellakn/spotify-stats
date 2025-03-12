import urllib.parse
from temp_client_creds import client_id, client_secret
from codeChallVerifier import genChallenge, genVerifier
# codeChallenge, codeVerifier
import webbrowser
import requests
from authReqCatcher import catchTokenResponse
# from auth import getAccessToken, getAuthCode, refreshAccessToken

codeVerifier = genVerifier()

redirectUri = 'http://127.0.0.1:8000'
scope = 'user-read-private user-read-email user-top-read user-read-recently-played user-read-playback-position user-read-playback-state user-modify-playback-state user-follow-read playlist-modify-private user-read-currently-playing playlist-read-private'
authUrl = "https://accounts.spotify.com/authorize/"
tokenUrl = "https://accounts.spotify.com/api/token"

def getAuthCode(codeChallenge: str): 
    params =  {
    "response_type": 'code',
    "client_id": client_id,
    "scope" : scope,
    "code_challenge_method": 'S256',
    "code_challenge": codeChallenge,
    "redirect_uri": redirectUri,
    }

    p = urllib.parse.urlencode(params)
    webbrowser.open(authUrl + "?" + p )

    authCode = catchTokenResponse('127.0.0.1', 8000)

    return authCode

def getAccessToken(authCode: str, codeVerifier: str) -> tuple[str, str]:

    params =  {
    "grant_type": 'authorization_code',
    "code" : authCode,
    "redirect_uri": redirectUri,
    "client_id": client_id,
    "code_verifier": codeVerifier,
    }

    p = urllib.parse.urlencode(params)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(tokenUrl, headers=headers, data=p)

    # print(f'\n\n <<< JSON >>> \n {response.json()}')

    accessToken = response.json().get('access_token')
    print(f'\nThe access token: {accessToken}\n')

    refreshToken = response.json().get('refresh_token')
    print(f'\nThe refresh token: {refreshToken}\n')

    return accessToken, refreshToken



def refreshAccessToken(refreshToken: str) -> tuple[str,str]:
    params = {
    "grant_type": 'refresh_token',
    "refresh_token" : refreshToken,
    "client_id": client_id,
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(tokenUrl, headers=headers, params=params)

    accessToken = response.json().get('access_token')
    refreshToken = response.json().get('refresh_token')

    return accessToken, refreshToken
    


def writeTokens() -> tuple[str, str]:
    accessToken, refreshToken = getAccessToken(getAuthCode(genChallenge(codeVerifier)), codeVerifier)

    with open('access_token.txt', 'w') as f:
        f.write(accessToken)

    with open('refresh_token.txt', 'w') as f:
        f.write(refreshToken)

    return accessToken, refreshToken

def readTokens():
    global accessToken
    with open('access_token.txt', 'r') as f:
        accessToken = f.read().strip()
        if not accessToken:
            raise ValueError("Access token file is empty.")
        else: 
            print("access token read successfully.")

    with open('refresh_token.txt', 'r') as f:
        refreshedToken = f.read().strip()













# def writeTokens() -> tuple[str, str]:
#     accessToken, refreshToken = getAccessToken(getAuthCode(genChallenge(codeVerifier)), codeVerifier)

#     with open('access_token.txt', 'w') as f:
#         f.write(accessToken)

#     with open('refresh_token.txt', 'w') as f:
#         f.write(refreshToken)

#     # return accessToken, refreshToken




# accessToken, refreshToken = getTokens()


# refreshAccessToken(refreshToken)

# print(f'\nThe access token: {accessToken}\n')
# print(f'\nThe refresh token: {refreshToken}\n')
