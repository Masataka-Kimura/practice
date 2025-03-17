from flask import Flask, render_template, jsonify, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/bpm')
def api_bpm():
    # cron.pyで作成されたdata.jsonを読み込んで返す
    data_file = os.path.join(app.static_folder, 'data.json')
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            return jsonify(f.read())
    else:
        return jsonify({})

# JSONを静的ファイルとして提供（任意・安全のため）
@app.route('/data.json')
def data_json():
    return send_from_directory(app.static_folder, 'data.json')

if __name__ == '__main__':
    app.run(debug=True)
