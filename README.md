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
2.首頁直接轉入登入頁面，
