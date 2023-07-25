from flask import Flask, render_template, request

app = Flask(__name__)

# Hardcoded reader list
reader_list = ["apple", "banana", "orange", "grape", "watermelon"]

def check_words_in_reader_list(text_words):
    return [word for word in text_words if word in reader_list]

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        text = uploaded_file.read().decode("utf-8")
        text_words = text.split(",")
        matching_words = check_words_in_reader_list(text_words) #function call to get the correct words
        return render_template("result.html", words=matching_words)
    return render_template("form2.html")

if __name__ == "__main__":
    app.run(debug=True)
