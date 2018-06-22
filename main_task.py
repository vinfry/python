import boto3
import socket
import subprocess
import datetime
from termcolor import colored
import requests
import random

ec2 = boto3.resource('ec2', region_name='eu-west-1')

def getIds(): # get instance ids + their ips
	ids = []
	ips = []
	instances = ec2.instances.filter(Filters=[{'Name': 'tag:Name', 'Values': ['test_evgeniy']}])
	for instance in instances:
		ids.append(instance.id)
		ips.append(instance.public_ip_address)
#		print(instance.id, instance.instance_type, instance.tags)
	print("We own the following instances:", ids)
	print("With the following IPs:", ips, '\n')
getIds()

def pingCheck(): # ping test, !requires admin rights!
	domains = ("a.ridis.gq", "b.ridis.gq", "c.ridis.gq")
	for domain in domains:
		print("Checking ping for: ", domain)
		proc = subprocess.Popen(['ping', '-c', '1', domain],stdout=subprocess.PIPE)
		stdout, stderr = proc.communicate()
		print('ping output for domain:', domain)
		print(stdout.decode('ASCII'))
pingCheck()

def testConn(): # tcp test on 22 port
	ids = []
	ips = []
	instances = ec2.instances.filter(Filters=[{'Name': 'tag:Name', 'Values': ['test_evgeniy']}])
	for instance in instances:
		ids.append(instance.id)
		ips.append(instance.public_ip_address)
	for ip in ips:
		try:
			print("Checking ping for: ", ip)
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(1)
			s.connect((ip, 22))
			print ("tcp on port 22 for", ip, "successful")
		except:
			print(ip, 'is down')
testConn()

def stopIns(): # stops random instance
	ids = []
	out = []
	instances = ec2.instances.filter(Filters=[{'Name': 'tag:Name', 'Values': ['test_evgeniy']}])
	for instance in instances:
		if instance.state["Name"] == "running":
			ids.append(instance.id)
	L = len(ids)
	print("\nYou have", L, "instances running \n")
	N = range(1, L)
	RM = random.choice(N)
	print("Stopping random instance \n")
	unlucky = ids[RM]
	out.append(unlucky)
	ec2.instances.filter(InstanceIds=out).stop()
	print("it will  be ", unlucky)
	print("\ninstance is stopping\n")
	instance.wait_until_stopped()
stopIns()

def createAMI(): # create ami from stopped instance
	create_time = datetime.datetime.now()
	create_fmt = create_time.strftime('%Y-%m-%d')
	instances = ec2.instances.filter(Filters=[{'Name': 'tag:Name', 'Values': ['test_evgeniy']}])
	ids = []
	for instance in instances:
		if instance.state["Name"] == "stopped":
			ids.append(instance.id)
			boto3.client('ec2', region_name='eu-west-1').create_image(InstanceId=instance.id, Name="Evgeniy's " + instance.id + '_' + create_fmt, Description='evgenys AMI of instance ' + instance.id, NoReboot=True, DryRun=False)
	print("Created backup of ", ids)
	
createAMI()

def getOldAmi(): # get all amis and if ami older than 7 days this will be indicated
	ec2 = boto3.resource('ec2', region_name='eu-west-1')
	images = ec2.images.filter(Owners=["self"])
	#date = datetime.datetime.now()
	for image in images:
		created_at = datetime.datetime.strptime(image.creation_date, "%Y-%m-%dT%H:%M:%S.000Z")
		if created_at > datetime.datetime.now() - datetime.timedelta(7):
			print (image.id, 'is fine')
		else:
			print (image.id, 'is folder than 7 days')
getOldAmi()

def termIns():
	ec2 = boto3.resource('ec2', region_name='eu-west-1')
	instances = ec2.instances.filter(Filters=[{'Name': 'tag:Name', 'Values': ['test_evgeniy']}])
	ids = []
	for instance in instances:
		if instance.state["Name"] == "stopped":
			ids.append(instance.id)
			print('terminating ', ids)
			ec2.instances.filter(InstanceIds=ids).terminate()
termIns()
			
def color(): # shows all instances under my tag in colored style (i hope so)
	ec2 = boto3.resource('ec2', region_name='eu-west-1')
	instances = ec2.instances.filter(Filters=[{'Name': 'tag:Name', 'Values': ['test_evgeniy']}])
	for instance in instances:
		if instance.state["Name"] == "running":
			print("{0} instance is running\nIts IP is {1}\n".format(colored(instance.id, 'green'), colored(instance.public_ip_address, 'white')))
		if instance.state["Name"] == "stopped":
			print("{0} instance is stopped\n".format(colored(instance.id, 'red')))
		if instance.state["Name"] == "terminated":
			print("{0}, instance is terminated\n".format(colored(instance.id, 'yellow')))
color()

def httpCheck(): # checking http , added google.com to make sure that function is working
	domains = ('a.ridis.gq', 'b.ridis.gq', 'c.ridis.gq', 'google.com')
	for domain in domains:
		try:
			print("trying domain ", domain)
			response = requests.get('http://' + domain)
			response.raise_for_status()
			print("Status code: ", response.status_code)
		except requests.exceptions.ConnectionError as err:
			print('Oops. HTTP Error occured for ', domain,'\n')
			pass
			
httpCheck()