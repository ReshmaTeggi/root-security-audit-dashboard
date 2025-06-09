# AWS Root User Security Audit Dashboard

This project audits AWS accounts for:
- Root user MFA enabled
- Root user access keys present

It centralizes the data in a DynamoDB table and can be visualized with AWS QuickSight.

## 🚀 Features

✅ Cross-account auditing using an IAM role  
✅ Centralized storage in DynamoDB  
✅ Automated daily checks via EventBridge  
✅ Ready for dashboarding in QuickSight  

## 🏗️ Deploy Instructions

### 1️⃣ Build the Lambda Deployment Package
```bash
cd lambda
./build.sh
