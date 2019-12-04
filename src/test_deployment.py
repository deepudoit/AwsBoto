from src.ec2.vpc import VPC
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

if __name__ == '__main__':
    main()