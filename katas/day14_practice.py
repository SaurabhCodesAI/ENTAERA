"""
ENTAERA Kata - Day 14: Unstructured to Structured Data Practice
Complete all exercises to master data extraction and transformation.
"""

import re
import json
from typing import Dict, List, Optional
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime

# =============================================================================
# Exercise 1: Parse Server Logs
# =============================================================================

print("=" * 60)
print("Exercise 1: Parse Server Logs")
print("=" * 60)

logs = """
2024-01-15 10:30:45 INFO Server started on port 8000
2024-01-15 10:31:12 DEBUG Received request from 192.168.1.100
2024-01-15 10:31:15 ERROR Database connection timeout after 30s
2024-01-15 10:32:01 WARNING High memory usage: 85%
2024-01-15 10:35:23 CRITICAL Disk space critically low: 2% remaining
"""

def parse_logs(log_text: str) -> List[Dict]:
    """
    Parse logs into list of dicts with:
    - timestamp (datetime)
    - level (str)
    - message (str)
    - severity (int: 1-5)
    """
    # TODO: Implement
    pass

# parsed_logs = parse_logs(logs)
# print(f"Parsed {len(parsed_logs)} log entries")
# print(f"First entry: {parsed_logs[0]}")


# =============================================================================
# Exercise 2: Extract Contact Information
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 2: Extract Contact Information")
print("=" * 60)

contact_text = """
For support, contact our team:
- Technical Support: tech@company.com, (555) 123-4567
- Sales: sales@company.com, 555-234-5678
- General Inquiries: info@company.com

Office hours: Monday-Friday, 9am-5pm EST
Address: 123 Main Street, New York, NY 10001
"""

def extract_contacts(text: str) -> List[Dict]:
    """
    Extract all contact information:
    - department (str)
    - email (str)
    - phone (str)
    """
    # TODO: Implement
    pass

# contacts = extract_contacts(contact_text)
# print(f"Extracted {len(contacts)} contacts")
# for contact in contacts:
#     print(f"  {contact}")


# =============================================================================
# Exercise 3: Parse API Response
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 3: Parse API Response")
print("=" * 60)

api_response = {
    "status": "success",
    "data": {
        "user": {
            "id": 123,
            "profile": {
                "name": "Alice",
                "age": 25,
                "preferences": {
                    "theme": "dark",
                    "notifications": True
                }
            },
            "posts": [
                {"id": 1, "title": "Hello World", "likes": 10},
                {"id": 2, "title": "Python Tips", "likes": 25}
            ]
        }
    },
    "metadata": {
        "timestamp": "2024-01-15T10:30:00Z",
        "version": "1.0"
    }
}

def flatten_api_response(response: Dict) -> Dict:
    """Flatten nested response to single-level dict."""
    # TODO: Implement using recursive flattening
    pass

# flat = flatten_api_response(api_response)
# print(f"Flattened response:")
# for key, value in flat.items():
#     print(f"  {key}: {value}")


# =============================================================================
# Exercise 4: CSV to Pydantic Models
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 4: CSV to Pydantic Models")
print("=" * 60)

# TODO: Define Pydantic model for user data
class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    city: str
    
    @validator('age')
    def validate_age(cls, v):
        # TODO: Ensure age is between 0 and 120
        pass

csv_data = """id,name,email,age,city
1,Alice,alice@email.com,25,NYC
2,Bob,bob@email.com,30,LA
3,Charlie,charlie@email.com,35,Chicago
4,Invalid,not-an-email,200,Boston"""

def parse_csv_to_models(csv_text: str) -> tuple[List[User], List[Dict]]:
    """
    Parse CSV to User models.
    Returns: (valid_users, errors)
    """
    # TODO: Parse CSV
    # TODO: Validate each row with Pydantic
    # TODO: Collect valid users and errors separately
    pass

# valid_users, errors = parse_csv_to_models(csv_data)
# print(f"Valid users: {len(valid_users)}")
# print(f"Errors: {len(errors)}")


# =============================================================================
# Exercise 5: Extract Structured Data from Natural Language
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 5: Extract Meeting Information")
print("=" * 60)

meeting_text = """
Let's schedule a meeting for next Tuesday, January 16th at 2:30 PM.
Attendees: Alice Smith, Bob Johnson, and Charlie Davis
Location: Conference Room B
Duration: 1.5 hours
Agenda: Q1 planning and budget review
"""

