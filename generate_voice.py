#!/usr/bin/env python3
"""
Voice Generation Script with Better Quality and Speed
Enhanced TTS voice generation with optimized settings and multiple quality presets
"""

import sys
import os
import torch
import torchaudio
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_voices
import time
from pathlib import Path

class ImprovedTortoiseGenerator:
    def __init__(self, voice_name="alex"):
        """Initialize with optimized settings"""
        self.voice_name = voice_name
        self.device = self._get_best_device()
        self.tts = None
        
        print(f"🔧 Using device: {self.device}")
        
        # Quality presets with optimized settings
        self.quality_presets = {
            'ultra_fast': {
                'preset': 'ultra_fast',
                'num_autoregressive_samples': 1,
                'diffusion_iterations': 5,
                'temperature': 0.7,
                'description': 'Fastest generation (~30 seconds)',
                'quality_score': 6
            },
            'fast': {
                'preset': 'fast', 
                'num_autoregressive_samples': 16,
                'diffusion_iterations': 30,
                'temperature': 0.8,
                'description': 'Fast with decent quality (~2 minutes)',
                'quality_score': 7
            },
            'standard': {
                'preset': 'standard',
                'num_autoregressive_samples': 256,
                'diffusion_iterations': 100,
                'temperature': 0.8,
                'description': 'Good balance (~5 minutes)',
                'quality_score': 8
            },
            'high_quality': {
                'preset': 'high_quality',
                'num_autoregressive_samples': 512,
                'diffusion_iterations': 200,
                'temperature': 0.7,
                'description': 'Best quality (~10 minutes)',
                'quality_score': 9
            },
            'custom_optimized': {
                'preset': None,
                'num_autoregressive_samples': 128,
                'diffusion_iterations': 75,
                'temperature': 0.75,
                'repetition_penalty': 2.0,
                'length_penalty': 1.0,
                'description': 'Optimized balance of speed/quality (~3 minutes)',
                'quality_score': 8
            }
        }
    
    def _get_best_device(self):
        """Determine the best available device"""
        if torch.cuda.is_available():
            return 'cuda'
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            return 'mps'
        else:
            return 'cpu'
    
    def initialize_tts(self):
        """Initialize TTS model with optimizations"""
        if self.tts is None:
            print("🧠 Loading Tortoise TTS (optimized)...")
            
            # Use half precision on compatible devices for speed
            use_half = self.device in ['cuda', 'mps']
            
            self.tts = TextToSpeech(
                device=self.device,
                use_deepspeed=False,  # Disable for compatibility
                half=use_half,
                autoregressive_batch_size=1 if self.device == 'cpu' else 4
            )
            print("✅ Tortoise TTS loaded!")
    
    def list_quality_presets(self):
        """Display available quality presets"""
        print("\n🎯 Available Quality Presets:")
        print("-" * 60)
        
        for preset_name, settings in self.quality_presets.items():
            quality_bar = "★" * settings['quality_score'] + "☆" * (10 - settings['quality_score'])
            print(f"{preset_name:16} │ {quality_bar} │ {settings['description']}")
        
        print("-" * 60)
        print("💡 Recommendation: Use 'custom_optimized' for best speed/quality balance")
    
    def generate_speech(self, text, preset='custom_optimized', output_file=None):
        """Generate speech with improved settings"""
        
        if not output_file:
            safe_text = "".join(c for c in text[:25] if c.isalnum() or c in (' ', '_')).strip()
            safe_text = safe_text.replace(' ', '_')
            output_file = f"improved_{safe_text}_{preset}.wav"
        
        print(f"\n🎤 Generating speech with '{preset}' preset")
        print(f"📝 Text: '{text}'")
        print(f"🎯 Using voice model: {self.voice_name}")
        
        if preset not in self.quality_presets:
            print(f"❌ Unknown preset '{preset}'. Available: {list(self.quality_presets.keys())}")
            return None
        
        settings = self.quality_presets[preset]
        print(f"⚙️  Settings: {settings['description']}")
        
        self.initialize_tts()
        
        try:
            # Load voice samples
            print("📂 Loading voice samples...")
            voices_base_dir = os.path.join(os.path.expanduser("~"), ".cache", "tortoise", "voices")
            voice_samples, _ = load_voices([self.voice_name], extra_voice_dirs=[voices_base_dir])
            
            print("⏳ Generating speech... This may take a while on Intel Mac")
            start_time = time.time()
            
            # Generate with custom settings if available
            if settings['preset']:
                # Use built-in preset
                gen = self.tts.tts_with_preset(
                    text=text,
                    voice_samples=voice_samples,
                    preset=settings['preset']
                )
            else:
                # Use custom settings
                gen = self.tts.tts(
                    text=text,
                    voice_samples=voice_samples,
                    num_autoregressive_samples=settings['num_autoregressive_samples'],
                    diffusion_iterations=settings['diffusion_iterations'],
                    temperature=settings['temperature'],
                    repetition_penalty=settings.get('repetition_penalty', 2.0),
                    length_penalty=settings.get('length_penalty', 1.0)
                )
            
            # Save with better quality settings
            sample_rate = 24000
            torchaudio.save(
                output_file, 
                gen.squeeze(0).cpu(), 
                sample_rate,
                encoding="PCM_S",
                bits_per_sample=16
            )
            
            generation_time = time.time() - start_time
            
            print(f"\n🎉 Speech generation complete!")
            print(f"💾 Saved to: {output_file}")
            print(f"⏱️  Generation time: {generation_time:.1f} seconds")
            print(f"🔊 Play the file to hear your improved cloned voice!")
            
            return output_file
            
        except Exception as e:
            print(f"❌ Error generating speech: {e}")
            print("\nTroubleshooting:")
            print("1. Make sure voice files exist in ~/.cache/tortoise/voices/target_voice/")
            print("2. Try a faster preset if generation is too slow")
            print("3. Ensure sufficient memory available")
            return None

def main():
    if len(sys.argv) < 2:
        print("🚀 Voice Generation - High Quality TTS")
        print("=" * 40)
        print("\nUsage: python generate_voice.py \"Your text here\" [options]")
        print("\nOptions:")
        print("  --preset [ultra_fast|fast|standard|high_quality|custom_optimized]")
        print("  --output filename.wav")
        print("  --voice voice_name")
        print("  --list-presets")
        print("\nExamples:")
        print('  python generate_voice.py "Hello world!"')
        print('  python generate_voice.py "Hello!" --preset custom_optimized')
        print('  python generate_voice.py "Test" --preset ultra_fast --output test.wav')
        
        # Show available presets by default
        generator = ImprovedTortoiseGenerator()
        generator.list_quality_presets()
        return
    
    text = sys.argv[1]
    preset = 'custom_optimized'
    output_file = None
    voice_name = 'alex'
    
    # Parse arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--preset' and i + 1 < len(sys.argv):
            preset = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--output' and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--voice' and i + 1 < len(sys.argv):
            voice_name = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--list-presets':
            generator = ImprovedTortoiseGenerator()
            generator.list_quality_presets()
            return
        else:
            i += 1
    
    # Generate speech
    generator = ImprovedTortoiseGenerator(voice_name)
    result = generator.generate_speech(text, preset, output_file)
    
    if result:
        print(f"\n✅ Success! Generated: {result}")
    else:
        print("\n❌ Generation failed")

if __name__ == "__main__":
    main()