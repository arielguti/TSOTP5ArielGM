"""
UNJu - Facultad de Ingeniería
Teoría de Sistemas Operativos (TSO) - Ciclo Lectivo 2026
Cátedra: Ing. María Fernanda Vázquez - JTP: Ing. Fabio D. Argañaraz

Ejercicio Práctico N° 2: El Problema del Oso y las Abejas
Bibliografía de Referencia:
- Silberschatz: Cap. 6.6 (Problemas clásicos de sincronización)
- Stallings: Cap. 5.4 (Sincronización con semáforos)
"""

import sys
import threading
import time
import random

# Configuración UTF-8 para consola Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

M = 10                  # Capacidad del tarro de miel
NUM_ABEJAS = 5          # Número de abejas obreras
tarro_miel = 0          # Variable compartida
simulacion_activa = True

# TODO PARA EL ESTUDIANTE:
# 1. Define los mecanismos de sincronización necesarios:
# - Un cerrojo (Lock) o semáforo binario para exclusión mutua en el tarro.
# - Un semáforo para despertar al oso cuando el tarro esté lleno.
# - Un semáforo para que las abejas esperen si el tarro está lleno o el oso está comiendo.
mutex = threading.Lock()
sem_oso = threading.Semaphore(0)
sem_tarro_disponible = threading.Semaphore(1)

def abeja(id_abeja):
    global tarro_miel, simulacion_activa
    while simulacion_activa:
        time.sleep(random.uniform(0.05, 0.2))
        
        # TODO: Sincronizar el acceso al tarro de miel:
        # 1. Esperar a que el tarro esté disponible.
        with sem_tarro_disponible:            
        # 2. Entrar en exclusión mutua con el tarro.
            if not simulacion_activa: 
                break           
        # 3. Depositar una porción de miel (tarro_miel += 1).
            with mutex:
                tarro_miel += 1
                print(f"🐝 Abeja {id_abeja} depositó miel. Tarro actual: {tarro_miel}/{M}")
        # 4. Si tarro_miel == M, avisar/despertar al oso dormido.
                if tarro_miel == M:
                    print(f"🚨 🐝 Abeja {id_abeja}: ¡El tarro está LLENO! ¡Zzz... Despertando al oso!")
                    sem_oso.release() # Despierta al oso
        # 5. Si no está lleno, permitir que otras abejas sigan produciendo.
        pass

def oso(max_tarros=2):
    global tarro_miel, simulacion_activa
    tarros_comidos = 0
    sem_tarro_disponible.acquire()

    while tarros_comidos < max_tarros and simulacion_activa:
        # =====================================================================
        # TODO PARA EL ESTUDIANTE:
        # 1. Esperar pasivamente (bloqueado) hasta que una abeja señale que el tarro está lleno:
        #    sem_oso.acquire()
        sem_tarro_disponible.release()
        # 2. Comerse toda la miel (tarro_miel = 0).
        sem_oso.acquire()
        # 3. Incrementar tarros_comidos += 1.
        sem_tarro_disponible.acquire()
        if not simulacion_activa:
            break
        # 4. Avisar a las abejas que el tarro está vacío y disponible (sem_tarro_disponible.release()).
        # =====================================================================
        print(f"🐻 Oso: ¡Me desperté! Comiendo delicioso tarro de miel N° {tarros_comidos + 1}...")
        time.sleep(1.0) # Tiempo simulado comiendo
        tarro_miel = 0
        tarros_comidos += 1
        print(f"🐻 Oso: ¡Terminé! Tarro vacío ({tarro_miel}/{M}). Me voy a dormir... 😴")
        print("-" * 40)
        pass
        time.sleep(0.05)
        break  # Evita bucle infinito 
        
    simulacion_activa = False

    try:
        sem_tarro_disponible.release()
    except RuntimeError:
        pass

if __name__ == "__main__":
    print("=" * 60)
    print(" Iniciando Simulación: El Oso y las Abejas (UNJu FI)")
    print("=" * 60)
    # TODO: Crear e iniciar los hilos para el oso y las N abejas
    hilo_oso = threading.Thread(target=oso, args=(2,)) # Comerá 2 tarros completos
    hilo_oso.start()
    
    # Crear e iniciar los hilos de las N abejas
    hilos_abejas = []
    for i in range(NUM_ABEJAS):
        t = threading.Thread(target=abeja, args=(i + 1,))
        hilos_abejas.append(t)
        t.start()
        
    # Esperar a que el oso termine de comer sus tarros programados
    hilo_oso.join()
    
    # Esperar a que las abejas terminen y cierren sus ciclos de manera limpia
    for t in hilos_abejas:
        t.join()
        
    print("=" * 60)
    print(" Simulación finalizada correctamente.")
    print("=" * 60)
    pass

