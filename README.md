# 與iis結合的上傳刪除網頁模組

##templages放置頁面
1.layout.html，放著網頁的框架，所有的頁面都會繼承他  
2.login.html，登入頁面，在import_config.py中可以自訂帳號密碼  
3.upload.html檔案上傳頁面，可以根據自訂的跟目錄列出可以上傳的檔案路徑  
4.delete.html檔案刪除頁面，上傳錯誤的檔案可以做刪除動作  

##static放置css樣式
1.stytle.css自訂各種不同標籤的樣式，其他頁面透過繼承layout.html達到頁面一致性  


##falsk_upload.py主程式

1.透過import_config.py，將相關的app.config引入，在後續可以直接使用  
```python
app = Flask(__name__)
#將config變量放在其他文件，並導入若在當前文件可以改為app.config.from_object(__name__)
app.config.from_object(import_config)
#導入其他環境變量，silent若沒有此變量也不報錯，給予這變量一個名稱
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
```
2.若有登入過，直接轉入上傳頁面，若沒有首頁直接轉入登入頁面(此時會在session做紀錄方便之後確認登入狀態)
```python
@app.route('/')
def show_entries():
    if "logged_in" not in session:
        session['logged_in']=None
    if session['logged_in']:
        return redirect(url_for('upload_file'))
    else:
        return redirect(url_for('login'))
```
3.登入頁面，比對與config的資料，錯誤在flash傳出錯誤
```python
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
    ```
4.登出直接移除session中的logged_in資料
5.上傳因程式碼較長，直接參閱檔案，主要步驟有  

  +  透過處理將跟目錄下的子目錄放到list中，並放到select標籤中
  +  查詢是否已登入，登入才可以坐上傳動作
  +  當檔案選擇後可以直接上傳，並透過js處理進度條
  +  並透過flash傳出相關的訊息
4.刪除頁面，列出全部的檔案目錄與檔案，可以選取相關檔案做刪除，刪除不會直接刪除會放到recycle資料夾避免誤刪
