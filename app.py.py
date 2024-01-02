from flask import Flask, render_template, redirect, request
from flask_pymongo import PyMongo
from flask_cors import CORS
import base64
import pymongo
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key' 
uri = "mongodb+srv://admin:admin123@cluster0.lexpcdj.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
db = client['project']
mydb = db['username']
class UploadForm(FlaskForm):
    image = FileField('Image', validators=[FileRequired()])
    document = FileField('Document', validators=[FileRequired()])
    description = StringField('Description')

@app.route('/', methods=['POST', 'GET'])
def upload():
    form = UploadForm()
    if request.method == 'POST':
      if form.validate_on_submit():
         if form.validate_on_submit():
            image = form.image.data
            file = form.document.data
            description = form.description.data
         if image.filename == '':
            print('empty')
            return redirect(request.url)

         if file.filename == '':
            mydb.insert_one({'document': 'NO FILE TO DISPLAY','image': encoded_data, 'description': description})
            return render_template('project.html',form=form)
         else:
              image_data = image.read()
              description = request.form['description']
              encoded_data = base64.b64encode(image_data).decode()
              file_data = file.read()
              encoded_data1 = base64.b64encode(file_data).decode()
              mydb.insert_one({'document': encoded_data1, 'description': description,'image': encoded_data})

         return 'Document and image upload successful.'
    return render_template('project.html',form=form)

@app.route('/display')
def display():
    documents = mydb.find({'$or': [{'image': {'$exists': True}}, {'document': {'$exists': True}}]})
    imagelist = []
    for document in documents:
        description = document.get('description', 'No description available')
        imagelist.append({
            'description': description,
            'image': document.get('image'),
            'document': document.get('document')
        })
    return render_template('display.html', imagelist=imagelist)
    

if __name__ == '__main__':
    app.run(port=5000)
