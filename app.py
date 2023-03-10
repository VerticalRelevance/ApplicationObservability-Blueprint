import os.path

import aws_cdk

from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    App, Stack
)

from constructs import Construct

dirname = os.path.dirname(__file__)


class EC2InstanceStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # VPC
        vpc = ec2.Vpc(self, "VPC",
                      nat_gateways=0,
                      subnet_configuration=[ec2.SubnetConfiguration(name="public", subnet_type=ec2.SubnetType.PUBLIC)]
                      )

        # AMI
        ubuntu_server_20_04_linux = ec2.MachineImage.generic_linux(
            {'us-east-1': 'ami-0b93ce03dcbcb10f6'}
        )


        # Instance Role and SSM Managed Policy
        role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AWSXrayFullAccess"))

        # Instance
        instance = ec2.Instance(self, "DjangoInstanceTarget",
                                instance_type=ec2.InstanceType("t3.medium"),
                                machine_image=ubuntu_server_20_04_linux,
                                vpc = vpc,
                                role = role
                                )
        #Xray Port
        instance.connections.allow_from_any_ipv4(ec2.Port.tcp(2000))
        instance.connections.allow_from_any_ipv4(ec2.Port.udp(2000))

        #Django Port
        instance.connections.allow_from_any_ipv4(ec2.Port.tcp(8000))

        #User data for Ubunutu Server 20.04
        instance.add_user_data('sudo apt update');
        instance.add_user_data('sudo apt install -y python3-pip unzip');
        instance.add_user_data('pip3 install opentelemetry-instrumentation-django');
        instance.add_user_data('pip3 install django');
        instance.add_user_data('pip3 install aws_xray_sdk');

        instance.add_user_data('export DJANGO_SETTINGS_MODULE="pollme.settings"');
        instance.add_user_data('cd ~');
        instance.add_user_data('wget https://s3.us-east-2.amazonaws.com/aws-xray-assets.us-east-2/xray-daemon/aws-xray-daemon-linux-3.x.zip');
        instance.add_user_data('unzip aws-xray-daemon-linux-3.x.zip');
        instance.add_user_data('./xray -o -n us-east-1 &');

        instance.add_user_data('git clone git@github.com:VerticalRelevance/ApplicationObservability-Blueprint.git');
        instance.add_user_data('cd ~/ApplicationObservability-Blueprint/Django-Poll-App');
        instance.add_user_data('python3 manage.py runserver 0.0.0.0:8000 --noreload &')

        instance.add_user_data('cd ~/ApplicationObservability-Blueprint')
        instance.add_user_data('python3 LoadScriptDjango.py &')


env_USA = aws_cdk.Environment(account="XXXXXXXXXXXX", region="us-east-1")

app = App()
EC2InstanceStack(app, "django-instance", env=env_USA)

app.synth()
