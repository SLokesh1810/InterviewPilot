import os
import uuid
import shutil

from fastapi import UploadFile
from dotenv import load_dotenv

load_dotenv()

AUDIO_STORAGE_PATH = os.getenv('BASE_PATH')

def save_audio_file(audio: UploadFile) -> str:
    """
    Saves the uploaded audio file and returns its absolute path.
    """

    os.makedirs(AUDIO_STORAGE_PATH, exist_ok=True)

    print(audio.filename)

    extension = os.path.splitext(audio.filename)[1]

    if extension == "":
        extension = ".wav"

    filename = f"{uuid.uuid4().hex}{extension}"

    audio_path = os.path.join(
        AUDIO_STORAGE_PATH,
        filename
    )

    print(audio_path)

    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    return filename


def delete_audio_file(audio_path: str) -> bool:
    """
    Deletes the temporary audio file.
    """

    try:
        if os.path.exists(audio_path):
            os.remove(audio_path)
            return True

        return False

    except Exception as e:
        print(f"Audio Delete Error: {e}")
        return False