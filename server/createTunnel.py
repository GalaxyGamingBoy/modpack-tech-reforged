import shutil, os


def cloudflared_exists():
    print("Checking if cloudflared exists...")
    exist = shutil.which("cloudflared") != None
    print(f"Cloudflared check complete: {exist}!")
    return exist


def create_track_tunnel():
    print("Creating a create-track-mod website tunnel...")
    os.system("cloudflared tunnel --url http://localhost:3876/ --no-autoupdate")
    print("Done!")


if __name__ == "__main__":
    if cloudflared_exists():
        create_track_tunnel()
