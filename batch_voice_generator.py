#!/usr/bin/env python3
"""
Batch Voice Generation Script
Generate multiple speech samples efficiently with different settings
"""

import os
import sys
import json
import time
from pathlib import Path
from generate_voice import ImprovedTortoiseGenerator

class BatchVoiceGenerator:
    def __init__(self, voice_name="target_voice"):
        self.generator = ImprovedTortoiseGenerator(voice_name)
        self.batch_results = []
    
    def generate_batch_from_file(self, text_file, preset='custom_optimized', output_dir='batch_output'):
        """Generate speech for multiple texts from a file"""
        
        if not os.path.exists(text_file):
            print(f"❌ Text file not found: {text_file}")
            return []
        
        # Create output directory
        Path(output_dir).mkdir(exist_ok=True)
        
        # Read texts
        with open(text_file, 'r') as f:
            texts = [line.strip() for line in f if line.strip()]
        
        if not texts:
            print("❌ No text found in file")
            return []
        
        print(f"🎤 Generating {len(texts)} speech samples...")
        print(f"📁 Output directory: {output_dir}")
        print(f"⚙️  Using preset: {preset}")
        
        start_time = time.time()
        
        for i, text in enumerate(texts, 1):
            print(f"\n--- Processing {i}/{len(texts)} ---")
            
            # Generate filename
            safe_text = "".join(c for c in text[:20] if c.isalnum() or c in (' ', '_')).strip()
            safe_text = safe_text.replace(' ', '_')
            output_file = os.path.join(output_dir, f"{i:03d}_{safe_text}.wav")
            
            # Generate speech
            result = self.generator.generate_speech(text, preset, output_file)
            
            self.batch_results.append({
                'index': i,
                'text': text,
                'output_file': result,
                'success': result is not None
            })
            
            if result:
                print(f"✅ Generated: {result}")
            else:
                print(f"❌ Failed to generate speech for: {text[:50]}...")
        
        total_time = time.time() - start_time
        successful = sum(1 for r in self.batch_results if r['success'])
        
        print(f"\n📊 Batch Generation Complete!")
        print(f"✅ Successful: {successful}/{len(texts)}")
        print(f"⏱️  Total time: {total_time:.1f} seconds")
        print(f"⚡ Average per sample: {total_time/len(texts):.1f} seconds")
        
        return self.batch_results
    
    def generate_comparison_samples(self, text, output_dir='comparison_output'):
        """Generate the same text with different quality presets for comparison"""
        
        Path(output_dir).mkdir(exist_ok=True)
        
        presets_to_test = ['ultra_fast', 'fast', 'custom_optimized', 'standard']
        
        print(f"🎤 Generating comparison samples for: '{text}'")
        print(f"🔬 Testing presets: {', '.join(presets_to_test)}")
        
        results = {}
        
        for preset in presets_to_test:
            print(f"\n--- Testing preset: {preset} ---")
            
            output_file = os.path.join(output_dir, f"comparison_{preset}.wav")
            
            start_time = time.time()
            result = self.generator.generate_speech(text, preset, output_file)
            generation_time = time.time() - start_time
            
            results[preset] = {
                'file': result,
                'time': generation_time,
                'success': result is not None
            }
        
        # Print comparison summary
        print(f"\n📊 Comparison Results:")
        print("-" * 60)
        print(f"{'Preset':<16} │ {'Time (s)':<8} │ {'Status'}")
        print("-" * 60)
        
        for preset, data in results.items():
            status = "✅ Success" if data['success'] else "❌ Failed"
            time_str = f"{data['time']:.1f}" if data['success'] else "N/A"
            print(f"{preset:<16} │ {time_str:<8} │ {status}")
        
        print("-" * 60)
        print("🎧 Listen to each file to compare quality vs speed trade-offs")
        
        return results
    
    def create_sample_text_file(self, filename='sample_texts.txt'):
        """Create a sample text file for batch processing"""
        
        sample_texts = [
            "Hello, this is a test of my cloned voice using Tortoise TTS.",
            "The quick brown fox jumps over the lazy dog.",
            "I'm experimenting with different voice cloning technologies.",
            "This sentence tests how well the model handles longer phrases with multiple clauses.",
            "Short test.",
            "How are you doing today? I hope you're having a wonderful time!",
            "Voice cloning technology has advanced significantly in recent years.",
            "Let's see how this sounds with some technical terminology and acronyms like AI, ML, and TTS."
        ]
        
        with open(filename, 'w') as f:
            for text in sample_texts:
                f.write(text + '\n')
        
        print(f"📝 Created sample text file: {filename}")
        print(f"📄 Contains {len(sample_texts)} sample texts for batch processing")
        
        return filename

def main():
    if len(sys.argv) < 2:
        print("🚀 Batch Voice Generation Tool")
        print("=" * 35)
        print("\nModes:")
        print("  1. Batch from file:  python batch_voice_generator.py batch <text_file> [preset]")
        print("  2. Quality comparison: python batch_voice_generator.py compare \"Your text\"")
        print("  3. Create sample file: python batch_voice_generator.py create-samples")
        print("\nExamples:")
        print("  python batch_voice_generator.py create-samples")
        print("  python batch_voice_generator.py batch sample_texts.txt custom_optimized")
        print('  python batch_voice_generator.py compare "Hello world!"')
        
        return
    
    mode = sys.argv[1].lower()
    
    if mode == 'create-samples':
        generator = BatchVoiceGenerator()
        generator.create_sample_text_file()
        
    elif mode == 'batch':
        if len(sys.argv) < 3:
            print("❌ Please provide a text file for batch processing")
            return
        
        text_file = sys.argv[2]
        preset = sys.argv[3] if len(sys.argv) > 3 else 'custom_optimized'
        
        generator = BatchVoiceGenerator()
        results = generator.generate_batch_from_file(text_file, preset)
        
        # Save results summary
        with open('batch_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        print(f"📊 Results saved to: batch_results.json")
        
    elif mode == 'compare':
        if len(sys.argv) < 3:
            print("❌ Please provide text for comparison")
            return
        
        text = sys.argv[2]
        
        generator = BatchVoiceGenerator()
        results = generator.generate_comparison_samples(text)
        
        # Save comparison results
        with open('comparison_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"📊 Comparison results saved to: comparison_results.json")
        
    else:
        print(f"❌ Unknown mode: {mode}")
        print("Available modes: batch, compare, create-samples")

if __name__ == "__main__":
    main()