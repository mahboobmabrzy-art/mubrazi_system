try:
    from google.cloud import vision
    print("SUCCESS: Google Cloud Vision loaded correctly!")
except ImportError as e:
    print(f"ERROR: {e}")
