import requests
import pandas as pd

# Function to get Spotify access token
def get_spotify_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    auth_data = auth_response.json()
    return auth_data['access_token']
print("done 1")
# Function to search for a track and get its ID
def search_track(track_name, artist_name, token):
    query = f"{track_name} artist:{artist_name}"
    url = f"https://api.spotify.com/v1/search?q={query}&type=track"
    response = requests.get(url, headers={'Authorization': f'Bearer {token}'})
    json_data = response.json()
    try:
        first_result = json_data['tracks']['items'][0]
        track_id = first_result['id']
        return track_id
    except (KeyError, IndexError):
        return None
print("done 2")
# Function to get track details, including image URL
def get_track_details(track_id, token):
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    response = requests.get(url, headers={'Authorization': f'Bearer {token}'})
    json_data = response.json()
    image_url = json_data['album']['images'][0]['url']
    return image_url
print("done 3")
# Your Spotify API Credentials
client_id = 'insert your client id'
client_secret = 'insert your secret id'

# Get Access Token
access_token = get_spotify_token(client_id, client_secret)

# Read your DataFrame (replace 'your_file.csv' with the path to your CSV file)
url='E:\\power_bi\\projects\\Advanced Power bi project\\track_details.csv'
df_spotify = pd.read_csv(url, encoding='ISO-8859-1')
print("done 4")
# Loop through each row to get track details and add to DataFrame
v=0
for i, row in df_spotify.iterrows():
    track_id = search_track(row['track_name'], row['artist_name'], access_token)
    if track_id:
        image_url = get_track_details(track_id, access_token)
        df_spotify.at[i, 'image_url'] = image_url
        print(row,v)
        v+=1
        

# Save the updated DataFrame (replace 'updated_file.csv' with your desired output file name)
url2='E:\\power_bi\\projects\\Advanced Power bi project\\url_data.csv'
df_spotify.to_csv(url2, index=False)
print("done 5")
