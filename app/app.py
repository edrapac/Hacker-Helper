from flask import Flask, request, jsonify, render_template
import requests
import subprocess
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
@app.route('/health', methods=['GET'])
def hello_geek():
    return '<h1>Hello from Flask & Docker</h1>'

@app.route('/scans', methods=['GET']) 
def scans():
    output_dir = '/tmp'
    scan_files = []
    tool_map = {
        'nmap': 'Nmap',
        'gobuster_dirs': 'Gobuster (Directories)',
        'gobuster_files': 'Gobuster (Files)',
        'gobuster_vhosts': 'Gobuster (VHosts)',
        'gobuster_dns': 'Gobuster (DNS)',
    }
    for fname in os.listdir(output_dir):
        fpath = os.path.join(output_dir, fname)
        if os.path.isfile(fpath):
            with open(fpath, 'r') as f:
                content = f.read()
            # Determine tool name from filename
            tool = next((tool_map[key] for key in tool_map if key in fname), fname)
            scan_files.append({'tool': tool, 'filename': fname, 'content': content})
    return render_template('scans.html', scan_files=scan_files)

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    host = data.get('host')
    ssl = data.get('ssl', False)
    dns = data.get('dns', False)

    if not host:
        return jsonify({'error': 'host is required'}), 400

    cmd = ["./entrypoint.sh"]
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
    app.run(debug=True, host="0.0.0.0", port=5002)