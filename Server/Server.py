import socket
import sys
import traceback
import threading

BUFFER = 1024

def send_file(conn, namefile):
    try:
        with open('Server\\Files\\' + namefile, 'rb') as file:
            file_size = len(file.read())
            conn.send(str(file_size).encode())

            file.seek(0)
            for data in file.readlines():
                conn.send(data)

            print(f'{namefile} sent!')

    except Exception as error:
        message_error = "Error:" + str(error)
        conn.send(message_error.encode())
 
def receive_file(conn, namefile):

    with open('Server\\Files\\' + namefile, 'wb') as file:
        while True:
            data = conn.recv(BUFFER)
            if not data:
                break
            file.write(data)

    print(f'{namefile} received!')

def handle(conn,addr):
    print('Connection accepted:', addr)
    operation, namefile = conn.recv(BUFFER).decode().split(' ')

    if operation == "1":
        receive_file(conn, namefile)
    elif operation == "2":
        send_file(conn, namefile)

    conn.close()
    print("Connection closed:", addr)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 25565))
        s.listen(100)
        print("Server active!")
        
        while True:
            try:
                conn, addr = s.accept()
                cliente_thread = threading.Thread(target=handle, args=(conn,addr,))
                cliente_thread.start()
            except KeyboardInterrupt:
                sys.exit(1)
            except:
                traceback.print_exc()

if __name__ == '__main__':
    main()
