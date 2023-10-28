import urllib.request, os, shutil, socket, sys, requests
from zipfile import ZipFile
from datetime import datetime

GITHUB_REPO = "GalaxyGamingBoy/modpack-tech-reforged"
PORT = "25565"
IP = "127.0.0.1"


def create_server():
    print("Creating Server Directory...")
    try:
        os.makedirs("./.minecraft-server/")
    except FileExistsError:
        print("ERR - Server Directory Exists, Removing...")
        shutil.rmtree("./.minecraft-server/")
        os.makedirs("./.minecraft-server/")

    os.chdir("./.minecraft-server/")
    print("Creating Server Directory Finished!")


def get_server():
    print("Getting Server ZIP...")
    urllib.request.urlretrieve(
        f"https://github.com/{GITHUB_REPO}/releases/latest/download/server.zip",
        "server.zip",
    )
    print("Succesfully Got Server ZIP!")


def extract_server():
    print("Extracting Server ZIP...")
    with ZipFile("./server.zip", "r") as z:
        z.extractall()
    os.remove("server.zip")
    os.chdir("./server/")
    print("Extracting Server ZIP Finished!")


def install_mods():
    print("Installing Forge & Mods...")
    os.system("bash installForge.sh")
    os.system("bash installMods.sh")
    print("Installing Forge & Mods Finished!")


def discover_portip():
    global IP, PORT
    print("Discovering IP & Port...")
    if "SF_HOSTNAME" in os.environ:
        with open("/config/self/reverse_port", "r") as f:
            PORT = f.read()

        with open("/config/self/reverse_ip", "r") as f:
            IP = f.read()
    else:
        IP = socket.gethostbyname(socket.gethostname())
    print(f"Discovered {IP}:{PORT}!")


def change_server_properties():
    print("Changing server.properties...")
    changes = {"server-port=20000": f"server-port={PORT}"}
    data = ""

    with open("server.properties") as f:
        data = f.read()

    for key in changes:
        data = data.replace(key, changes[key])

    with open("server.properties", "w") as f:
        f.write(data)
    print("Finished chaning server.properties!")


def get_world(id):
    print("Downloading world.zip...")
    urllib.request.urlretrieve(
        f"https://pixeldrain.com/api/file/{id}?download", "world.zip"
    )
    print("Downloading complete!")


def extract_world():
    print("Extracting world...")
    with ZipFile("world.zip") as z:
        z.extractall()
    print("Extraction Complete!")


def notify(token, chat_id, id):
    print("Notifying via telegram...")
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={
            "chat_id": chat_id,
            "text": f"""
~~~ Server Setup Notifier ~~~
DateTime: {datetime.now()}

IP: {IP}
PORT: {PORT}
Connection Details: {IP}:{PORT}

World Exists: {sys.argv[1] != "-1"}
{f'World Pixeldrain ID: {id}' if sys.argv[1] != "-1" else ""}
""",
        },
    )


if __name__ == "__main__":
    if len(sys.argv) == 3:
        # create_server()
        # get_server()
        # extract_server()
        os.chdir("./.minecraft-server/server/")
        install_mods()
        discover_portip()
        change_server_properties()
        if sys.argv[1] != "-1":
            get_world(sys.argv[1])
            extract_world()

        if sys.argv[2] != "-1":
            notify(sys.argv[2].split("|")[0], sys.argv[2].split("|")[1], sys.argv[1])
    else:
        print(
            "python3 setupServer.py <PIXELDRAIN_ID>(or -1 to generate) <TELEGRAM_TOKEN|TELEGRAM_CHATID>(or -1 to skip)"
        )
