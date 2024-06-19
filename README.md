To run this:

```bash
python main.py --help
```

**Output:**

```
usage: link_extractor.py [-h] [-m MAX_URLS] url

Link Extractor Tool with Python

positional arguments:
url                   The URL to extract links from.

optional arguments:
-h, --help            show this help message and exit
-m MAX_URLS, --max-urls MAX_URLS
                        Number of max URLs to crawl, default is 30.
```

For instance, to extract all links from 2 first URLs appeared in github.com:

```
python link_extractor.py https://github.com -m 2
```

This will result in a large list, here is the last 5 links:

```
[!] External link: https://developer.github.com/
[*] Internal link: https://help.github.com/
[!] External link: https://github.blog/
[*] Internal link: https://help.github.com/articles/github-terms-of-service/
[*] Internal link: https://help.github.com/articles/github-privacy-statement/
[+] Total Internal links: 85
[+] Total External links: 21
[+] Total URLs: 106
```

This will also save these URLs in `github.com_external_links.txt` for external links and `github.com_internal_links.txt` for internal links.

# Docker

Pull the repo with `docker pull org-name/container-name`

Enumerating usernames

```shell
docker run -it --rm org-name/container-name --url https://target.tld/
```

...

What's next?
Start your application by running → docker compose up --build
Your application will be available at http://localhost:8000
