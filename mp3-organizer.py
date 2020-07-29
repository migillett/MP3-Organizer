#! /usr/bin/env python3

import os
import shutil
from tinytag import TinyTag, TinyTagException

source_folder = ''
destination_folder = ''


def main(source, destination):

    os.chdir(source)

    for root, dirs, files in os.walk('.', topdown=False):

        for audio_file in files:

            if audio_file.endswith(('.mp3', '.m4a')):

                file_source = os.path.join(root, audio_file)

                error_folder = os.path.join(destination, 'Corrupted files')
                if not os.path.exists(error_folder):
                    os.mkdir(error_folder)

                try:
                    track = TinyTag.get(os.path.join(root, audio_file))
                    track_genre = track.genre
                    try:
                        track_genre = track_genre.replace('/', '_')
                    except AttributeError:
                        print('Error copying file', track.title)
                        continue

                    genre_folder = os.path.join(destination, track_genre)

                    if not os.path.exists(genre_folder):
                        os.mkdir(genre_folder)

                    file_destination = os.path.join(genre_folder, audio_file)

                    if not os.path.isfile(file_destination):
                        shutil.copyfile(file_source, file_destination)
                        print('Moved', audio_file, 'to', file_destination)
                    else:
                        print('Skipped file:', audio_file)

                except TinyTagException:
                    print('Error reading ID3 tag for file:', audio_file)
                    error_save = os.path.join(error_folder, audio_file)
                    if not os.path.isfile(error_save):
                        shutil.copyfile(file_source, error_save)


if __name__ == '__main__':
    main(source_folder, destination_folder)
