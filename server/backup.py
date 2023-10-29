import os, requests, sys
from zipfile import ZipFile
from datetime import datetime


def get_files(directory):
    file_paths = []
    for root, _, files in os.walk(directory):
        for filename in files:
            file_paths.append(os.path.join(root, filename))
    return file_paths


def zip_world():
    print("Zipping World...")
    with ZipFile("world.zip", "w") as z:
        for f in get_files("world"):
            z.write(f)
    print("World Zipped!")


def upload_world():
    print(f"Uploading world.zip to pixeldrain...")
    data = requests.post(
        f"https://pixeldrain.com/api/file",
        files=dict(file=open("world.zip", "rb")),
    ).json()
    print(f"Finished uploading, {data['id']}!")
    return data["id"]


def notify(token, chat_id, id):
    print("Notifying via telegram...")
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={
            "chat_id": chat_id,
            "text": f"""
~~~ Server Backup Notifier ~~~
DateTime: {datetime.now()}
Server: https://pixeldrain.com/
ID: {id}

View: https://pixeldrain.com/u/{id}
Download: https://pixeldrain.com/api/file/{id}?download
""",
        },
    )


if __name__ == "__main__":
    if len(sys.argv) == 2:
        zip_world()
        ID = upload_world()

        if sys.argv[1] != "-1":
            notify(sys.argv[1].split("|")[0], sys.argv[1].split("|")[1], ID)

    else:
        print("python3 backup.py <TELEGRAM_TOKEN|TELEGRAM_CHATID>(or -1 to skip)")
