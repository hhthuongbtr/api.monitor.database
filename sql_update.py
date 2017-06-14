#!/usr/bin/python
import pika
import os, time

routing_key = 'hello'

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
            return ""
        time.sleep(0.5)
        query = ''
        for i in range(queue_len):
            method_frame, header_frame, body = self.channel.basic_get(self.routing_key)
            if method_frame:
                query = query + body
                #clear messages from queue
                self.channel.basic_ack(method_frame.delivery_tag)
            else:
                print 'No message returned'
        #close BlockingConnection
        self.connection.close()
        return query

if __name__ == "__main__":
    query = RabbitMQQueue().push_current_query()
    if query:
        command = """mysql -uroot -proot monitor -h localhost -e "%s" """%(query)
        os.system(command)
 
