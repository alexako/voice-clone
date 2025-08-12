# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a voice cloning project using Tortoise TTS that allows training and generating speech with a cloned voice from audio samples. The project includes both legacy scripts and improved high-performance scripts with optimized quality presets.

## Virtual Environment Setup

This project uses a Python virtual environment located at `venv/`. To activate it:

```bash
source venv/bin/activate
```

Key dependencies include:
- `tortoise-tts` (3.0.0) - Main TTS engine 
- `torch` (2.2.2) + `torchaudio` (2.2.2) - Deep learning framework
- `librosa` (0.11.0) - Audio processing
- `numpy`, `scipy` - Numerical computing

## Core Scripts and Workflow

### 1. Training Pipeline (`train_voice.py`)
- Main training script that sets up voice cloning for the target voice
- Copies processed audio files from `audio_data/your_voice_processed/` to Tortoise's cache directory (`~/.cache/tortoise/voices/alex/`)  
- Performs initial voice generation test with "fast" preset
- Outputs: `test_output.wav`

### 2. Speech Generation Scripts

#### Original Scripts:
- `generate_speech.py` - Basic generation with standard presets
- `quick_test.py` - Simple test script for rapid validation

#### **Improved Scripts (Recommended):**
- **`generate_voice.py`** - Enhanced generation with optimized settings
  - 5 quality presets with performance ratings: `ultra_fast`, `fast`, `custom_optimized`, `standard`, `high_quality`
  - Better device optimization and memory management
  - Detailed timing and progress information
  - Usage: `python generate_voice.py "Text" --preset custom_optimized`

- **`batch_voice_generator.py`** - Batch processing and comparison tools
  - Generate multiple samples from text files
  - Quality comparison across different presets
  - Batch processing with progress tracking
  - Usage: `python batch_voice_generator.py create-samples` then `python batch_voice_generator.py batch sample_texts.txt`

### 3. Quality Presets and Performance

| Preset | Quality | Speed | CPU Time | Use Case |
|--------|---------|-------|----------|----------|
| `ultra_fast` | ★★★★★★☆☆☆☆ | Fastest | ~2-3 minutes | Quick testing |
| `fast` | ★★★★★★★☆☆☆ | Fast | ~3-5 minutes | Development |
| `custom_optimized` | ★★★★★★★★☆☆ | Balanced | ~3-4 minutes | **Recommended** |
| `standard` | ★★★★★★★★☆☆ | Moderate | ~5-7 minutes | Good quality |
| `high_quality` | ★★★★★★★★★☆ | Slow | ~8-12 minutes | Final output |

## Audio Data Structure

```
audio_data/
├── your_voice/           # Original voice samples
└── your_voice_processed/ # Processed samples ready for training
```

## Device Support and Performance

The scripts automatically detect and use available hardware:
- **CUDA** (NVIDIA GPU) - Best performance
- **MPS** (Apple Silicon) - Good performance on M1/M2 Macs  
- **CPU** - Slowest, especially on Intel Macs

Performance notes:
- Training and generation can be very slow on CPU-only systems
- Use faster presets (`ultra_fast`, `fast`) for development/testing
- Higher quality presets (`standard`, `high_quality`) for final output

## Common Development Tasks

```bash
# Activate virtual environment
source venv/bin/activate

# Train voice model (run once initially)
python train_voice.py

# RECOMMENDED: Use improved scripts for better quality and speed
# Show available presets
python generate_voice.py

# Quick test (ultra_fast preset)
python generate_voice.py "Hello world!" --preset ultra_fast

# Balanced quality/speed (recommended for most use)
python generate_voice.py "Your text here" --preset custom_optimized

# High quality output (slow but best results)
python generate_voice.py "Final speech" --preset high_quality

# Batch processing
python batch_voice_generator.py create-samples
python batch_voice_generator.py batch sample_texts.txt custom_optimized

# Compare quality presets
python batch_voice_generator.py compare "Test comparison"

# LEGACY: Original scripts (slower, less optimized)
python generate_speech.py "Hello world" --preset ultra_fast
python quick_test.py
```

## Voice Model Location

Trained voice data is stored at: `~/.cache/tortoise/voices/alex/`

This is where Tortoise TTS looks for custom voice samples. The training script automatically copies processed audio files here.

## Important Notes

### Dependencies and Compatibility
- **Transformers version**: Must use `transformers==4.31.0` (not newer versions)
- **XTTS-v2 installation**: Complex compilation issues on some systems. Tortoise TTS is more reliable.
- **Device optimization**: Scripts auto-detect best device (CUDA > MPS > CPU)

### Performance Tips
- **CPU-only systems**: Expect 2-10 minutes per generation depending on preset
- **Memory usage**: High-quality presets require more RAM
- **First run**: Model downloads may take time, be patient

### Alternative TTS Models Researched
- **XTTS-v2**: Superior quality but difficult installation on some systems
- **ElevenLabs**: Commercial option but requires API subscription  
- **Bark**: Open-source option but development has stalled
- **Tortoise TTS**: Most reliable for local setup, especially with improvements

## Error Handling and Troubleshooting

All scripts include comprehensive error handling with helpful troubleshooting suggestions:
- Audio file validation
- Hardware compatibility checks  
- Voice sample loading verification
- Clear error messages with actionable steps
- Progress tracking and timing information