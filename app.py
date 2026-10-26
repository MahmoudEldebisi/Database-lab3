import glob
import os

import mysql.connector
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "lab3-library"
UPLOAD_DIR = os.path.join(app.static_folder, "uploads")
ALLOWED = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "King2020"),
        database="library",
    )


def run(sql, params=(), fetch=False):
    """Run one SQL statement. Returns rows (fetch) or the last inserted id."""
    conn = get_db()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params)
        if fetch:
            return cur.fetchall()
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


# ---------- bonus: images (stored as static/uploads/book_<id>.ext, no schema change)
def image_url(kind, item_id):
    files = glob.glob(os.path.join(UPLOAD_DIR, f"{kind}_{item_id}.*"))
    if not files:
        return None
    return url_for("static", filename="uploads/" + os.path.basename(files[0]))


def delete_image(kind, item_id):
    for f in glob.glob(os.path.join(UPLOAD_DIR, f"{kind}_{item_id}.*")):
        os.remove(f)


def save_image(kind, item_id, file):
    if not file or not file.filename:
        return
    ext = os.path.splitext(file.filename)[1].lower()
    if ext in ALLOWED:
        delete_image(kind, item_id)
        file.save(os.path.join(UPLOAD_DIR, f"{kind}_{item_id}{ext}"))


app.jinja_env.globals["image_url"] = image_url


# ---------- F2.1 show both tables
@app.route("/")
def index():
    books = run("SELECT * FROM book", fetch=True)
    authors = run("SELECT * FROM author", fetch=True)
    return render_template("index.html", books=books, authors=authors)


# ---------- F2.2 / F2.3 books
@app.route("/book/add", methods=["GET", "POST"])
def add_book():
    authors = run("SELECT author_id, name FROM author", fetch=True)
    if request.method == "POST":
        try:
            new_id = run(
                "INSERT INTO book (title, price, author_id) VALUES (%s, %s, %s)",
                (request.form["title"], request.form["price"], request.form["author_id"]),
            )
            save_image("book", new_id, request.files.get("image"))
            flash("Book added.")
            return redirect(url_for("index"))
        except mysql.connector.Error as e:
            flash(f"Database error: {e}")
    return render_template("book_form.html", book=None, authors=authors)


@app.route("/book/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
    authors = run("SELECT author_id, name FROM author", fetch=True)
    rows = run("SELECT * FROM book WHERE book_id = %s", (book_id,), fetch=True)
    if not rows:
        flash("Book not found.")
        return redirect(url_for("index"))
    if request.method == "POST":
        try:
            run(
                "UPDATE book SET title = %s, price = %s, author_id = %s WHERE book_id = %s",
                (request.form["title"], request.form["price"],
                 request.form["author_id"], book_id),
            )
            save_image("book", book_id, request.files.get("image"))
            flash("Book updated.")
            return redirect(url_for("index"))
        except mysql.connector.Error as e:
            flash(f"Database error: {e}")
    return render_template("book_form.html", book=rows[0], authors=authors)


# ---------- F2.4 remove a book
@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    run("DELETE FROM book WHERE book_id = %s", (book_id,))
    delete_image("book", book_id)
    flash("Book removed.")
    return redirect(url_for("index"))


# ---------- F2.2 / F2.3 authors
@app.route("/author/add", methods=["GET", "POST"])
def add_author():
    if request.method == "POST":
        try:
            new_id = run(
                "INSERT INTO author (name, country) VALUES (%s, %s)",
                (request.form["name"], request.form["country"]),
            )
            save_image("author", new_id, request.files.get("image"))
            flash("Author added.")
            return redirect(url_for("index"))
        except mysql.connector.Error as e:
            flash(f"Database error: {e}")
    return render_template("author_form.html", author=None)


@app.route("/author/<int:author_id>/edit", methods=["GET", "POST"])
def edit_author(author_id):
    rows = run("SELECT * FROM author WHERE author_id = %s", (author_id,), fetch=True)
    if not rows:
        flash("Author not found.")
        return redirect(url_for("index"))
    if request.method == "POST":
        try:
            run(
                "UPDATE author SET name = %s, country = %s WHERE author_id = %s",
                (request.form["name"], request.form["country"], author_id),
            )
            save_image("author", author_id, request.files.get("image"))
            flash("Author updated.")
            return redirect(url_for("index"))
        except mysql.connector.Error as e:
            flash(f"Database error: {e}")
    return render_template("author_form.html", author=rows[0])


# ---------- F2.5 remove an author (the books are deleted by ON DELETE CASCADE)
@app.route("/author/<int:author_id>/delete", methods=["POST"])
def delete_author(author_id):
    books = run("SELECT book_id FROM book WHERE author_id = %s", (author_id,), fetch=True)
    run("DELETE FROM author WHERE author_id = %s", (author_id,))
    for b in books:
        delete_image("book", b["book_id"])
    delete_image("author", author_id)
    flash("Author and all of his/her books removed.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
