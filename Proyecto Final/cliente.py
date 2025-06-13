import asyncio

# Configuración de los servidores (¡CAMBIAR CON LAS IPs REALES!)
SERVIDOR_SUMA_RESTA = ('131.196.247.29', 5000)  # IP Máquina 1
SERVIDOR_MULT_DIV   = ('192.168.1.101', 5001)  # IP Máquina 2

async def enviar_operacion(operacion: str, valor1: float, valor2: float) -> str:
    """
    Corutina que envía la operación al servidor correspondiente
    usando streams asíncronos.
    """
    # Selecciona el servidor según la operación
    host, port = (SERVIDOR_SUMA_RESTA if operacion in ["1", "2"]
                  else SERVIDOR_MULT_DIV)
    try:
        # Crea la conexión asíncrona
        reader, writer = await asyncio.open_connection(host, port)
        
        mensaje = f"{operacion},{valor1},{valor2}"
        writer.write(mensaje.encode())
        await writer.drain()
        
        # Espera respuesta con timeout de 5 segundos
        data = await asyncio.wait_for(reader.read(1024), timeout=5)
        respuesta = data.decode()
        
        writer.close()
        await writer.wait_closed()
        return respuesta

    except asyncio.TimeoutError:
        return "Error: Tiempo de espera agotado"
    except ConnectionRefusedError:
        return "Error: No se pudo conectar al servidor"
    except Exception as e:
        return f"Error inesperado: {e}"

async def menu_loop():
    """
    Bucle principal asíncrono. Para no bloquear el loop al pedir
    input(), usamos run_in_executor para delegar en un hilo.
    """
    loop = asyncio.get_running_loop()
    
    print("\nCalculadora Distribuida (asyncio)")
    print("================================")
    print("Operaciones disponibles:")
    print("1. Suma")
    print("2. Resta")
    print("3. Multiplicación")
    print("4. División")
    print("Pulsa 'q' para salir.\n")
    
    while True:
        # Pedimos la opción sin bloquear el event loop
        opcion = await loop.run_in_executor(
            None, input, "Seleccione operación (1-4) o 'q' para salir: "
        )
        opcion = opcion.strip().lower()
        
        if opcion == 'q':
            print("¡Hasta luego!")
            break
        
        if opcion not in ["1", "2", "3", "4"]:
            print("Opción inválida, intenta de nuevo.")
            continue
        
        try:
            # Pedimos valores al usuario
            v1 = await loop.run_in_executor(None, input, "Ingrese el primer valor: ")
            v2 = await loop.run_in_executor(None, input, "Ingrese el segundo valor: ")
            valor1 = float(v1)
            valor2 = float(v2)
        except ValueError:
            print("⚠️ Error: Debes ingresar números válidos.")
            continue

        # Llamamos a la corutina de envío
        resultado = await enviar_operacion(opcion, valor1, valor2)
        print(f"\n🔹 Resultado: {resultado}\n")

async def main():
    try:
        await menu_loop()
    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario. ¡Nos vemos!")

if __name__ == "__main__":
    asyncio.run(main())
