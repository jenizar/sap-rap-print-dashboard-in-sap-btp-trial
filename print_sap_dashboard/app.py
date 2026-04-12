from markupsafe import Markup
import json
import urllib.request
from flask import Flask, request, jsonify, render_template
from datetime import datetime
from dateutil.relativedelta import relativedelta
import jinja2
import pdfkit
import os
import ast

app = Flask(__name__)
# Configuration
OUTPUT_FOLDER = 'HTML_CHART'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/dashboard', methods=['GET', 'POST'])
def show_element():
    receive_data = request.get_json()     
    json_string = json.dumps(receive_data)
    json_output = json.loads(json_string) 
    python_list = ast.literal_eval(json_output)
    print(type(python_list))
    print(python_list)  
    # Render template
    for item in python_list: 
        company = item["company"]
        address = item["address"]
        service_name = item["service_name"]
        begin_date = item["begin_date"]
        end_date = item["end_date"]
        remain_days = item["remain_days"]
        status = item["status"]
 
    context = {
            'company': company,
            'address': address,
            'service_name': service_name,
            'begin_date': begin_date,
            'end_date': end_date,
            'remain_days': remain_days,
            'status': status,    
            'items': receive_data        
        } 
    # Render template
    rendered_html = render_template('page.html', **context)  
    # Save to file
    filename = f"page_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    filepath = os.path.join(OUTPUT_FOLDER, filename)      
    with open(filepath, 'w', encoding='utf-8') as f:
         f.write(rendered_html)
        
    return jsonify({
            'success': True,
            'message': 'HTML file generated successfully',
            'filename': filename,
            'path': os.path.abspath(filepath)
        })     
    return render_template("index.html", data = receive_data) 
if __name__ == "__main__":
    app.run()  