#!/usr/bin/python
import pika
import os

routing_key = 'hello'
tmpdir = '/tmp/inprocess.sql'

class File:
    def __init__(self):
        self.inprocess=tmpdir
        if not os.path.exists(self.inprocess):
            command="echo '\n' >"+self.inprocess
            os.system(command)
    def append(self, text):
            f = open(self.inprocess, 'a')
            f.write(text+"\n")
            f.close()

class RabbitMQQueue:
    def __init__(self):
        self.routing_key = routing_key
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.queue = self.channel.queue_declare(queue=self.routing_key)

    def push_current_query(self):
        queue_len = self.queue.method.message_count
        if not queue_len:
            #close BlockingConnection
            self.connection.close()
            return False
        for i in range(queue_len):
            method_frame, header_frame, body = self.channel.basic_get(self.routing_key)
            if method_frame:
                File().append(body)
                #clear messages from queue
                self.channel.basic_ack(method_frame.delivery_tag)
            else:
                print 'No message returned'
        #close BlockingConnection
        self.connection.close()
        return True
if __name__ == "__main__":
    command = "cat /dev/null > %s"%(tmpdir)
    os.system(command)
    if RabbitMQQueue().push_current_query():
        command = "mysql -uroot -proot monitor -h localhost < %s"%(tmpdir)
        os.system(command)
 
