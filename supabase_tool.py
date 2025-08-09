from supabase import create_client
from dotenv import load_dotenv
import os
import logging

load_dotenv()
logger = logging.getLogger(__name__)

try:
    supabase = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )
    logger.info("Supabase client initialized successfully")
except Exception as e:
    logger.error(f"Supabase initialization failed: {str(e)}")
    raise