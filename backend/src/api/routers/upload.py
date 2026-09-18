import os
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from src.api.dependencies import get_current_user
from src.infrastructure.database.models import UserModel
from src.config import get_settings
import aiofiles

settings = get_settings()

router = APIRouter(prefix="/upload", tags=["Upload"])

ALLOWED_EXTENSIONS = set(settings.ALLOWED_UPLOAD_EXTENSIONS.split(","))
MAX_SIZE = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024


@router.post("")
async def upload_file(
    file: UploadFile = File(...),
    current_user: UserModel = Depends(get_current_user),
):
    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de arquivo não permitido. Tipos aceitos: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Arquivo excede o tamanho máximo de {settings.MAX_UPLOAD_SIZE_MB}MB",
        )

    user_dir = os.path.join(settings.STORAGE_PATH, "uploads", str(current_user.id))
    os.makedirs(user_dir, exist_ok=True)

    file_id = str(uuid.uuid4())
    filename = f"{file_id}.{ext}"
    filepath = os.path.join(user_dir, filename)

    async with aiofiles.open(filepath, "wb") as f:
        await f.write(content)

    return {
        "id": file_id,
        "filename": file.filename,
        "saved_as": filename,
        "size": len(content),
        "path": f"uploads/{current_user.id}/{filename}",
    }
