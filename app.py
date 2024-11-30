
from flask import Flask, redirect, request, jsonify, render_template, session
import requests
import strava_api
import matplotlib.pyplot as plt
import io
import base64
from flask import send_file


app = Flask(__name__)


CLIENT_ID = '141132'
CLIENT_SECRET = 'e3a24de0ded5ddc970ec540cc37c491f9c7bd856'
REDIRECT_URI = 'http://localhost:5000/exchange_token'

@app.route('/')
def home():
    auth_url = strava_api.generate_auth_url()
    return redirect(auth_url)

@app.route('/exchange_token')
def exchange_token():
    code = request.args.get('code')
    if code:
        token_data = strava_api.exchange_token(code)
        if token_data:
            access_token = token_data.get("access_token")

            activities = strava_api.get_activity_data(access_token)
            print('Activities passed:', activities)

            return render_template('dashboard.html', activities=activities)
        else:
            return "Error exchanging code for token", 400
    else:
        return "Error: No authorization code received", 400

@app.route('/graph')
def graph():
    access_token = session.get("access_token")
    if not access_token:
        return "No access token found. Authenticate first!", 400

    activities = strava_api.get_activity_data(access_token)
    if not activities:
        return "No activities found to plot!"

    names, distances, moving_times = strava_api.process_activity_data(activities)

    plt.figure(figsize=(10, 6))
    plt.bar(names, distances, color='skyblue')
    plt.xlabel('Activity Name')
    plt.ylabel('Distance (km)')
    plt.title('Distance Covered in Activities')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)

