# Lab 3 – Library website (Problem 2)

Stack: Python 3 + Flask + MySQL. (If your Lab 2 site uses another stack, the SQL
in `problem2_DDL.sql` / `problem2_DML.sql` and the queries in `website/app.py` can be reused as-is.)

## Run it, step by step
1. Make sure MySQL is running and you know the root password.
2. Build the database and insert the seed data (from the repo folder):
   ```
   mysql -u root -p < problem2_DDL.sql
   mysql -u root -p < problem2_DML.sql
   ```
3. Install the website's dependencies:
   ```
   cd website
   pip install -r requirements.txt
   ```
4. Set the database password and start the site:
   - Linux / macOS: `export DB_PASSWORD=your_password`
   - Windows (cmd): `set DB_PASSWORD=your_password`

   ```
   python app.py
   ```
   Optional variables: `DB_HOST` (default `localhost`), `DB_USER` (default `root`).
5. Open http://127.0.0.1:5000

## Pages / features
| Req  | Feature |
|------|---------|
| F2.1 | Home page shows the books table (with `author_id`) and the authors table |
| F2.2 | "+ Add book" and "+ Add author" |
| F2.3 | "Edit" button on every row |
| F2.4 | "Remove" a book |
| F2.5 | "Remove" an author – the author's books are deleted too (`ON DELETE CASCADE`) |
| Bonus | Optional cover / photo upload in the add and edit forms (saved in `website/static/uploads/`) |
