import grpc
from concurrent import futures
import time
import key_value_store_pb2
import key_value_store_pb2_grpc
import threading
import logging
import sys
from datetime import datetime

def current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

logging.basicConfig(level=logging.INFO)

class KeyValueStoreServicer(key_value_store_pb2_grpc.KeyValueStoreServicer):
    def __init__(self):
        self.store = {}
        self.lock = threading.Lock()

    def Put(self, request, context):
        with self.lock:
            self.store[request.key] = request.value
            logging.info(f"{current_timestamp()} - PUT request received: key={request.key}, value={request.value}")
        return key_value_store_pb2.PutResponse(status="SUCCESS")

    def Get(self, request, context):
        with self.lock:
            value = self.store.get(request.key, None)
            logging.info(f"{current_timestamp()} - GET request received: key={request.key}")
        if value:
            return key_value_store_pb2.GetResponse(value=value, status="FOUND")
        else:
            return key_value_store_pb2.GetResponse(value="", status="NOT_FOUND")

    def Delete(self, request, context):
        with self.lock:
            logging.info(f"{current_timestamp()} - DELETE request received: key={request.key}")
            if request.key in self.store:
                del self.store[request.key]
                return key_value_store_pb2.DeleteResponse(status="DELETED")
            else:
                return key_value_store_pb2.DeleteResponse(status="NOT_FOUND")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    key_value_store_pb2_grpc.add_KeyValueStoreServicer_to_server(KeyValueStoreServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("{current_timestamp()} - Server is starting and listening on port 50051")
    
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
