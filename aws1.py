import boto3
print('all ok')

ec2 = boto3.resource('ec2', region_name='eu-west-1')
tags = [{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'test_evgeniy'}]}]
	
def createIns():
	my_ids = []
#	instances = ec2.create_instances(MinCount=3, MaxCount=3, ImageId='ami-6a4aa80d', InstanceType='t2.micro', TagSpecifications=tags)
	instances = ec2.create_instances(MinCount=3, MaxCount=3, ImageId='ami-7c491f05', InstanceType='t2.micro', TagSpecifications=tags)
	for instance in instances:
		instance.wait_until_running()
		instance.reload()
		my_ids.append(instance.id)
	print(my_ids)

createIns()	


#ec2.instances.filter(InstanceIds=ins).stop()
#ec2.instances.filter(InstanceIds=ins).terminate()
