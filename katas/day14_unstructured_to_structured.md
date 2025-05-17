# ENTAERA Kata - Day 14: Unstructured to Structured Data

## 🎯 Learning Objectives

Raw data is messy. Logs are unstructured text. API responses are nested JSON. PDFs contain tables hidden in text. Today you'll master the art of extracting structured data from chaos—a critical skill for any AI system that deals with real-world data.

- **Parse and extract data from unstructured text**
- **Use regex patterns to extract structured information**
- **Parse JSON, XML, CSV, and other formats**
- **Extract data from logs, emails, and natural language**
- **Convert nested dictionaries to flat, queryable formats**
- **Build schemas from unstructured data**
- **Use Pydantic for validation and transformation**

---

## 🧠 For the Absolute Beginner

### What is Unstructured Data?
**Unstructured data** is information without a predefined format:
- Raw text: "John Smith, age 30, lives in NYC"
- Log files: "2024-01-15 ERROR: Connection timeout"
- Emails, PDFs, social media posts, chat messages

### What is Structured Data?
**Structured data** is organized in a clear format:
```python
{
    "name": "John Smith",
    "age": 30,
    "city": "NYC"
}
```

### Why Convert?
You can't query, analyze, or store unstructured data efficiently. Converting it to structured format lets you:
- Search by specific fields
- Store in databases
- Perform analytics
- Feed into ML models

---

## 📚 Core Techniques

### 1. Regex Pattern Matching

```python
import re
from typing import Dict, List

def extract_email_data(text: str) -> Dict:
    """Extract structured data from email text."""
    
    # Extract email address
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email = re.search(email_pattern, text)
    
    # Extract phone number
    phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    phone = re.search(phone_pattern, text)
    
    # Extract dates
    date_pattern = r'\b\d{4}-\d{2}-\d{2}\b'
    dates = re.findall(date_pattern, text)
    
    return {
        "email": email.group() if email else None,
        "phone": phone.group() if phone else None,
        "dates": dates
    }

# Example
text = "Contact John at john.doe@email.com or call 555-123-4567. Meeting on 2024-01-15."
data = extract_email_data(text)
# {'email': 'john.doe@email.com', 'phone': '555-123-4567', 'dates': ['2024-01-15']}
```

### 2. Log Parsing

```python
from datetime import datetime
from typing import List, Dict

def parse_log_line(line: str) -> Dict:
    """Parse a log line into structured data."""
    
    # Pattern: "2024-01-15 10:30:45 ERROR Database connection failed"
    pattern = r'^(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+(\w+)\s+(.+)$'
    match = re.match(pattern, line)
    
    if not match:
        return None
    
    timestamp_str, level, message = match.groups()
    
    return {
        "timestamp": datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S"),
        "level": level,
        "message": message,
        "severity": {"DEBUG": 1, "INFO": 2, "WARNING": 3, "ERROR": 4, "CRITICAL": 5}.get(level, 0)
    }

# Example
log = "2024-01-15 10:30:45 ERROR Database connection failed"
parsed = parse_log_line(log)
# {'timestamp': datetime(...), 'level': 'ERROR', 'message': 'Database connection failed', 'severity': 4}
```

### 3. Named Groups for Complex Parsing

```python
def parse_user_info(text: str) -> Dict:
    """Extract user information using named regex groups."""
    
    pattern = r'(?P<name>[A-Z][a-z]+\s[A-Z][a-z]+),\s+age\s+(?P<age>\d+),\s+(?P<city>[A-Za-z\s]+)'
    match = re.search(pattern, text)
    
    if not match:
        return None
    
    return match.groupdict()

# Example
text = "User profile: John Smith, age 30, New York City"
user = parse_user_info(text)
# {'name': 'John Smith', 'age': '30', 'city': 'New York City'}
```

### 4. CSV/TSV to Structured Data

```python
def parse_csv_to_dicts(csv_text: str) -> List[Dict]:
    """Convert CSV text to list of dictionaries."""
    lines = csv_text.strip().split('\n')
    headers = lines[0].split(',')
    
    data = []
    for line in lines[1:]:
        values = line.split(',')
        row = {headers[i]: values[i].strip() for i in range(len(headers))}
        data.append(row)
    
    return data

# Example
csv = """name,age,city
Alice,25,NYC
Bob,30,LA
Charlie,35,Chicago"""

users = parse_csv_to_dicts(csv)
# [{'name': 'Alice', 'age': '25', 'city': 'NYC'}, ...]
```

### 5. Nested JSON Flattening

```python
def flatten_dict(d: Dict, parent_key: str = '', sep: str = '_') -> Dict:
    """Flatten nested dictionary."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    items.extend(flatten_dict(item, f"{new_key}_{i}", sep=sep).items())
                else:
                    items.append((f"{new_key}_{i}", item))
        else:
            items.append((new_key, v))
    
    return dict(items)

# Example
nested = {
    "user": {
        "name": "Alice",
        "address": {
            "city": "NYC",
            "zip": "10001"
        }
    },
    "orders": [{"id": 1}, {"id": 2}]
}

flat = flatten_dict(nested)
# {'user_name': 'Alice', 'user_address_city': 'NYC', 'user_address_zip': '10001', 
#  'orders_0_id': 1, 'orders_1_id': 2}
```

