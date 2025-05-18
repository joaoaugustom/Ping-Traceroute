import sys
from icmplib import multiping
from icmplib import traceroute
from icmplib.exceptions import NameLookupError
import socket


# Para fazer o controle de cada argumento
ip4 = False
ip6 = False
tr = False
pin = False
fi = False

# Verificando os argumentos passados
def defi_argv():

    global ip6, ip4, tr, pin, fi

    # Se não passou argumento será executado no modo padrão, se passou "-h" irá mostrar o HELP, se passou outros arumentos o script irá tratar
    if len(sys.argv) <= 1:
        print('Não foi passado argumentos, será executado no modo padrão.\nUse "-h" para ajuda.')
        ip4 = True
        ip6 = True
        tr = True
        pin = True
        fi = False
        pass
    elif sys.argv[1] == '-h':
        print('Use "-4" para IPv4.\nUse "-6" para IPv6.\nUse "-t" para executar Traceroute.' \
            '\nUse "-p" para executar Ping.\nUse "hosts.txt" para passar os hosts a ser testado.')
        pass
    else:
        i = 1
        while True:
            try:
                arg = sys.argv[i]
            except:
                break
            match arg:
                case '-4':
                    ip4 = True
                case '-6':
                    ip6 = True
                case '-t':
                    tr = True
                case '-p':
                    pin = True
                case 'hosts.txt':
                    fi = True
                case _:
                    print(f'\nArgumento "{arg}" é invalido. Recomenda-se reinciar o teste corrigindo o argumento.\nUse "-h" para ajuda.')
            i += 1
        if (ip4 == False and ip6 == False) or (tr == False and pin == False):
            print("\nArgumentos passados são invalidos. Script será executado no modo padrão.")
            ip4 = True
            ip6 = True
            tr = True
            pin = True
            fi = False

# Verifica se vai ser importado os Hosts ou será usado o padrão
def defi_hosts():

    global fi, ip4, ip6
    hosts_controle = []
    hosts_controle_final = []

    # Esse IF verifica se irá usar arquivo importado ou a lista padrão
    if fi == True:
        try:
            with open("hosts.txt", "r") as f:
                hosts_controle = f.readlines()
                # Após abrir o arquivo irá passar IP por IP do arquivo e verificar se precisa incluir ou não ele a lista, a condição vai depender se o usuário escolheu IPv4 ou IPv6
                for host in hosts_controle:
                    if ip6 == False:
                        if host.find('.') != -1:
                            hosts_controle_final += [host.replace("\n", "")]
                    elif ip4 == False:
                            if host.find('.') == -1:
                                hosts_controle_final += [host.replace("\n", "")]  
                    else:
                        hosts_controle_final = [host.replace("\n", "") for host in hosts_controle]
                return hosts_controle_final  
        except:
            print("Arquivo invalido, será executado com endereços padrão.")
            return ['1.1.1.1', '8.8.8.8', '208.67.222.222', '2001:4860:4860::8888', '2606:4700:4700::1111', '2620:119:35::35']
    else:
        # Verifica o que o usuário escolheu e inclui na lista
        if ip4 == True:
            hosts_controle += ['1.1.1.1', '8.8.8.8', '208.67.222.222']
        if ip6 == True:
            hosts_controle += ['2001:4860:4860::8888', '2606:4700:4700::1111', '2620:119:35::35']
        return hosts_controle  


def ping(addresses:list):

    print('*'*140, f"\nTestando Ping em seguintes endereços: ", end='')
    print(*addresses , sep=", ")
    print('*'*140)

    # Tentando fazer os PING nos HOST definidos, se caso nao conseguir PRINTA uma mensagem de erro
    try:
        hosts = multiping(addresses, count=5)
    except NameLookupError:
        print("\nSome IP is down! Check IPs.\n")
        quit()

    print('-'*77)
    print('Address                      Min rrt     Avg rrt     Max rrt    Packet Loss')
    print('-'*21, ' '*5, '-'*9, ' ', '-'*9, ' ', '-'*9, ' ', '-'*13)

    # Printa cada HOST e os tempos e as perdas, caso esteja OFF cai no ELSE    
    for host in hosts:
        if host.is_alive:
            print(f"{host.address:<24}{host.min_rtt:>9.2f} ms{host.avg_rtt:>9.2f} ms{host.max_rtt:>9.2f} ms{host.packet_loss*100:>13.2f} %")
        else:
            print(f'{host.address} is down!')
    print('-'*77)
    return


def tracert(addresses:list):
    # Ira pegar HOST por HOST para fazer o TRACEROUTE
    for address in addresses:
        print('*'*124, f"\nTestando Traceroute no IP: {address}")
        print('*'*124)
        # Testando um dos HOST
        hops = traceroute(address, max_hops=50)

        print('-'*115)
        print('Distance/TTL                                Address                                         Hostname      Avg rrt')
        print('-'*12, ' '*2, '-'*35, ' ', '-'*46, ' ', '-'*10)

        last_distance = 0
        for hop in hops:
            # Se caso um HOST da rota estiver OFFLINE
            if last_distance + 1 != hop.distance:
                print('Some gateways are not responding')
            # Ira tentar pegar o HOSTNAME
            try:
                hostname = socket.gethostbyaddr(hop.address)
                print(f'{hop.distance:<13}{hop.address:>38}{hostname[0]:>50}{hop.avg_rtt:>9} ms')
            except socket.herror:
                print(f'{hop.distance:<13}{hop.address:>38}{hop.avg_rtt:>59} ms')


            last_distance = hop.distance
        print('-'*115)
    return


if __name__ == "__main__":
    # Execução das funções
    defi_argv()
    hosts = defi_hosts()

    if pin == True:
        ping(hosts)
    if tr == True:
        tracert(hosts)

