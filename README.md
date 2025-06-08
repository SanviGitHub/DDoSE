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


## Importante  
Este proyecto es **solo** para probar y aprender en entornos propios o donde **tengas permiso**.  
No lo uses para nada ilegal ni contra sistemas que **no sean tuyos**.  
No me hago responsable si lo usás para hacer lío. Te avisamos.

---

## Configuración  

Ejemplo de cosas que podés cambiar en `config.json`:

- `target_ip`: IP a la que vas a “atacar”.
- `num_bots`: cantidad de bots que se van a simular.
- `num_packets_per_bot`: cuántos paquetes va a mandar cada bot.
- `attack_duration`: duración total del ataque (en segundos).
- `interface`: interfaz de red desde la que se van a enviar los paquetes.

---

## Contribuciones  

¿Te copa la idea? ¿Querés agregarle cosas o mejorar el código?  
Hacete un fork, mandá un pull request, y vemos qué onda.  
**Todo suma.**

---

## ¿Para qué sirve esto?

- Para entender cómo funcionan ataques básicos de red tipo SYN flood, UDP flood, etc.
- Para practicar Python con cosas como `asyncio`, `multiprocessing` y `scapy`.
- Para armar tu propio laboratorio de pruebas sin drama.

