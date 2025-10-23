#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///

"""
Batch OCR Processing Script
Processes multiple images in a directory (PNG, JPG, WEBP, GIF, BMP, TIFF)
Note: PDFs not supported - convert them to images first

Usage:
    uv run batch_ocr.py <input_directory> [--output-dir OUTPUT] [--model MODEL] [--pattern PATTERN]

Examples:
    uv run batch_ocr.py ./documents/
    uv run batch_ocr.py ./invoices/ --output-dir ./results/ --model nanonets
    uv run batch_ocr.py ./scans/ --pattern "*.png" --model granite
"""

import argparse
import subprocess
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


def process_file(input_file, output_dir, model, max_tokens):
    """Process a single file with OCR"""
    output_file = output_dir / f"{input_file.stem}_ocr.txt"
    
    try:
        print(f"📄 Processing: {input_file.name}")
        
        cmd = [
            "uv", "run", "ocr.py",
            str(input_file),
            "--model", model,
            "--max-tokens", str(max_tokens),
            "--output", str(output_file)
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        print(f"✅ Completed: {input_file.name} -> {output_file.name}")
        return True, input_file.name
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {input_file.name} - {e}", file=sys.stderr)
        return False, input_file.name


def main():
    parser = argparse.ArgumentParser(
        description="Batch OCR processing for multiple files",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "input_dir",
        type=str,
        help="Directory containing images to process (PNG, JPG, WEBP, etc.)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Output directory (default: <input_dir>_ocr_results)"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default="granite",
        choices=["granite", "nanonets", "paddleocr"],
        help="Model to use (default: granite)"
    )
    
    parser.add_argument(
        "--pattern",
        type=str,
        default="*.*",
        help="File pattern to match (default: *.*)"
    )
    
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=4096,
        help="Maximum tokens per file (default: 4096)"
    )
    
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of parallel workers (default: 1, recommended for MLX)"
    )
    
    args = parser.parse_args()
    
    # Setup directories
    input_dir = Path(args.input_dir)
    if not input_dir.exists() or not input_dir.is_dir():
        print(f"❌ Error: Directory not found: {args.input_dir}", file=sys.stderr)
        sys.exit(1)
    
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = input_dir.parent / f"{input_dir.name}_ocr_results"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all matching files (images only, no PDFs)
    image_extensions = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.tiff', '.tif', '.bmp'}
    
    if args.pattern == "*.*":
        files = [f for f in input_dir.iterdir() if f.suffix.lower() in image_extensions]
    else:
        files = list(input_dir.glob(args.pattern))
        files = [f for f in files if f.suffix.lower() in image_extensions]
    
    if not files:
        print(f"❌ No files found matching pattern: {args.pattern}", file=sys.stderr)
        sys.exit(1)
    
    print("🚀 Batch OCR Processing")
    print("=" * 60)
    print(f"📁 Input directory: {input_dir}")
    print(f"📁 Output directory: {output_dir}")
    print(f"🤖 Model: {args.model}")
    print(f"📊 Files to process: {len(files)}")
    print(f"👷 Workers: {args.workers}")
    print("=" * 60)
    
    # Process files
    successful = 0
    failed = 0
    
    if args.workers == 1:
        # Sequential processing
        for file in files:
            success, filename = process_file(file, output_dir, args.model, args.max_tokens)
            if success:
                successful += 1
            else:
                failed += 1
    else:
        # Parallel processing (use with caution on Mac)
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(process_file, file, output_dir, args.model, args.max_tokens): file
                for file in files
            }
            
            for future in as_completed(futures):
                success, filename = future.result()
                if success:
                    successful += 1
                else:
                    failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Processing Complete!")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Results saved to: {output_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()

