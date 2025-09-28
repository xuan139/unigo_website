import asyncio
import websockets

connected_clients = set()

async def echo(websocket):  # ✅ 仅一个参数
    connected_clients.add(websocket)
    print("🟢 客户端连接")

    try:
        await websocket.send("Welcome to Info Center!")
        async for message in websocket:
            print(f"📩 收到客户端消息: {message}")
            # await websocket.send(f"Echo: {message}")

    except websockets.exceptions.ConnectionClosed:
        print("❌ 客户端断开连接")

    finally:
        connected_clients.remove(websocket)

async def broadcast_input():
    while True:
        msg = await asyncio.get_event_loop().run_in_executor(None, input, "✏️ 输入广播消息: ")
        for ws in connected_clients.copy():
            try:
                await ws.send(f"{msg}")
            except Exception as e:
                print(f"⚠️ 广播失败: {e}")

async def main():
    server = await websockets.serve(echo, "localhost", 8765)
    print("✅ WebSocket 服务已启动：ws://localhost:8765")

    await broadcast_input()  # 开始监听终端输入进行广播

asyncio.run(main())
