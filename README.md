# brave-context-downloader

This document is created by Gemini2.5-Flash.

`brave-context-downloader` is a Python library that helps you download web content using your Brave browser's context, specifically its cookies and user agent. This is particularly useful for scraping websites that require authentication or have specific access restrictions.

## Features

* **Cookie Extraction:** Safely extracts and decrypts cookies directly from your Brave browser's cookie database.
* **User Agent Retrieval:** Automatically retrieves your Brave browser's user agent string, allowing your requests to mimic a real browser session and avoid being blocked.
* **Content Downloading:** Provides straightforward methods to download HTML content or files from a URL, leveraging the extracted cookies and user agent for authenticated access.

---

## Installation

This library has the following dependencies:

* `requests`
* `pycryptodomex`
* `selenium`

You will also need to have the **Brave browser** and **chromedriver** installed on your system.

You can install the Python dependencies using pip:

```bash
pip install requests pycryptodomex selenium
````

-----

## Usage

Here is a basic example of how to use `brave-context-downloader`.

First, import the necessary classes:

```python
from brave_context_downloader import Cookie, UserAgent, Downloader
```

Next, create instances of the `Cookie` and `UserAgent` classes to retrieve your browser's data.

```python
# Get cookies for a specific domain (e.g., "example.com")
cookies = Cookie().get_cookie(domain_filter="example.com")

# Get the Brave browser's user agent string
user_agent = UserAgent().get_user_agent()
```

Finally, use the `Downloader` class to make your requests.

```python
from pathlib import Path
import os

# Initialize the downloader with the retrieved user agent and cookies
downloader = Downloader(user_agent=user_agent, cookies=cookies, parallel=1)

# Get HTML content from a URL
url = "[https://example.com/protected_page](https://example.com/protected_page)"
html_content = downloader.get_html(url)
print(html_content)

# Download a file from a URL to a specified directory
save_directory = Path("./downloads")
os.makedirs(save_directory, exist_ok=True)
file_url = "[https://example.com/some_file.pdf](https://example.com/some_file.pdf)"
downloader.get_file(file_url, save_directory)
print("File downloaded successfully!")
```

