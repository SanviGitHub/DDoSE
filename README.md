# Simulador de Ataques DDoS con Python y Scapy

Esta herramienta sirve para simular ataques DDoS (SYN flood, UDP flood, HTTP flood) con Python y Scapy. Está pensada para que puedas entender cómo funcionan estos ataques en un entorno de prueba controlado y seguro.

---

## Qué hace

- Simula varios bots atacando al mismo tiempo.
- Cambia entre tipos de ataques (SYN, UDP, HTTP).
- Usa `asyncio` para manejar muchas tareas a la vez.
- Ejecuta bots en diferentes procesos para que no se trabe todo.
- Genera IPs y User Agents random para hacer el tráfico más “real”.
- Lee configuración de un archivo JSON que puedes cambiar en cualquier momento.
- Muestra logs en tiempo real para que veas qué está pasando.

---

## Requisitos

- Python 3.7 o superior.
- Scapy instalado (`pip install scapy`).
- Ejecutar con permisos de administrador/root para enviar paquetes raw.

---

## Cómo usarlo

1. Clona o descarga el proyecto.
2. Edita el archivo `config.json` para poner la IP de destino, número de bots, duración, etc.
3. Corre el script con permisos elevados:
   ```bash
   sudo python3 ddos_simulator.py
