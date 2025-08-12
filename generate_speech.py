#!/usr/bin/env python3
"""
Generate speech using your cloned voice
Usage: python generate_speech.py "Text you want to say"
"""

import sys
import os
import torch
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_voices

def generate_speech(text, voice_name="target_voice", output_file=None, preset="standard"):
    """
    Generate speech using the cloned voice
    
    Args:
        text (str): Text to convert to speech
        voice_name (str): Name of the voice (default: "target_voice")
        output_file (str): Output filename (auto-generated if None)
        preset (str): Quality preset - "ultra_fast", "fast", "standard", "high_quality"
    """
    if output_file is None:
        # Create filename from first few words
        safe_text = "".join(c for c in text[:30] if c.isalnum() or c in (' ', '_')).strip()
        safe_text = safe_text.replace(' ', '_')
        output_file = f"generated_{safe_text}.wav"
    
    print(f"🎤 Generating speech with voice: {voice_name}")
    print(f"📝 Text: '{text}'")
    print(f"⚡ Preset: {preset}")
    print("⏳ This may take a while...")
    
    # Initialize TTS
    device = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'
    print(f"🔧 Using device: {device}")
    
    tts = TextToSpeech(device=device)
    
    # Generate speech
    try:
        # Load voice samples properly
        voice_samples, _ = load_voices([voice_name])
        
        gen = tts.tts_with_preset(
            text=text,
            voice_samples=voice_samples,
            preset=preset
        )
        
        # Save the output using torchaudio
        import torchaudio
        torchaudio.save(output_file, gen.squeeze(0).cpu(), 24000)
        
        print(f"🎉 Speech generated successfully!")
        print(f"💾 Saved to: {output_file}")
        print(f"🔊 Play the file to hear your cloned voice!")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Error generating speech: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure training completed successfully")
        print("2. Check that voice files exist in ~/.cache/tortoise/voices/target_voice/")
        print("3. Try a shorter text or different preset")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_speech.py \"Your text here\"")
        print("\nOptional arguments:")
        print("  --preset [ultra_fast|fast|standard|high_quality]  (default: standard)")
        print("  --output filename.wav  (auto-generated if not specified)")
        print("  --voice voice_name     (default: target_voice)")
        return
    
    text = sys.argv[1]
    preset = "standard"
    output_file = None
    voice_name = "target_voice"
    
    # Parse optional arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--preset" and i + 1 < len(sys.argv):
            preset = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--output" and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--voice" and i + 1 < len(sys.argv):
            voice_name = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    generate_speech(text, voice_name, output_file, preset)

if __name__ == "__main__":
    main()