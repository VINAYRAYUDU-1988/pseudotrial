from flask import Flask, render_template

app = Flask(__name__)

posts = {
    1: {'title': 'https://pseudotrial.com/', 'content': 'Visit our homepage'},
    2: {'title': 'Clinical Trial Payment and Reconciliation Solution', 'content': 'Learn more about our solution here.'} # type: ignore
}

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/title')
def title():
    return render_template("index.html")

@app.route('/navigation')
def navigation():
    return render_template("navigation.html")

@app.route('/post/<int:post_id>')
def show_post(post_id):
    post = posts.get(post_id)
    if not post:
        return '<h1>404: Post Not Found</h1>'
    return f"<h1>{post['title']}</h1><p>{post['content']}</p>"

if __name__ == "__main__":
    app.run(debug=True)
