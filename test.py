#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = [
#   "requests>=2.31.0",
# ]
# ///

"""
Quick test script - downloads a sample document and runs OCR on it
Usage: uv run test.py
"""

import subprocess
import sys
from pathlib import Path
import requests


def download_sample_image():
    """Download a sample document image for testing"""
    print("📥 Downloading sample document...")
    
    # Sample document from HuggingFace
    url = "https://huggingface.co/datasets/merve/vlm_test_images/resolve/main/throughput_smolvlm.png"
    
    response = requests.get(url)
    response.raise_for_status()
    
    sample_path = Path("sample_document.png")
    sample_path.write_bytes(response.content)
    
    print(f"✅ Downloaded: {sample_path}")
    return sample_path


def main():
    print("🧪 OCR Test Script")
    print("=" * 60)
    
    try:
        # Download sample
        sample_path = download_sample_image()
        
        print("\n🚀 Running OCR with Granite model (fastest)...")
        print("=" * 60)
        
        # Run OCR
        result = subprocess.run(
            ["uv", "run", "ocr.py", str(sample_path), "--model", "granite"],
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print("\n✅ Test completed successfully!")
            print(f"\n💡 Try other models:")
            print(f"   uv run ocr.py {sample_path} --model nanonets")
            print(f"   uv run ocr.py {sample_path} --model paddleocr")
        else:
            print("\n❌ Test failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

