from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

auth = DummyAuthorizer()
auth.add_anonymous('/home/lhasya/Documents')
auth.add_user('user', '12345', '/home/lhasya/Documents', perm='elradfmw')

handl = FTPHandler
handl.authorizer = auth

serv = FTPServer(('0.0.0.0', 1234), handl)
serv.serve_forever()

