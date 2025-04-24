import yaml
import requests
import time
from collections import defaultdict
import json

# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to perform health checks
def check_health(endpoint):
    url = endpoint['url']

    #If method field is omitted, the default is GET.
    # Added default value as GET method in case of None
    method = endpoint.get('method','GET')

    # If header field is omitted, no headers need to be added to or modified in the HTTP request.
    # Added default value as empty dictionary in case of None
    headers = endpoint.get('headers', {})

    # If body field is omitted, no body is sent in the request.
    # If body field is not None, it loads the json. Else, keep the body as None.
    body = endpoint.get('body')

    if body is not None:
        body = json.loads(body)
    else:
        body = None

    try:
        response = requests.request(method, url, headers=headers, json=body)
        # Endpoints are only considered available if they meet the following conditions
        # - Status code is between 200 and 299
        # - Endpoint responds in 500ms or less

        #Added logic to check if endpoint responds in 500ms or less
        if 200 <= response.status_code < 300 and response.elapsed.total_seconds() * 1000 < 500:
            return "UP"
        else:
            return "DOWN"
    except requests.RequestException:
        return "DOWN"

# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})
    while True:

        for endpoint in config:
            #Must ignore port numbers when determining domain

            #Added logic to remove port based on split with ":"
            domain = endpoint["url"].split("//")[-1].split("/")[0].split(':')[0]
            result = check_health(endpoint)

            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

        # Log cumulative availability percentages
        for domain, stats in domain_stats.items():
            print()
            availability = round(100 * stats["up"] / stats["total"])
            print(f"{domain} has {availability}% availability percentage")

        print("---")
        time.sleep(15)

# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")