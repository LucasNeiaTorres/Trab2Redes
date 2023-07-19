import socket


endereco_local = socket.gethostbyname_ex(socket.gethostname())[-1][0]
print("Endereço IP local da máquina", socket.gethostname(), ":", socket.gethostbyname_ex('natael-550XDA'))


# 127.0.1.1