"""
Audio transcription logic.
"""

import os
from .models import get_device, get_or_load_model

def transcribe_audio(audio_array, model_size="small"):
    """
    Transcribe audio using Whisper.
    
    Args:
        audio_array (np.ndarray): Audio data
        model_size (str): Whisper model size
    
    Returns:
        str: Transcribed text
    """
    device = get_device()
    use_fp16 = device == "cuda"

    print(f"Using device : {device}")
    if device == "cuda":
        import torch
        print(f"GPU detected : {torch.cuda.get_device_name(0)}")

    model = get_or_load_model(model_size, device)

    print("Transcribing audio...")
    
    result = model.transcribe(
        audio_array,
        language='en',
        verbose=False,
        fp16=use_fp16,
        word_timestamps=False,
        beam_size=1,
        temperature=0.0,
        condition_on_previous_text=False
    )

    return result["text"].strip()