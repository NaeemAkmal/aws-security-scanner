import boto3

def check_cloudtrail_status():
    """
    Check 4: CloudTrail Enabled & Logging status
    API: cloudtrail.describe_trails, cloudtrail.get_trail_status
    """
    try:
        client = boto3.client('cloudtrail')
        trails = client.describe_trails()['trailList']
        
        active_trails = 0
        for trail in trails:
            arn = trail['TrailARN']
            status = client.get_trail_status(Name=arn)
            if status.get('IsLogging', False):
                active_trails += 1
                
        if active_trails > 0:
            return {"check": "CloudTrail Logging", "status": "PASS", "risk": "Low", "details": f"{active_trails} active CloudTrail(s) found logging events."}
        else:
            return {"check": "CloudTrail Logging", "status": "FAIL", "risk": "High", "details": "No active CloudTrails found. Your AWS environment lacks audit logging."}
    except Exception as e:
        return {"check": "CloudTrail Logging", "status": "ERROR", "risk": "Unknown", "details": str(e)}