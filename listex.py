import requests
import time
import html
from pprint import pprint

API_KEY = 'PASTE_YOUR_API_KEY_HERE'
API_BASE_URL = 'RED_BASE_URL_HERE'

def get_collage_details(collage_id):
    url = f'{API_BASE_URL}/ajax.php?action=collage&id={collage_id}'
    headers = {'Authorization': API_KEY}
    response = requests.get(url, headers=headers)
    return response.json() if response.ok else None

def get_torrent_details(torrent_id):
    url = f'{API_BASE_URL}/ajax.php?action=torrent&id={torrent_id}'
    headers = {'Authorization': API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()['response'] if response.ok else None

def parse_file_list(file_list):
    files = file_list.split("|||")
    return [file.split("{{{")[0] for file in files]

def create_m3u(output_filename, m3u_content):
    with open(output_filename, 'w') as f:
        f.write(m3u_content)
    print(f"M3U file '{output_filename}' has been created.")

if __name__ == "__main__":
    collage_id = COLLAGE_ID_HERE  # Example collage ID
    torrent_media = 'Vinyl'
    torrent_format = 'FLAC'
    torrent_encoding = 'Lossless'
    collage_details = get_collage_details(collage_id)
    pprint(collage_details)
    time.sleep(1)
    m3u_content = "#EXTM3U\n\n"

    if collage_details:
        for torrent_group in collage_details['response']['torrentgroups']:
            for torrent in torrent_group['torrents']:
                if torrent['media'] == torrent_media and torrent['format'] == torrent_format and torrent['encoding'] == torrent_encoding:
                    torrent_details = get_torrent_details(torrent['torrentid'])
                    time.sleep(1)  # Respect rate limits
                    if torrent_details:
                        fileList = torrent_details['torrent']['fileList']
                        directory = torrent_details['torrent']['filePath']
                        filenames = parse_file_list(fileList)
                        for filename in filenames:
                            if f'.{torrent_format.lower()}' in filename.lower():
                                m3u_content += html.unescape(f"{directory}/{filename}\n")

        create_m3u(f"collage_{str(collage_id)}_playlist.m3u", m3u_content)
