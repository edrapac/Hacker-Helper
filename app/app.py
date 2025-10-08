from flask import Flask, request, jsonify, render_template
import requests
import subprocess
import os
import threading
import uuid

app = Flask(__name__)

scan_threads = {}

def run_scan(cmd, output_file):
    with open(output_file, 'w') as f:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            f.write(line)
            f.flush()
        process.wait()

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

@app.route('/scan', methods=['POST','GET'])
def scan():
    # render form for starting the scan
    if request.method == 'GET':
        return render_template('start_scan.html')
    if request.method == 'POST':
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

        scan_id = str(uuid.uuid4())
        output_file = f"/tmp/scan_{scan_id}.txt"
        thread = threading.Thread(target=run_scan, args=(cmd, output_file))
        thread.start()
        scan_threads[scan_id] = thread

        return jsonify({'scan_id': scan_id})

@app.route('/scan_output/<scan_id>', methods=['GET'])
def scan_output(scan_id):
    output_file = f"/tmp/scan_{scan_id}.txt"
    if not os.path.exists(output_file):
        return jsonify({'output': '', 'finished': False})
    with open(output_file, 'r') as f:
        content = f.read()
    finished = not scan_threads[scan_id].is_alive() if scan_id in scan_threads else True
    return jsonify({'output': content, 'finished': finished})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)