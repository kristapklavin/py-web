import socket
# import usocket as socket
import re

# from wificonnect import connect_to_wifi
# wifissid = ""
# wifipass = ""

# con = connect_to_wifi(wifissid, wifipass)


SENSORS = {
    "mois0": {
    "id": 1,
    "active": True,
    "pin": 35,
    "accDry": 2900,
    "accWet": 1000
},
"mois1": {
    "id": 2,
    "active": True,
    "pin": 34,
    "accDry": 2900,
    "accWet": 1000
},
"mois2": {
    "id": 3,
    "active": True,
    "pin": 39,
    "accDry": 2800,
    "accWet": 1000
},
"mois3": {
    "id": 4,
    "active": True,
    "pin": 36,
    "accDry": 3000,
    "accWet": 1000
}
}

RELAYS = {
    "rel0": {
        "type": "solenoid",
        "active": True,
        "openTime": 200,
        "pin": 14
    },
    "rel1": {
        "type": "solenoid",
        "active": True,
        "openTime": 200,
        "pin": 27
    },
    "rel2": {
        "type": "solenoid",
        "active": True,
        "openTime": 200,
        "pin": 26
    },
    "rel3": {
        "type": "solenoid",
        "active": True,
        "openTime": 200,
        "pin": 25
    }
}

def handle_client(client_socket):
    # Receive the request data
    request = client_socket.recv(1024)
    request_str = request.decode('utf-8')
    print("Received:")
    print(request_str)

    # Check if the request is for the /getmoisture endpoint
    match_getmoisture = re.match(r'GET /moist/(\d+) HTTP/1.1', request_str)
    match_open = re.match(r'GET /open/(\d+) HTTP/1.1', request_str)
    match_close = re.match(r'GET /close/(\d+) HTTP/1.1', request_str)

    if match_getmoisture:
        sensorid = match_getmoisture.group(1)
        


        # GEt MOISTURE READING



        response_body = f'Moisture level for sensor {sensorid}'
    elif match_open:
        open_id = match_open.group(1)
        


        # RELAY OPEN



        response_body = f'Open command received for ID {open_id}'
    elif match_close:
        close_id = match_close.group(1)
        


        # RELAY OPEN



        response_body = f'Close command received for ID {close_id}'
    else:
        response_body = 'Hello, World!'

    # Prepare the HTTP response
    http_response = f"""\
HTTP/1.1 200 OK

{response_body}
"""
    # Send the HTTP response
    client_socket.sendall(http_response.encode('utf-8'))
    client_socket.close()

def main():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to a public host and a port
    server_socket.bind(('0.0.0.0', 8123))
    
    # Become a server socket
    server_socket.listen(5)
    print("Listening on port 8123...")

    while True:
        # Accept connections from outside
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        
        # Handle the client connection
        handle_client(client_socket)

if __name__ == "__main__":
    main()