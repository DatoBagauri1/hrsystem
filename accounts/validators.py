from pathlib import Path

from django.core.exceptions import ValidationError


ALLOWED_DOCUMENT_EXTENSIONS = {".pdf", ".doc", ".docx"}


def validate_document_file(file_obj):
    extension = Path(file_obj.name).suffix.lower()
    if extension not in ALLOWED_DOCUMENT_EXTENSIONS:
        raise ValidationError("Please upload a PDF, DOC, or DOCX document.")
