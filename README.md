# Highlighter
Text Mining and Flask Web Application

This is an application helping students who speak Mandarin to prepare GRE and TOEFL tests. 
It uses pandas and nltk packages to scan 7,000 GRE and TOEFL words in the articles which provided by users, and output the vocabulary lists with meanings. 
Users can download the list into Excel file. 

**Sample Image**
![alt text](https://github.com/yichiehyang/Highlighter/blob/b0e55c0c91402774643613206eec3576b3625be1/Highlighter_sample.png?raw=true)
### Packages
There are two packages that users need to download first. 
>import nltk   
>nltk.download('punkt')    
>nltk.download('wordnet')    

If you have already download these two packages, you can comment those two lines in the app.py.
If not, the first time you run the app.py, it will download by itself.

### How to run the code
1. First download the folder to your computer
2. Get in the terminal and open the folder
3. Type "python app.py" to run the server
4. Open this link: http://127.0.0.1:5000/
