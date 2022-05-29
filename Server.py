import socket

HOST = '127.0.0.1' #local host를 사용해 server-client 통신 구현
PORT = 9999 #PORT NUMBER 할당

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4, TCP socket 활용

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #WinError 10048 에러 해결(해당 포트가 사용 중일 경우)

server_socket.bind((HOST, PORT)) #bind 함수를 통해 socket과 HOST와 PORT NUMBER를 연결

server_socket.listen() #listen을 통해 client가 접속하면 새로운 socket을 return한다.

client_socket, addr = server_socket.accept() #client가 요청한 connection을 accept한다.

print("connected by ", addr) #client의 ip와 새로 할당된 port number를 출력한다.

dic_list = {} #client가 건네는 data를 저장하기 위해 빈 dictionary 생성

while True: #while loop를 통해 server가 지속적으로 client와 통신 가능한 상태 유지
    data1 = client_socket.recv(1024).decode() #client에게 받은 data를 decode 한다.

    if data1 == "close":
        break #"close"를 받을 시 연결을 종료

    elif data1 == "LIST":
        if dic_list == {}:
            client_socket.sendall("Not exist!".encode()) #dictionary에 아무 것도 없을 경우

        else:
            client_socket.sendall(repr(dic_list).encode()) #LIST를 받을 시 저장된 key-value를 문자열로 변환해 encoding 후 client에게 전달

    else:
        try:
            a, b, c = data1.split(',')
            if a == "PUT":
                key = b
                dic_list[key] = c
                client_socket.sendall("Success!".encode()) #data를 3개 받았을 시 맨 처음 받은 data가 PUT일 경우 dictionary에 저장
        
        except:
            a, b = data1.split(',') #client에게 받은 data가 2개일 경우

            if a == "GET":
                if b in dic_list:
                    client_socket.sendall(repr(dic_list[b]).encode()) #처음 data가 GET일 경우 찾고자 하는 value를 저장된 dictionary의 key를 통해서 client에게 전달
                else:
                    client_socket.sendall("Not exist!".encode()) #없을 경우

            if a == "DELETE":
                if b in dic_list:
                    del dic_list[b]
                    client_socket.sendall("Success!".encode()) #DELETE를 받은 경우 해당 key와 value를 dictionary에서 삭제
                else:
                    client_socket.sendall("Not exist!".encode()) #삭제할 key가 없을 경우
    
    print("received data : ", data1) #client에게 받은 data를 server창에 출력
    print(dic_list) #현재 server에 저장되어있는 key, value값을 출력

print("connection closed.") #연결 종료
client_socket.close() #client socket 닫음
server_socket.close() #server socket 닫음
