# OCR Model Comparison & Best Practices

Based on Hugging Face's OCR guide, here's a comprehensive comparison of available models and how to choose the right one.

## Available Models in This Project

### ✅ Currently Supported (MLX-optimized for Mac)

| Model | Size | Output Format | Best For | Languages |
|-------|------|---------------|----------|-----------|
| **Granite-Docling** | 258M | DocTags, Markdown | Fast processing, layout preservation | EN, JA, AR, ZH |
| **Nanonets-OCR2** | 3B | Markdown + HTML | Complex docs, signatures, watermarks | EN, ZH, FR, AR+ |
| **PaddleOCR-VL** | 0.9B | Markdown, JSON, HTML | Multilingual, handwriting, old docs | 109 languages |

### 🔜 Notable Models (Not Yet in MLX)

| Model | Size | Output Format | Best For | Languages |
|-------|------|---------------|----------|-----------|
| **DeepSeek-OCR** | 3B | Markdown + HTML | Charts→HTML, memory-efficient | ~100 languages |
| **OlmOCR** | 8B | Markdown, HTML, LaTeX | Batch processing, grounding | English only |
| **dots.ocr** | 3B | Markdown, JSON | Grounding, image extraction | Multilingual |

---

## Best Practices from Hugging Face

### 1. Choose Model Based on Output Format Needs

#### **Use DocTags/HTML** when:
- ✅ You need precise layout preservation
- ✅ Digital document reconstruction
- ✅ Multi-column layouts matter
- 📝 Example: Granite-Docling

#### **Use Markdown** when:
- ✅ Feeding output to LLMs
- ✅ Human-readable format needed
- ✅ Simple document structure
- 📝 Example: Nanonets, PaddleOCR

#### **Use JSON** when:
- ✅ Programmatic data extraction
- ✅ Structured data analysis
- ✅ Chart/table data needed
- 📝 Example: PaddleOCR (for charts)

### 2. Model Selection by Use Case

#### **Multilingual Documents** (100+ languages)
```bash
uv run ocr.py document.png --model paddleocr
```
- **Best:** PaddleOCR-VL (109 languages)
- **Future:** DeepSeek-OCR (~100 languages)

#### **Complex Layouts** (multi-column, tables, charts)
```bash
uv run ocr.py complex-doc.png --model nanonets
```
- **Best:** Nanonets (captions, signatures, watermarks)
- **Alternative:** Granite (with location tokens)

#### **Handwritten Text**
```bash
uv run ocr.py handwriting.jpg --model paddleocr
```
- **Best:** PaddleOCR-VL
- **Alternative:** Nanonets

#### **Mathematical Equations**
```bash
uv run ocr.py math-paper.png --prompt "Convert all equations to LaTeX"
```
- **Best:** Granite (with LaTeX prompt)
- **Future:** OlmOCR (specialized for LaTeX)

#### **Fast Batch Processing**
```bash
uv run batch_ocr.py ./documents/ --model granite
```
- **Best:** Granite (258M, very fast)
- **Future:** OlmOCR (optimized for batch)

#### **Charts & Tables to HTML**
```bash
uv run ocr.py chart.png --prompt "Convert this chart to HTML table"
```
- **Best:** Nanonets (HTML tables)
- **Future:** DeepSeek-OCR (specialized for charts→HTML)

### 3. Prompt Engineering Best Practices

#### **Task-Specific Prompts**
```bash
# Extract only tables
uv run ocr.py doc.png --prompt "Extract all tables as markdown. Ignore other text."

# Focus on specific elements
uv run ocr.py page.png --prompt "Extract: invoice number, date, total amount as JSON"

# Format conversion
uv run ocr.py formula.png --prompt "Convert all mathematical formulas to LaTeX"
```

#### **Model-Specific Prompting**

**Granite** (supports task switching):
- "Convert this page to Docling"
- "Convert this formula to LaTeX"
- "Extract table structure with locations"

**Nanonets** (semantic understanding):
- "Extract text naturally with proper reading order"
- "Return tables in HTML, equations in LaTeX"
- "Identify checkboxes, signatures, and watermarks"

**PaddleOCR** (general OCR):
- "Extract all text preserving layout"
- "Convert tables and charts to HTML"

### 4. Locality Awareness (Grounding)

Models with **grounding** preserve spatial information:
- ✅ **Granite**: Provides `<loc_X><loc_Y>` coordinates
- ✅ **OlmOCR**: Bounding box metadata
- ✅ **dots.ocr**: Coordinate extraction

