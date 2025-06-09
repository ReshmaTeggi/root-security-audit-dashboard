#!/bin/bash
set -e

# Clean up previous builds
rm -rf build
mkdir build

# Install dependencies
pip install -r requirements.txt -t build/

# Copy Lambda function
cp lambda_function.py build/

# Zip it up
cd build
zip -r ../root_audit_lambda.zip .
cd ..

echo "Deployment package: root_audit_lambda.zip"
