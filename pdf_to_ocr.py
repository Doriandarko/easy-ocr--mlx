#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///

"""
PDF to OCR - Complete Pipeline
Converts PDF to images and runs OCR on all pages

Usage:
    uv run pdf_to_ocr.py <pdf_file> [--model MODEL] [--output-dir OUTPUT]

Examples:
    uv run pdf_to_ocr.py document.pdf
    uv run pdf_to_ocr.py paper.pdf --model nanonets --output-dir ./results/
"""

import argparse
import subprocess
import sys
from pathlib import Path
import shutil


def check_poppler():
    """Check if poppler is installed"""
    if not shutil.which("pdftoppm"):
        print("❌ Error: poppler not installed", file=sys.stderr)
        print("\n💡 Install it with:", file=sys.stderr)
        print("   brew install poppler", file=sys.stderr)
        sys.exit(1)


def convert_pdf_to_images(pdf_path, output_dir):
    """Convert PDF to PNG images"""
    print(f"📄 Converting PDF: {pdf_path.name}")
    
    # Create temp directory for images
    temp_dir = output_dir / "temp_pages"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Convert PDF to images
    base_name = temp_dir / pdf_path.stem
    
    try:
        result = subprocess.run(
            ["pdftoppm", "-png", "-r", "300", str(pdf_path), str(base_name)],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Find all generated images
        images = sorted(temp_dir.glob(f"{pdf_path.stem}-*.png"))
        
        if not images:
            print("❌ Error: No images generated from PDF", file=sys.stderr)
            sys.exit(1)
        
        print(f"✅ Converted to {len(images)} pages")
        return images
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error converting PDF: {e}", file=sys.stderr)
        sys.exit(1)


def process_images(images, model, output_dir):
    """Run OCR on all images"""
    print(f"\n🚀 Processing {len(images)} pages with {model} model...")
    print("=" * 60)
    
    results = []
    
    for i, image in enumerate(images, 1):
        page_num = image.stem.split('-')[-1]
        output_file = output_dir / f"page_{page_num}.md"
        
        print(f"📄 Page {i}/{len(images)}: {image.name}")
        
        try:
            subprocess.run(
                ["uv", "run", "ocr.py", str(image), "--model", model, "--output", str(output_file)],
                capture_output=True,
                text=True,
                check=True
            )
            
            results.append((page_num, output_file))
            print(f"   ✅ Saved to {output_file.name}")
            
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed: {e}", file=sys.stderr)
    
    return results


def create_combined_output(results, output_dir, pdf_name):
    """Combine all pages into one file"""
    combined_file = output_dir / f"{pdf_name}_complete.md"
    
    print(f"\n📝 Creating combined output: {combined_file.name}")
    
    with open(combined_file, 'w', encoding='utf-8') as outfile:
        outfile.write(f"# OCR Results: {pdf_name}\n\n")
        outfile.write(f"Total Pages: {len(results)}\n\n")
        outfile.write("=" * 60 + "\n\n")
        
        for page_num, result_file in results:
            outfile.write(f"## Page {page_num}\n\n")
            
            if result_file.exists():
                content = result_file.read_text(encoding='utf-8')
                outfile.write(content)
                outfile.write("\n\n" + "=" * 60 + "\n\n")
    
    print(f"✅ Combined file created: {combined_file}")
    return combined_file


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF to images and run OCR on all pages",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "pdf_file",
        type=str,
        help="Path to PDF file"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default="granite",
        choices=["granite", "nanonets", "paddleocr"],
        help="OCR model to use (default: granite)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Output directory (default: <pdf_name>_ocr/)"
    )
    
    parser.add_argument(
        "--keep-images",
        action="store_true",
        help="Keep temporary PNG images"
    )
    
    args = parser.parse_args()
    
    # Check dependencies
    check_poppler()
    
    # Verify PDF exists
    pdf_path = Path(args.pdf_file)
    if not pdf_path.exists():
        print(f"❌ Error: PDF not found: {args.pdf_file}", file=sys.stderr)
        sys.exit(1)
    
    if pdf_path.suffix.lower() != '.pdf':
        print(f"❌ Error: Not a PDF file: {args.pdf_file}", file=sys.stderr)
        sys.exit(1)
    
    # Setup output directory
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = Path(f"{pdf_path.stem}_ocr")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("🎯 PDF to OCR Pipeline")
    print("=" * 60)
    print(f"📁 PDF: {pdf_path.name}")
    print(f"🤖 Model: {args.model}")
    print(f"📁 Output: {output_dir}")
    print("=" * 60)
    print()
    
    # Convert PDF to images
    images = convert_pdf_to_images(pdf_path, output_dir)
    
    # Process all images
    results = process_images(images, args.model, output_dir)
    
    # Create combined output
    combined_file = create_combined_output(results, output_dir, pdf_path.stem)
    
    # Cleanup temp images
    if not args.keep_images:
        temp_dir = output_dir / "temp_pages"
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
            print(f"🧹 Cleaned up temporary images")
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 Processing Complete!")
    print(f"✅ Processed: {len(results)} pages")
    print(f"📄 Individual pages: {output_dir}/page_*.md")
    print(f"📚 Combined file: {combined_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()

