import os
import json
import hashlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CACHE_DIR_NAME = ".cache"

def get_file_hash(file_path):
    """Calculates the SHA256 hash of a file's content."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read in chunks for memory efficiency
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_string_hash(text):
    """Calculates the SHA256 hash of a string."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def _get_cache_dir(base_dir):
    cache_dir = os.path.join(base_dir, CACHE_DIR_NAME)
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir

def get_cached_ocr(file_path):
    """Retrieves cached OCR text for a given file if the hash matches."""
    try:
        base_dir = os.path.dirname(file_path)
        cache_dir = _get_cache_dir(base_dir)
        file_hash = get_file_hash(file_path)
        
        cache_file = os.path.join(cache_dir, f"{os.path.basename(file_path)}.{file_hash}.txt")
        if os.path.exists(cache_file):
            logger.info(f"Cache HIT for OCR: {file_path}")
            with open(cache_file, "r", encoding="utf-8") as f:
                return f.read()
    except Exception as e:
        logger.error(f"Error reading OCR cache: {e}")
    return None

def save_ocr_cache(file_path, text):
    """Saves OCR text to cache with the file's hash."""
    try:
        base_dir = os.path.dirname(file_path)
        cache_dir = _get_cache_dir(base_dir)
        file_hash = get_file_hash(file_path)
        
        cache_file = os.path.join(cache_dir, f"{os.path.basename(file_path)}.{file_hash}.txt")
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(text)
        logger.info(f"Saved OCR cache for: {file_path}")
    except Exception as e:
        logger.error(f"Error saving OCR cache: {e}")

def get_cached_analysis(target_dir, pdf_files, syllabus_text):
    """Retrieves cached analysis JSON if the state of all files and syllabus matches."""
    try:
        cache_dir = _get_cache_dir(target_dir)
        
        # Create a combined state hash
        state_data = {
            "pdfs": {os.path.basename(f): get_file_hash(f) for f in sorted(pdf_files)},
            "syllabus_hash": get_string_hash(syllabus_text)
        }
        state_hash = get_string_hash(json.dumps(state_data, sort_keys=True))
        
        cache_file = os.path.join(cache_dir, f"analysis_result.{state_hash}.json")
        if os.path.exists(cache_file):
            logger.info(f"Cache HIT for full analysis: {target_dir}")
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error reading analysis cache: {e}")
    return None

def save_analysis_cache(target_dir, pdf_files, syllabus_text, result_data):
    """Saves the final analysis result to cache."""
    try:
        cache_dir = _get_cache_dir(target_dir)
        
        # Create a combined state hash
        state_data = {
            "pdfs": {os.path.basename(f): get_file_hash(f) for f in sorted(pdf_files)},
            "syllabus_hash": get_string_hash(syllabus_text)
        }
        state_hash = get_string_hash(json.dumps(state_data, sort_keys=True))
        
        cache_file = os.path.join(cache_dir, f"analysis_result.{state_hash}.json")
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(result_data, f, indent=2)
        logger.info(f"Saved analysis cache for: {target_dir}")
    except Exception as e:
        logger.error(f"Error saving analysis cache: {e}")
