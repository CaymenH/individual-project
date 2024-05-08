from flask import Flask, render_template
from flask_mqtt import Mqtt
import ssl

app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = "0a48cdf916404edea8461de766143f32.s1.eu.hivemq.cloud"
app.config['MQTT_USERNAME'] = "flask"
app.config['MQTT_PASSWORD'] = "Pleasework1"
app.config['MQTT_CLIENT_ID'] = "caymensflask"
app.config['MQTT_BROKER_PORT'] = 8883
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = True
app.config['MQTT_TLS_INSECURE'] = False
app.config['MQTT_TLS_CA_CERTS'] = 'isrgrootx1.pem'
app.config['MQTT_TLS_VERSION'] = ssl.PROTOCOL_TLSv1_2
app.config['MQTT_TLS_CIPHERS'] = None

mqtt = Mqtt(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


@mqtt.on_disconnect()
def handle_disconnect():
    print("disconnected")


@app.route('/publish')
def publish_test():
    mqtt.publish('caymen/is/ace', 'it works:)')
    return '<h1>Did it work?</h1> (Check your flask console)'

@app.route('/toggle-led')
def switchLight():
    result = mqtt.publish('led/topic', 'hellooooo')
    print(result)
    return render_template('ledstatus.html')

@app.route('/')
def ledStatus():
    return render_template('ledstatus.html', led=app.config.get('LED_STATUS', 'Unknown'))



@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print(str(message.payload))

    if message.topic == "distance":
        update_webpage(message.payload)

def update_webpage(ledStatus):
    app.config['LED_STATUS'] = ledStatus

if __name__ == '__main__':
    app.run(debug=True)
