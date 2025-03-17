import requests, datetime, json, os

OURA_TOKEN = os.environ.get('OURA_TOKEN')

def fetch_latest_bpm():
    dt_now = datetime.datetime.now(datetime.timezone.utc)
    dt_12h_ago = dt_now - datetime.timedelta(hours=12)

    url = 'https://api.ouraring.com/v2/usercollection/heartrate'
    params = {
        'start_datetime': dt_12h_ago.isoformat(),
        'end_datetime': dt_now.isoformat()
    }
    headers = {'Authorization': f'Bearer {OURA_TOKEN}'}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print("APIリクエスト失敗:", response.text)
        return {}

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

# JSONファイルに保存
def save_to_json(data):
    data_file = os.path.join('static', 'data.json')
    with open(data_file, mode='w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

if __name__ == "__main__":
    bpm_data = fetch_latest_bpm()
    save_to_json(bpm_data)
