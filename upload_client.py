"""upload_client.py

    Run python autograder.py
    
TODO -- complete header docstring

Champlain College CSI-235, Spring 2018
This code builds off skeleton code written by 
Prof. Joshua Auerbach (jauerbach@champlain.edu)
"""

import argparse
import socket
import os
import constants

class UploadError(Exception):
    """Error when uploading"""
    pass

class UploadClient:
    # TODO document this class and implement the specified functions
    # create TCP socket here

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.hostname, self.port))

        print('Client has been assigned socket name', self.sock.getsockname())


    def recv_all(self, length):
        data = b''
        while len(data) < length:
            more = self.sock.recv(length - len(data))
            if not more:
                raise EOFError('was expecting %d bytes but only received'
                               ' %d bytes before the socket closed'
                               % (length, len(data)))
            data += more
        return data

    def close(self):
        self.sock.close()

    def recv_until_delimiter(self, delimiter):
        while True:
            try:
                byte_string = self.sock.recv(constants.MAX_BYTES)
                if byte_string.find(delimiter) != -1:
                    break
            except:
                raise UploadError("AAAAAAAA")


if __name__ == '__main__':    
    parser = argparse.ArgumentParser(description='TCP File Uploader')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=8900,
                        help='TCP port (default 8900)')
    args = parser.parse_args()
    upload_client = UploadClient(args.host, args.p)
    upload_client.upload_file("upload_client.py")
    print(upload_client.list_files())
    upload_client.close()
