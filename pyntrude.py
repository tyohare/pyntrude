import requests
import sys
import urllib3

#########  Usage: python3 pyntrude.py <request_file> <payload_file> <error_keyword>  ##########
######### Example: python3 pyntrude.py req.txt /usr/share/wordlists/seclists/Passwords/Common-Credentials/best1050.txt Invalid #########
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Proxy set if you want to intercept request in burp
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

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
                
	    #find where the fuzzing parameter is so we can replace it with the current payload
            first_index = file_contents.find('§')
            last_index = file_contents.rfind('§')

            if first_index != -1 and last_index != -1:
                file_contents = file_contents[:first_index] + current_line + file_contents[last_index+1:]

	    #split headers and body into respective variables
            headersraw, body = file_contents.split('\n\n', 1)

	    #create dictionary for the headers
            headers = {}
            for line in headersraw.splitlines():
                if ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip()] = value.strip()

	    #craft the URL using the Origin header and given endpoint
            url = headers["Origin"]
            endpoint = headersraw.split()[1]
            target = url + endpoint


            #Craft the request
            r = s.post(target, headers=headers, data=body, verify=False, proxies=proxies)
            res = r.text

	    #return success or fail based on the response
            if error not in res:
                print("(+) Success with payload: " + current_line )
            else:
            	print("(-) Failed with payload: " + current_line )





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
