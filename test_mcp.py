from dotenv import load_dotenv
import requests
import logging
import sys
load_dotenv()
logging.basicConfig(level=logging.INFO)
def test_product_lookup():
    """Test product lookup functionality"""
    test_cases = [
        {"input": "3664142565543", "type": "barcode"},
        {"input": "22361022a", "type": "ref"}
    ]
    print("\n" + "="*40)
    print("PRODUCT LOOKUP TEST RESULTS")
    print("="*40)
    all_passed = True
    for case in test_cases:
        print(f"\nSearching by {case['type']}: {case['input']}")
        try:
            response = requests.post(
                "http://localhost:8000/mcp/call",
                json={
                    "tool": "fetch_product_by_code",
                    "args": {"code": case["input"]}
                },
                timeout=10
            )
            data = response.json()
            if response.status_code != 200:
                print(f" Error: HTTP {response.status_code}")
                all_passed = False
                continue
                
            if data.get("status") == "not_found":
                print(f" Product not found")
                all_passed = False
                continue
                
            if data.get("status") != "success":
                print(f"API Error: {data.get('message', 'Unknown error')}")
                all_passed = False
                continue
                
            product = data.get("product", {})
            if not product:
                print(" Empty product data")
                all_passed = False
                continue
            print("Product found:")
            print(f"ID: {product.get('id')}")
            print(f"Title: {product.get('title')}")
            print(f"Barcode: {product.get('barcode')}")
            print(f"Reference: {product.get('ref')}")
            print(f"Image: {product.get('image')}")
        except Exception as e:
            print(f" Test failed: {str(e)}")
            all_passed = False
    print("\n" + "="*40)
    print("FINAL RESULT:", " PASSED" if all_passed else " FAILED")
    print("="*40)
    sys.exit(0 if all_passed else 1)
if __name__ == "__main__":
    test_product_lookup()