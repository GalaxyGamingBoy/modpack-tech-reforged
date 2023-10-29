import shutil, requests, subprocess, time, sys
from datetime import datetime


def cloudflared_exists():
    print("Checking if cloudflared exists...")
    exist = shutil.which("cloudflared") != None
    print(f"Cloudflared check complete: {exist}!")
    return exist


def create_track_tunnel():
    print("Creating a create-track-mod website tunnel...")
    proc = subprocess.Popen(
        "cloudflared tunnel --url http://localhost:3876/ --no-autoupdate --metrics localhost:5555",
        shell=True,
    )
    print("Done!")
    return proc


def get_hostname():
    print("Getting Hostname...")
    hostname = (requests.get("http://localhost:5555/quicktunnel").json())["hostname"]
    print(f"Got hostname, {hostname}!")
    return hostname


def notify(token, chat_id, hostname):
    print("Notifying via telegram...")
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={
            "chat_id": chat_id,
            "text": f"""
~~~ Server Tunnel Notifier ~~~
DateTime: {datetime.now()}

Create Tunnel: {hostname}
""",
        },
    )


if __name__ == "__main__":
    if cloudflared_exists():
        PROC = create_track_tunnel()
        time.sleep(5)
        HOSTNAME = get_hostname()

        if sys.argv[1] != "-1":
            notify(sys.argv[1].split("|")[0], sys.argv[1].split("|")[1], HOSTNAME)

        input("Press any key to exit...")
        PROC.kill()
