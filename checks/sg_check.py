import boto3

def check_open_security_groups():
    """
    Check 3: Open Security Groups on sensitive ports to 0.0.0.0/0
    API: ec2.describe_security_groups
    """
    try:
        client = boto3.client('ec2')
        sgs = client.describe_security_groups()['SecurityGroups']
        sensitive_ports = {22, 3389, 3306, 5432, 27017}
        open_sgs = []
        
        for sg in sgs:
            sg_id = sg['GroupId']
            sg_name = sg.get('GroupName', 'N/A')
            
            for perm in sg.get('IpPermissions', []):
                from_port = perm.get('FromPort')
                to_port = perm.get('ToPort')
                ip_ranges = perm.get('IpRanges', [])
                
                if from_port is None or to_port is None:
                    continue
                
                # Check if 0.0.0.0/0 is configured
                is_open_to_world = any(r.get('CidrIp') == '0.0.0.0/0' for r in ip_ranges)
                
                if is_open_to_world:
                    for port in sensitive_ports:
                        if from_port <= port <= to_port:
                            open_sgs.append(f"{sg_name} ({sg_id}) [Port: {port}]")
                            break
                            
        if open_sgs:
            # removing duplicates
            unique_sgs = list(set(open_sgs))
            return {"check": "Security Groups", "status": "FAIL", "risk": "High", "details": f"Open to 0.0.0.0/0 on sensitive ports: {', '.join(unique_sgs)}"}
        else:
            return {"check": "Security Groups", "status": "PASS", "risk": "Low", "details": "No sensitive ports (22, 3389, DB ports) are completely open to the world."}
    except Exception as e:
        return {"check": "Security Groups", "status": "ERROR", "risk": "Unknown", "details": str(e)}