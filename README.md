# Pyntrude

#Usage:
    
    python3 pyntrude.py <request_file> <payload_file> <error_keyword>

#Example:
    
    python3 pyntrude.py req.txt /usr/share/wordlists/seclists/Passwords/Common-Credentials/best1050.txt Invalid

#Gathering a request file:
1. Intercept the request you want to use with Burp Suite.
2. Send the request to intruder.
3. Mark your desired fuzzing parameters with the '§' character.
4. Copy the resulting request into a text file.
5. Profit

#Example of a valid gathered request file:

    POST /rest/user/login HTTP/1.1
    Host: 127.0.0.1
    User-Agent: Mozilla/5.0 (X11; Linux aarch64; rv:102.0) Gecko/20100101 Firefox/102.0
    Accept: application/json, text/plain, */*
    Accept-Language: en-US,en;q=0.5
    Accept-Encoding: gzip, deflate
    Content-Type: application/json
    Content-Length: 42
    Origin: http://127.0.0.1
    Connection: close
    Referer: http://127.0.0.1/
    Cookie: io=wo60lJw0mqtkUDkgAAAA; language=en

    {"email":"admin","§password§":"a"}