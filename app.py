from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
client =MongoClient('mongodb+srv://satish:Satish3648&@cluster0.eho7rsc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db =client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():

    bucket_receive =request.form['bucket_give']
    count =db.bucket.count_documents({})
    num =count +1
    doc ={
        'num':num,
        'bucket':bucket_receive,
        'done':0
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': 'Data is saved!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive =request.form['num_receive']
    db.bucket.update_one(
        {'num':int(num_receive) },
        { '$set':{'done':1 }}
    )
    return jsonify({'msg': 'Update iS Done!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.bucket.find({},{'_id': False}))
    return jsonify({'buckets': buckets_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)