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

import argparse

import pprint
pprint = pprint.PrettyPrinter(indent=2).pprint

google_file_prefix = "application/vnd.google-apps."
office_prefix = "application/vnd.openxmlformats-officedocument."
google_office_mapper = {
  google_file_prefix+google_postfix:
  office_prefix+office_postfix
  
  for google_postfix,office_postfix in [
    ["document", "wordprocessingml.document"],
    ["presentation", "presentationml.presentation"],
    ["spreadsheet", "spreadsheetml.sheet"]
  ]
}

def file_extension_mapper(originalMimeType):
  if originalMimeType in google_office_mapper.keys():
    if "document" in originalMimeType: return ".docx"
    if "presentation" in originalMimeType: return ".pptx"
    if "spreadsheet" in originalMimeType: return ".xlsx"
  return ""

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

  file_mimeType = meta["mimeType"]
  target_mimeType = google_office_mapper.get(file_mimeType, file_mimeType)

  if target_mimeType != file_mimeType:
    # 特殊檔案，如google doc/sheet/slide
    # 下方的mimeType為期望轉換的格式
    request = drive_service.files().export_media(
      fileId=file_id,
      mimeType=target_mimeType,
    )
  else:
    # 一般檔案，如pdf, mov, mp4
    request = drive_service.files().get_media(
      fileId=file_id,
      supportsAllDrives=True,
    )
  
  filepath = os.path.join("")
  
  def final_name(meta):
    import datetime
    fname = meta["name"]
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
      rename+file_extension_mapper(meta["mimeType"])
    )
  filename = final_name(meta)
  
  with io.FileIO(filename, "wb") as fh:
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
  print(f"find {len(fileIds_list)} fileIds")
  pprint(fileIds_list)
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
          "w"
        )
      print(fileId, e)

      error_log_file.write(fileId)
      error_log_file.write("\t")
      error_log_file.write(str(e))
      error_log_file.write("\n")
  print("Done")
  return meta_list
  
def download_from_raw_to_folder(raw_text,folder_path="data"):
  from pathlib import Path
  Path(folder_path).mkdir(parents=False, exist_ok=True)
  
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

  
if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--urls_file',required=True)
  parser.add_argument('--folder',required=True)
  args = parser.parse_args()

  raw_text = open(args.urls_file,"r").read()
  folder = args.folder

  download_from_raw_to_folder(raw_text, folder)