import json

# send message
client = system.net.httpClient()

payload = {
    "message": "Hola desde Ignition!"
}
url = "http://192.168.68.111:8000/send_message/"
response = client.post(
    url,
    data=payload,
    # contentType="application/json"
)