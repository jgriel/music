import socket
import threading
from os import path
from stream import split_wav, get_params

def handle_client(conn, base_path):
    with conn:
        data = conn.recv(1024)
        request = data.decode().strip()
        print(f"{request}")
        args = request.split(', ')
        title = args[0]
        cmd = args[1]

        file_path = f"data/{title}.wav"

        if not path.exists(file_path):
            response = bytes(f"ERROR: {title} is not available", 'utf-8')

        elif cmd == "SPLIT":
            global chunks
            chunks = split_wav(file_path)
            l = len(chunks)
            response = l.to_bytes(2, "big")

        elif cmd == "PARAMS":
            params = get_params(file_path)
            p_str = f'{params.nchannels}, {params.sampwidth}, {params.framerate}'
            response = bytes(p_str, 'utf-8')

        else:
            response = chunks[int(cmd)]
        
        conn.sendall(response)

def start_server(host='localhost', port=5000, base_path='.'):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, base_path))
            thread.start()

if __name__ == "__main__":
    start_server(base_path='../music/')
