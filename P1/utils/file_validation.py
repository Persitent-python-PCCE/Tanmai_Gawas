# utils/file_validation.py
"""Helper functions for validating uploaded files according to Rules.md."""

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'mp4', 'doc', 'docx'}
MAX_SIZE_MB = 50

def allowed_file(filename, allowed=ALLOWED_EXTENSIONS):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed

def validate_file_size(file_storage, max_mb=MAX_SIZE_MB):
    # file_storage may be a Werkzeug FileStorage object
    file_storage.seek(0, 2)  # move to end to get size
    size = file_storage.tell()
    file_storage.seek(0)  # reset pointer
    return size <= max_mb * 1024 * 1024
