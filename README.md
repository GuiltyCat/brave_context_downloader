# brave-context-downloader

This document is created by Gemini2.5-Flash(preview).

This Python package provides utilities to assist with web scraping tasks that require using cookies and user agents from the Brave browser, specifically for downloading web content.

## Description

The `brave-context-downloader` package offers classes to:
- Extract and decrypt cookies directly from the Brave browser's SQLite cookie database.
- Retrieve the current user agent string from a Brave browser instance using Selenium.
- Download web content (HTML and files) using `wget` or `requests`, automatically applying the extracted cookies and user agent for authenticated requests.

It's designed for scenarios where accessing Brave's Browse context (like cookies and user agent) is necessary to successfully download resources from websites.

## Features

- **Brave Context Access:** Accesses Brave browser's cookie database and retrieves its user agent.
- **Cookie Decryption:** Decrypts cookies encrypted using the `v10` format (AES-CBC).
- **User Agent Retrieval:** Launches a headless Brave browser instance via Selenium to get the exact user agent string.
- **Authenticated Downloading:** Uses `wget` and `requests` to download resources with retrieved cookies and user agent headers, leveraging the Brave context.

## Requirements

- Python 3.6+
- Brave Browser installed.
- Linux
- Chromedriver installed and accessible in the system's PATH or specified by path.
- `wget` command-line utility installed.

## Installation

1.  Ensure you have the requirements listed above installed.
2.  Navigate to the directory containing the `pyproject.toml` file for the `brave-context-downloader` project.
3.  Install the package using pip:

    ```bash
    pip install .
    ```

    (If you are modifying the code and want it to reflect immediately, you might use `pip install -e .` for editable mode).

## Usage

After installing the package, you can import the necessary classes and use them as follows:

```python
# Assuming the classes are defined in a module like brave_context_downloader/core.py
from brave_context_downloader.core import Cookie, UserAgent, Downloader
from pathlib import Path

# --- Cookie Usage ---
# Instantiate the Cookie utility.
# You can optionally specify the cookie database path and a temporary copy path.
# cookie_path = "~/.config/BraveSoftware/Brave-Browser/Profile 1/Cookies" # Example non-default path
# tmp_cookie_path = "/tmp/my_brave_cookies.sqlite" # Example temporary path

cookie_util = Cookie() # Use default paths: ~/.config/BraveSoftware/Brave-Browser/Default/Cookies and /tmp/brave_cookies.sqlite
# cookie_util = Cookie(cookie_path=cookie_path, tmp_cookie_path=tmp_cookie_path)

# Get all cookies
all_cookies = cookie_util.get_cookie()
print("All Cookies:", all_cookies)

# Get cookies for a specific domain (e.g., "example.com")
# domain_cookies = cookie_util.get_cookie(domain_filter="example.com")
# print("Example.com Cookies:", domain_cookies)


# --- User Agent Usage ---
# Instantiate the UserAgent utility.
# You can optionally specify the Brave and Chromedriver executable paths.
# brave_path = "/opt/[brave.com/brave/brave](https://brave.com/brave/brave)" # Example non-default path
# chromedriver_path = "/usr/local/bin/chromedriver" # Example non-default path

user_agent_util = UserAgent() # Use default paths: /usr/bin/brave and /usr/bin/chromedriver
# user_agent_util = UserAgent(brave_path=brave_path, chromedriver_path=chromedriver_path)


user_agent_string = user_agent_util.get_user_agent()
print("Brave User Agent:", user_agent_string)


# --- Downloader Usage ---
# Instantiate the Downloader using the retrieved user agent and cookies (the Brave context).
# The 'parallel' parameter is currently not used by the methods.
downloader = Downloader(user_agent=user_agent_string, cookies=all_required_cookies, parallel=1)

# Download HTML content
url_html = "https://example.com"
try:
    html_content = downloader.get_html(url_html)
    print(f"Downloaded HTML from {url_html}:")
    # print(html_content[:500]) # Print first 500 characters
except Exception as e:
    print(f"Error downloading HTML: {e}")


# Download a file
# url_file = "[https://example.com/path/to/your/file.pdf](https://example.com/path/to/your/file.pdf)"
# save_directory = Path("./downloads")
# save_directory.mkdir(exist_ok=True) # Create directory if it doesn't exist
# try:
#     downloader.get_file(url_file, save_directory)
#     print(f"Downloaded file from {url_file} to {save_directory}")
# except Exception as e:
#     print(f"Error downloading file: {e}")
```
