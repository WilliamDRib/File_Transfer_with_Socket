import socket
import time
import os

BUFFER = 1024

def statistics(bytes_transmitted, start_time, file_size): 
    elapsed_time = time.time() - start_time
    transfer_rate = bytes_transmitted / elapsed_time if elapsed_time != 0 else 0
    porcentage = (bytes_transmitted / file_size) * 100

    print("Tranfer rate: {:.2f} Bytes/s | Porcentage transferred: {:.2f}%".format(transfer_rate, porcentage), end="\r", flush=True)

def send_file(client, namefile):

    if not os.path.exists('Client\\Files\\' + namefile):
        print("File does not exist!")
        return

    try:
        with open('Client\\Files\\' + namefile, 'rb') as file:
            file_size = len(file.read())
            file.seek(0)
            start_time = time.time()
            bytes_transmitted = 0

            for data in file.readlines():
                client.send(data)
                bytes_transmitted += len(data)
                statistics(bytes_transmitted, start_time, file_size)

        print("\n" + f'{namefile} sent!\n')
    except Exception as error:
        print(error)

def receive_file(client, namefile):
    data = client.recv(BUFFER).decode()

    if str(data).startswith("Error:"):
        print(data)
        return

    file_size = int(data)

    with open('Client\\Files\\' + namefile, 'wb') as file:
        start_time = time.time()
        bytes_transmitted = 0

        while True:
            data = client.recv(BUFFER)

            if not data:
                break
            
            file.write(data)
            bytes_transmitted += len(data)  
            statistics(bytes_transmitted, start_time, file_size)

    print("\n" + f'{namefile} received!')

def main():
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect(('localhost', 25565))
            print('Connected!\n')

            operation = input('1 - Upload\n2 - Download\n3 - Exit\n')

            if operation == '1':
                namefile = input('File Name: ')
                client.send((operation + ' ' + namefile).encode())
                send_file(client, namefile)
            elif operation == '2':
                namefile = input('File Name: ')
                client.send((operation + ' ' + namefile).encode())
                receive_file(client, namefile)
            elif operation == '3':
                break
            else:
                print('Invalid!\n')
                continue

            client.close()
            print("Connection closed!")

    client.close()
    print("Connection closed!")


if __name__ == '__main__':
    main()