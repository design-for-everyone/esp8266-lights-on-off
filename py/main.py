from machine import Pin

def led_switch(led, state, inverse):
    if state == b'on':
        led.value(1)
        if inverse == True:
            led.value(0)
    if state == b'off':
        led.value(0)
        if inverse == True:
            led.value(1)

def sub_cb(topic, msg):
    print((topic, msg))
    if topic == b'led/red':
        led = Pin(5,Pin.OUT)
        led_switch(led,msg, False)
    if topic == b'led/blue':
        led = Pin(2,Pin.OUT)
        led_switch(led,msg, True)

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(b'led/red')
  client.subscribe(b'led/blue')
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  sleep_ms(10000)
  machine.reset()

print("started in main.py")

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

from machine import Pin
#import dht

led = Pin(2,Pin.OUT)


while True:
  try:
    client.check_msg()
    if (time.time() - last_message) > message_interval:
      msg = b'Hello #%d' % counter
      
      last_message = time.time()
      counter += 1
  except OSError as e:
    restart_and_reconnect()