import requests
import sys
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")

def print_test(test_name):
    print(f"{Colors.BOLD}Testing: {test_name}{Colors.END}")

def print_pass(message):
    print(f"  {Colors.GREEN}✓ PASSED{Colors.END} - {message}")

def print_fail(message):
    print(f"  {Colors.RED}✗ FAILED{Colors.END} - {message}")

def print_info(message):
    print(f"  {Colors.YELLOW}ℹ{Colors.END} {message}")

def check_server_running():
    """Check if server is running"""
    print_test("Server Connection")
    try:
        response = requests.get(f"{BASE_URL}/orders/", timeout=2)
        print_pass(f"Server is running (Status: {response.status_code})")
        return True
    except requests.exceptions.ConnectionError:
        print_fail("Cannot connect to server")
        print_info("Make sure server is running: python manage.py runserver")
        return False
    except Exception as e:
        print_fail(f"Error: {e}")
        return False

def test_list_orders():
    """Test listing orders"""
    print_test("List Orders (GET /orders/)")
    try:
        response = requests.get(f"{BASE_URL}/orders/")
        data = response.json()
        count = data.get('count', 0)
        
        if response.status_code == 200:
            print_pass(f"Found {count} orders in database")
            if count > 0:
                print_info(f"Sample order: {data['results'][0]['order_id']}")
            return True
        else:
            print_fail(f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_fail(f"Error: {e}")
        return False

def test_create_order():
    """Test creating a new order"""
    print_test("Create Order (POST /orders/)")
    
    payload = {
        "customer_id": 1,
        "items": [
            {"product_id": 1, "sku": "SKU0001", "quantity": 1},
            {"product_id": 2, "sku": "SKU0002", "quantity": 2}
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Idempotency-Key": f"test-{datetime.now().timestamp()}"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/orders/", json=payload, headers=headers)
        
        if response.status_code in [200, 201]:
            data = response.json()
            print_pass(f"Order created successfully")
            print_info(f"Order ID: {data['order_id']}")
            print_info(f"Customer: {data['customer_name']}")
            print_info(f"Status: {data['order_status']}")
            print_info(f"Total: ${data['order_total']}")
            print_info(f"Items: {len(data['items'])}")
            return data['order_id']
        else:
            print_fail(f"Status code: {response.status_code}")
            print_info(f"Response: {response.json()}")
            return None
    except Exception as e:
        print_fail(f"Error: {e}")
        return None

def test_get_order_detail(order_id):
    """Test getting order details"""
    if not order_id:
        print_test("Get Order Detail (Skipped - no order_id)")
        return False
    
    print_test(f"Get Order Detail (GET /orders/{order_id}/)")
    try:
        response = requests.get(f"{BASE_URL}/orders/{order_id}/")
        
        if response.status_code == 200:
            data = response.json()
            print_pass("Order details retrieved")
            print_info(f"Items count: {len(data['items'])}")
            return True
        else:
            print_fail(f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_fail(f"Error: {e}")
        return False

def test_invalid_customer():
    """Test validation - invalid customer"""
    print_test("Validation: Invalid Customer")
    
    payload = {
        "customer_id": 99999,
        "items": [{"product_id": 1, "sku": "SKU0001", "quantity": 1}]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Idempotency-Key": f"test-invalid-{datetime.now().timestamp()}"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/orders/", json=payload, headers=headers)
        
        if response.status_code == 400:
            error = response.json().get('error', '')
            if 'not found' in error.lower() or 'customer' in error.lower():
                print_pass("Invalid customer rejected correctly")
                print_info(f"Error message: {error}")
                return True
        
        print_fail("Should reject invalid customer")
        return False
    except Exception as e:
        print_fail(f"Error: {e}")
        return False

def test_invalid_product():
    """Test validation - invalid product"""
    print_test("Validation: Invalid Product")
    
    payload = {
        "customer_id": 1,
        "items": [{"product_id": 99999, "sku": "SKU99999", "quantity": 1}]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Idempotency-Key": f"test-invalid-prod-{datetime.now().timestamp()}"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/orders/", json=payload, headers=headers)
        
        if response.status_code == 400:
            error = response.json().get('error', '')
            if 'not found' in error.lower() or 'product' in error.lower():
                print_pass("Invalid product rejected correctly")
                print_info(f"Error message: {error}")
                return True
        
        print_fail("Should reject invalid product")
        return False
    except Exception as e:
        print_fail(f"Error: {e}")
        return False

def test_idempotency():
    """Test idempotency"""
    print_test("Idempotency Check")
    
    payload = {
        "customer_id": 1,
        "items": [{"product_id": 1, "sku": "SKU0001", "quantity": 1}]
    }
    
    idempotency_key = f"test-idempotent-{datetime.now().timestamp()}"
    headers = {
        "Content-Type": "application/json",
        "Idempotency-Key": idempotency_key
    }
    
    try:
        # First request
        response1 = requests.post(f"{BASE_URL}/orders/", json=payload, headers=headers)
        
        if response1.status_code not in [200, 201]:
            print_fail("First request failed")
            return False
        
        order_id_1 = response1.json()['order_id']
        
        # Second request with same key
        response2 = requests.post(f"{BASE_URL}/orders/", json=payload, headers=headers)
        
        if response2.status_code not in [200, 201]:
            print_fail("Second request failed")
            return False
        
        order_id_2 = response2.json()['order_id']
        
        if order_id_1 == order_id_2:
            print_pass("Idempotency working - same order returned")
            print_info(f"Order ID: {order_id_1}")
            return True
        else:
            print_fail("Different order IDs - idempotency not working")
            print_info(f"First: {order_id_1}, Second: {order_id_2}")
            return False
            
    except Exception as e:
        print_fail(f"Error: {e}")
        return False

def test_filtering():
    """Test filtering"""
    print_test("Filter Orders by Status")
    
    try:
        response = requests.get(f"{BASE_URL}/orders/?order_status=CONFIRMED")
        
        if response.status_code == 200:
            count = response.json().get('count', 0)
            print_pass(f"Filtering works - found {count} CONFIRMED orders")
            return True
        else:
            print_fail(f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_fail(f"Error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print_header("ORDER SERVICE - QUICK TEST")
    print(f"Testing server at: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    results = []
    
    # Test 1: Server connection
    if not check_server_running():
        print(f"\n{Colors.RED}Cannot proceed - server not running{Colors.END}\n")
        return
    
    results.append(("Server Connection", True))
    
    # Test 2: List orders
    results.append(("List Orders", test_list_orders()))
    
    # Test 3: Create order
    order_id = test_create_order()
    results.append(("Create Order", order_id is not None))
    
    # Test 4: Get order detail
    results.append(("Get Order Detail", test_get_order_detail(order_id)))
    
    # Test 5: Invalid customer
    results.append(("Invalid Customer Validation", test_invalid_customer()))
    
    # Test 6: Invalid product
    results.append(("Invalid Product Validation", test_invalid_product()))
    
    # Test 7: Idempotency
    results.append(("Idempotency", test_idempotency()))
    
    # Test 8: Filtering
    results.append(("Filtering", test_filtering()))
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    failed = sum(1 for _, result in results if not result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{Colors.GREEN}PASS{Colors.END}" if result else f"{Colors.RED}FAIL{Colors.END}"
        print(f"  {status}  {test_name}")
    
    print(f"\n{Colors.BOLD}Results: {passed}/{total} tests passed{Colors.END}")
    
    if failed == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! Your Order Service is working perfectly! 🎉{Colors.END}\n")
    else:
        print(f"\n{Colors.YELLOW}⚠️  {failed} test(s) failed. Check the output above for details.{Colors.END}\n")
    
    print_header("NEXT STEPS")
    print("✓ View orders in browser: http://localhost:8000/api/v1/orders/")
    print("✓ Admin panel: http://localhost:8000/admin/")
    print("✓ Create more orders using the API")
    print()

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Test interrupted by user{Colors.END}\n")
        sys.exit(0)