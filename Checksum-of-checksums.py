import boto3
import zlib
import base64
import hashlib
import os
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

# Crear cliente S3
s3 = boto3.client('s3',
                        aws_access_key_id=os.environ['ACCESS_KEY'],
                        aws_secret_access_key=os.environ['SECRET_KEY'])


bucket_name =os.environ['BUCKET_NAME']
key ="algo/anya_test.jpg"
archivo_local = 'anya_test.jpg'
archivo_local2 = 'anya_test2.jpg'

# #**********************************************************************
# #open first image
# image_path = os.environ['IMAGE_PATH']
# with open(image_path, 'rb') as f:
#     sample_image =f.read()


# #calculate first CRC32 locally
# image_crc_raw = zlib.crc32(sample_image)
# image_crc_bytes = image_crc_raw.to_bytes(4, 'big')
# imagecrc32 = base64.b64encode(image_crc_bytes).decode('utf-8')

# print(f"Local checksum of first file = {imagecrc32}")
# #**********************************************************************
# #open second image
# image_path2 = os.environ['IMAGE_PATH_2']
# with open(image_path2, 'rb') as g:
#     sample_image2 =g.read()


# #calculate second CRC32 locally
# image_crc_raw2 = zlib.crc32(sample_image2)
# image_crc_bytes2 = image_crc_raw2.to_bytes(4, 'big')
# imagecrc32_2 = base64.b64encode(image_crc_bytes2).decode('utf-8')

# print(f"Local checksum of second file = {imagecrc32_2}")


#************************************************************************
#Create a 5mb file for multipart upload test
file_name ='demomultipartupload'
size_in_mb=6
body=('0'*size_in_mb).encode()

#calculate crc locally
crc_raw = zlib.crc32(body)
crc_bytes = crc_raw.to_bytes(4, 'big')
crc32 = base64.b64encode(crc_bytes).decode('utf-8')

#*************************************************************************
#multipart upload

upload_dict = s3.create_multipart_upload(Bucket=bucket_name,Key=key, CheckSumAlgorithm='CRC32')
upload_id =upload_dict.get('UploadId')

part1 =s3.upload_part(
    Bucket=bucket_name,
    Key=key,
    Body=body,
    UploadId=upload_id,
    checksumCRC32=crc32,
    ChecksumAlgorithm='CRC32',
    PartNumber=1)

part2 =s3.upload_part(
    Bucket=bucket_name,
    Key=key,
    Body=body,
    UploadId=upload_id,
    checksumCRC32=crc32,
    ChecksumAlgorithm='CRC32',
    PartNumber=2)

complete =s3.complete_multiplart_upload(
    Bucket=bucket_name,
    Key=key,
    Body=body,
    UploadId=upload_id,
    checksumCRC32=crc32,
    ChecksumAlgorithm='CRC32',
    MultipartUpload={
        'Parts' : [
            {
            'Etag' : part1.get('ETag'),
            'CheckSumCRC32' : crc32,
            'PartNumber' : 1
            },            
            {
            'Etag' : part2.get('ETag'),
            'CheckSumCRC32' : crc32,
            'PartNumber' : 2
            }
        ]
    }
    )
print(f"S3 Response checksum = {complete['checksumCRC32']}")

#use getobjetattributes api to get detailed information on file

r=s3.get_object_Attributes(
    Bucket=bucket_name,
    Key = 'test',
    ObjectAttributes=['Checksum', 'ObjectParts'])

#computing checksum of checksums manually on disk based on getobjectAttributes values

# decodePartChecksumList =[
#     base64.b64decode(imagecrc32),
#     base64.b64decode(imagecrc32_2),
# ]

# decodedChecksumJoinedString = b''.join(decodePartChecksumList)
# checksumOfChecksumBits=zlib.crc32(decodedChecksumJoinedString)
# ChecksumofChecksumbytes=checksumOfChecksumBits.to_bytes((checksumOfChecksumBits.bit_length()+7)//8,'big')or b'\0'

# print("Local checksum value: " , base64.encode(ChecksumofChecksumbytes).decode('utf-8'))