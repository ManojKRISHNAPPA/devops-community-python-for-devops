import boto3

# Initialize EC2 client
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    """
    Lambda function to list and delete all unused EBS volumes (state=available)
    """

    # 1️⃣ Describe all available volumes
    response = ec2.describe_volumes(
        Filters=[
            {
                'Name': 'status',
                'Values': ['available']  # only unused volumes
            }
        ]
    )

    # 2️⃣ Collect unused volume IDs
    unused_volumes = [vol['VolumeId'] for vol in response['Volumes']]

    deleted_volumes = []

    # 3️⃣ Delete each unused volume
    for volume_id in unused_volumes:
        try:
            ec2.delete_volume(VolumeId=volume_id)
            deleted_volumes.append(volume_id)
        except Exception as e:
            print(f"Failed to delete {volume_id}: {e}")

    # 4️⃣ Return result
    return {
        "statusCode": 200,
        "unused_volume_count": len(unused_volumes),
        "deleted_volumes_count": len(deleted_volumes),
        "deleted_volumes": deleted_volumes
    }