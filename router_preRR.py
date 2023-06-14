import sys
import socket

router_ip = sys.argv[1]
router_port = int(sys.argv[2])
routes_path = sys.argv[3]
buff_size = 1000
road_to = {}
def read_line(line):
    parsed_line = {}
    index = line.find(" ")
    parsed_line["IP_DESTINATION"] = line[:index]
    line= line[index+1:]
    index = line.find(" ")
    parsed_line["LOW_PORT"] = int(line[:index])
    line= line[index+1:]
    index = line.find(" ")
    parsed_line["HIGH_PORT"] = int(line[:index])
    line= line[index+1:]
    index = line.find(" ")
    parsed_line["IP_NEXT"] = line[:index]
    parsed_line["PORT_NEXT"] = int(line[index+1:])
    line= line[index+1:]
    return parsed_line
def parse_packet(ip_packet):
    ip_packet = ip_packet.decode()
    parsed_packet = {}
    index = ip_packet.find(",")
    parsed_packet["IP"] = ip_packet[:index]
    ip_packet= ip_packet[index+1:]
    index = ip_packet.find(",")
    parsed_packet["PORT"] = int(ip_packet[:index])
    parsed_packet["MSG"] = ip_packet[index+1:]
    return parsed_packet
def create_packet(parsed_packet):
    return (parsed_packet["IP"]+","+str(parsed_packet["PORT"])+","+parsed_packet["MSG"]).encode()
def check_routes(routes_file_name,destination_address):
    file = open(routes_file_name,"r")
    while(True):
        data = file.readline()
        if not data:
            return None
        data_parsed = read_line(data)
        if data_parsed["IP_DESTINATION"] == destination_address[0] and (data_parsed["LOW_PORT"]<=destination_address[1]<=data_parsed["HIGH_PORT"]):
            return (data_parsed["IP_NEXT"], data_parsed["PORT_NEXT"])

print(f"IP: {router_ip}, PORT: {router_port}")

router_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
router_socket.bind((router_ip,router_port))

while True:
    og, add = router_socket.recvfrom(buff_size)
    msg = parse_packet(og)

    if msg["IP"]==router_ip and msg["PORT"]==router_port:
        print(msg["MSG"])
    else:
        tupla = check_routes(routes_path, (msg["IP"], msg["PORT"]))
        if tupla == None:
            print(f"No hay rutas hacia {msg['IP']} {msg['PORT']} para {og.decode()}")
            continue
        ip, port = tupla
        print(f"redirigiendo paquete {og} con destino final {(msg['IP'],msg['PORT'])} desde {(router_ip,router_port)} hacia {(ip,port)}")
        router_socket.sendto(og,(ip,port))
    
        
