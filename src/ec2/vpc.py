class VPC:
    def __init__(self, client):
        self._client = client
        """ :type: pyboto3.ec2 """

    def create_vpc(self):
        return self._client.create_vpc(
            CidrBlock='10.0.0.0/16'
        )

    def add_name_tag(self, resource_id, resource_name):
        print('Adding resource name tag...!')
        self._client.create_tags(
            Resources=[resource_id],
            Tags=[{
                'Key': 'Name',
                'Value': resource_name
            }]
        )

    def create_igw(self):
        return self._client.create_internet_gateway()

    def attach_igw(self, igw_id, vpc_id):
        return self._client.attach_internet_gateway(
            InternetGatewayId=igw_id,
            VpcId=vpc_id
        )

    def create_subnet(self, vpc_id, cidr_block):
        return self._client.create_subnet(
            VpcId=vpc_id,
            CidrBlock=cidr_block
        )

    def create_route_table(self, vpc_id):
        return self._client.create_route_table(
            VpcId=vpc_id
        )

    def create_igw_route(self, rtb_id, igtw_id):
        return self._client.create_route(
            RouteTableId=rtb_id,
            GatewayId=igtw_id,
            DestinationCidrBlock='0.0.0.0/0'
        )

    def associate_subnet_routetb(self, subnet_id, rtb_id):
        return self._client.associate_route_table(
            SubnetId=subnet_id,
            RouteTableId=rtb_id
        )

    def auto_assign_ip_subnet(self, subnet_id):
        return self._client.modify_subnet_attribute(
            SubnetId=subnet_id,
            MapPublicIpOnLaunch={'Value': True}
        )