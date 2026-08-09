import uuid
from pathlib import Path

from fastapi import UploadFile
from PIL import Image as PILImage

from app.core.config import settings

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def save_upload(file: UploadFile) -> tuple[str, str, int, int]:
    """업로드 파일을 storage/uploads에 저장하고 (파일명, 경로, 너비, 높이)를 반환한다."""
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"지원하지 않는 파일 형식입니다: {ext or '(확장자 없음)'}")

    stored_name = f"{uuid.uuid4().hex}{ext}"
    dest_path = settings.upload_dir / stored_name

    with dest_path.open("wb") as f:
        f.write(file.file.read())

    with PILImage.open(dest_path) as img:
        width, height = img.size

    return stored_name, str(dest_path), width, height
