from src.ec2.vpc import VPC
from src.ec2.ec2 import EC2
from src.client_locator import EC2Client

def main():
    #VPC creation
    ec2_client = EC2Client().get_client()
    vpc = VPC(ec2_client)
    response = vpc.create_vpc()
    vpc_id = response['Vpc']['VpcId']
    print('VPC ==> ', str(response))
    igw_instance = vpc.create_igw()
    igw_id = igw_instance['InternetGateway']['InternetGatewayId']
    vpc.attach_igw(igw_id, vpc_id)
    #Add name tag
    vpc_name = 'VPC-Igw-sub-route'
    vpc.add_name_tag(vpc_id, vpc_name)

    pub_subnet_resp = vpc.create_subnet(vpc_id, '10.0.1.0/24')
    subnet_id = pub_subnet_resp['Subnet']['SubnetId']
    vpc.add_name_tag(subnet_id, 'Boto3-AWS')
    pub_routetable_resp = vpc.create_route_table(vpc_id)
    rtb_id = pub_routetable_resp['RouteTable']['RouteTableId']

    vpc.create_igw_route(rtb_id, igw_id)

    vpc.associate_subnet_routetb(subnet_id, rtb_id)

    vpc.auto_assign_ip_subnet(subnet_id)

    # Create a private subnet
    priv_response = vpc.create_subnet(vpc_id, '10.0.0.0/24')
    priv_subnet_id = priv_response['Subnet']['SubnetId']

    # Add name tag to private subnet
    vpc.add_name_tag(priv_subnet_id, 'Boto3-AWS')


    # EC2 Instances
    # Create a keypair
    ec2 = EC2(ec2_client)
    key_name = 'boto3-key'
    key_pair = ec2.create_key_pair(key_name)

    print('Key ==> ', str(key_pair))

    # Create security group
    pub_sec_grp = 'Boto-pub-sec-grp'
    secgrp_res = ec2.create_sec_grp(pub_sec_grp, 'Public Security group', vpc_id)
    scgrp_id = secgrp_res['GroupId']
    ec2.add_inbound_sg_rule(scgrp_id)

    user_data = """
                    #!/bin/bash
                    yum update -y
                    yum install httpd24 -y
                    service httpd start
                    chkconfig httpd on
                    echo "<html><body><h1> Hello from <b>Boto3</b></h1></body></html>" > /var/www/html/index.html
                """
    ec2.launch_ec2_instance('ami-00068cd7555f543d5', key_name, 1, 1, scgrp_id, subnet_id, user_data)

if __name__ == '__main__':
    main()