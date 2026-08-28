import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

def create_html_report(results_data):
    """
    Generates a modern HTML report using Jinja2
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(current_dir))
    template = env.get_template('template.html')
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_output = template.render(
        results=results_data,
        timestamp=timestamp
    )
    
    # Save report to root directory
    report_path = os.path.join(current_dir, '..', 'security_report.html')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_output)
        
    return os.path.abspath(report_path)