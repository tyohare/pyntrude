import requests
import sys
import urllib3

#########  Make sure to customize variables: url, headers, payload, error, and body  ##########
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def intrude(s, url, headers, payload, error):
    # Open the file in read mode
    with open(payload, 'r') as file:

        # Loop through each line in the file
        for line in file:
            
            # Set the current line as a string
            current_line = line
            
            #Set the request body: (Example: "action=reset&username=admin&pin="+payload)
            body = None + payload

            #Craft the request
            r = s.post(url, headers=headers,data=body, verify=False, proxies=proxies)
            res = r.text

            if error not in res:
                print("(+) Success with payload: " + current_line )




def main():
    s = requests.Session()

    #Set the URL; (Example: "http://127.0.0.1/login.php")
    url = None

    #Set the headers: (Example: {'Host': '127.0.0.1', 'User-Agent': 'python-requests/2.27.1','Accept-Encoding': 'gzip, deflate','Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','X-Requested-With': 'XMLHttpRequest','Accept': '*/*','Connection': 'close','Content-Length': '36','Origin': 'http://127.0.0.1','Referer': 'http://127.0.0.1/login.php','Cookie': 'PHPSESSID=g07akds4q318d5q7vkh6pevrb3'})
    headers = {None:None, None:None, None:None, None:None}


    #Set the payload: (Example: "/path/to/payload.txt")
    payload = None


    #Set the error message: (Example: "Invalid")
    error = None

    #Begin the intrusion!!!
    intrude(s, url, headers, payload, error)



    

if __name__ == "__main__":
    main()
