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

1️⃣ Build the Lambda Deployment Package
```bash
cd lambda
./build.sh
chmod +x lambda/build.sh```

Upload root_audit_lambda.zip to an S3 bucket.

## 2️⃣ Deploy the CloudFormation Stack

aws cloudformation create-stack \
  --stack-name root-audit-dashboard \
  --template-body file://cloudformation/root_audit_dashboard.yml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameters ParameterKey=LambdaS3Bucket,ParameterValue=<YOUR_S3_BUCKET> \
               ParameterKey=LambdaS3Key,ParameterValue=root_audit_lambda.zip


3️⃣ In Each Member Account

    Create the IAM Role: RootComplianceAuditRole

    Grant iam:GetAccountSummary and iam:ListAccessKeys permissions

    Trust policy: Allow assume role by management account

4️⃣ Set Up the Dashboard

In QuickSight:

    Connect to DynamoDB table: RootSecurityAuditResults

    Build visuals for compliance status
