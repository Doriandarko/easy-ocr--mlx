#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = [
#   "mlx-vlm>=0.0.9",
#   "pillow>=10.0.0",
#   "huggingface-hub>=0.20.0",
# ]
# ///

"""
OCR Script for Mac (Apple Silicon Optimized)
Supports: PNG, JPG, JPEG, WEBP, GIF, BMP, TIFF (Images only - PDFs not supported)

Usage:
    uv run ocr.py <image_path> [--model MODEL_NAME] [--prompt CUSTOM_PROMPT] [--max-tokens MAX]
    
Examples:
    uv run ocr.py document.png
    uv run ocr.py invoice.jpg --model granite
    uv run ocr.py chart.png --prompt "Convert this chart to JSON"
"""

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="OCR script optimized for Mac using MLX",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available Models:
  granite    - IBM Granite Docling (258M) - Fast, outputs DocTags
  nanonets   - Nanonets OCR2 (3B) - Semantic tagging, captions
  paddleocr  - PaddleOCR-VL (0.9B) - 109 languages, ultra-fast
  
Examples:
  uv run ocr.py document.png
  uv run ocr.py invoice.jpg --model granite
  uv run ocr.py chart.png --prompt "Convert this chart to JSON" --model granite
  uv run ocr.py scan.png --max-tokens 8000
  
Note: PDFs not supported. Convert PDFs to images first:
  brew install poppler
  pdftoppm -png document.pdf page
        """
    )
    
    parser.add_argument(
        "image",
        type=str,
        help="Path to image file (PNG, JPG, WEBP, GIF, BMP, TIFF)"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default="granite",
        choices=["granite", "nanonets", "paddleocr"],
        help="Model to use (default: granite)"
    )
    
    parser.add_argument(
        "--prompt",
        type=str,
        default=None,
        help="Custom prompt (default: extract all text naturally)"
    )
    
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=4096,
        help="Maximum tokens to generate (default: 4096)"
    )
    
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Sampling temperature (default: 0.0)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Save output to file instead of printing"
    )
    
    args = parser.parse_args()
    
    # Verify image exists and is a supported format
    image_path = Path(args.image)
    if not image_path.exists():
        print(f"❌ Error: Image file not found: {args.image}", file=sys.stderr)
        sys.exit(1)
    
    # Check file extension
    supported_formats = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.tiff', '.tif'}
    if image_path.suffix.lower() not in supported_formats:
        print(f"❌ Error: Unsupported file format: {image_path.suffix}", file=sys.stderr)
        print(f"📝 Supported formats: {', '.join(sorted(supported_formats))}", file=sys.stderr)
        if image_path.suffix.lower() == '.pdf':
            print(f"\n💡 Tip: PDFs are not directly supported by MLX-VLM.", file=sys.stderr)
            print(f"    Convert your PDF to images first:", file=sys.stderr)
            print(f"    brew install poppler", file=sys.stderr)
            print(f"    pdftoppm -png your.pdf output", file=sys.stderr)
        sys.exit(1)
    
    # Model mapping
    MODEL_MAP = {
        "granite": "ibm-granite/granite-docling-258M-mlx",
        "nanonets": "nanonets/Nanonets-OCR2-3B-mlx",
        "paddleocr": "PaddlePaddle/PaddleOCR-VL-0.9B-mlx",
    }
    
    # Default prompts per model
    # Note: <image> token is required for MLX-VLM
    DEFAULT_PROMPTS = {
        "granite": "<image>\nConvert this page to markdown format.",
        "nanonets": """<image>
Extract the text from the above document as if you were reading it naturally. 
Return tables in HTML format. Return equations in LaTeX. 
If there's an image without a caption, add a description inside <img></img> tags.
Use ☐ and ☑ for checkboxes.""",
        "paddleocr": "<image>\nExtract all text from this document preserving the layout and structure.",
    }
    
    model_id = MODEL_MAP[args.model]
    prompt = args.prompt if args.prompt else DEFAULT_PROMPTS[args.model]
    
    # Ensure prompt has <image> token (required for MLX-VLM)
    if "<image>" not in prompt:
        prompt = f"<image>\n{prompt}"
    
    print(f"🚀 Loading model: {args.model} ({model_id})")
    print(f"📄 Processing: {args.image}")
    print(f"💭 Prompt: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")
    print("=" * 60)
    
    try:
        import subprocess
        import json
        
        # Use MLX-VLM's command-line interface which is more stable
        # Remove <image> token from prompt for CLI (it handles it automatically)
        cli_prompt = prompt.replace("<image>", "").replace("\n\n", "\n").strip()
        
        cmd = [
            sys.executable, "-m", "mlx_vlm.generate",
            "--model", model_id,
            "--max-tokens", str(args.max_tokens),
            "--temperature", str(args.temperature),
            "--prompt", cli_prompt,
            "--image", str(image_path),
        ]
        
        # Run the command
        result_process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        # Extract the output and clean it up
        output = result_process.stdout
        
        # Parse the output - the actual OCR text is between the ========== markers
        if "==========" in output:
            parts = output.split("==========")
            if len(parts) >= 3:
                # The generated text is in the middle section
                result = parts[1].strip()
                # Remove the prompt echo and extract only the assistant's response
                if "<|start_of_role|>assistant<|end_of_role|>" in result:
                    result = result.split("<|start_of_role|>assistant<|end_of_role|>")[1].strip()
                # Remove trailing stats section if present
                if "Prompt:" in result:
                    result = result.split("\nPrompt:")[0].strip()
            else:
                result = output.strip()
        else:
            result = output.strip()
        
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(result, encoding="utf-8")
            print(f"\n✅ Output saved to: {args.output}")
            print(f"📊 Length: {len(result)} characters")
        else:
            print("\n" + "=" * 60)
            print("📝 OCR OUTPUT:")
            print("=" * 60)
            print(result)
            print("=" * 60)
            print(f"📊 Length: {len(result)} characters")
        
    except ImportError as e:
        print(f"\n❌ Error: Missing dependencies. This shouldn't happen with uv.", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during OCR processing: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

