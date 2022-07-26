# working kiran
# https://github.com/shubhamc183/way2sms
# Username - 7743939980
# Pass - sshubhamm

import way2sms

for x in range(1):
	print(x) 

	q=way2sms.Sms('7743939980','sshubhamm') #username = 1234567890
	# kiran '8108412112', abhijit '9359082883', shubham '8983930994' 
	q.send('7743939980','Hi, how are you today? Someone is trying to open your door now') #receiver ph no.:0987654321, message=hello
	# n=q.msgSentToday()
	q.logout()

