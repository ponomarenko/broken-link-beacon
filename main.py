import os
import re
import requests
import colorama
from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup, UnicodeDammit
from rich.console import Console
from rich.table import Table
from collections import Counter

load_dotenv()

url_table = Table(title="Link audit report")

url_table.add_column("What", style="cyan", no_wrap=True)
url_table.add_column("Where", style="cyan", no_wrap=True)
url_table.add_column("Why", justify="right", style="green")

colorama.init()

GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW

MAX_URLS_DEFAULT = 30

report_folder = "out-data"

internal_links = set()
broken_links = set()

total_urls_visited = 0


def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def is_excluded_link(url):
    excluded_patterns = [r"^mailto:", r"^javascript:", r"^tel:", r"^viber:"]

    for pattern in excluded_patterns:
        if re.match(pattern, url, re.IGNORECASE):
            return True
    return False


def get_all_website_links(url, parent):
    urls = set()
    response = None

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
        }

        response = requests.get(url.strip(), headers=headers, timeout=10)
        if response.status_code != 200:
            broken_links.add(url)
            url_table.add_row(url, parent, f"[yellow]{response.status_code}")
            return []
    except requests.exceptions.ConnectionError:
        broken_links.add(url)
        url_table.add_row(url, parent, "[red]Error")
        print(f"{GRAY}[!] Connection refused: {url}{RESET}")
        return []

    content_type = response.headers.get("Content-Type", None)
    if content_type is None or not content_type.startswith("text/"):
        return []

    soup = BeautifulSoup(
        UnicodeDammit(
            response.content, ["latin-1", "iso-8859-1", "windows-1251"]
        ).unicode_markup,
        "html.parser",
    )

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")

        if href == "" or href is None:
            continue

        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)

        if not is_valid(href) or is_excluded_link(href):
            continue

        if href in broken_links:
            # already in the set
            continue

        if domain_name not in href:
            # external link
            continue

        if href in internal_links:
            # already in the set
            continue

        urls.add(href)

        internal_links.add(href)

    return urls


def crawl(url, parent="", max_urls=MAX_URLS_DEFAULT):
    global total_urls_visited

    total_urls_visited += 1

    print(f"{YELLOW}[*] Crawling: {url}{RESET}")

    links = get_all_website_links(url, parent)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, parent, max_urls=max_urls)


def show_stats():
    console = Console(record=True)

    print("[+] Total Broken links:", len(broken_links))
    print("[+] Total Crawled URLs:", max_urls)

    # save the broken links to a file
    with open(
        os.path.join(report_folder, f"{domain_name}_broken_links.txt"),
        "w",
        encoding="utf-8",
    ) as f:
        for internal_link in broken_links:
            print(internal_link.strip(), file=f)

    console.print(url_table)

    console.save_html(os.path.join(report_folder, f"{domain_name}_links.html"))


if __name__ == "__main__":

    max_urls = os.getenv("MAX_URLS", MAX_URLS_DEFAULT)
    url = os.getenv("URL")

    if url is None:
        import argparse

        parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
        parser.add_argument("url", help="The URL to extract links from.")
        parser.add_argument(
            "-m",
            "--max-urls",
            help=f"Number of max URLs to crawl, default is {MAX_URLS_DEFAULT}.",
            default=MAX_URLS_DEFAULT,
            type=int,
        )

        args = parser.parse_args()
        max_urls = args.max_urls
        url = args.url

    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc

    Path(report_folder).mkdir(parents=True, exist_ok=True)

    crawl(url, max_urls=int(max_urls))

    show_stats()
