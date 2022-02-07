from os import environ
import os
import shutil
import requests
import tempfile
import nltk.data

from gevent.pywsgi import WSGIServer
from flask import Flask, after_this_request, render_template, request, send_file
from subprocess import call

from predict_certainty import CertaintyEstimator
#from certainty_estimator.predict_certainty import CertaintyEstimator
from tqdm import tqdm
#import csv


from transformers import (
    AdamW,
    T5ForConditionalGeneration,
    T5Tokenizer,
    get_linear_schedule_with_warmup
)



from transformers import AutoModelWithLMHead, AutoTokenizer

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['doc', 'docx', 'txt'])

app = Flask(__name__)


# Convert using Libre Office
def convert_file(output_dir, input_file):
    testArr = []
    nltk.data.path.append(os.path.dirname(__file__))
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    fp = open(input_file, 'r', encoding='utf-8-sig')
    data = fp.read()
    testArr = tokenizer.tokenize(data)
    

    #ZACH ADDED "TEST" BELOW TO CAPTURE MORE IN TESTING
    matchers = ['will','shall', 'must', 'is required', 'are required', 'should', 'requires','test']
    matching = [s for s in testArr if any(xs in s for xs in matchers)]
    #print(matching)
    

    #construct a CertaintyEstimator for sentence-level certainty
    sentence_estimator = CertaintyEstimator(task ='sentence-level',use_auth_token=False)
    allCertainties = sentence_estimator.predict(testArr)
    belowThreshold = []
    for i in range(len(testArr)):
    #print(a[i], findings[i])
        if allCertainties[i] < 4.2:
            belowThreshold.append(testArr[i])






    T5Path = os.path.dirname(__file__) + '/t5NASA'
    model = AutoModelWithLMHead.from_pretrained(T5Path,local_files_only=True)
    tokenizer = AutoTokenizer.from_pretrained(T5Path,local_files_only=True)
    
    propArr = ""
    for s in belowThreshold:
        #print('SENTENCE 1')
        #print('\n\n')
        test_sent = 'falsify: ' + s +' </s>'
        inputs = tokenizer.encode(test_sent, return_tensors="pt", max_length=512)
        #print('INPUTS IN 1')
        outputs = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
        #print('OUTPUTS OUT')
        #print(outputs)    
        currentPropSent =  ' '.join([tokenizer.decode(ids) for ids in outputs])
        #propArr = propArr + str([tokenizer.decode(ids) for ids in outputs])
        propArr = propArr + currentPropSent + '<br/>' + '\n\n'
    print(propArr)
    return propArr


    #return str(output_dir + " OUTPUT DIR" + str(testArr))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def api():
    work_dir = tempfile.TemporaryDirectory()
    file_name = 'document'
    input_file_path = os.path.join(work_dir.name, file_name)
    # Libreoffice is creating files with the same name but .pdf extension
    output_file_path = os.path.join(work_dir.name, file_name + '.pdf')

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file provided'
        file = request.files['file']
        if file.filename == '':
            return 'No file provided'
        if file and allowed_file(file.filename):
            file.save(input_file_path)

    if request.method == 'GET':
        url = request.args.get('url', type=str)
        if not url:
            return render_template('index.html')
        # Download from URL
        response = requests.get(url, stream=True)
        with open(input_file_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        del response
    
    fp = open(input_file_path, 'r', encoding='utf-8-sig')
    print(fp.read())

    testme = convert_file(work_dir.name, input_file_path)

    @after_this_request
    def cleanup(response):
        work_dir.cleanup()
        return response
 
    return testme


#if __name__ == "__main__":
#    http_server = WSGIServer(('', int(os.environ.get('PORT', 8080))), app)
#    http_server.serve_forever()

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)