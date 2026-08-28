import boto3

def check_s3_public_buckets():
    """
    Check 2: Public S3 Buckets Detection
    API: s3.list_buckets, s3.get_public_access_block, s3.get_bucket_acl
    """
    try:
        client = boto3.client('s3')
        buckets = client.list_buckets().get('Buckets', [])
        public_buckets = []
        
        for b in buckets:
            name = b['Name']
            is_public = False
            
            try:
                # Check Public Access Block settings
                pab = client.get_public_access_block(Bucket=name)['PublicAccessBlockConfiguration']
                is_blocked = (pab.get('BlockPublicAcls') and pab.get('IgnorePublicAcls') and 
                              pab.get('BlockPublicPolicy') and pab.get('RestrictPublicBuckets'))
                
                if not is_blocked:
                    # Fallback to check ACLs if not fully blocked at the bucket level
                    acl = client.get_bucket_acl(Bucket=name)
                    for grant in acl.get('Grants', []):
                        grantee = grant.get('Grantee', {})
                        if grantee.get('URI') == 'http://acs.amazonaws.com/groups/global/AllUsers':
                            is_public = True
            except client.exceptions.ClientError as e:
                # If No PublicAccessBlock is configured, we must check ACLs directly
                if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
                    acl = client.get_bucket_acl(Bucket=name)
                    for grant in acl.get('Grants', []):
                        grantee = grant.get('Grantee', {})
                        if grantee.get('URI') == 'http://acs.amazonaws.com/groups/global/AllUsers':
                            is_public = True
            
            if is_public:
                public_buckets.append(name)
                
        if public_buckets:
            return {"check": "Public S3 Buckets", "status": "FAIL", "risk": "Critical", "details": f"Public buckets found: {', '.join(public_buckets)}"}
        else:
            return {"check": "Public S3 Buckets", "status": "PASS", "risk": "Low", "details": "No publicly accessible S3 buckets found via ACL AllUsers URI."}
    except Exception as e:
        return {"check": "Public S3 Buckets", "status": "ERROR", "risk": "Unknown", "details": str(e)}