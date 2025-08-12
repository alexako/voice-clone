#!/usr/bin/env python3
"""
Quick test to generate speech with your cloned voice
"""

import torch
import torchaudio
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_voices

def main():
    print("🎤 Testing your cloned voice...")
    
    # Initialize TTS
    device = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'
    print(f"🔧 Using device: {device}")
    
    tts = TextToSpeech(device=device)
    
    # Load voice samples
    voice_samples, _ = load_voices(['target_voice'])
    
    # Test text
    test_text = "Hello, this is a test of my cloned voice!"
    print(f"📝 Generating: '{test_text}'")
    print("⏳ Generating with ultra_fast preset...")
    
    # Generate with faster preset
    gen = tts.tts_with_preset(
        text=test_text,
        voice_samples=voice_samples,
        preset='ultra_fast'  # Much faster for testing
    )
    
    # Save using torchaudio instead
    output_file = "target_voice_test.wav"
    torchaudio.save(output_file, gen.squeeze(0).cpu(), 24000)
    
    print(f"🎉 Voice generated successfully!")
    print(f"💾 Saved to: {output_file}")
    print(f"🔊 Play the file to hear your cloned voice!")
    
    return output_file

if __name__ == "__main__":
    try:
        output = main()
        print(f"\n✅ Success! Your voice clone: {output}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()