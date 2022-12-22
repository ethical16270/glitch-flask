from flask import Flask, request
import asyncio
import json
import websocket
import websockets

app = Flask(__name__)

@app.route('/send_message', methods=['POST'])
async def send_message():
    bet = request.form['bet']
    async with websockets.connect('ws://western-lavish-barracuda.glitch.me/:5000') as websocket:
        await websocket.send(bet)
        response = await websocket.recv()
        return response

betting=[]

def on_message(ws, message):
    data = json.loads(message)
    if "result" in data['data']:
        betting.clear()
    if "betInfos" in data['data']:
        data_field = data["data"]
        bet_data = json.loads(data_field)
        bet_infos = bet_data["betInfos"]
        type_field = bet_infos[0]["type"]
        betting.append(type_field)

        if(len(betting)==5):
            print(betting)
            json_data=json.dumps(betting)
            asyncio.get_event_loop().run_until_complete(send_message(betting))


    else:
        print("biInfos not found in data")
    

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("Connection closed")

ws = websocket.WebSocketApp("wss://luckyhit.colorwiz.in/luckyhit_ws/?token=7e8ae837dd4cad4378f04dda193167fd3a4191ae",
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

ws.run_forever()

if __name__ == '__main__':
    app.run()
