import requests

# Strava App Credentials
CLIENT_ID = "141132"
CLIENT_SECRET = "e3a24de0ded5ddc970ec540cc37c491f9c7bd856"
REDIRECT_URI = "http://localhost:5000/exchange_token"

def generate_auth_url():
    """Generate the URL for user authorization."""
    auth_url = (
        f"https://www.strava.com/oauth/authorize"
        f"?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
        f"&response_type=code&scope=read,activity:read_all"
    )
    return auth_url

def exchange_token(code):
    url = "https://www.strava.com/oauth/token"
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json()  # Contains access_token
    else:
        print("Error exchanging token:", response.status_code, response.text)
        return None

def get_activity_data(access_token):
    """
    Fetch the user's recent activity data.
    :param access_token: The access token to authenticate API requests
    :return: A list of activities or an empty list in case of failure
    """
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        activities = response.json()
        detailed_activities = [
            {
                'name': activity.get('name', 'Unnamed Activity'),
                'distance': activity.get('distance', 0),  
                'moving_time': activity.get('moving_time', 0), 
                'calories': activity.get('calories')  
            }
            for activity in activities
        ]
        return detailed_activities
    else:
        print("Error fetching activities:", response.status_code, response.text)
        return []
def process_activity_data(activities):
    distances = [activity['distance'] / 1000 for activity in activities]  
    moving_times = [activity['moving_time'] / 60 for activity in activities]  
    names = [activity['name'] for activity in activities]
    return names, distances, moving_times
