# Download Google Drive Files From URLs

## -1. Create Virtaul Environment
```
python3 -m venv .env
env/Scripts/activate
```

## 0. Install Library
```
pip install --upgrade -r requirements.txt
```

## 1. Prepare User Token
```
python makeauth.py # Then select an account.
```
After That, it will create token.json<br>
If want to switch account, please delete token.json then re-run

## 2. Start Download From Urls
Prepare a files contain urls<br>
```
url1
url2
url3
...
```
Then Run
```
python download_utils.py --urls_file=sample_urls.txt --target_folder=data > log.txt
```
