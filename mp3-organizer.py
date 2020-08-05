#! /usr/bin/env python3

import os
import shutil
from tinytag import TinyTag, TinyTagException
from pydub import AudioSegment

source_folder = ''

destination_folder = ''


def normalize_audio(audio_file):
    audio_file = audio_file.split('.')
    sound = AudioSegment.from_file(audio_file[0], audio_file[1])
    normalized_sound = match_target_amplitude(sound, -20.0)
    normalized_sound.export("{0}.mp3".format(audio_file[0]), format="mp3")


def match_target_amplitude(sound, target):
    change_in_db = target - sound.dBFS
    return sound.apply_gain(change_in_db)


def copy_file(source, destination):
    if not os.path.isfile(destination):
        shutil.copy(source, destination)
        print('Copied file:', source, 'to', destination)
    else:
        print('Skipped file', source)


def main(source, destination):

    os.chdir(source)

    error_folder = os.path.join(destination, 'Corrupted files')
    if not os.path.exists(error_folder):
        os.mkdir(error_folder)

    for root, dirs, files in os.walk('.', topdown=False):

        for audio_file in files:

            if audio_file.endswith(('.mp3', '.m4a')):

                file_source = os.path.join(root, audio_file)

                error_save = os.path.join(error_folder, audio_file)

                try:
                    track = TinyTag.get(os.path.join(root, audio_file))
                    track_genre = track.genre
                    try:
                        track_genre = track_genre.replace('/', '_')

                        genre_folder = os.path.join(destination, track_genre)

                        if not os.path.exists(genre_folder):
                            os.mkdir(genre_folder)

                        file_destination = os.path.join(genre_folder, audio_file)

                        if not os.path.isfile(file_destination):
                            copy_file(file_source, file_destination)

                    except AttributeError:
                        print('Error copying file: {0}. Saving to error folder'.format(track.title))
                        copy_file(file_source, error_save)
                        continue

                except TinyTagException:
                    print('Error reading ID3 tag for file:', audio_file)
                    if not os.path.isfile(error_save):
                        copy_file(file_source, error_save)
                    continue


if __name__ == '__main__':
    main(source_folder, destination_folder)
