# Download Google Drive Files From URLs
For chinese version step-by-step tutorial, please refer to my [medium](https://changethewhat.medium.com/google-drive-api-python-%E5%BE%9E0%E9%96%8B%E5%A7%8B%E5%88%B0%E5%BE%9Eurl%E4%B8%8B%E8%BC%89%E6%AA%94%E6%A1%88%E7%AF%84%E4%BE%8B-a182ce279073)

## 0. Install Library
```
pip install --upgrade -r requirements.txt
```

## 1. Prepare User Token
```
python makeauth.py # Then select an account.
# After That, it will create token.json
# If want to switch account, please delete token.json then re-run
```
# DO NOT SHARE token.json TO OTHER!
# DO NOT SHARE token.json TO OTHER!
# DO NOT SHARE token.json TO OTHER!

## 2. Start Download From Urls
### In command line
Prepare a files contain urls #like sample_urls.txt
Then Run
```
python download_utils.py --urls_file=sample_urls.txt --folder=data > log.txt
```
### In notebook
```
# in notebook
from download_utils import download_from_raw_to_folder
from pathlib import Path
data_path = "path_to_save_file"
Path(data_path).mkdir(parents=True, exist_ok=True)

# urls = """
# url1
# utl2
# url3...
# """

urls = """
# Not support folder
https://drive.google.com/drive/folders/1aQXUUaKQkBDz7cofkil-WyNBPmFSd_DW?usp=sharing # Folder -> not support

# Following types are supported
https://docs.google.com/spreadsheets/d/1bAyTQqBuUcIVrLYnDXjwCKvliHq_DoU0rwn_CjJFrao/edit#gid=0 # Google Sheet -> *.xlsx
https://docs.google.com/presentation/d/1_nvCSaU6UUKOeoCeytfZcZPbg5MoiCCF1zKTPntAXuI/edit?usp=sharing # Google Slide -> *.pptx
https://docs.google.com/document/d/1Ad8LR5MlEFsXyrRlCmmyoycxkvQeoUt4rBzNCjeSCfo/edit?usp=sharing # Google doc -> *.docx
https://drive.google.com/file/d/1FP7dKwdSiH_YNFU_nm82IWiE-YFyUKfp/view?usp=sharing # Normal File -> work
https://drive.google.com/file/d/13n2MpP2xojhXEfuTehnCMhlE0XWOOdXc/view?usp=sharing # Normal File -> work
"""

download_from_raw_to_folder(urls, path)
```

### Note
The FileId Parser is based on 
https://stackoverflow.com/questions/16840038/easiest-way-to-get-file-id-from-url-on-google-apps-script
```
def parse_urls_to_fileIds(raw_text):
  """\
  https://stackoverflow.com/questions/16840038/easiest-way-to-get-file-id-from-url-on-google-apps-script
  """
  pattern = "([-\w]{25,})"
  fileIds_list = re.findall(pattern, raw_text)
  print(f"find {len(fileIds_list)} fileIds")
  pprint(fileIds_list)
  return fileIds_list
```
