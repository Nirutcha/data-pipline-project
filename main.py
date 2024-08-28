from flask import Flask, request, render_template
from google.cloud import storage
from google.api_core.exceptions import NotFound

app = Flask(__name__)

# Initialize the Google Cloud Storage client
storage_client = storage.Client()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get the bucket name from the form input
        bucket_name = request.form['bucket_name']
        
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']
        
        if file.filename == '':
            return 'No selected file'
        
        if file and bucket_name:
            try:
                # Attempt to get the bucket, which will raise an exception if it does not exist
                bucket = storage_client.get_bucket(bucket_name)
                
                # Upload the file to the specified GCS bucket
                blob = bucket.blob(file.filename)
                blob.upload_from_file(file)
                return f'File {file.filename} uploaded to {bucket_name}.'
            except NotFound:
                return "This GCS Bucket Name does not exist."
            except Exception as e:
                return f'An error occurred: {str(e)}'
    
    return render_template('app.html')

if __name__ == '__main__':
    # Ensure the environment variable for the GCS service account key is set
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/service-account-file.json'
    app.run(debug=True)
