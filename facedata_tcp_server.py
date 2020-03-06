import socket
import select
import numpy as np
import datetime as dt


class SocketServer:
    def __init__(self, host = '0.0.0.0', port = 2020):

        """Initialize the server with a host and port to listen to."""
        # AF_INT: Specifies IPv4 protocol
        # SOCK_STREAM: Specifies TCP Communcation for connection based communication
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # SO_REUSEADDR: Indicates that the system can reuse this socket
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind socket to host address and listen on a port. Local server on 127.0.0.1 (localhost)
        # For access from other machaines use 0.0.0.0 on local network
        self.host = '0.0.0.0'
        self.port = 2020
        self.sock.bind((host, port))

        # Set up socket so that it waits for incoming connections. Set number of clients to 1
        self.sock.listen(1)

    def close(self):
        """ Close the server socket. """
        print('Closing server socket (host {}, port {})'.format(self.host, self.port))
        if self.sock:
            self.sock.close()
            self.sock = None
 
    def run_server(self,savepath):
        """ Accept and handle an incoming connection. """
        print("-------------------------------------------")
        print('Starting socket server (host {}, port {})'.format(self.host, self.port))
        full_file = savepath + "_" + str(dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ".txt")
        client_sock, client_addr = self.sock.accept()
        count = 0
        writecount = 0
        f = open(full_file,'w')
        print('New connections from {}'.format(client_addr))
 
        stop = False
        while not stop:
            if client_sock:
                # Check if the client is still connected and if data is available:
                try:
                    rdy_read, rdy_write, sock_err = select.select([client_sock,], [], [])
                except select.error:
                    print('Select() failed on socket with {}'.format(client_addr))
                    return 1
 
                if len(rdy_read) > 0:

                    data = client_sock.recv(1024).decode("utf-8")

                    # Check if socket has been closed
                    if len(data) == 0:
                        print('{} closed the socket.'.format(client_addr))
                        stop = True
                    if "a" in data:
                        if count == 0:
                            count = count + 1 
                            print('Server waiting for data stream....')
                    if "z" in data:
                        print('!!!Data stream stopped!!!')
                        f.close()
                        client_sock.close()
                        stop = True
                    if not "z" in data and "a" not in data:
                        if writecount == 0:
                            print("Writing data to: " + full_file)
                            writecount = writecount + 1
                        f.write(data)
            else:
                print("No client is connected, SocketServer can't receive data")
                stop = True
 
def main():
    ###### Define save path ######
    savepath = '/Users/home/../../out/'
    filename = 'filename'

    ###### Build Server Object ######
    server = SocketServer()

    ###### Run server until user interrupts with keyboard ######
    while not False:
        server.run_server(savepath + filename)
    print('Exiting')
 
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('')
        print('EXIT_SUCCESS')