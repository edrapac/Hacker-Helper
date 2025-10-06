from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask & Docker</h1>'

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    host = data.get('host')
    ssl = data.get('ssl', False)
    dns = data.get('dns', False)

    if not host:
        return jsonify({'error': 'host is required'}), 400

    # Call the hacker-helper API
    try:
        resp = requests.post(
            'http://hacker-helper:8081/scan',
            json={'host': host, 'ssl': ssl, 'dns': dns},
            timeout=900
        )
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")