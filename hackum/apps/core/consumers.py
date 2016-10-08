import tempfile
from binascii import a2b_base64

from channels.handler import AsgiHandler
from channels.sessions import channel_session

from .views import process_file
 
def http_consumer(message):
    # Make standard HTTP response - access ASGI path attribute directly
    response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
    # Encode that response into message format (ASGI)
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)


@channel_session
def ws_connect(message):
    pass

@channel_session
def ws_receive(message):
    if 'b64' in message:
        b64_data = message['b64']
        bin_data = a2b_base64(b64_data)
        file = tempfile.TemporaryFile()
        file.write(bin_data)
        resp = process_file(file)

@channel_session
def ws_disconnect(message):
    pass