# -*- coding: utf-8 -*-

"""
This script is used to fix the file names of mp3 files
that have been downloaded from the internet.
Specifically from spotify-downloader.com.
It opens the mp3 files in the current directory and
reads the ID3 tags using the library music-tag.
Then it renames the files using the following pattern:
<artist> - <title>.mp3
If the title is not available, the file is renamed to:
<artist>.mp3
If the artist is not available, the file is renamed to:
<title>.mp3
If neither artist nor title are available, the file is renamed to:
<filename>.mp3
"""

import os
import sys
import argparse
import logging
import music_tag


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fix mp3 file names.')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Enable debug output')
    parser.add_argument('-t', '--target', type=str, default='.',
                        help='Target directory')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    target_dir = args.target
    if not target_dir.endswith('/'):
        target_dir += '/'

    for filename in os.listdir(target_dir):
        if filename.endswith('.mp3'):
            logging.debug('Processing file: %s', filename)
            try:
                song = music_tag.load_file(target_dir + filename)
            except Exception as e:
                logging.error('Error loading file: %s', e)
                continue
            artist = str(song['artist'])
            title = str(song['title'])

            # Remove illegal characters from artist and title
            
            artist = artist.replace('/', '-')
            title = title.replace('/', '-')
            artist = artist.replace(':', '-')
            title = title.replace(':', '-')
            artist = artist.replace('?', '')
            title = title.replace('?', '')
            artist = artist.replace('"', '')
            title = title.replace('"', '')
            artist = artist.replace('*', '')
            title = title.replace('*', '')
            artist = artist.replace('<', '')
            title = title.replace('<', '')
            artist = artist.replace('>', '')
            title = title.replace('>', '')
            artist = artist.replace('|', '')
            title = title.replace('|', '')
            artist = artist.replace('\\', '')
            title = title.replace('\\', '')
            
            new_filename = f'{artist} - {title}.mp3'
            logging.debug('New filename: %s', new_filename)
            os.rename(target_dir + filename, target_dir + new_filename)         
    sys.exit(0)
