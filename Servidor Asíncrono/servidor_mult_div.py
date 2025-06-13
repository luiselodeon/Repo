import asyncio

HOST = '0.0.0.0'
PORT = 5001  # Puerto para multiplicación y división

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        data = await reader.read(1024)
        mensaje = data.decode().strip()
        partes = mensaje.split(',')

        if len(partes) != 3:
            respuesta = "Error: formato inválido"
        else:
            oper, v1_str, v2_str = partes
            try:
                v1 = float(v1_str)
                v2 = float(v2_str)

                if oper == '3':         # Multiplicación
                    resultado = v1 * v2
                elif oper == '4':       # División
                    if v2 == 0:
                        respuesta = "Error: división por cero"
                        writer.write(respuesta.encode())
                        await writer.drain()
                        return
                    resultado = v1 / v2
                else:
                    respuesta = "Error: operación no soportada"
                    writer.write(respuesta.encode())
                    await writer.drain()
                    return

                respuesta = str(resultado)
            except ValueError:
                respuesta = "Error: valores numéricos inválidos"

        writer.write(respuesta.encode())
        await writer.drain()

    except Exception as e:
        error_msg = f"Error inesperado: {e}"
        writer.write(error_msg.encode())
        await writer.drain()
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    addr = server.sockets[0].getsockname()
    print(f"Servidor de mult/división escuchando en {addr}")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
