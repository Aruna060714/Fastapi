from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import uvicorn
import logging
import openai
from typing import Dict, Any

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/mcp/call")
async def fetch_product_by_code(request: Dict[str, Any]):
    from supabase_tool import supabase
    try:
        code = str(request.get("args", {}).get("code", "")).strip()
        if not code:
            raise HTTPException(status_code=400, detail="Missing 'code' in arguments")
        all_products = supabase.table("products_new2").select("*").execute()
        logger.info(f"All products in DB: {[(p.get('barcode'), p.get('ref')) for p in all_products.data]}")
        response = supabase.table("products_new2") \
                     .select("*") \
                     .eq("barcode", code) \
                     .execute()
        if not response.data:
            response = supabase.table("products_new2") \
                         .select("*") \
                         .eq("ref", code) \
                         .execute()
        
        if not response.data:
            return {
                "status": "not_found",
                "debug": {
                    "searched_code": code,
                    "available_barcodes": [p.get('barcode') for p in all_products.data],
                    "available_refs": [p.get('ref') for p in all_products.data]
                }
            }
        product = response.data[0]
        return {
            "status": "success",
            "product": {
                "id": product.get("id"),
                "title": product.get("title"),
                "barcode": product.get("barcode"),
                "ref": product.get("ref"),
                "image": product.get("image")
            }
        }
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }
@app.get("/")
async def health_check():
    return {
        "status": "running",
        "endpoints": ["POST /mcp/call"]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )