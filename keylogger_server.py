import socket
import errno
HOST = ''
PORT = 19000

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
    
        with conn:
            print('Connected by: ', addr[0])
            filename = addr[0] + '.txt'
            print(filename)
            f = open(filename, "a")
            f.write('------------------------------------------------------------------\n')
            f.write('New session to ' + addr[0] + ':\n')
            while True:
                try:
                    data = conn.recv(2000)
                    outData = data.decode()
                    print(outData)
                    f.write(outData)
                    #f.write('\n')
                    conn.send(b'data recieved')
                except socket.error:
                    print('socket error')
                    f.write('\nclient discconected\n')
                    f.write('------------------------------------------------------------------\n')
                    s.close()
                    f.close()
                    break
