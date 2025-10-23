# Changelog

## Fixed: Image-Only Support (Latest)

### What Changed
- **Clarified**: Scripts only support **images** (PNG, JPG, WEBP, GIF, BMP, TIFF)
- **Removed**: All misleading PDF examples from documentation
- **Added**: Helpful error messages when trying to process PDFs
- **Created**: `pdf_to_ocr.py` - automated PDF conversion and OCR pipeline

### Files Updated
1. **ocr.py**
   - Added file format validation
   - Shows helpful error for PDFs with conversion instructions
   - Updated all examples to use images

2. **README.md**
   - Added prominent warning at top
   - Updated all examples to use images
   - Added PDF conversion guide (automated & manual)

3. **QUICKSTART.md**
   - Added PDF conversion section
   - Updated all examples to use images

4. **EXAMPLES.md**
   - Added warning at top
   - Updated 20+ examples to use images
   - Added complete PDF workflow section

5. **batch_ocr.py**
   - Removed PDF from supported formats
   - Updated documentation

6. **New: pdf_to_ocr.py**
   - Automated PDF → images → OCR pipeline
   - Converts all pages automatically
   - Creates individual and combined output files
   - Cleans up temporary files

### How to Use PDFs Now

#### Easy Way (Recommended)
```bash
# Install poppler once
brew install poppler

# Process any PDF
uv run pdf_to_ocr.py document.pdf
```

#### Your PDF Specifically
```bash
uv run pdf_to_ocr.py DeepSeek_OCR_paper.pdf --model granite
```

This will:
1. Convert PDF to high-quality images (300 DPI)
2. Process each page with OCR
3. Create individual markdown files for each page
4. Combine all pages into one file
5. Clean up temporary images

### Error Messages

Now when you try to process a PDF directly:
```bash
uv run ocr.py document.pdf
```

You'll see:
```
❌ Error: Unsupported file format: .pdf
📝 Supported formats: .bmp, .gif, .jpeg, .jpg, .png, .tiff, .webp

💡 Tip: PDFs are not directly supported by MLX-VLM.
    Convert your PDF to images first:
    brew install poppler
    pdftoppm -png your.pdf output
```

### Why Images Only?

MLX-VLM (the underlying framework) processes images through vision transformers. PDFs are document containers that need to be rendered into images first. This is a limitation of the framework, not the models themselves.

## Original Release

- Created ocr.py with 3 models (Granite, Nanonets, PaddleOCR)
- Created test.py for quick testing
- Created batch_ocr.py for batch processing
- Added comprehensive documentation
- Mac-optimized using MLX for Apple Silicon

