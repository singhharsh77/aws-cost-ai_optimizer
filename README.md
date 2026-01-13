# AWS Cost AI Optimizer 🚀

An end-to-end cloud-native solution that harvests AWS billing data and uses Machine Learning to predict future spending.

## 🏗️ Architecture
- **Infrastructure:** Terraform (IaC)
- **Data Source:** AWS Cost Explorer API
- **Compute:** AWS Lambda (Python 3.9)
- **Storage:** Amazon S3
- **AI Engine:** Scikit-Learn (Linear Regression)
- **Environment:** GitHub Codespaces

## 📊 How it Works
1. **Terraform** deploys a Lambda function and an S3 bucket.
2. The **Lambda** function fetches the last 6 months of costs and stores them as `train.csv` in S3.
3. We sync the data to our **Codespace**.
4. A **Python AI script** analyzes the trend and predicts the next month's bill.

## 🛠️ Usage
```bash
cd terraform && terraform apply -auto-approve
aws lambda invoke --function-name cost_harvester_api response.json
aws s3 sync s3://YOUR_BUCKET_NAME .
python scripts/optimizer_ai.py