**Why it matters:**
- Preserves reading order in multi-column layouts
- Reduces hallucination
- Enables document reconstruction

### 5. Cost-Efficiency Considerations

| Model | Params | Speed | Memory | Best For |
|-------|--------|-------|--------|----------|
| **Granite** | 258M | ⚡⚡⚡ | ~1.4GB | High-volume, fast turnaround |
| **PaddleOCR** | 0.9B | ⚡⚡⚡ | ~2GB | Multilingual, budget-friendly |
| **Nanonets** | 3B | ⚡⚡ | ~4GB | Quality over speed |
| **DeepSeek** | 3B | ⚡⚡ | ~3GB | Memory-efficient for 3B |

**On Mac M-series:**
- **M1/M2 (8GB)**: Use Granite or PaddleOCR
- **M1/M2 Pro (16GB+)**: Can use Nanonets
- **M3 Max (32GB+)**: All models comfortable

### 6. Benchmarking Your Domain

The guide recommends creating domain-specific test sets:

```bash
# Test multiple models on your data
uv run ocr.py your-test-1.png --model granite --output test1-granite.md
uv run ocr.py your-test-1.png --model nanonets --output test1-nanonets.md
uv run ocr.py your-test-1.png --model paddleocr --output test1-paddleocr.md

# Compare results manually
diff test1-granite.md test1-nanonets.md
```

**Standard Benchmarks:**
- **OmniDocBenchmark**: Books, magazines, textbooks
- **OlmOCR-Bench**: English-focused unit tests
- **CC-OCR**: Multilingual evaluation

---

## Model Roadmap

### Potentially Coming to MLX

Models that would be great additions:

1. **DeepSeek-OCR** 
   - 3B params, ~100 languages
   - Specialized for charts→HTML conversion
   - Memory-efficient architecture

2. **OlmOCR**
   - 8B params, English only
   - Optimized for batch processing
   - Excellent grounding capabilities

3. **dots.ocr**
   - 3B params, multilingual
   - Strong image extraction
   - Grounding support

### How to Request MLX Conversion

If you need a model in MLX format:
1. Check https://huggingface.co/mlx-community
2. Request conversion via Hugging Face forums
3. Convert yourself using `mlx-vlm` conversion tools

---

## Quick Decision Tree

```
Need multilingual (50+ languages)?
  → Use PaddleOCR-VL

Need fastest processing?
  → Use Granite

Need complex layout handling?
  → Use Nanonets

Need layout coordinates?
  → Use Granite (with DocTags)

Need handwriting support?
  → Use PaddleOCR-VL

Need LaTeX equations?
  → Use Granite (with LaTeX prompt)

Processing 1000s of pages?
  → Use Granite (fastest) or batch with PaddleOCR
```

---

## Example: Choosing the Right Model

### Scenario 1: Legal Contract (English, Multi-column)
```bash
uv run ocr.py contract.png --model nanonets --max-tokens 8000
```
**Why:** Complex layout, signatures, need HTML output

### Scenario 2: Chinese Restaurant Menu
```bash
uv run ocr.py menu.jpg --model paddleocr
```
**Why:** Chinese text, 109 language support

### Scenario 3: Research Paper with Math
```bash
uv run ocr.py paper-page.png --model granite \
  --prompt "Extract text and convert equations to LaTeX"
```
**Why:** Fast, supports LaTeX, good for academic content

### Scenario 4: Old Handwritten Document
```bash
uv run ocr.py old-letter.jpg --model paddleocr --max-tokens 4096
```
**Why:** Handles handwriting and old documents well

---

## Performance Tips

1. **First Run**: Models download automatically (600MB-3GB)
2. **Quantization**: All MLX models are pre-quantized for efficiency
3. **Batch Processing**: Use `batch_ocr.py` for multiple files
4. **Temperature**: Keep at 0.0 for deterministic output
5. **Max Tokens**: Adjust based on document length:
   - Single page: 4096 (default)
   - Dense page: 8000-12000
   - Multiple columns: 12000+

---

## Further Reading

- [Hugging Face OCR Guide](https://huggingface.co/blog/ocr-models)
- [Vision Language Models Explained](https://huggingface.co/blog/vlms)
- [MLX-VLM Documentation](https://github.com/Blaizzy/mlx-vlm)
- [Model Cards on Hugging Face Hub](https://huggingface.co/models?pipeline_tag=image-to-text)

