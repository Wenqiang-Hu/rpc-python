import grpc
import key_value_store_pb2
import key_value_store_pb2_grpc
import logging
import sys
from datetime import datetime

def current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  

logging.basicConfig(level=logging.INFO)

def run():
    with grpc.insecure_channel('server:50051') as channel:
        stub = key_value_store_pb2_grpc.KeyValueStoreStub(channel)

        # Accept commands from arguments if provided
        if len(sys.argv) > 1:
            command = sys.argv[1].upper()
            if command == "PUT":
                key = sys.argv[2]
                value = sys.argv[3]
                response = stub.Put(key_value_store_pb2.PutRequest(key=key, value=value))
                print(f"{current_timestamp()} - PUT {key} status: {response.status} - {key} -> {value}\n", flush=True)

            elif command == "GET":
                key = sys.argv[2]
                response = stub.Get(key_value_store_pb2.GetRequest(key=key))
                print(f"{current_timestamp()} - GET {key} status: {response.status} - {key} -> {response.value}\n", flush=True)

            elif command == "DELETE":
                key = sys.argv[2]
                response = stub.Delete(key_value_store_pb2.DeleteRequest(key=key))
                print(f"{current_timestamp()} - DELETE {key} status: {response.status} \n", flush=True)
          
            else:
                print("{current_timestamp()} - Invalid command. Please enter PUT, GET, DELETE.")
        else:
            # Pre-populate the key-value store 
            logging.info("Pre-populated actions....")

            for i in range(5):
                response = stub.Put(key_value_store_pb2.PutRequest(key=f'key{i}', value=f'value{i}'))
                print(f"{current_timestamp()} - PUT {i} status: {response.status} - key{i} -> value{i}\n")

            for i in range(5):
                response = stub.Get(key_value_store_pb2.GetRequest(key=f'key{i}'))
                print(f"{current_timestamp()} - GET {i} status: {response.status} - key{i} -> {response.value}\n")

        
            for i in range(5):
                response = stub.Delete(key_value_store_pb2.DeleteRequest(key=f'key{i}'))
                print(f"{current_timestamp()} - DELETE {i} status: {response.status}\n")


if __name__ == '__main__':
    run()
