from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    host = data.get('host')
    ssl = data.get('ssl', False)
    dns = data.get('dns', False)

    if not host:
        return jsonify({'error': 'host is required'}), 400

    cmd = ["/entrypoint.sh"]
    if ssl:
        cmd.append("--ssl")
    if dns:
        cmd.append("--dns")
    cmd.append(host)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081,debug=True)