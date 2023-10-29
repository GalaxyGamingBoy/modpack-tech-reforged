import os, socket, requests, os, sys
from datetime import datetime

PORT = "25565"
IP = "127.0.0.1"


def discover_portip():
    global IP, PORT
    print("Discovering IP & Port...")
    if "SF_HOSTNAME" in os.environ:
        with open("/config/self/reverse_port", "r") as f:
            PORT = f.read().strip()

        with open("/config/self/reverse_ip", "r") as f:
            IP = f.read().strip()
    else:
        IP = socket.gethostbyname(socket.gethostname())
    print(f"Discovered {IP}:{PORT}!")


def notify(token, chat_id):
    print("Notifying via telegram...")
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={
            "chat_id": chat_id,
            "text": f"""
~~~ Server Run Notifier ~~~
DateTime: {datetime.now()}

IP: {IP}
PORT: {PORT}
Connection Details: {IP}:{PORT}
""",
        },
    )


discover_portip()
if sys.argv[1] != "-1":
    notify(sys.argv[1].split("|")[0], sys.argv[1].split("|")[1])
os.system("./run.sh")
