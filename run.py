import requests
import os
import subprocess
import sys


PLAYLISTS_DIR = sys.argv[1]
DOWNLOAD_DIR = sys.argv[2]


def load(name):
    res = requests.get(f'https://www.youtube.com/results', params={'search_query': name})
    print(name)

    try:
        code = res.text.split('href="/watch?v=')[1].split('"')[0]

        href = subprocess.check_output(['node', 'you.js', f'https://www.youtube.com/watch?v={code}'])
        href = href.decode('utf-8').strip()
        if href == 'error':
            print('Failed: ', name)
            return
        with requests.get(href, stream=True) as r:
            f_name = r.headers.get('Content-Disposition').split('filename="')[1].replace('"', '')
            r.raise_for_status()
            print(f_name)
            with open(os.path.join(DOWNLOAD_DIR, f'{f_name}.mp3'), 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
    except Exception as e:
        print(e)
        print('Failed', name)


for path in os.listdir(PLAYLISTS_DIR):
    with open(os.path.join(PLAYLISTS_DIR, path)) as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            parts = line.split('","')
            name = f"{parts[1]} {parts[2]}"

            load(name)
            print()


