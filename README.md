# Download Google Drive Files From URLs

## 0. Install Library
```
pip install requirements.txt
```

## 1. Prepare User Token
```
python makeauth.py # The select an account.
# After That, it will create token.json
```
<p style="color:red;font-size:30px">DO NOT SHARE token.json TO OTHER!</p>

## 2. Start Download From Urls
```
# in notebook
import os
from download_util import download_from_raw_to_folder
path = "path_to_save_file"
os.mkdir(path)

urls = """
url1
utl2
url3...
"""

download_from_raw_to_folder(urls, path)
```

