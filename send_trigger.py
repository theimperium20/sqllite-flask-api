import email_to
import sys

f = open('changes.txt')
data = f.read().split(',')
f.close()
server = email_to.EmailServer('smtp.mail.com', 587, 'devicesatminance@mail.com', 'minance@123')
send_to = data[1]
name = data[0]

server.quick_email(send_to, 'Device Associated/Disassociated',
                   ['# Hello {}, There is a change in the devices associated with your account. Contact administrator for more details'.format(name)],
                   style='h1 {color: blue}')
sys.exit()


