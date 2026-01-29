import requests
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime

CONTENT_DISPOSITION = "Content-Disposition"
CONTENT_TYPE = "Content-Type"

def valid_dir(path)->Path:
    directory_location = Path(path)
    if not directory_location.exists():
        raise argparse.ArgumentTypeError(f"Directory path for {path} does not exist")
    return directory_location

parser = argparse.ArgumentParser(
    description="Download content from a URL and save it to a specific location."
)

parser.add_argument(
    "url", 
    help="The URL of the content to download"
)

parser.add_argument(
    "-o", "--output", 
    help="The name of the file to save as (e.g., 'image.png')"
)

parser.add_argument(
    "-d", "--dir", 
    default=".", 
    type=valid_dir,
    help="The directory to save the file in (defaults to current directory)"
)



@dataclass
class Config:
    url: str
    directory: Path
    file_name: Optional[str]

def validate_correct_content(headers:Dict[str,str]):
    if not '.pdf' in headers.get(CONTENT_DISPOSITION, "").lower():
        return False
    if not 'pdf' in headers.get(CONTENT_TYPE, "").lower():
        return False
    return True

def extract_file_name(headers:Dict[str,str])->Optional[str]:
    content_disposition = headers.get(CONTENT_DISPOSITION)
    if not content_disposition:
        return None
    else:
        content_info = content_disposition.split(';')
        for each in content_info:
            if 'filename' in each:
                return each.split('=')[-1].replace('"' ,'')
    return None


def fetch_file(config:Config):
    try:
        data = requests.get(config.url)
        if not validate_correct_content(data.headers):
            print(f'Invalid content')
            exit(1)
        possible_file_name = extract_file_name(data.headers)
        actual_file_name = config.file_name if config.file_name else possible_file_name if possible_file_name else f'file-{int(datetime.timestamp(datetime.now()))}.pdf'
        with Path(config.directory, actual_file_name).open('wb') as f:
            f.write(data.content)
    except Exception as e:
        print(f"An error occurred while trying to fetch {config.url} {e.with_traceback()}")
        exit(1)
    exit(0)

def main()->Config:
    args = parser.parse_args()
    return Config(url=args.url, directory=args.dir, file_name=args.output)



if __name__ == "__main__":
    config: Config = main()
    fetch_file(config)
