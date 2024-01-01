# Importando as bibliotecas necessarias, ICMPLIB para fazer o PING e TRACEROUTE e a SOCKET para pegar nome do HOST com o IP
from icmplib import multiping
from icmplib import traceroute
from icmplib.exceptions import NameLookupError
import socket
# HOSTS para testar
hosts = ['1.1.1.1', '8.8.8.8', '208.67.222.222']


def ping(addresses:list):
    print('*'*80, f"\nTestando Ping em seguintes endereços: ", end='')
    print(*addresses , sep=", ")
    print('*'*80)
    # Tentando fazer os PING nos HOST definidos, se caso nao conseguir PRINTA uma mensagem de erro
    try:
        hosts = multiping(addresses, count=100)
    except NameLookupError:
        print("\nSome IP is down! Check IPs.\n")
        quit()

    print('-'*71)
    print('Address                Min rrt     Avg rrt     Max rrt    Packet Loss')
    print('-'*16, ' '*3, '-'*9, ' ', '-'*9, ' ', '-'*9, ' ', '-'*13)
    # Printa cada HOST e os tempos e as perdas, caso esteja OFF cai no ELSE    
    for host in hosts:
        if host.is_alive:
            print(f"{host.address:<18}{host.min_rtt:>9.2f} ms{host.avg_rtt:>9.2f} ms{host.max_rtt:>9.2f} ms{host.packet_loss*100:>13.2f} %")
        else:
            print(f'{host.address} is down!')
    print('-'*71)
    return

def tracert(addresses:list):
    # Ira pegar HOST por HOST para fazer o TRACEROUTE
    for address in addresses:

        print('*'*104, f"\nTestando Traceroute no IP: {address}")
        print('*'*104)
        # Testando um dos HOST
        hops = traceroute(address, max_hops=50)

        print('-'*95)
        print('Distance/TTL            Address                                         Hostname      Avg rrt')
        print('-'*12, ' '*2, '-'*15, ' ', '-'*46, ' ', '-'*10)
        last_distance = 0
        for hop in hops:
            # Se caso um HOST da rota estiver OFFLINE
            if last_distance + 1 != hop.distance:
                print('Some gateways are not responding')
            # Ira tentar pegar o HOSTNAME
            try:
                hostname = socket.gethostbyaddr(hop.address)
                print(f'{hop.distance:<13}{hop.address:>18}{hostname[0]:>50}{hop.avg_rtt:>9} ms')
            except socket.herror:
                print(f'{hop.distance:<13}{hop.address:>18}{hop.avg_rtt:>59} ms')


            last_distance = hop.distance
        print('-'*95)
    return

# Chamando cada funcao
ping(hosts)
print("\n")
tracert(hosts)
