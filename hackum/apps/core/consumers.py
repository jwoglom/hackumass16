import time
import tempfile
import json
from binascii import a2b_base64

from channels import Group
from channels.handler import AsgiHandler
from channels.sessions import channel_session

from .views import process_file_b64
 
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
    print("WSconnect", label)
    Group('chat-'+label, channel_layer=message.channel_layer).add(message.reply_channel)

@channel_session
def ws_receive(message):
    t0 = time.time()
    label = message.channel_session['room']
    print("WSreceive", label, message['text'][:100])
    js = json.loads(message['text'])
    print(len(js['b64']))
    if 'b64' in js:
        b64_data = js['b64']
        resp = process_file_b64(b64_data)
        print(resp)
        t1 = time.time()
        resp["timing"] = [t0, t1]
        Group('chat-'+label, channel_layer=message.channel_layer).send({"text": json.dumps({"response": resp})})

@channel_session
def ws_disconnect(message):
    label = message.channel_session['room']
    print("WSdisc", label)
    Group('chat-'+label, channel_layer=message.channel_layer).discard(message.reply_channel)