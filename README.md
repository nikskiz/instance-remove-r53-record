# README #

### What is this repository for? ###

* Lambda function written in python3 which removes route53 zone based on instance tags.
* The purpose is to target dynamic private instances, where the private IP will be removed in the specified Route53 zone based on a shutdown event.
* This attempts to have a sanitize DNS Zone, used inconjuction with instance_add_r53_record
* Version 1

### How do I get set up? ###

#### Summary of set up ####
* Python script will utilize the following modules
      * boto3 - Used for querying the AWS API
      * Json, sys - Only used for manual execution via cli not AWS Lambda
      * re - Regex in python
#### Configuration ####
* Create lambda using Python Version 3.6
* In AWS setup a Lambda function, ensure the following permissions:
    * EC2 - Describe permissions
    * Cloudwatch - create groups and streams. Put logs
    * Route53 Update record
* Create a cloudwatch rule to trigger the event when a instance is in a terminated state
* Ensure instances are tagged with `Hosted_Zone: Value`, `DNS_Name: Value`, `Private_Ip_Address: Value`
    * DNS_Name - The name of the dns record i.e docker-cluster-1
    * Hosted_Zone - The Zone Name in route53 - i.e private.company.com
    * Private_Ip_Address -The private IP associated to the instance - 172.16.18.5
* create a test with the following json. You can replace the instance Id's with your own.
```json
{
  "version": "0",
  "id": "f74e985d-c3ff-415d-b5fa-d3614c5e3434",
  "detail-type": "EC2 Instance State-change Notification",
  "source": "aws.ec2",
  "account": "123456789012",
  "time": "2015-11-11T21:36:48Z",
  "region": "us-east-1",
  "resources": [
    "arn:aws:ec2:us-east-1:123456789012:instance/i-123456789"
  ],
  "detail": {
    "instance-id": "i-123456789",
    "state": "terminated"
  }
}
```
* Configure lambda timeout 30 Seconds
#### Dependencies ####
* N/A
* How to run tests
  * Tests can be performed via linux CLI. Ensure the modules exampled above are installed. To run a test perform the following. `cat example_event.json| python3 main.py`
* Deployment instructions
  * Ensure tests are performed to the develop branch first, or checkout master in your own branch. Once tested, merge to master. Please ensure to create tags with each release to master.

### Who do I talk to? ###

* Repo owner or admin
* Nikola Sepentulevski
