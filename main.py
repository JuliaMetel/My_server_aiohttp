from aiohttp import web
from aiohttp.web_request import Request
import json
import ssl


async def handle(request: Request) -> web.Response:
    response_obj = {'status': 'success'}
    return web.Response(text=json.dumps(response_obj), status=200)


async def new_user(request: Request) -> web.Response:
    try:
        user = request.query['name']
        print('Crieating  new user with name', user)

        response_obj = {'status':'success', 'massage':'user successfully created'}
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        response_obj = {'status': 'failed', 'massage': repr(e)}
        return web.Response(text=json.dumps(response_obj), status=500)


async def ws_echo(request: Request) -> web.WebSocketResponse:
    websocket = web.WebSocketResponse()  # Create a websocket response object
    await websocket.prepare(request) # Load it with the request object
    async for message in websocket:  # For each message in the websocket connection
        await websocket.send_str(message[1])
    return websocket


async def ws_echo_for_all(request: Request) -> web.WebSocketResponse:
    current_websocket = web.WebSocketResponse()  # Create a websocket response object
    await current_websocket.prepare(request)  # Load it with the request object
    async for message in current_websocket:  # For each message in the websocket connection
        await current_websocket.send_str(f'Your name: {request.query["name"]} and your message: {message[1]}')
    return current_websocket


app =web.Application()
app.router.add_get('/', handle)
app.router.add_post('/user', new_user)
app.add_routes([web.get('/ws_echo', handler=ws_echo)])
app.add_routes([web.get('/ws_echo_for_all', handler=ws_echo_for_all)])

ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain('./certs/hellfish.test.crt', './certs/hellfish.test.key')

# web.run_app(app, ssl_context=ssl_context, port=443)
web.run_app(app, port=443)

