# OCR on Mac (Apple Silicon Optimized)

This script uses MLX to run state-of-the-art OCR models directly on your Mac with optimal performance.

**⚠️ Images Only**: Supports PNG, JPG, WEBP, GIF, BMP, TIFF  
**📄 For PDFs**: Use `pdf_to_ocr.py` (see below) or convert manually with `poppler`

## Quick Start

### Process Images
```bash
uv run ocr.py your-image.png
```

### Process PDFs (automated)
```bash
# Install poppler once
brew install poppler

# Convert and process PDF in one command
uv run pdf_to_ocr.py your-document.pdf
```

The scripts automatically download dependencies on first run.

## Usage Examples

### Basic OCR (default: Granite model)
```bash
uv run ocr.py document.png
```

### Use different models
```bash
# Fast and tiny (258M params)
uv run ocr.py document.png --model granite

# Best quality (3B params) 
uv run ocr.py invoice.jpg --model nanonets

# Multilingual (109 languages, 0.9B params)
uv run ocr.py scan.png --model paddleocr
```

### Custom prompts
```bash
# Extract as JSON
uv run ocr.py chart.png --prompt "Convert this chart to JSON format"

# Focus on tables
uv run ocr.py invoice.jpg --prompt "Extract all tables as markdown"

# LaTeX extraction
uv run ocr.py math.png --prompt "Convert all equations to LaTeX"
```

### Save to file
```bash
uv run ocr.py document.png --output result.md
```

### Advanced options
```bash
uv run ocr.py long-scan.png --max-tokens 8000 --temperature 0.0
```

## Available Models

| Model | Size | Best For | Languages |
|-------|------|----------|-----------|
| **granite** | 258M | Fast processing, DocTags format | English, Japanese, Arabic, Chinese |
| **nanonets** | 3B | Highest quality, captions, signatures | English, Chinese, French, Arabic, more |
| **paddleocr** | 0.9B | Multilingual documents | 109 languages |

📚 **See [MODELS.md](MODELS.md)** for detailed comparison, best practices from Hugging Face, and how to choose the right model.

**Note**: DeepSeek-OCR, OlmOCR, and dots.ocr are mentioned in the guide but not yet available in MLX format.

## Model Features

### Granite (Default)
- Lightning fast on Mac
- Prompt-based task switching
- Great for batch processing
- Outputs DocTags/Markdown

### Nanonets
- Generates image captions
- Extracts signatures & watermarks
- Handles checkboxes and flowcharts
- Best for complex documents

### PaddleOCR
- Supports 109 languages
- Handles handwriting
- Processes old/low-quality docs
- Ultra-efficient (0.9B params)

## Supported File Types

**Images Only**: `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`, `.bmp`, `.tiff`

**⚠️ PDFs are NOT directly supported** by MLX-VLM.

### Option 1: Automated (Recommended)
```bash
# Install poppler once
brew install poppler

# Use the PDF helper script
uv run pdf_to_ocr.py document.pdf

# With options
uv run pdf_to_ocr.py paper.pdf --model nanonets --output-dir ./results/
```

This creates:
- Individual markdown files for each page
- A combined file with all pages
- Automatic cleanup of temporary images

### Option 2: Manual Conversion
```bash
# Convert PDF to images
pdftoppm -png document.pdf output

# This creates: output-1.png, output-2.png, etc.

# Process each page
uv run ocr.py output-1.png --output page1.md
```

## Tips

1. **First run**: Models download automatically (~500MB-3GB depending on model)
2. **Speed**: Granite is fastest, Nanonets is most accurate
3. **Languages**: Use PaddleOCR for non-English documents
4. **Complex layouts**: Nanonets handles multi-column and charts best
5. **Batch processing**: Run in a loop or use shell scripting

## Troubleshooting

### "Model not found"
The model will download on first use (~500MB-3GB). Ensure you have internet connection.

### "Out of memory"
Try the smaller granite model (258M) or reduce `--max-tokens`.

### "Slow performance"
- Ensure you're on Apple Silicon (M1/M2/M3/M4). MLX only works on these chips.
- First generation is slower as it loads the model into memory.
- Subsequent runs on the same file are much faster.

### Models already downloaded?
Models are cached in `~/.cache/huggingface/`. Delete this directory to re-download.

## Examples

```bash
# Process multiple files
for file in documents/*.pdf; do
    uv run ocr.py "$file" --output "output/$(basename "$file" .pdf).md"
done

# Compare models
uv run ocr.py test.png --model granite --output granite.md
uv run ocr.py test.png --model nanonets --output nanonets.md
```

## Requirements

- Mac with Apple Silicon (M1/M2/M3/M4)
- macOS 13.5 or later
- `uv` package manager ([install here](https://docs.astral.sh/uv/))

That's it! The script handles everything else automatically.

