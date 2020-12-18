qaus321_cfg = {
    "BlockDeviceMappings": [
        {
            "DeviceName": "/dev/sda1",
            "Ebs": {
                "SnapshotId": "snap-0e51cf9f819e2454b"
            }
        }
    ],
    "ImageId": "ami-04443675a4021a357",
    "InstanceType": "m5.large",
    "KeyName": "sqad_ted",
    "MaxCount": 0,
    "MinCount": 0,
    "Monitoring": {
        "Enabled": True
    },
    "SecurityGroupIds": [
        "sg-06eed225148ad0625"
    ],
    "SubnetId": "subnet-06675fc5f9ae56080",
    "DryRun": False,
    "EbsOptimized": True,
    "InstanceInitiatedShutdownBehavior": "terminate",
    "TagSpecifications": [
        {
            "ResourceType": "instance",
            "Tags": [
                {
                    "Key": "Name",
                    "Value": "SQAD_dcd_tool"
                }
            ]
        },
        {
            "ResourceType": "volume",
            "Tags": [
                {
                    "Key": "Name",
                    "Value": "SQAD_dcd_tool_vol"
                }
            ]
        }
    ]
}

out_qaus321_cfg = {
    "BlockDeviceMappings": [
        {
            "DeviceName": "/dev/sda1",
            "Ebs": {
                "SnapshotId": "snap-0e51cf9f819e2454b"
            }
        }
    ],
    "ImageId": "ami-04443675a4021a357",
    "InstanceType": "m5.large",
    "KeyName": "SQAD_S1",
    "MaxCount": 0,
    "MinCount": 0,
    "Monitoring": {
        "Enabled": True
    },
    "SecurityGroupIds": [
        "sg-0c8dcd8606ece9f14"
    ],
    "SubnetId": "subnet-f343a2aa",
    "DryRun": False,
    "EbsOptimized": True,
    "InstanceInitiatedShutdownBehavior": "terminate",
    "TagSpecifications": [
        {
            "ResourceType": "instance",
            "Tags": [
                {
                    "Key": "Name",
                    "Value": "SQAD_jmeter_tool"
                }
            ]
        },
        {
            "ResourceType": "volume",
            "Tags": [
                {
                    "Key": "Name",
                    "Value": "SQAD_jmeter_tool_vol"
                }
            ]
        }
    ]
}

