\# AWS Security Scanner 🛡️



!\[Python Version](https://img.shields.io/badge/python-3.9%2B-blue)

!\[AWS Boto3](https://img.shields.io/badge/AWS-Boto3-orange)

!\[License](https://img.shields.io/badge/License-MIT-green)



A production-ready, open-source Python script to perform basic security posture assessments on your AWS Account without incurring any costs.



\## Security Best Practices

\- \*\*Cost Free:\*\* Designed to strictly use AWS Free Tier API endpoints.

\- \*\*Read-Only:\*\* Ensure your IAM user ONLY has the `SecurityAudit` AWS Managed Policy attached. This tool does not modify or delete any resources.



\## Setup Instructions (Windows 11)



1\. Create a virtual environment: `python -m venv venv`

2\. Activate it: `.\\venv\\Scripts\\Activate`

3\. Install dependencies: `pip install -r requirements.txt`

4\. Configure AWS CLI with read-only credentials: `aws configure`

5\. Run the scanner: `python scanner.py`



\## Features / Checks Performed

\- IAM: Root Account MFA Status.

\- S3: Detects Publicly exposed buckets via ACLs and PublicAccessBlocks.

\- EC2: Flags Security Groups open to `0.0.0.0/0` on sensitive ports (22, 3389, 3306, etc).

\- CloudTrail: Verifies if auditing and logging are actively running.