### 6. Natural Language Extraction

```python
from typing import Optional
from pydantic import BaseModel, Field

class PersonInfo(BaseModel):
    """Structured person data."""
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None

def extract_person_from_text(text: str) -> PersonInfo:
    """Extract person information from natural language."""
    
    # Name pattern (capitalized words)
    name_pattern = r'\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)\b'
    name_match = re.search(name_pattern, text)
    
    # Age pattern
    age_pattern = r'\b(\d{1,2})\s*(?:years?\s*old|yo)\b'
    age_match = re.search(age_pattern, text, re.IGNORECASE)
    
    # Email pattern
    email_pattern = r'\b([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b'
    email_match = re.search(email_pattern, text)
    
    # Phone pattern
    phone_pattern = r'\b(\d{3}[-.]?\d{3}[-.]?\d{4})\b'
    phone_match = re.search(phone_pattern, text)
    
    return PersonInfo(
        name=name_match.group(1) if name_match else None,
        age=int(age_match.group(1)) if age_match else None,
        email=email_match.group(1) if email_match else None,
        phone=phone_match.group(1) if phone_match else None
    )

# Example
text = "My name is John Smith, I'm 30 years old. You can reach me at john@email.com or 555-123-4567."
person = extract_person_from_text(text)
# PersonInfo(name='John Smith', age=30, email='john@email.com', phone='555-123-4567')
```

---

## 💻 Exercises

Create `katas/day14_practice.py` and complete these exercises.

### Exercise 1: Parse Server Logs

```python
# TODO: Parse these log lines into structured data
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

parsed_logs = parse_logs(logs)
# Expected: List of 5 dicts with structured data
```

### Exercise 2: Extract Contact Information

```python
# TODO: Extract structured contact data from text
text = """
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
```

### Exercise 3: Parse API Response

```python
# TODO: Flatten this complex API response
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

# Expected: All data in flat structure with underscore-separated keys
```

### Exercise 4: CSV to Pydantic Models

```python
from pydantic import BaseModel, EmailStr, validator
from typing import List

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
```

### Exercise 5: Extract Structured Data from Natural Language

```python
# TODO: Extract meeting information from natural language
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
```

### Exercise 6: Parse Stack Traces

```python
# TODO: Parse Python stack trace into structured data
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
```

### Exercise 7: Convert Unstructured Product Data

```python
# TODO: Extract product information from messy text
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
```

### Exercise 8: Real-World Challenge - Invoice Parser

```python
# TODO: Parse invoice text into structured data
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
```

---

## 🚀 Advanced Techniques

### Using LLMs for Extraction

For complex, highly variable text, use an LLM:

```python
from openai import OpenAI

def llm_extract(text: str, schema: type[BaseModel]) -> BaseModel:
    """Use LLM to extract structured data."""
    
    client = OpenAI()
    
    prompt = f"""
    Extract information from this text and return valid JSON matching this schema:
    {schema.model_json_schema()}
    
    Text:
    {text}
    
    Return only valid JSON, no explanation.
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    data = json.loads(response.choices[0].message.content)
    return schema.model_validate(data)
```

### Handling Multiple Formats

```python
def smart_parse(text: str) -> Dict:
    """Auto-detect format and parse accordingly."""
    
    # Try JSON
    try:
        return json.loads(text)
    except:
        pass
    
    # Try CSV
    if ',' in text and '\n' in text:
        return parse_csv_to_dicts(text)
    
    # Try key-value pairs
    if ':' in text:
        pairs = re.findall(r'(\w+):\s*([^\n]+)', text)
        return dict(pairs)
    
    # Fallback to NLP extraction
    return extract_with_nlp(text)
```

---

## 🤔 Mastery Questions

### Beginner
1. **What's the difference between `re.match()` and `re.search()`?**
   - `match()` checks only at the start, `search()` finds pattern anywhere

2. **Why use named groups in regex?**
   - Makes extracted data self-documenting and easier to access

### Intermediate
3. **How do you handle data that doesn't match your expected format?**
   - Use try-except, validation, and error collection to handle gracefully

4. **When should you use regex vs an LLM for extraction?**
   - Regex: Consistent, predictable formats. LLM: Variable, natural language

### Advanced
5. **How do you design a schema when the input format is unknown?**
   - Sample the data, identify common patterns, build flexible validators

6. **What's the trade-off between strict and lenient parsing?**
   - Strict: Accurate but may reject valid data. Lenient: Accepts more but may have errors

---

## 🎯 Real-World Applications

- **Log Analysis**: Convert server logs to queryable database
- **Email Processing**: Extract tasks, dates, contacts from emails
- **Document Processing**: Extract tables from PDFs/Word docs
- **API Integration**: Normalize data from multiple API formats
- **Data Migration**: Convert legacy data to modern schemas
- **Web Scraping**: Structure HTML content into clean data

**Time to Complete:** 5-7 hours

You can now **tame any data chaos**! 🎉
