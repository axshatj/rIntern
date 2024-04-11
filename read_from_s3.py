import boto3
from PyPDF2 import PdfReader
from io import BytesIO
import textract

class S3PDFExtractor:
    def __init__(self, bucket_name, folder_prefix=''):
        self.bucket_name = bucket_name
        self.folder_prefix = folder_prefix
        client = boto3.client('s3')

    def extract_text_from_pdf(self, pdf_file):
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=self.bucket_name, Key=pdf_file)
        pdf_data = response['Body'].read()
        pdf_reader = PdfReader(BytesIO(pdf_data))
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

    def list_pdf_files(self):
        s3_client = boto3.client('s3')
        try:
            response = s3_client.list_objects_v2(Bucket=self.bucket_name)
            pdf_files = []
            for obj in response['Contents']:
                key = obj['Key']
                if key.endswith('.pdf'):
                    pdf_files.append(key)

            return pdf_files

        except Exception as e:
            # print("Error listing PDF files in S3 bucket:", str(e))
            return None
