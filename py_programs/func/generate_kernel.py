import socket, json, os, sys

def generate_kernel(psf_target, psf_origin, output):
    request_port = int(os.environ.get('REQUEST_PORT'))
    response_port = int(os.environ.get('RESPONSE_PORT'))

    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('127.0.0.1', request_port))

    subprocess_call_args = {'psf_target': psf_target, 'psf_origin': psf_origin, 'output': output}

    data = json.dumps(subprocess_call_args)

    clientsocket.send(bytes(data, 'utf-8'))

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('0.0.0.0', response_port))
    serversocket.listen(5)

    while True:
        connection, address = serversocket.accept()
        buf = connection.recv(64)

        if len(buf) > 0:
            data = buf.decode('utf-8')

            obj = json.loads(data)

            if 'exit_code' in obj:
                exit_code = int(obj['exit_code'])
                if exit_code == 0:
                    return
                else:
                    raise RuntimeError('IDL exited unexpectedly')
            else:
                raise RuntimeError('unexpected response')

