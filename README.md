# python
for testing python purposes
aws1.py - creates 3 instances
  createIns() - the only func here
main_task.py - does the main work
  getIds() - get all instances and their pub ip
  pingCheck() - checks ping for created domains
  testConn() - tcp test on 22 port
  stopIns() - stops random instance and prints its id
  createAMI() - create ami of stopped instance
  getOldAmi() - get all ami, if ami older than 7 days this will be printed
  termIns() - terminated stopped instance
  color() - prints all instances and colour them based on the current state
  httpCheck() - http check for domains + added google.com to make sure that it is working
