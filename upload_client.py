"""udp_client.py
    Run python autograder.py
Author:              Tony Calarese, Paul Lindberg
Class:               CSI-235
Assignment:          Lab 2
Date Assigned:       2/08/2018
Due Date:            2/15/2018 11:59 PM
Description:
To get a TCp connection working and to make sure tha we are able to send packets voer the TCP connection
While also sending the contents of the file over as well
This code has been adapted from that provided by Prof. Joshua Auerbach:
Champlain College CSI-235, Spring 2018
The following code was written by Tony Calarese (anthony.calarese@champlain.edu) and was adpted from Joshua Auberach's code for  lab 2
Also Paul Lindberg (paul.lindberg@mymail.champlain.edu)
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
        if len(self.byte_string_buffer) != 0 :
            # [len(delimiter):] == delimiter: # if the buffer doesn't end with a delimiter, put the new call
            byte_string = self.byte_string_buffer
        else:
            byte_string = self.sock.recv(constants.MAX_BYTES)


        while byte_string.find(delimiter) == -1:  # if delimiter is not included, then merge.
            temp_byte_string = self.sock.recv(constants.MAX_BYTES)
            byte_string = b"".join((byte_string, temp_byte_string))
        # Now that there is a delimiter, either return the message that ends with a delimiter

        if byte_string.endswith(delimiter):
            return byte_string[:byte_string.index(delimiter)]
        else:  # or return everything up until the delimiter and then store the rest in a buffer
            self.byte_string_buffer = byte_string[byte_string.index(delimiter) +  1:]
            # and return the first one in the list.
            return byte_string[:byte_string.index(delimiter)]

    def upload_file(self, file_path):

        try:
            self.file = open(file_path, 'rb')

        except OSError:
            print("ERROR OSERROR")
            raise OSError

        self.file_contents = self.file.read()
        self.file_length = len(self.file_contents)

        header = b"UPLOAD " + os.path.basename(file_path).encode("ascii") + b" " + str(self.file_length).encode("ascii") + b"\n"
        self.sock.sendall(header + self.file_contents)

        reply = self.recv_until_delimiter(b'\n')

        if reply == b"ERROR":
            raise UploadError


    def list_files(self):
        pair = {}
        return_val = []
        self.sock.sendall(b"LIST\n")
        while True:
            reply = self.recv_until_delimiter(b'\n').decode("ascii")
            reply = reply.split()
            if not reply:
                break
            else:
                pair.update({reply[0]: reply[1]})
        # adapted from https://stackoverflow.com/questions/3294889/iterating-over-dictionaries-using-for-loops
        for key, value in pair.items():
            return_val.append((key, value))
        return return_val

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
