import requests
import sys
import urllib3
import concurrent.futures
import os

#########  Usage: python3 pyntrude.py <request_file> <payload_file> <error_keyword>  ##########
######### Example: python3 pyntrude.py req.txt /usr/share/wordlists/seclists/Passwords/Common-Credentials/best1050.txt Invalid ##########
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Proxy set if you want to intercept request in burp
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def send_request(payload, filename, error):
    # Set the current line as a string
    current_line = payload.rstrip()

    # Open the file in read mode
    with open(filename, 'r') as file:
        file_contents = file.read()
        lines = file_contents.splitlines()

        # Find the fuzzing parameter and replace it with the current payload
        first_index = file_contents.find('§')
        last_index = file_contents.rfind('§')

        if first_index != -1 and last_index != -1:
            file_contents = file_contents[:first_index] + current_line + file_contents[last_index+1:]

        # Split headers and body into respective variables
        headersraw, body = file_contents.split('\n\n', 1)

        # Create dictionary for the headers
        headers = {}
        for line in headersraw.splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()

        # Craft the URL using the Origin header and given endpoint
        url = headers["Origin"]
        endpoint = headersraw.split()[1]
        target = url + endpoint

        # Craft the request
        r = requests.post(target, headers=headers, data=body, verify=False, proxies=proxies)
        res = r.text

        # Return success or fail based on the response
        if error not in res:
            return "(+) Success with payload: " + current_line
        else:
            return "(-) Failed with payload: " + current_line


def intrude(s):
    # Get the payload filename from command line arguments
    payload_file = sys.argv[2]

    # Read the payloads from the file
    with open(payload_file, 'r') as file:
        payloads = file.readlines()

    # Get the filename and error keyword from command line arguments
    filename = sys.argv[1]
    error = sys.argv[3]

    # Send HTTP requests concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Map the payloads to the send_request function
        results = executor.map(send_request, payloads, [filename]*len(payloads), [error]*len(payloads))

        # Print the results as they become available
        for result in results:
            print(result)
            if "Success" in result:
                 os._exit(0)
                 return



def main():
    s = requests.Session()

    #if the user needs help
    if sys.argv[1] == "--help":
        print("Usage: python3 pyntrude.py <request_file> <payload_file> <error_keyword>")
        print("Example: python3 pyntrude.py req.txt /usr/share/wordlists/seclists/Passwords/Common-Credentials/best1050.txt Invalid")
        return
    
    #if the user provides insufficent arguments
    if len(sys.argv) < 4:
        print("Not enough arguments!")
        print("Try: 'python3 pyntrude.py --help' for syntax")
        return

    #Begin the intrusion!!!
    intrude(s)


if __name__ == "__main__":
    main()
