# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, get_flashed_messages
import os,re
from contextlib import closing
import import_config
import shutil


app = Flask(__name__)
#將config變量放在其他文件，並導入若在當前文件可以改為app.config.from_object(__name__)
app.config.from_object(import_config)
#導入其他環境變量，silent若沒有此變量也不報錯，給予這變量一個名稱
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


folders = []
#將跟目錄下的目錄作為列表
folders.append("/")
for folder in os.listdir(app.config['UPLOAD_FOLDER']):
    if re.search('\.',folder)==None:
        folders.append(folder)



def s_filename(filename):
    assert re.search('\w+\.\w+',filename)!=None
    return filename


@app.route('/')
def show_entries():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('upload_file'))
    return render_template('login.html', error=error)



@app.route("/loguot")
def logout():
    session.pop("logged_in",None)
    flash("You were logged out")
    return redirect(url_for('login'))


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
      if session['logged_in']:
        if request.method == 'POST':
            # 檢查是否有檔案
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']

            # 如果沒有檔案秀出錯誤訊息
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            #儲存目錄，o_path為選擇到的目錄
            o_path = str(request.form['comp_select'])
            #因前面把跟目錄取代為/符號，這邊改變回去
            if o_path =='/':
                path  = app.config['UPLOAD_FOLDER']
            #這邊將選取的目錄，加上絕對位置
            else:
                path = app.config['UPLOAD_FOLDER']+'/'+o_path
            #如果有檔案在且儲存目錄也不是為空值，做存檔動作

            if file and path :
                filename = s_filename(file.filename)
                file.save(os.path.join(path, filename))
                #存檔完畢轉回上傳頁
                flash("Sucessfully!!")
                return redirect(url_for('upload_file'))
        return render_template("upload.html",folders =folders )


@app.route('/delete', methods=['GET', 'POST'])
def delete_file():

       file_path= []
       path  = app.config['UPLOAD_FOLDER']
       for dirPath, dirNames, fileNames in os.walk(path):
           file_path.append(dirPath)
           for f in fileNames:
               file_path.append(os.path.join(dirPath, f))
       if request.method == 'POST':
         remove_file = str(request.form['comp_select'])

         if os.path.exists("C:/recycle")!=True:
             os.mkdir("C:/recycle")
         shutil.move(remove_file,"C:/recycle")

         return redirect(url_for('delete_file'))
       return render_template('delete_page.html',folders = file_path)

if __name__ =="__main__":

    app.debug = True

    app.run()
