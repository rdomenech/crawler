# crawler
Technical test as Python developer in redpoints

## How to use it
- Open a terminal.
- Download the source code.
- Create a virtualenv or virtualenwrapper with python 3.x.
- Install the requirements.
- Open a Python terminal inside the virtualenv.

```python
import json
from crawler import Crawler

query_params = json.dumps({
    "keywords": [
        "openstack",
        "nova",
        "css"],
    "proxies": [
        "194.126.37.94:8080",
        "13.78.125.167:8080"],
    "type": "Repositories"})

cr = Crawler()
cr.query(query_params)
```

- The response should be something similar to:

```python
'[{"url": "https://github.com/atuldjadhav/DropBox-Cloud-Storage", "extra": {"owner": "atuldjadhav", "language_stats": {"CSS": 52.0, "JavaScript": 47.2, "HTML": 0.8}}}]'
```

## How to run the tests
Open a terminal and activate the virtualenv.

```bash
py.test --cov-report html:cov_html --cov=crawler test_crawler.py
```

You could check the coverage by opening your browser and type: file://<REPO_PATH>/crawler/cov_html/index.html
