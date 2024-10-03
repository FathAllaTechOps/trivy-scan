import os
import json
from datetime import datetime
import pandas as pd

# Reading Environment variables
html_name = os.getenv('HTML')

# Construct the file path using f-string
file_path = f'{html_name}.json'
# Read the JSON data from the file
with open(file_path, 'r') as file:
    data = json.load(file)

# Extract the "Results" list
results = data['Results']

# Get the current date
current_date = datetime.now().strftime('%Y-%m-%d')

# Initialize HTML string with CSS style and table headers
html = f'''
<!DOCTYPE html>
<html>
<head>
<style>
table {{
  border-collapse: collapse;
  width: 100%;
}}

th, td {{
  text-align: left;
  padding: 8px;
}}

th {{
  background-color: #f2f2f2;
}}

tr:nth-child(even) {{
  background-color: #f2f2f2;
}}
</style>
</head>
<body>

<h2> {html_name} Service Vulnerabilities - {current_date}</h2>

<table border="1">
<tr>
  <th>Date</th>
  <th>Vulnerability ID</th>
  <th>Package Name</th>
  <th>Installed Version</th>
  <th>Fixed Version</th>
  <th>Status</th>
  <th>Title</th>
  <th>Description</th>
  <th>Severity</th>
  <th>Primary URL</th>
</tr>
'''

# Helper function to sort vulnerabilities by severity
def sort_vuln_by_severity(vuln):
    severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
    return severity_order[vuln['Severity'].lower()]

# Iterate over the results and add rows to the table
for result in results:
    if 'Vulnerabilities' in result:
        vulnerabilities = result['Vulnerabilities']
        vulnerabilities.sort(key=sort_vuln_by_severity)  # Sort by severity
        for vuln in vulnerabilities:
            html += '<tr>'
            html += f'<td>{vuln.get("PublishedDate", "")}</td>'
            html += f'<td>{vuln.get("VulnerabilityID", "")}</td>'
            html += f'<td>{vuln.get("PkgName", "")}</td>'
            html += f'<td>{vuln.get("InstalledVersion", "")}</td>'
            html += f'<td>{vuln.get("FixedVersion", "")}</td>'
            html += f'<td>{vuln.get("Status", "")}</td>'
            html += f'<td>{vuln.get("Title", "")}</td>'
            html += f'<td>{vuln.get("Description", "")}</td>'
            html += f'<td>{vuln.get("Severity", "")}</td>'
            html += f'<td><a href="{vuln.get("PrimaryURL", "")}" target="_blank">{vuln.get("PrimaryURL", "")}</a></td>'
            html += '</tr>'

# Close the HTML table and body
html += '''
</table>

</body>
</html>
'''

# Construct the output file using f-string
output_file = f'{html_name}.html'
# Write the HTML assessment to a file
with open(output_file, 'w') as file:
    file.write(html)
    print(f"HTML file '{output_file}' created successfully.")