import boto3
import textract

class S3PDFExtractor:
    def __init__(self, bucket_name, folder_prefix=''):
        self.bucket_name = bucket_name
        self.folder_prefix = folder_prefix

    def list_pdf_files(self):
        s3_client = boto3.client('s3')
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=self.bucket_name, Prefix=self.folder_prefix)
        pdf_files = []
        for page in pages:
            for obj in page['Contents']:
                key = obj['Key']
                if key.endswith('.pdf'):
                    pdf_files.append(key)
        return pdf_files

    def extract_text_from_pdf(self, pdf_filename):
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=self.bucket_name, Key=pdf_filename)
        text = textract.process(response['Body'], method='pdftotext')
        return text.decode('utf-8')

