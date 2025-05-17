import requests
from pathlib import Path
import shutil
import sqlite3
import hashlib
import subprocess

from Cryptodome.Cipher import AES

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class Cookie:
    def __init__(self,
                 cookie_path="~/.config/BraveSoftware/Brave-Browser/Default/Cookies",
                 tmp_cookie_path="/tmp/brave_cookies.sqlite"):
        self.cookie_path = Path(
            cookie_path).expanduser()
        self.tmp_cookie_db = Path(tmp_cookie_path)
        self.key = hashlib.pbkdf2_hmac("sha1", b"peanuts", b"saltysalt", 1, 16)
        pass

    def compat_ord(self, c):
        return c if isinstance(c, int) else ord(c)

    def decrypt_cookie(self, encrypted_value, key) -> str:
        try:
            if encrypted_value[:3] == b"v10":  # v10 uses AES-GCM
                iv = b" " * 16
                encrypted_value = encrypted_value[3:]
                cipher = AES.new(key, AES.MODE_CBC, iv)
                decrypted_with_pad = cipher.decrypt(encrypted_value)
                decrypted = decrypted_with_pad[: -
                                               self.compat_ord(decrypted_with_pad[-1])]
                return decrypted[32:].decode("utf-8")
            elif encrypted_value[:3] == b"v11":  # v11 uses AES-GCM
                raise Exception("v11 is not supported yet.")
            else:
                raise Exception(f"Unknown version: {encrypted_value[:3]}")
        except Exception as e:
            raise Exception(f"Decryption failed: {e}")

    def get_cookie(self, domain_filter=None):
        cookies = {}
        BRAVE_COOKIE_PATH = self.cookie_path
        tmp_cookie_db = self.tmp_cookie_db
        key = self.key

        shutil.copy2(BRAVE_COOKIE_PATH, tmp_cookie_db)
        conn = sqlite3.connect(tmp_cookie_db)
        cursor = conn.cursor()
        query = "SELECT host_key, name, encrypted_value FROM cookies"
        if domain_filter:
            query += " WHERE host_key LIKE ?"
        cursor.execute(query, (f"%{domain_filter}%",) if domain_filter else ())
        for host_key, name, encrypted_value in cursor.fetchall():
            decrypted_value = self.decrypt_cookie(encrypted_value, key)
            cookies[name] = decrypted_value
        conn.close()
        tmp_cookie_db.unlink()
        return cookies


class UserAgent:
    def __init__(self):
        self.brave_path = "/usr/bin/brave"
        self.chromedriver_path = "/usr/bin/chromedriver"
        self.user_agent = self.get_user_agent()

    def get_user_agent(self):
        brave_path = self.brave_path
        chromedriver_path = self.chromedriver_path

        options = Options()
        options.binary_location = brave_path
        options.add_argument("--headless")

        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)

        user_agent = driver.execute_script("return navigator.userAgent;")

        driver.quit()
        user_agent = user_agent.replace("Headless", "")
        return user_agent


class Downloader:
    def __init__(self, user_agent: str, cookies: dict[str, str], parallel: int):
        self.cookies = cookies
        self.user_agent = user_agent
        self.parallel = parallel

    def get_html(self, url: str):
        # download html by wget
        res = subprocess.run(
            [
                "wget",
                url,
                "-q",
                "-O",
                "-",
                "--user-agent",
                self.user_agent,
                "--header",
                "cookie: " + "; ".join(f"{k}={v}" for k,
                                       v in self.cookies.items()),
            ],
            stdout=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            check=True,
            env={"WGETRC": Path("~/.wgetrc").expanduser()},
        )
        # read from stdout
        html = res.stdout
        return html

    def get_file(self, url: str, save_dir: Path):
        headers = {"User-Agent": self.user_agent}
        res = requests.get(url, data=headers, cookies=self.cookies)
        file_name = Path(url).name
        with open(save_dir / file_name, "wb") as f:
            f.write(res.content)
