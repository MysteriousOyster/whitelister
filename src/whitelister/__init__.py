from dotenv import load_dotenv
import subprocess

def main() -> None:
    load_dotenv()
    subprocess.run(["uv", "run", "waitress-serve", "--host=0.0.0.0", "--port=80", "src.whitelister.app:app"])
