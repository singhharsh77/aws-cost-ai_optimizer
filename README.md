### 🚀 AWS Cost AI Optimizer
A serverless MLOps pipeline that transforms reactive cloud budgeting into proactive forecasting. This tool automates the ingestion of AWS Cost Explorer data into an S3 Data Lake, trains a Scikit-Learn time-series model via AWS Lambda, and performs automated inference to predict end-of-month spend. By integrating Infrastructure as Code (Terraform) with Amazon SNS, the system provides real-time observability and intelligent alerting, ensuring budget thresholds are never breached without notice.

### 🎯 Project Overview
The Problem Statement
Many organizations suffer from "Cloud Bill Shock" unexpectedly high AWS costs due to unmonitored resource scaling. Standard budget alerts are often reactive (notifying you after spend occurs).

#### The Solution
A proactive system that:

Harvests 6 months of historical cost data.

Predicts future spend using a Linear Regression AI model.

Alerts admins via Amazon SNS if the forecasted spend exceeds a predefined limit.

### 🛠 Tech Stack
- Infrastructure: Terraform (IaC)

- Cloud Provider: AWS (Lambda, S3, SNS, Cost Explorer)

- Language: Python 3.9

- AI/ML: Scikit-Learn, NumPy

- Automation: Boto3 (AWS SDK)

### 🏗 System Architecture
Project Flow
Deployment: Terraform provisions the Lambda, S3 Bucket, and SNS Topic.

Data Ingestion: Lambda triggers and pulls historical data from AWS Cost Explorer.

AI Training: Python's scikit-learn trains on the data to find the cost-over-time trend.

Forecasting: The model predicts the total cost for the current month.

Notification: If Predicted_Cost > Threshold, an alert is fired through SNS.

### 📸 Proof of Concept
1. AI Prediction Engine
The optimizer_ai.py script analyzes the trend and outputs the forecasted spend.

<img width="794" height="192" alt="Screenshot 2026-01-13 at 2 25 29 PM" src="https://github.com/user-attachments/assets/0be25bb5-d44e-4a8d-b327-4bf9af60f874" />

2. Automated Email Alert
When the threshold is breached, the system sends an immediate notification via Amazon SNS.

"AWS Cost Optimizer Alert" 
<img width="1438" height="559" alt="Screenshot 2026-01-13 at 2 53 47 PM" src="https://github.com/user-attachments/assets/8dda265c-1aa8-488f-9d36-4e86e08cf7f5" />


### 🚀 How to Use
Prerequisites
AWS Account with CLI configured.

Terraform installed.

1. Clone & Initialize
```Bash

git clone https://github.com/singhharsh77/aws-cost-ai_optimizer.git
cd aws-cost-ai_optimizer/terraform
terraform init
```
2. Deploy
```Bash

terraform apply -auto-approve
```
Note: Check your email to confirm the SNS subscription after this step.

3. Trigger the Analysis
```Bash

aws lambda invoke --function-name cost_harvester_api response.json
```
4. Cleanup
To avoid unwanted AWS charges:

```Bash

terraform destroy -auto-approve
```
### 🛡️ Security & Best Practices
- IAM Least Privilege: Lambda is only granted permissions to specific S3 buckets and SNS topics.

- Environment Variables: Sensitive data like the SNS ARN is injected via Terraform, not hardcoded.

- State Management: Terraform state files and binaries are excluded via .gitignore.
