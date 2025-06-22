from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = os.getenv("DEBUG", False)

    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "").split(",")

    # Cloudinary
    CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")

settings = Settings()
