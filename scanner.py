import sys
from checks.mfa_check import check_root_mfa
from checks.s3_check import check_s3_public_buckets
from checks.sg_check import check_open_security_groups
from checks.cloudtrail_check import check_cloudtrail_status
from report.generate_report import create_html_report

def run_scanner():
    print("[*] Starting AWS Security Scanner...")
    results = []
    
    print("[*] Running Check 1: Root Account MFA...")
    results.append(check_root_mfa())
    
    print("[*] Running Check 2: Public S3 Buckets...")
    results.append(check_s3_public_buckets())
    
    print("[*] Running Check 3: Open Security Groups...")
    results.append(check_open_security_groups())
    
    print("[*] Running Check 4: CloudTrail Logging Status...")
    results.append(check_cloudtrail_status())
    
    print("[*] All checks completed. Generating report...")
    report_path = create_html_report(results)
    print(f"[+] Security report successfully generated at:\n    {report_path}")

if __name__ == "__main__":
    try:
        run_scanner()
    except Exception as e:
        print(f"[-] A fatal error occurred: {e}")
        sys.exit(1)