class Meeting(BaseModel):
    date: Optional[str] = None
    time: Optional[str] = None
    attendees: List[str] = []
    location: Optional[str] = None
    duration: Optional[str] = None
    agenda: Optional[str] = None

def extract_meeting_info(text: str) -> Meeting:
    """Extract meeting details from natural language text."""
    # TODO: Use regex to extract:
    # - Date pattern
    # - Time pattern
    # - Names (capitalized words)
    # - Location (after "Location:")
    # - Duration (number + hours/minutes)
    # - Agenda (after "Agenda:")
    pass

# meeting = extract_meeting_info(meeting_text)
# print(f"Meeting details: {meeting}")


# =============================================================================
# Exercise 6: Parse Stack Traces
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 6: Parse Stack Traces")
print("=" * 60)

stack_trace = """
Traceback (most recent call last):
  File "app.py", line 45, in main
    result = process_data(data)
  File "utils.py", line 23, in process_data
    return transform(data)
  File "utils.py", line 12, in transform
    return data['value'] / divisor
ZeroDivisionError: division by zero
"""

class StackFrame(BaseModel):
    file: str
    line: int
    function: str
    code: Optional[str] = None

class Error(BaseModel):
    type: str
    message: str
    frames: List[StackFrame]

def parse_stack_trace(trace: str) -> Error:
    """Parse stack trace into structured error data."""
    # TODO: Extract error type and message
    # TODO: Extract each frame (file, line, function, code)
    pass

# error = parse_stack_trace(stack_trace)
# print(f"Error type: {error.type}")
# print(f"Frames: {len(error.frames)}")


# =============================================================================
# Exercise 7: Convert Unstructured Product Data
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 7: Parse Product Descriptions")
print("=" * 60)

product_descriptions = [
    "iPhone 15 Pro - 256GB - Titanium Blue - $999.99 - In Stock (45 units)",
    "Samsung Galaxy S24 Ultra | 512GB | Phantom Black | Price: $1,199.99 | Available: 23",
    "Google Pixel 8 Pro, 128GB, Obsidian, $899, Stock: Out of Stock"
]

class Product(BaseModel):
    name: str
    storage: str
    color: str
    price: float
    stock_status: str
    stock_count: Optional[int] = None

def parse_product(description: str) -> Product:
    """Extract structured product data from various text formats."""
    # TODO: Handle multiple formats (-, |, comma-separated)
    # TODO: Extract price (handle $X,XXX.XX format)
    # TODO: Extract storage (GB/TB)
    # TODO: Extract stock info
    pass

# for desc in product_descriptions:
#     product = parse_product(desc)
#     print(f"Parsed: {product.name} - ${product.price}")


# =============================================================================
# Exercise 8: Real-World Challenge - Invoice Parser
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 8: Invoice Parser")
print("=" * 60)

invoice_text = """
INVOICE #INV-2024-001
Date: January 15, 2024
Due Date: February 15, 2024

Bill To:
Acme Corporation
123 Business Ave
New York, NY 10001

Items:
1. Web Development Services    $5,000.00
2. UI/UX Design                 $2,500.00
3. Cloud Hosting (Annual)       $1,200.00

Subtotal:                       $8,700.00
Tax (8.5%):                     $739.50
Total:                          $9,439.50

Payment Terms: Net 30
"""

class InvoiceItem(BaseModel):
    description: str
    amount: float

class Invoice(BaseModel):
    invoice_number: str
    date: str
    due_date: str
    bill_to: Dict[str, str]  # company, address, city, state, zip
    items: List[InvoiceItem]
    subtotal: float
    tax_rate: float
    tax_amount: float
    total: float
    payment_terms: str

def parse_invoice(text: str) -> Invoice:
    """Parse invoice text into structured data."""
    # TODO: Extract all invoice information
    # TODO: Parse line items
    # TODO: Parse billing address
    # TODO: Calculate and verify totals
    pass

# invoice = parse_invoice(invoice_text)
# print(f"Invoice: {invoice.invoice_number}")
# print(f"Total: ${invoice.total}")
# print(f"Items: {len(invoice.items)}")

print("\n" + "=" * 60)
print("All exercises complete! Review your solutions.")
print("=" * 60)
