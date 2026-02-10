import hashlib
import numpy as np

def generate_audio_fingerprint(file_bytes: bytes):
    """
    Generates a simple audio fingerprint using hash-based approach.
    This is a lightweight alternative to MFCC features.
    """
    # Create a hash-based fingerprint
    # We'll use multiple hash chunks to create a fingerprint vector
    chunk_size = len(file_bytes) // 13  # Simulate 13 features like MFCC
    
    fingerprint = []
    
    for i in range(13):
        start = i * chunk_size
        end = start + chunk_size if i < 12 else len(file_bytes)
        chunk = file_bytes[start:end]
        
        # Create a hash of this chunk and convert to a numeric value
        chunk_hash = hashlib.md5(chunk).hexdigest()
        # Take first 8 characters and convert to int
        numeric_value = int(chunk_hash[:8], 16) / (16**8)  # Normalize to 0-1
        fingerprint.append(numeric_value)
    
    return fingerprint


def is_replay(new_fp, existing_fps, threshold=0.95):
    """
    Compares fingerprints to detect replayed audio.
    Uses cosine similarity instead of correlation.
    """
    if not existing_fps:
        return False
    
    new_fp_array = np.array(new_fp)
    
    for old_fp in existing_fps:
        old_fp_array = np.array(old_fp)
        
        # Calculate cosine similarity
        dot_product = np.dot(new_fp_array, old_fp_array)
        norm_new = np.linalg.norm(new_fp_array)
        norm_old = np.linalg.norm(old_fp_array)
        
        if norm_new == 0 or norm_old == 0:
            similarity = 0
        else:
            similarity = dot_product / (norm_new * norm_old)
        
        if similarity > threshold:
            return True
    
    return False