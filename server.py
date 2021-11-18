import socket, json, subprocess, os

def launch_server():
    request_port = int(os.environ.get('REQUEST_PORT'))
    response_port = int(os.environ.get('RESPONSE_PORT'))

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', request_port))
    serversocket.listen(5)

    while True:
        connection, address = serversocket.accept()
        buf = connection.recv(1024)
        
        if len(buf) > 0:
        
            data = buf.decode('utf-8')

            obj = json.loads(data)

            if 'psf_target' in obj and 'psf_origin' in obj and 'output' in obj:
                psf_target = obj['psf_target']
                psf_origin = obj['psf_origin']
                output = obj['output']

                exit_code = subprocess.call(['idl', '-e', f"""generate_kernel, '{psf_target}', '{psf_origin}', '{output}'"""])
               
                clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientsocket.connect(('127.0.0.1', response_port))
                #use the line below for Mac and Windows users
                #clientsocket.connect(('host.docker.internal', response_port))

                exit_code = json.dumps({'exit_code': exit_code})
                
                clientsocket.send(bytes(exit_code, 'utf-8'))

                clientsocket.close()
            else:
                raise ValueError('unexpected payload')

if __name__ == '__main__':
    launch_server()
