import json
import boto3
import boto3.session

def lambda_handler(event, context):
    body = {}
    body['list_backup_object'] = []
    session = boto3.session.Session()
    s3 = session.resource('s3',
        aws_access_key_id='ASIAVY4INUFHB7QYXC6F',
        aws_secret_access_key='D7M2KdcXVTyKV4U6OenqhfteN8vSuQimPUfgJafX',
        aws_session_token ='FwoGZXIvYXdzEPP//////////wEaDOThF5X7R3SOiVQIdSLNAUcZ/J5Ymkr0lTYeYNEck1V4vPPwR4TEdREuBRi63nqfqytTUSL7nZB0KyiiFeHSy7Ty9JpvFEsDzmIZYI2x7JflGV8u1vg/ebgkNlGEqkvKoz01kaRx51YlOM3hAqi/6kITROCvkuwRhIzLfhA4eJQ4haVUeW80Y2UQ59WoUcgTjjUBsXL+2U12JQGYLDcQhsoH0cFTNrfaz+ahHyCPsq+WgkocQGTaHky6O2BCD9HKiHmf2wMiHPiM/Eml/i1BpXIpAedNZsQzJ1l9oVko1ZudkwYyLebOV5YkN7/T6T9JXX7pTEOJUku+j5xjmMaxdmrj1eaSmMqFg1WYpg0xykRbkA=='
    )
    bucket1 = s3.Bucket('miebakso')
    for my_bucket_object in bucket1.objects.all():
        key = my_bucket_object.key
        copy_source = {
            'Bucket': 'miebakso',
            'Key': key
        }
        bucket2 = s3.Bucket('stockforum')
        bucket2.copy(copy_source, key)
        body['list_backup_object'].append(key)
    # copy_source = {
    #     'Bucket': 'miebakso',
    #     'Key': 'image1.png'
    # }
    # bucket2 = s3.Bucket('stockforum')
    # bucket2.copy(copy_source, 'image1.png')
    # body['list_backup_object'].append(key)

    print(body)
    body['status'] = 'Backup complete!'
    return {
        'statusCode': 200,
        'headers': {
        	'Content-Type': 'application.json'
        },
        'statusCode': 200,
        'body': json.dumps(body)
    }
   

lambda_handler('a','b')

	
