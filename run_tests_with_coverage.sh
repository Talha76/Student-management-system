#!/bin/bash

# Install coverage if not already installed
pip install coverage

# Run tests with coverage
coverage run --source="." -m unittest test_student_management.py

# Generate coverage report
coverage report -m

# Generate HTML report for detailed analysis
coverage html

echo "Coverage analysis completed. See htmlcov/index.html for detailed report."
