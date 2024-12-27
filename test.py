import json
import csv

# Load JSON file
with open('results.json', 'r') as json_file:
    # Try loading multiple JSON objects if the file contains more than one
    try:
        data = json.load(json_file)  # Try loading as a single object
    except json.JSONDecodeError:
        # If that fails, try loading as a list of objects
        json_file.seek(0)  # Reset the file pointer
        data = [json.loads(line) for line in json_file]

# Extract data (example for HTTP request timings)
csv_data = []
for entry in data:
    if isinstance(entry, dict) and 'metrics' in entry:
        for metric in entry['metrics']:
            if 'http_req_duration' in metric:
                csv_data.append({
                    'Timestamp': metric['timestamp'],
                    'Request Duration (ms)': metric['http_req_duration']['value'],
                    'Status': metric['status']
                })

# Write to CSV
with open('results.csv', 'w', newline='') as csv_file:
    fieldnames = ['Timestamp', 'Request Duration (ms)', 'Status']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(csv_data)

print("Results exported to results.csv")
