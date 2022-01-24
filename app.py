from flask import Flask, render_template, request, session
import boto3

app = Flask(__name__)

# adding secret key to be able to utilize sessions
app.secret_key = 'super secret key'

# add bucket name
bucket_name = ""

# add folder name -- DONT FORGET TRAILING "/"
folder_name = ""

# add table name
table_name = ''

# init resources
region = 'us-east-1'
dynamodb = boto3.resource('dynamodb', region_name=region)
s3 = boto3.client("s3")


@app.route("/", methods=['post', 'get'])
@app.route("/index", methods=['post', 'get'])
def index():
    if request.method == "POST":
        try:
            img = request.files['img']
            filename = folder_name+img.filename
            if img:
                s3.put_object(
                    Bucket=bucket_name,
                    Body=img,
                    Key=filename
                )
                # saves filename in session so it can be referenced later on
                session['filename'] = filename
                return render_template("uploading.html")
        except Exception as e:
            return (str(e))
    return render_template("index.html")


@app.route("/uploading")
def uploading():
    return render_template("uploading.html")


@app.route("/display", methods=['GET', 'POST'])
def display():
    # identifies dynamoDB table we're querying from
    table = dynamodb.Table(table_name)

    # grabs full filename from upload
    filename = session.get('filename')
    # gets just the filename not the folder too
    pic_id = filename.split('/')[1]

    # queries based on filename and returns info to display
    response = table.get_item(Key={'pic_id': pic_id})

    age_low = response['Item']['age_low']
    age_high = response['Item']['age_high']
    response_Smile = response['Item']['response_Smile']
    response_Eyeglasses = response['Item']['response_Eyeglasses']
    response_Sunglasses = response['Item']['response_Sunglasses']
    response_Gender = response['Item']['response_Gender']
    response_Beard = response['Item']['response_Beard']
    response_Mustache = response['Item']['response_Mustache']
    response_EyesOpen = response['Item']['response_EyesOpen']
    response_MouthOpen = response['Item']['response_MouthOpen']
    face_id = response['Item']['face_id']

    return render_template('display.html', age_low=age_low, age_high=age_high, response_Smile=response_Smile,
                           response_Eyeglasses=response_Eyeglasses, response_Sunglasses=response_Sunglasses,
                           response_Gender=response_Gender, response_Beard=response_Beard,
                           response_Mustache=response_Mustache, response_EyesOpen=response_EyesOpen,
                           response_MouthOpen=response_MouthOpen, face_id=face_id)


if __name__ == '__main__':
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()
