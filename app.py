from flask import Flask, redirect, url_for, render_template, request, session, send_file
from flask_sqlalchemy import SQLAlchemy
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import pandas as pd
import numpy as np
from pandas import DataFrame
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('wordnet')
from nltk.tokenize import punkt
from tkinter import _flatten
import io

app = Flask(__name__)
app.secret_key = "wearehappyhighlighter"

@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html", **locals())


@app.route("/submitGRE", methods=["GET", "POST"])
def submitGRE():
    if request.method == "POST":
        article = request.values["article"]
        gre_dict = pd.read_table('GRE_voc.txt', encoding='utf-8')
        del gre_dict["Unnamed: 2"]
        article_split = article.split("\n")
        sep_all = []
        for i in range(len(article_split)):
            sep_text = word_tokenize(article_split[i])
            sep_all.append(sep_text)
        sep = list(_flatten(sep_all))
        lemmatizer = WordNetLemmatizer()
        verb = []
        for i in range(len(sep)):
            verb.append(lemmatizer.lemmatize(sep[i], pos="v"))
        noun = []
        for i in range(len(sep)):
            noun.append(lemmatizer.lemmatize(verb[i], pos="n"))
        adjective = []
        for i in range(len(sep)):
            adjective.append(lemmatizer.lemmatize(noun[i], pos="a"))
        adverb = []
        for i in range(len(sep)):
            adverb.append(lemmatizer.lemmatize(adjective[i], pos="r"))
        result = DataFrame(adverb, columns=['word'], index=None)
        df_merge = pd.merge(gre_dict, result, how='inner', on=['word'])
        df_temp = df_merge.drop_duplicates()
        session["highlighter"] = df_temp.to_csv(encoding="utf_8_sig", index=False)
        return render_template("index.html", article=article, column_names=df_temp.columns.values, row_data=list(df_temp.values.tolist()), zip=zip)
    else:
        return render_template("index.html")

@app.route("/submitTOEFL", methods=["GET", "POST"])
def submitTOEFL():
    if request.method == "POST":
        article = request.values["article"]
        gre_dict = pd.read_table('toefl_voc.txt', encoding='utf-8')
        article_split = article.split("\n")
        sep_all = []
        for i in range(len(article_split)):
            sep_text = word_tokenize(article_split[i])
            sep_all.append(sep_text)
        sep = list(_flatten(sep_all))
        lemmatizer = WordNetLemmatizer()
        verb = []
        for i in range(len(sep)):
            verb.append(lemmatizer.lemmatize(sep[i], pos="v"))
        noun = []
        for i in range(len(sep)):
            noun.append(lemmatizer.lemmatize(verb[i], pos="n"))
        adjective = []
        for i in range(len(sep)):
            adjective.append(lemmatizer.lemmatize(noun[i], pos="a"))
        adverb = []
        for i in range(len(sep)):
            adverb.append(lemmatizer.lemmatize(adjective[i], pos="r"))
        result = DataFrame(adverb, columns=['word'], index=None)
        df_merge = pd.merge(gre_dict, result, how='inner', on=['word'])
        df_temp = df_merge.drop_duplicates()
        session["highlighter"] = df_temp.to_csv(encoding="utf_8_sig", index=False)
        return render_template("index.html", article=article, column_names=df_temp.columns.values, row_data=list(df_temp.values.tolist()), zip=zip)
    else:
        return render_template("index.html")

@app.route("/download", methods=["GET", "POST"])
def download():
    if "highlighter" in session:
        csv = session["highlighter"]
    else:
        return render_template("index.html")

    buf_str = io.StringIO(csv)
    # Create a bytes buffer from the string buffer
    buf_byt = io.BytesIO(buf_str.read().encode("utf-8"))

    # Return the CSV data as an attachment
    return send_file(buf_byt,
                     mimetype="text/csv",
                     as_attachment=True,
                     attachment_filename="your_highlighter.csv")


@app.route("/clear")
def clear():
    session.pop("highlighter", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
