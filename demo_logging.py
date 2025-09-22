#!/usr/bin/env python3
"""
Demo script showcasing ENTAERA's comprehensive logging infrastructure.

This script demonstrates:
- Multiple logging handlers (console, file, JSON)
- Colored console output
- Performance monitoring and timing
- Structured logging with extra fields
- Exception logging with full traceback
- Integration with configuration system
"""

import time
import json
from pathlib import Path

from src.entaera.core.logger import (
    setup_logging, 
    get_logger, 
    get_performance_logger,
    time_function,
    shutdown_logging
)
from src.entaera.core.config import Settings


def demonstrate_basic_logging():
    """Demonstrate basic logging functionality."""
    logger = get_logger('demo.basic')
    
    logger.debug("This is a debug message (may not show if level is INFO)")
    logger.info("🚀 Starting logging demonstration")
    logger.warning("⚠️ This is a warning message")
    logger.error("❌ This is an error message")
    logger.critical("🔥 This is a critical message")


def demonstrate_structured_logging():
    """Demonstrate structured logging with extra fields."""
    logger = get_logger('demo.structured')
    
    # Log with extra structured data
    logger.info("User logged in", extra={
        'user_id': '12345',
        'username': 'demo_user',
        'ip_address': '192.168.1.100',
        'session_id': 'sess_abc123',
        'login_method': 'oauth'
    })
    
    logger.info("API request processed", extra={
        'endpoint': '/api/v1/users',
        'method': 'GET',
        'status_code': 200,
        'response_time_ms': 45.7,
        'user_agent': 'ENTAERA/1.0'
    })


def demonstrate_performance_logging():
    """Demonstrate performance monitoring and timing."""
    perf_logger = get_performance_logger('demo.performance')
    
    # Manual timing
    perf_logger.start_timer('data_processing')
    time.sleep(0.1)  # Simulate work
    duration = perf_logger.end_timer('data_processing', {
        'records_processed': 1000,
        'memory_used_mb': 45.2
    })
    
    # Context manager timing
    with perf_logger.timer('api_call', {'endpoint': '/api/health'}):
        time.sleep(0.05)  # Simulate API call
    
    print(f"🕐 Manual timing recorded: {duration:.3f} seconds")


@time_function(get_logger('demo.decorator'))
def demonstrate_function_timing(items_count: int, processing_mode: str):
    """Demonstrate function timing decorator."""
    time.sleep(0.03)  # Simulate processing
    return f"Processed {items_count} items in {processing_mode} mode"


def demonstrate_exception_logging():
    """Demonstrate exception logging with full traceback."""
    logger = get_logger('demo.exceptions')
    
    try:
        # Simulate a complex error scenario
        data = {'user': 'demo', 'operation': 'divide'}
        result = 10 / 0  # This will raise ZeroDivisionError
    except ZeroDivisionError as e:
        logger.error("Mathematical error occurred", extra={
            'error_type': 'ZeroDivisionError',
            'operation': data['operation'],
            'user': data['user'],
            'timestamp': time.time()
        }, exc_info=True)


def show_log_files():
    """Show the contents of generated log files."""
    print("\n" + "="*60)
    print("📁 GENERATED LOG FILES")
    print("="*60)
    
    log_dir = Path("logs")
    
    # Show regular log file
    log_file = log_dir / "entaera.log"
    if log_file.exists():
        print(f"\n📄 {log_file} (last 5 lines):")
        print("-" * 40)
        lines = log_file.read_text().strip().split('\n')
        for line in lines[-5:]:
            print(line)
    
    # Show JSON structured log file
    json_file = log_dir / "entaera_structured.json"
    if json_file.exists():
        print(f"\n📄 {json_file} (last entry):")
        print("-" * 40)
        lines = json_file.read_text().strip().split('\n')
        if lines:
            try:
                last_entry = json.loads(lines[-1])
                print(json.dumps(last_entry, indent=2))
            except json.JSONDecodeError:
                print("Could not parse JSON")


def main():
    """Main demonstration function."""
    print("🎯 ENTAERA Logging System Demonstration")
    print("=" * 50)
    
    # Setup logging with all features enabled
    settings = Settings()
    settings.log_level = "DEBUG"
    settings.log_to_console = True
    settings.log_to_file = True
    settings.log_json_format = True
    settings.log_colored_output = True
    
    # Initialize logging system
    manager = setup_logging(settings)
    
    try:
        print("\n1️⃣ Basic Logging (different levels and colors)")
        print("-" * 50)
        demonstrate_basic_logging()
        
        print("\n2️⃣ Structured Logging (with extra fields)")
        print("-" * 50)
        demonstrate_structured_logging()
        
        print("\n3️⃣ Performance Monitoring")
        print("-" * 50)
        demonstrate_performance_logging()
        
        print("\n4️⃣ Function Timing Decorator")
        print("-" * 50)
        result = demonstrate_function_timing(500, "batch")
        print(f"✅ Function result: {result}")
        
        print("\n5️⃣ Exception Logging")
        print("-" * 50)
        demonstrate_exception_logging()
        print("✅ Exception logged with full traceback")
        
        # Show generated files
        show_log_files()
        
        print("\n" + "="*60)
        print("🎉 DEMONSTRATION COMPLETE!")
        print("="*60)
        print("✅ Console logging: Colors and formatting")
        print("✅ File logging: Rotating file handler")
        print("✅ JSON logging: Structured data for analysis")
        print("✅ Performance timing: Operation monitoring")
        print("✅ Exception handling: Full traceback capture")
        print("✅ Configuration integration: Settings-driven setup")
        
    finally:
        # Proper cleanup
        shutdown_logging()


if __name__ == "__main__":
    main()