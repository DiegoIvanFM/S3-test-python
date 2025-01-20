from dotenv import load_dotenv
import boto3
import os
#load .env variables

load_dotenv()

def upload_file(client):
    filename = "anya_test.jpg"
    bucket_name =os.environ['BUCKET_NAME']
    key = "algo/anya_test.jpg"
    client.upload_file(filename, bucket_name, key,)
    print('file uploaded!!!')

def download_file(client):
    filename = "anya_test_downloaded.jpg"
    bucket_name =os.environ['BUCKET_NAME']
    key = "algo/anya_test.jpg"
    with open(filename, 'wb') as data:
        client.download_fileobj(bucket_name, key, data)
    print('file downloaded!!!')

if __name__=="__main__":
    print ("key_id: ", os.environ['ACCESS_KEY'])
    print ("secret_key_id: ", os.environ['SECRET_KEY'])
    print ("bucket: ", os.environ['BUCKET_NAME'])
    client =boto3.client('s3',
                        aws_access_key_id=os.environ['ACCESS_KEY'],
                        aws_secret_access_key=os.environ['SECRET_KEY'])
    
    #upload_file(client)
    download_file(client)