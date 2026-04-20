import os
import sys
import time
import shutil

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import cache_manager

def test_cache():
    # Setup test paths
    test_dir = "uploads/test_cache_subject"
    os.makedirs(test_dir, exist_ok=True)
    test_file = os.path.join(test_dir, "test.txt")
    
    with open(test_file, "w") as f:
        f.write("Initial content")
        
    print("Testing OCR Cache...")
    # First time: Save to cache
    text = "Extracted OCR text"
    cache_manager.save_ocr_cache(test_file, text)
    
    # Second time: Retrieve from cache
    cached_text = cache_manager.get_cached_ocr(test_file)
    if cached_text == text:
        print("[OK] OCR Cache HIT successful!")
    else:
        print("[ERROR] OCR Cache MISMATCH!")

    print("\nTesting Analysis Cache...")
    pdf_files = [test_file]
    syllabus = "Test syllabus"
    result = {"data": "API result"}
    
    # First time: Save to cache
    cache_manager.save_analysis_cache(test_dir, pdf_files, syllabus, result)
    
    # Second time: Retrieve from cache
    cached_analysis = cache_manager.get_cached_analysis(test_dir, pdf_files, syllabus)
    if cached_analysis == result:
        print("[OK] Analysis Cache HIT successful!")
    else:
        print("[ERROR] Analysis Cache MISMATCH!")

    print("\nTesting Cache Invalidation (file change)...")
    with open(test_file, "w") as f:
        f.write("Modified content")
    
    invalidated_ocr = cache_manager.get_cached_ocr(test_file)
    if invalidated_ocr is None:
        print("[OK] Cache correctly invalidated on file change!")
    else:
        print("[ERROR] Cache FAILED to invalidate!")

    # Cleanup
    shutil.rmtree(test_dir)
    print("\nCleanup complete.")

if __name__ == "__main__":
    test_cache()
