# Quick Start Guide

## 1. Install UV (if you haven't already)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 2. Test the OCR Script

Run the test script which downloads a sample image and processes it:

```bash
uv run test.py
```

**First run**: This will take a few minutes to download the model (~630MB for Granite).

## 3. Use Your Own Images

```bash
# Basic usage
uv run ocr.py /path/to/your/document.pdf

# Save to file
uv run ocr.py /path/to/your/document.pdf --output result.md

# Try different models
uv run ocr.py document.png --model nanonets
uv run ocr.py document.png --model paddleocr
```

## Understanding the Output

### Granite (Default)
Outputs DocTags format with location information:
```xml
<doctag>
  <text><loc_15><loc_87>Invoice Number: 12345</text>
  <text><loc_15><loc_120>Date: 2025-01-15</text>
</doctag>
```

This format preserves:
- Exact text location (coordinates)
- Reading order
- Document structure

### Custom Prompts

Extract specific information:

```bash
# Extract tables only
uv run ocr.py invoice.pdf --prompt "Extract all tables as markdown"

# Convert math to LaTeX
uv run ocr.py math-paper.pdf --prompt "Convert all mathematical equations to LaTeX"

# Get JSON structure
uv run ocr.py chart.png --prompt "Convert this chart to JSON format"
```

## What's Happening Under the Hood?

1. **First Run**: UV automatically:
   - Creates a Python environment
   - Installs MLX-VLM and dependencies
   - Downloads the selected model from Hugging Face

2. **Model Loading**: MLX loads the model into your Mac's unified memory

3. **OCR Processing**: The model processes your image and generates structured output

4. **Output**: Results are displayed or saved to a file

## Performance Tips

- **Granite** (258M): ~175 tokens/sec - Best for batch processing
- **Nanonets** (3B): Slower but more accurate - Best for complex documents
- **PaddleOCR** (0.9B): Good balance - Best for multilingual

## Next Steps

- See `README.md` for detailed documentation
- Try different models and compare results
- Adjust `--max-tokens` for longer documents (default: 4096)
- Use `--temperature 0.0` for consistent output (default)

## Need Help?

Check the main README.md or look at the examples in the test.py script!

