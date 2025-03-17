from flask import Flask, render_template, jsonify
import requests, datetime, os

app = Flask(__name__)

OURA_TOKEN = os.environ.get('OURA_TOKEN')

def get_latest_bpm():
    dt_now = datetime.datetime.now(datetime.timezone.utc)
    dt_12h_ago = dt_now - datetime.timedelta(hours=12)

    url = 'https://api.ouraring.com/v2/usercollection/heartrate'
    params = {
        'start_datetime': dt_12h_ago.isoformat(),
        'end_datetime': dt_now.isoformat()
    }
    headers = {'Authorization': f'Bearer {OURA_TOKEN}'}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    hrs = data.get('data', [])

    if hrs:
        latest = hrs[-1]
        return {
            'bpm': latest['bpm'],
            'timestamp': latest['timestamp']
        }
    else:
        return {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/bpm')
def api_bpm():
    return jsonify(get_latest_bpm())

if __name__ == '__main__':
    app.run(debug=True)
