import boto3

def check_root_mfa():
    """
    Check 1: Root Account MFA Enabled
    API: iam.get_account_summary -> AccountMFAEnabled
    """
    try:
        client = boto3.client('iam')
        summary = client.get_account_summary()
        mfa_enabled = summary['SummaryMap'].get('AccountMFAEnabled', 0)
        
        if mfa_enabled == 1:
            return {"check": "Root MFA", "status": "PASS", "risk": "Low", "details": "Root account MFA is enabled."}
        else:
            return {"check": "Root MFA", "status": "FAIL", "risk": "Critical", "details": "Root account MFA is NOT enabled. Highly recommended to enable it."}
    except Exception as e:
        return {"check": "Root MFA", "status": "ERROR", "risk": "Unknown", "details": str(e)}