# license-scan
Web application leveraging rekogntion, lambda, and S3 to scan face images and return pertinent information. This version only supports face scans but a later version can include text detection to pull information such as name, DoB, etc from the license. 

# Setup Steps

## Setup IDE
- Open up the code in your favorite IDE
- Create a venv in your IDE
- install the dependencies in your requirements.txt file using the “pip install -r requirements.txt”

## Setup AWS Env
- sam build
- sam deploy --guided

## Set up Flask App
- Update the “app.py” file with the bucket, folder, and DynamoDB table name output from the cloudformation deployment.
- Run “python app.py” to start the flask app

## Using App
- Navigate to the URL and upload a picture
- Wait a few seconds as the process takes place and click on the display tab to view the results
