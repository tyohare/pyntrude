import requests
import sys
import urllib3

#########  Usage: python3 pyntrude.py <request_file> <payload_file> <error_keyword>  ##########
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def parse_req(file):
    print()

def intrude(s):
    filename = sys.argv[1]

    payload = sys.argv[2]
    
    error = sys.argv[3]
    # Open the file in read mode
    with open(payload, 'r') as file:

        # Loop through each line in the file
        for line in file:
            
            # Set the current line as a string
      
            current_line = line.rstrip()
            with open(filename, 'r') as file:
                file_contents = file.read()
                lines = file_contents.splitlines()

            first_index = file_contents.find('§')
            last_index = file_contents.rfind('§')

            if first_index != -1 and last_index != -1:
                file_contents = file_contents[:first_index] + current_line + file_contents[last_index+1:]

            #print(file_contents)


            headersraw, body = file_contents.split('\n\n', 1)

            #print('Headers:')
            #print(headersraw)
            #print('Body:')
            #print(body)


            headers = {}
            for line in headersraw.splitlines():
                if ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip()] = value.strip()

            url = headers["Origin"]
            endpoint = headersraw.split()[1]
            target = url + endpoint
            #Set the request payload in the request:

            #Craft the request
            r = s.post(target, headers=headers, data=body, verify=False, proxies=proxies)

            res = r.text
            #print(res)

            if error not in res:
                print("(+) Success with payload: " + current_line )






def main():
    s = requests.Session()

    #Begin the intrusion!!!
    intrude(s)



    

if __name__ == "__main__":
    main()
