#!/usr/bin/env python3
"""
Tortoise TTS Voice Cloning Training Script
This script will train a voice clone using your audio samples.
"""

import os
import torch
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_voices

def main():
    print("🎤 Starting Tortoise TTS Voice Cloning Training...")
    print("=" * 50)
    
    # Check if we have processed audio files
    voice_dir = "audio_data/your_voice_processed"
    if not os.path.exists(voice_dir):
        print(f"❌ Audio directory not found: {voice_dir}")
        return
    
    audio_files = [f for f in os.listdir(voice_dir) if f.endswith('.wav')]
    if not audio_files:
        print(f"❌ No audio files found in {voice_dir}")
        return
    
    print(f"✓ Found {len(audio_files)} audio files")
    for file in sorted(audio_files):
        print(f"  - {file}")
    
    print("\n🧠 Loading Tortoise TTS...")
    
    # Initialize TTS with device detection
    device = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'
    print(f"🔧 Using device: {device}")
    
    # This might take a while on first run as it downloads models
    tts = TextToSpeech(device=device)
    
    print("✓ Tortoise TTS loaded successfully!")
    
    # Copy our processed audio files to Tortoise's voice directory
    tortoise_voice_dir = os.path.join(os.path.expanduser("~"), ".cache", "tortoise", "voices", "target_voice")
    os.makedirs(tortoise_voice_dir, exist_ok=True)
    
    import shutil
    print(f"\n📁 Copying audio files to Tortoise voice directory...")
    for file in audio_files:
        src = os.path.join(voice_dir, file)
        dst = os.path.join(tortoise_voice_dir, file)
        shutil.copy2(src, dst)
        print(f"  ✓ Copied {file}")
    
    print("\n🎯 Testing voice generation...")
    
    # Test with a simple sentence
    test_text = "Hello, this is a test of my cloned voice using Tortoise TTS."
    
    print(f"📝 Generating: '{test_text}'")
    print("⏳ This will take a while... grab some coffee!")
    
    # Load voice samples properly
    voice_samples, _ = load_voices(['target_voice'])
    
    # Generate speech (this is the slow part)
    gen = tts.tts_with_preset(
        text=test_text,
        voice_samples=voice_samples,
        preset='fast'  # Use 'fast' preset for quicker generation during testing
    )
    
    # Save the output
    output_file = "test_output.wav"
    tts.save_wav(gen.squeeze(0).cpu(), output_file)
    
    print(f"🎉 Voice generation complete!")
    print(f"💾 Saved to: {output_file}")
    print(f"🎵 Play the file to hear your cloned voice!")
    
    return output_file

if __name__ == "__main__":
    try:
        output = main()
        print("\n✅ Training and testing completed successfully!")
        if output:
            print(f"🔊 Your cloned voice sample: {output}")
    except Exception as e:
        print(f"\n❌ Error during training: {e}")
        print("\nThis might be due to:")
        print("- Insufficient audio data")
        print("- Audio quality issues") 
        print("- Hardware limitations")
        import traceback
        traceback.print_exc()