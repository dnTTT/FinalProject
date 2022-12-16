"""import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import WindowsAuthorizer

authorizer = WindowsAuthorizer(allowed_users=["Shw"])
authorizer.override_user("Shw", homedir='C:/', perm="elradfmw")

#authorizer = WindowsAuthorizer(anonymous_user="Guest", anonymous_password="")
# Create an FTP handler that uses the dummy authorizer
handler = FTPHandler
handler.authorizer = authorizer


# Create an SFTP server that listens on a particular host and port
server = FTPServer(("0.0.0.0", 2221), handler)
# Start the server
server.serve_forever()
"""

from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import WindowsAuthorizer
import pyftpdlib.handlers
from OpenSSL import SSL

def main():

    ## Create DummyUsers to not use windowsAuth
    authorizer = WindowsAuthorizer(allowed_users=["Shw"])
    authorizer.override_user("Shw", homedir='C:/', perm="elradfmw")
    handler = pyftpdlib.handlers.TLS_FTPHandler
    handler.certfile = 'keycert.pem'
    handler.authorizer = authorizer
    # requires SSL for both control and data channel
    #handler.tls_control_required = True
    #handler.tls_data_required = True
    server = FTPServer(('0.0.0.0', 2221), handler)
    server.serve_forever()

if __name__ == '__main__':
    main()