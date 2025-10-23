# OCR Examples

Real-world examples of using the OCR scripts for common tasks.

## Basic Document Processing

### Extract text from a scanned PDF
```bash
uv run ocr.py scanned_document.pdf --output text_output.txt
```

### Process a photo of a receipt
```bash
uv run ocr.py receipt.jpg --model nanonets --output receipt.md
```

### Multilingual document (109 languages)
```bash
uv run ocr.py chinese_doc.pdf --model paddleocr
```

## Advanced Prompting

### Extract only tables
```bash
uv run ocr.py financial_report.pdf \
  --prompt "Extract all tables from this document in markdown format. Ignore other text." \
  --output tables.md
```

### Convert math equations
```bash
uv run ocr.py math_homework.pdf \
  --prompt "Extract all mathematical equations and convert them to LaTeX format." \
  --output equations.tex
```

### Extract structured data
```bash
uv run ocr.py invoice.pdf \
  --prompt "Extract: invoice number, date, total amount, and line items as JSON." \
  --output invoice.json
```

### Chart to data
```bash
uv run ocr.py sales_chart.png \
  --prompt "Convert this chart to a JSON object with all data points." \
  --output chart_data.json
```

## Batch Processing

### Process all PDFs in a directory
```bash
uv run batch_ocr.py ./documents/
```

### Process with specific model
```bash
uv run batch_ocr.py ./invoices/ \
  --model nanonets \
  --output-dir ./processed_invoices/
```

### Process only PNG files
```bash
uv run batch_ocr.py ./scans/ \
  --pattern "*.png" \
  --output-dir ./results/
```

## Shell Scripting Integration

### Process and rename files
```bash
for file in documents/*.pdf; do
    output="processed/$(basename "$file" .pdf)_ocr.md"
    uv run ocr.py "$file" --output "$output"
    echo "Processed: $file -> $output"
done
```

### Compare models
```bash
#!/bin/bash
# Compare output from different models

IMAGE="test_document.pdf"

echo "Testing Granite (fast)..."
uv run ocr.py "$IMAGE" --model granite --output granite_result.txt

echo "Testing Nanonets (accurate)..."
uv run ocr.py "$IMAGE" --model nanonets --output nanonets_result.txt

echo "Testing PaddleOCR (multilingual)..."
uv run ocr.py "$IMAGE" --model paddleocr --output paddleocr_result.txt

echo "Done! Check *_result.txt files"
```

### Extract and search
```bash
# Extract text and search for keywords
uv run ocr.py document.pdf --output temp.txt
grep -i "invoice" temp.txt
```

## Use Cases by Document Type

### Legal Documents
```bash
uv run ocr.py contract.pdf \
  --model nanonets \
  --max-tokens 8000 \
  --output contract.md
```
*Nanonets handles complex multi-column layouts well*

### Handwritten Notes
```bash
uv run ocr.py notes.jpg \
  --model paddleocr \
  --output notes.txt
```
*PaddleOCR trained on handwriting*

### Technical Papers with Math
```bash
uv run ocr.py research_paper.pdf \
  --model granite \
  --prompt "Extract all text, convert equations to LaTeX, and preserve section structure" \
  --max-tokens 8000 \
  --output paper.md
```

### Receipts and Invoices
```bash
uv run ocr.py receipt.jpg \
  --model nanonets \
  --prompt "Extract merchant name, date, items, prices, and total as structured text" \
  --output receipt.txt
```

### Foreign Language Documents
```bash
# Arabic document
uv run ocr.py arabic_doc.pdf --model paddleocr

# Japanese document  
uv run ocr.py japanese_doc.pdf --model granite

# Mixed languages
uv run ocr.py multilingual.pdf --model paddleocr
```

## Automation Examples

### Watch folder for new documents
```bash
#!/bin/bash
# Simple watch script

WATCH_DIR="./inbox/"
OUTPUT_DIR="./processed/"

while true; do
    for file in "$WATCH_DIR"*.{pdf,png,jpg}; do
        if [ -f "$file" ]; then
            echo "Processing: $file"
            uv run ocr.py "$file" \
              --output "$OUTPUT_DIR/$(basename "$file").txt"
            mv "$file" "$OUTPUT_DIR/originals/"
        fi
    done
    sleep 5
done
```

### Process with error handling
```bash
#!/bin/bash

process_with_retry() {
    local file=$1
    local max_attempts=3
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        echo "Attempt $attempt: $file"
        
        if uv run ocr.py "$file" --output "${file}.txt"; then
            echo "✅ Success"
            return 0
        fi
        
        attempt=$((attempt + 1))
        sleep 2
    done
    
    echo "❌ Failed after $max_attempts attempts"
    return 1
}

for doc in documents/*.pdf; do
    process_with_retry "$doc"
done
```

## Tips & Tricks

### Faster processing
```bash
# Use Granite for speed
uv run ocr.py document.pdf --model granite
```

### Better accuracy
```bash
# Use Nanonets for quality
uv run ocr.py complex_doc.pdf --model nanonets --max-tokens 8000
```

### Save intermediate results
```bash
# Process and keep both formats
uv run ocr.py doc.pdf --output result.txt
cat result.txt  # View in terminal
```

### Chain with other tools
```bash
# OCR + grep + process
uv run ocr.py invoice.pdf --output - | grep "Total:" | awk '{print $2}'

# OCR + convert to another format
uv run ocr.py doc.pdf --output doc.md
pandoc doc.md -o doc.html
```

## Performance Notes

- **Granite**: ~675 tokens/sec (prompt), ~175 tokens/sec (generation)
- **First run**: Slower due to model download (~600MB-3GB)
- **Cached runs**: Much faster, model loaded from disk
- **Memory**: ~1.4GB peak for Granite

Enjoy your OCR processing! 🚀

