import asyncio

async def echo(reader, writer):
    print(writer.get_extra_info('peername'))
    while not reader.at_eof():
        data = await reader.readline()
        print(data)
        print(data[5:9])
        host, port = writer.get_extra_info('peername')
        if data[:5] == b"print":
            writer.write(data[6:])
        elif data[:4] == b"info":
            if data[5:9] == b"port":
                writer.write(f'{port}'.encode())
            elif data[5:9] == b"host":
                writer.write(host.encode())
        else:
            writer.write(data.swapcase())
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())