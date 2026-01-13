import boto3
import csv
import os
from datetime import datetime, timedelta

def lambda_handler(event, context):
    ce = boto3.client('ce')
    s3 = boto3.client('s3')
    sns = boto3.client('sns') # Added SNS client
    
    bucket_name = os.environ['BUCKET_NAME']
    sns_topic_arn = os.environ['SNS_TOPIC_ARN']
    
    # Get last 6 months of data
    end = datetime.now().strftime('%Y-%m-%d')
    start = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
    
    response = ce.get_cost_and_usage(
        TimePeriod={'Start': start, 'End': end},
        Granularity='MONTHLY',
        Metrics=['UnblendedCost']
    )
    
    # Parse to CSV and find latest cost
    path = '/tmp/train_data.csv'
    latest_cost = 0.0
    
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'cost'])
        for row in response['ResultsByTime']:
            amount = float(row['Total']['UnblendedCost']['Amount'])
            writer.writerow([row['TimePeriod']['Start'], amount])
            latest_cost = amount # This will end up as the most recent month

    # Alert Logic: Send email if latest month > $10
    threshold = -1.0
    if latest_cost > threshold:
        sns.publish(
            TopicArn=sns_topic_arn,
            Message=f"Alert! Your current AWS spend is ${latest_cost:.2f}, which exceeds your ${threshold} limit.",
            Subject="AWS Cost Optimizer Alert"
        )
            
    # Upload to S3
    s3.upload_file(path, bucket_name, 'train.csv')
    
    return {
        "status": "Success",
        "latest_cost": latest_cost,
        "message": f"Data uploaded to {bucket_name}/train.csv"
    }