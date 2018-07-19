import boto3
import re
import json, sys # Only used for manual testing

def GetZoneId(hosted_zone):
    client = boto3.client('route53')
    try:
        zoneId = client.list_hosted_zones_by_name(DNSName=hosted_zone,MaxItems='1')
        for zone in zoneId["HostedZones"]:
            zid = zone['Id']
            break
        # Regex remove /hostedzone/ string in the return of zid
        zid = re.sub('(/.*/)', '', zid)
    except Exception as e:
        print(e)
    else:
        return zid

def DeleteRecord(r53,zoneId,DNSName,HostedZone,PrivateIpAddress):
                try:
                    response = r53.change_resource_record_sets(
                        HostedZoneId=zoneId,
                        ChangeBatch={
                            'Comment': 'LambdaFunction',
                            'Changes': [
                                {
                                    'Action': 'DELETE',
                                    'ResourceRecordSet': {
                                        'Name': DNSName+'.'+HostedZone,
                                        'Type': 'A',
                                        'SetIdentifier': 'LambdaFunction',
                                        'Region': 'ap-southeast-2',
                                        "TTL": 300,
                                        'ResourceRecords': [
                                            {
                                                'Value': PrivateIpAddress
                                            }
                                        ]
                                    }
                                },
                            ]
                        }
                    )
                except Exception as e:
                    print("Unexpected error: %s" % e)
                else:
                    print("Complete")

def lambda_handler(context,event):
    instanceId = context['detail']['instance-id']
    # print(instanceId)
    # Define Filters
    filters=[
        {
            'Name': 'instance-id',
            'Values': [
                instanceId
            ]
        }
    ]
    # Define EC2 objects
    ec2 = boto3.resource('ec2', region_name='ap-southeast-2')
    # ec2_list = ec2.instances.all()
    ec2_list = ec2.instances.filter(Filters=filters)

    # Define Route53 object
    r53 = boto3.client('route53')

    # Define List from EC2Instance Class
    Ec2_Instance = []


    # Define Variables
    DNS_Name = ''
    Hosted_Zone = ''
    Private_Ip_Address = ''

    for instance in ec2_list:
        # print(instance.instance_id)
        if instance.tags:
            for tag in instance.tags:
                if tag['Key'] == "Hosted_Zone":
                    Hosted_Zone = (tag['Value'])
                elif  tag['Key'] == "DNS_Name":
                    DNS_Name = (tag['Value'])
                elif  tag['Key'] == "Private_IP_Address":
                    Private_Ip_Address = (tag['Value'])
            ZoneId = GetZoneId(Hosted_Zone)
            # Delete Record
            print("========= DELETING RECORD  ========\nHosted Zone: %s\nDNS Name: %s\nPrviate IP Address: %s" % (Hosted_Zone, DNS_Name,Private_Ip_Address))
            DeleteRecord(r53,ZoneId,DNS_Name,Hosted_Zone,Private_Ip_Address)
        else:
            print("Instance ID: %s has no tags" % (instance.instance_id))
            continue

if __name__ == '__main__':
    context = json.load( sys.stdin )
    lambda_handler(context)
