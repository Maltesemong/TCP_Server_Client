import socket

HOST = '127.0.0.1' #server ip로 local host 사용
PORT = 9999 #server가 지정한 port number

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4, TCP socket 사용

client_socket.connect((HOST, PORT)) #connect 함수를 통해서 server와 연결 요청

while True: #while loop를 통해 지속적으로 server에게 data 전달
    data1 = input("data: ") #server에 전송할 data
    client_socket.sendall(data1.encode()) #data1이 string이므로 encoding 후 전송

    if data1 == "close":
        break #client가 close 입력 시 connection 종료

    data = client_socket.recv(1024) #server로부터 받은 data
    print('Received', repr(data.decode())) #server로부터 받은 data 출력

client_socket.close() #connection 종료
