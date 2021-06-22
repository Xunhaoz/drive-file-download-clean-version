# source : https://developers.google.com/drive/api/v3/manage-downloads

from __future__ import print_function
import makeauth
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload
import io
import sys
import re
import json

import pprint
pprint = pprint.PrettyPrinter(indent=2).pprint

GOOGLE_SLIDE_MIMETYPE = "application/vnd.google-apps.presentation"
PPTX_MIMETYPE = "application/vnd.openxmlformats-officedocument.presentationml.presentation"

def download_a_file_with_id(file_id, folder_path="data"):
  creds = makeauth.get_creds(force=False)

  drive_service = build('drive', 'v3', credentials=creds)
  r = drive_service.files().get(
    fileId=file_id,
    fields="kind, id, name, mimeType, size, parents",
    supportsAllDrives=True
  )
  meta = r.execute()
  pprint(meta)

  if meta["mimeType"] == GOOGLE_SLIDE_MIMETYPE:
    request = (
      drive_service.files()
      .export_media(
        fileId=file_id,
        mimeType=PPTX_MIMETYPE,
        # supportsAllDrives=True,
      )
    )
    filename = meta["name"]+".pptx"
  else:
    request = (
      drive_service.files()
      .get_media(
        fileId=file_id,
        supportsAllDrives=True
      )
    )
    filename = meta["name"]
  
  filepath = os.path.join("")
  
  def final_name(fname):
    import datetime
    fmt='%Y-%m-%d-%H-%M-%S'
    timestamp = datetime.datetime.now().strftime(fmt)
    
    fname_split = fname.split(".")
    if len(fname_split) > 1:
      rename = ".".join(
        fname_split[:-1]+[timestamp]+fname_split[-1:]
      )
    else:
      rename = ".".join(
        fname_split+[timestamp]
      )
      
    return os.path.join(
      folder_path,
      rename,
    )
  
  with io.FileIO(final_name(filename), "wb") as fh:
    print("start downloading")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
      status, done = downloader.next_chunk()
      print(f"{filename} Download  {status.progress()*100:7.2f}%." )
  print("download complete")
  return meta

def parse_urls_to_fileIds(raw_text):
  """\
  https://stackoverflow.com/questions/16840038/easiest-way-to-get-file-id-from-url-on-google-apps-script
  """
  pattern = "([-\w]{25,})"
  fileIds_list = re.findall(pattern, raw_text)
  print(f"find {len(fileIds_list)} urls")
  print(*fileIds_list, sep='\n')
  return fileIds_list

def download_from_fileIds_to_folder(fileIds_list, folder_path="data"):
  from pathlib import Path
  Path(folder_path).mkdir(parents=False, exist_ok=True)
  
  error_log_file = None
  print("fileIds list")
  print(fileIds_list)
  
  meta_list = []
  for itr, fileId in enumerate(fileIds_list):
    print("*"*100)
    print(f"current fileId:{fileId}, progress:{itr}/{len(fileIds_list)}")
    try:
      meta = download_a_file_with_id(
          fileId,
          folder_path
      )
      meta_list.append(meta)
    except Exception as e:
      import datetime
      if not error_log_file:
        error_log_file = open(
          os.path.join(folder_path, f"error_log_{datetime.date.today()}.txt"),
          "a"
        )
      print(fileId, e)

      error_log_file.write(fileId)
      error_log_file.write("\t")
      error_log_file.write(str(e))
      error_log_file.write("\n")
  print("Done")
  return meta_list
  
def download_from_raw_to_folder(raw_text,folder_path="data"):
  fileIds_list = parse_urls_to_fileIds(raw_text)
  json.dump(
    fileIds_list,
    open(
      os.path.join(
        folder_path,
        "fileIds_list.json"),
      "w"
    ),
    indent=2,
  )
  meta_list = download_from_fileIds_to_folder(fileIds_list, folder_path)
  json.dump(
    meta_list,
    open(
      os.path.join(
        folder_path,
        "correct_meta_list.json"),
      "w"
    ),
    indent=2,
  )
  