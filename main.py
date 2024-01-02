from pydub import AudioSegment
import shutil
import os
import random

def generate_custom_click_sound(file_path):
    custom_click_sound = AudioSegment.from_wav(file_path)
    return custom_click_sound

def preprocess_click_data(input_file, output_file):
    shutil.copyfile(f"{file_name}.txt", f"{file_name}.process")

    with open(output_file, 'r') as file:
        lines = file.readlines()[1:]

    lines = [line.replace(" 0 1 1", "") for line in lines]

    with open(output_file, 'w') as file:
        file.writelines(lines)

def read_click_data(file_path):
    click_data = []
    with open(file_path, 'r') as file:
        for line in file:
            frame, *click_state = map(int, line.split())
            click_data.append((frame, click_state))
    return click_data

def create_click_audio(click_data, frame_rate=144, click_sound_paths=None, release_sound_path="release.wav",
                       output_file=None):
    if output_file is None:
        output_file = f"{file_name}_clicks.mp3"

    frame_duration = 1000 / frame_rate
    audio = AudioSegment.silent(duration=int(click_data[-1][0] * frame_duration) + 100)

    release_sound = generate_custom_click_sound(release_sound_path)

    for frame, click_state in click_data:
        if any(click_state):
            click_sound_path = random.choice(click_sound_paths)
            click_sound = generate_custom_click_sound(click_sound_path)
            audio = audio.overlay(click_sound, position=int(frame * frame_duration))
        else:
            audio = audio.overlay(release_sound, position=int(frame * frame_duration))

    audio.export(output_file, format="mp3")

def process():
    global file_name, framerate
    file_name = input('\nInput only name of the txt file: ')
    framerate = int(input("Input FPS's of the GDBot record: "))

    file_path = f"{file_name}.txt"
    temp_file = f"{file_name}.process"
    frame_rate = framerate
    click_sound_paths = ["hard_mouse_click_sound3.wav", "hard_mouse_click_sound4.wav", "hard_mouse_click_sound5.wav"]
    release_sound_path = "mouse_release_sound1.wav"
    output_file = f"{file_name}_clicks.mp3"

    preprocess_click_data(temp_file, temp_file)

    click_data = read_click_data(temp_file)
    create_click_audio(click_data, frame_rate, click_sound_paths, release_sound_path, output_file)

    os.remove(temp_file)

    print('\nDone! Restarting...')

if __name__ == "__main__":
    print('Welcome to GDClick 1.12\nMade by watakak')
    process()
    while True:
        process()