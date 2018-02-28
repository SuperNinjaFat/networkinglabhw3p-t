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
        self.byte_string_buffer = ""
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
        byte_string = ""
        if len(self.byte_string_buffer) != 0:  # [len(delimiter):] == delimiter: # if the buffer doesn't end with a delimiter, put the new call
            byte_string = self.byte_string_buffer + self.sock.recv(constants.MAX_BYTES).decode("ascii")
        else:
            byte_string = self.sock.recv(constants.MAX_BYTES).decode("ascii")
        while byte_string.find(delimiter.decode("ascii")) == -1:  # if delimiter is not included, then merge.
            temp_byte_string = self.sock.recv(constants.MAX_BYTES).decode("ascii")
            byte_string = "".join((byte_string, temp_byte_string))
        # Now that there is a delimiter, either return the message that ends with a delimiter
        if byte_string.encode("ascii").endswith(delimiter):
            return byte_string.encode("ascii")[:byte_string.index(delimiter.decode("ascii"))]
        else:  # or return everything up until the delimiter and then store the rest in a buffer
            self.byte_string_buffer = byte_string[byte_string.index(delimiter.decode("ascii")):]
            # and return the first one in the list.
            return byte_string.encode("ascii")[:byte_string.index(delimiter.decode("ascii"))]



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
