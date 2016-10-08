import tempfile
from binascii import a2b_base64

from channels import Group
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
    prefix, label = message['path'].strip('/').split('/')
    message.channel_session['room'] = label    
    Group('chat-'+label, channel_layer=message.channel_layer).add(message.reply_channel)

@channel_session
def ws_receive(message):
    label = message.channel_session['room']
    if 'b64' in message:
        b64_data = message['b64']
        bin_data = a2b_base64(b64_data)
        file = tempfile.TemporaryFile()
        file.write(bin_data)
        resp = process_file(file)
        Group('chat-'+label, channel_layer=message.channel_layer).send({"response": resp})

@channel_session
def ws_disconnect(message):
    label = message.channel_session['room']
    Group('chat-'+label, channel_layer=message.channel_layer).discard(message.reply_channel)