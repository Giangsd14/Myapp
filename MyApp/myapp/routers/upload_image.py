from fastapi import UploadFile, File, APIRouter, HTTPException, status
import cloudinary
from cloudinary.uploader import upload, destroy
from PIL import Image
import io
from fastapi import APIRouter, Depends
from .. import schemas, oauth2
from typing import Annotated
from fastapi import UploadFile, File

# cloudinary.config(secure=True)


router = APIRouter(
    prefix="/upload_image",
    tags=['Upload Image']
)

current_user = Annotated[schemas.User, Depends(oauth2.get_current_user)]

@router.post("/")
async def upload_image(get_current_user: current_user, file: UploadFile = File(...)):
    try:
        contents = await file.read()

        image = Image.open(io.BytesIO(contents))
        image.thumbnail((60, 60)) 

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")  
        buffer.seek(0)

        result = upload(buffer, resource_type="image")

        return {
                "url": result["secure_url"],
                "public_id": result["public_id"]
                }

    except Exception as e:
        return {"error": str(e)}
    
@router.delete("/")
async def delete_image(get_current_user: current_user, url: str):
    last_part = url.split("/")[-1]
    public_id = last_part.rsplit(".", 1)[0]
    try:
        result = destroy(public_id, resource_type="image")
        
        if result.get("result") == "ok":
            return {"message": f"Image with public_id '{public_id}' deleted successfully."}
        elif result.get("result") == "not found":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail="Image not found")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail=f"Failed to delete image: {result}")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))