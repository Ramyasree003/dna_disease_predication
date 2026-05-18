# main.py
import os
import base64
import io
import math
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import mysql.connector
import hashlib
import datetime
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from random import randint
from werkzeug.utils import secure_filename
from PIL import Image
import stepic
import urllib.request
import urllib.parse
import socket    
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import pickle
import csv
import codecs
from flask import (jsonify, request)
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import to_categorical

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="dna_disease"

)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = { 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####
@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM patient WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('pat_home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('web/index.html',msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM dn_admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('web/login.html',msg=msg)


@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM dn_patient WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('pat_home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('web/login_user.html',msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    mess=""
    email=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM dn_patient")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1

    if request.method=='POST':
        name=request.form['name']
        gender=request.form['gender']
        dob=request.form['dob']
        mobile=request.form['mobile']
        email=request.form['email']
        address=request.form['address']
        city=request.form['city']
        uname=request.form['uname']
        pass1=request.form['pass']

        mycursor.execute('SELECT count(*) FROM dn_patient WHERE uname = %s', (uname, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            sql = "INSERT INTO dn_patient(id,name,gender,dob,mobile,email,uname,pass,address,city) VALUES (%s,%s,%s,%s,%s, %s, %s, %s, %s, %s)"
            val = (maxid,name,gender,dob,mobile,email,uname,pass1,address,city)
            mycursor.execute(sql, val)
            mydb.commit()            

            msg="success"
        else:
            msg="fail"
       
    return render_template('web/register.html',msg=msg)



@app.route('/pat_home', methods=['GET', 'POST'])
def pat_home():
    msg=""
    data1=[]
    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM dn_patient WHERE uname = %s', (uname, ))
    data = cursor.fetchone()
    
        
    return render_template('pat_home.html',msg=msg, data=data)

@app.route('/view_patient', methods=['GET', 'POST'])
def view_patient():
    msg=""
    data1=[]
    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM dn_patient")
    data = cursor.fetchall()
    
        
    return render_template('view_patient.html',msg=msg, data=data)

@app.route('/pat_test', methods=['GET', 'POST'])
def pat_test():
    msg=""
    act=request.args.get("act")
    data1=[]
    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM dn_patient WHERE uname = %s', (uname, ))
    data = cursor.fetchone()
    
    if request.method=='POST':
        sequence=request.form['sequence']
        ff=open("static/dna.txt","w")
        ff.write(sequence)
        ff.close()
        act="load"

    if act=="result":
        ff=open("static/dna.txt","r")
        value=ff.read()
        ff.close()
        filename = 'static/dataset/Genome_Disease_Dataset.csv'
        df = pd.read_csv(filename, header=0)
        for drow in df.values:
            if drow[0]==value:
                data1.append(drow[1])
                data1.append(drow[2])
                data1.append(drow[3])
                data1.append(drow[4])
                data1.append(drow[5])
                data1.append(drow[6])
                data1.append(drow[7])
                data1.append(drow[8])
                data1.append(drow[9])
                
                break
    
        
    return render_template('pat_test.html',msg=msg,act=act,data=data,data1=data1)

@app.route('/test2', methods=['GET', 'POST'])
def test2():
    msg=""
    act=request.args.get("act")
    data1=[]
    if 'username' in session:
        uname = session['username']

    ff=open("static/dna.txt","r")
    value=ff.read()
    ff.close()
    
    print(value)
        
    return render_template('test2.html',msg=msg,act=act,value=value)

@app.route('/test5', methods=['GET', 'POST'])
def test5():
    msg=""
    act=request.args.get("act")
    data1=[]
    if 'username' in session:
        uname = session['username']

    ff=open("static/dna.txt","r")
    value=ff.read()
    ff.close()
    
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM dn_patient WHERE uname = %s', (uname, ))
    data = cursor.fetchone()

    import datetime
    now1 = datetime.datetime.now()
    rdate=now1.strftime("%d-%m-%Y")
    
    filename = 'static/dataset/Genome_Disease_Dataset.csv'
    df = pd.read_csv(filename, header=0)
    for drow in df.values:
        if drow[0]==value:
            data1.append(drow[1])
            data1.append(drow[2])
            data1.append(drow[3])
            data1.append(drow[4])
            data1.append(drow[5])
            data1.append(drow[6])
            data1.append(drow[7])
            data1.append(drow[8])
            data1.append(drow[9])
            
            break
        
    return render_template('test5.html',msg=msg,act=act,value=value,data=data,data1=data1,rdate=rdate)

@app.route('/test4', methods=['GET', 'POST'])
def test4():
    msg=""
    act=request.args.get("act")
    data1=[]
    if 'username' in session:
        uname = session['username']

    ff=open("static/dna.txt","r")
    value=ff.read()
    ff.close()
    
    print(value)
        
    return render_template('test4.html',msg=msg,act=act,value=value)

@app.route('/test_report', methods=['GET', 'POST'])
def test_report():
    msg=""
    act=request.args.get("act")
    tid=request.args.get("tid")
    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
    
    cursor.execute('SELECT * FROM test_data where id=%s',(tid,))
    pdata = cursor.fetchone()
    pat=pdata[1]
    cursor.execute('SELECT * FROM patient where uname=%s',(pat,))
    data1 = cursor.fetchone()

    
        
    return render_template('test_report.html',msg=msg, rs=pdata,data1=data1)



@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""
    
    return render_template('admin.html',msg=msg)


@app.route('/load_data', methods=['GET', 'POST'])
def load_data():
    msg=""
    cnt=0
    filename = 'static/dataset/dataset.csv'
    data1 = pd.read_csv(filename, header=0)
    data2 = list(data1.values.flatten())
    data=[]
    i=0
    sd=len(data1)
    rows=len(data1.values)
    
    #print(str(sd)+" "+str(rows))
    for ss in data1.values:
        cnt=len(ss)
        if i<200:        
            data.append(ss)
        i+=1
    cols=cnt
    #if request.method=='POST':
    #    return redirect(url_for('preprocess'))
    return render_template('load_data.html',data=data, msg=msg, rows=rows, cols=cols)

@app.route('/preprocess', methods=['GET', 'POST'])
def preprocess():
    msg=""
    mem=0
    cnt=0
    cols=0
    filename = 'static/dataset/dataset.csv'
    data1 = pd.read_csv(filename, header=0)
    data2 = list(data1.values.flatten())
    cname=[]
    data=[]
    dtype=[]
    dtt=[]
    nv=[]
    i=0
    
    sd=len(data1)
    rows=len(data1.values)
    
    #print(data1.columns)
    col=data1.columns
    #print(data1[0])
    for ss in data1.values:
        cnt=len(ss)
        

    i=0
    while i<cnt:
        j=0
        x=0
        for rr in data1.values:
            dt=type(rr[i])
            if rr[i]!="":
                x+=1
            
            j+=1
        dtt.append(dt)
        nv.append(str(x))
        
        i+=1

    arr1=np.array(col)
    arr2=np.array(nv)
    data3=np.vstack((arr1, arr2))


    arr3=np.array(data3)
    arr4=np.array(dtt)
    
    data=np.vstack((arr3, arr4))
   
    print(data)
    cols=cnt
    mem=float(rows)*0.75

    #if request.method=='POST':
    #    return redirect(url_for('feature_ext'))
    
    return render_template('preprocess.html',data=data, msg=msg, rows=rows, cols=cols, dtype=dtype, mem=mem)

def extract_features_and_plot(df):
    # Clean and extract
    df['Gene'] = df['Gene Variant / Mutation Identified'].str.split().str[0]
    df['DNA Change Type'] = df['Type of DNA Change'].str.strip()
    df['Implication'] = df['Implication'].str.strip()

    # Plot: Type of DNA Change count
    plt.figure(figsize=(10,5))
    df['DNA Change Type'].value_counts().plot(kind='bar', color='skyblue')
    plt.title('Distribution of DNA Change Types')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    #plt.savefig('static/graph.png')
    
@app.route('/feature', methods=['GET', 'POST'])
def feature():
    msg=""
    data=[]
    CSV_PATH = 'static/dataset/dataset.csv'
    filename = 'static/dataset/dataset.csv'
    df = pd.read_csv(filename, header=0)

    #extract_features_and_plot(df)
    
    implication_map = {
        "Protective effect": -1,
        "Carrier": 0,
        "Moderate risk": 0.5,
        "Increased risk": 1,
        "High predisposition": 2
    }

    # Load static CSV file
    df = pd.read_csv(CSV_PATH)

    # Feature engineering
    df['Implication_Score'] = df['Implication'].map(implication_map)

    # One-hot encoding
    encoded = pd.get_dummies(df[['Gene Variant / Mutation Identified',
                                 'Type of DNA Change',
                                 'Associated Disease / Risk']])
    final_df = pd.concat([encoded, df[['Implication_Score']]], axis=1)

    # Convert to HTML table
    table_html = final_df.to_html(classes='table table-striped table-bordered', index=False)

    # Plotly chart
    count_df = df['Implication_Score'].value_counts().reset_index()
    count_df.columns = ['Implication Score', 'Count']
    fig = px.bar(count_df, x='Implication Score', y='Count',
                 title='Distribution of Implication Scores',
                 labels={'Implication Score': 'Score', 'Count': 'Frequency'},
                 color='Implication Score')
    graph_html = fig.to_html(full_html=False)

    
    return render_template('feature.html',table_html=table_html, graph_html=graph_html)

#LSTM
def model():
    # Load data
    df = pd.read_csv("static/dataset/dataset.csv")

    # Map implication to categorical labels
    df['Implication_Label'] = LabelEncoder().fit_transform(df['Implication'])

    # One-hot encode categorical input features
    X = pd.get_dummies(df[['Gene Variant / Mutation Identified',
                           'Type of DNA Change',
                           'Associated Disease / Risk']])

    y = to_categorical(df['Implication_Label'])

    # Reshape for LSTM: (samples, timesteps, features)
    X_lstm = np.array(X).reshape((X.shape[0], 1, X.shape[1]))

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X_lstm, y, test_size=0.2, random_state=42)

    # LSTM model
    model = Sequential()
    model.add(LSTM(64, input_shape=(1, X.shape[1])))
    model.add(Dense(y.shape[1], activation='softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.summary()

    # Train
    model.fit(X_train, y_train, epochs=20, batch_size=8, validation_split=0.2)

    # Evaluate
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Test Accuracy: {accuracy:.2f}")

@app.route('/classify', methods=['GET', 'POST'])
def classify():
    msg=""
    data=[]
    f1=0
    f2=0
    file_path = "static/dataset/dataset.csv" 
    df = pd.read_csv(file_path)
    df['Gene'] = df['Gene Variant / Mutation Identified'].str.split().str[0]
    # Classification dictionary
    disease_categories = {
        "Alzheimer's Disease": 'Alzheimer',
        'Cystic Fibrosis':'Cystic Fibrosis',
        'Diabetes': 'Diabetes',
        
        'Pancreatic Cancer': 'Pancreatic Cancer',
        'Prostate Cancer': 'Prostate Cancer',
        'Hereditary Breast': 'Hereditary Breast',
        'Heart Disease': 'Heart Disease',
        
        'Obesity': 'Obesity',
        'Vitamin D Deficiency': 'Deficiency',        
        'Lactose Intolerance': 'Lactose'
    }

    # Apply classification
    df['Disease Category'] = df['Associated Disease / Risk'].map(disease_categories)

    # Plot Disease Category distribution
    plt.figure(figsize=(8,5))
    df['Disease Category'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    plt.title('Distribution of Disease Categories')
    plt.ylabel('')
    plt.tight_layout()
    #plt.savefig('static/disease_pie.png')
    plt.close()
    ######
    
    plt.figure(figsize=(10, 6))
    df['Disease Category'].value_counts().plot(kind='bar', color='coral')
    plt.title('Disease Category Distribution')
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    #plt.savefig('static/disease_bar.png')
    plt.close()
    #######
    implication_order = ['Protective effect', 'Carrier', 'Moderate risk', 'Increased risk', 'High predisposition']
    pivot = df.pivot_table(index='Disease Category', columns='Implication', aggfunc='size', fill_value=0)
    pivot = pivot[implication_order]  # Optional ordering
    pivot.plot(kind='bar', stacked=True, figsize=(12,6), colormap='Set3')
    plt.title('Implication per Disease Category')
    plt.ylabel('Number of Mutations')
    plt.xticks(rotation=45)
    plt.tight_layout()
    #plt.savefig('static/stacked_bar.png')
    plt.close()
    #####
    pivot = df.pivot_table(index='Gene', columns='Disease Category', aggfunc='size', fill_value=0)
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, cmap='YlGnBu', fmt='d')
    plt.title('Gene vs. Disease Category')
    plt.tight_layout()
    #plt.savefig('static/gene_disease_heatmap.png')
    plt.close()
    #########################
    
    implication_map = {
        'Protective effect': 0,
        'Carrier': 1,
        'Moderate risk': 2,
        'Increased risk': 3,
        'High predisposition': 4
    }
    df['DNA Length'] = df['DNA Sequence'].str.len()
    df['Implication Code'] = df['Implication'].map(implication_map)

    plt.figure(figsize=(10,6))
    sns.scatterplot(data=df, x='DNA Length', y='Implication Code', hue='Disease Category')
    plt.title('DNA Length vs. Risk Level')
    plt.tight_layout()
    #plt.savefig('static/dna_vs_risk.png')
    plt.close()
    
    
    #####################33
    '''file_path = "static/upload/datafile.csv"  # Update path if needed
    dff = pd.read_csv(file_path)
    rx=0
    ry=0
    rz=0
    for dn in dff.values:
        if dn[25]=="Low":
            rx+=1
        if dn[25]=="Moderate":
            ry+=1
        if dn[25]=="High":
            rz+=1
    values=[rx,ry,rz]
    gt=0
    if rx>ry and rx>rz:
        gt=rx+5
    elif ry>rz:
        gt=ry+5
    else:
        gt=rz+5
    doc=["Low Risk","Moderate","High"]
    fig = plt.figure(figsize = (10, 8))
     
    # creating the bar plot
    cc=['green','yellow','red']
    plt.bar(doc, values, color =cc,
            width = 0.4)
 

    plt.ylim((1,gt))
    plt.xlabel("Class")
    plt.ylabel("Count")
    plt.title("")

    rr=randint(100,999)
    fn="tclass.png"
    #plt.xticks(rotation=20)
    plt.savefig('static/'+fn)
    
    plt.close()'''

    
    return render_template('classify.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


