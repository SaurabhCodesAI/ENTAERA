
# This is your practice file for the Day 2 Kata.
# Complete the exercises from katas/day2_config_logging.md here.

import os
import logging
import json
from datetime import datetime
from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# --- Exercise 1: Basic Pydantic Settings ---

class DatabaseSettings(BaseModel):
    # TODO: Define fields and validator
    pass

print("--- Exercise 1 ---")
# TODO: Instantiate and test your model


# --- Exercise 2: Environment-backed Settings ---

class EnvDatabaseSettings(BaseSettings):
    # TODO: Add SettingsConfigDict and fields
    pass

print("\n--- Exercise 2 ---")
# TODO: Set environment variables and test instantiation


# --- Exercise 3: Simple Log Formatter ---

def setup_simple_logging():
    # TODO: Configure a logger with a simple formatter
    pass

print("\n--- Exercise 3 ---")
# TODO: Call setup_simple_logging() and log some messages


# --- Exercise 4: JSON Logging ---

class MyJSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        # TODO: Implement the JSON formatting logic
        pass

def setup_json_logging():
    # TODO: Configure a logger to use MyJSONFormatter
    pass

print("\n--- Exercise 4 ---")
# TODO: Call setup_json_logging() and log a message with 'extra' data

