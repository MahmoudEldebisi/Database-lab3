USE library;

INSERT INTO author (author_id, name, country) VALUES
  (1, 'Naguib Mahfouz',   'Egypt'),
  (2, 'George Orwell',    'United Kingdom'),
  (3, 'Gabriel Garcia Marquez', 'Colombia'),
  (4, 'Agatha Christie',  'United Kingdom');

INSERT INTO book (book_id, title, price, author_id) VALUES
  (1, 'Palace Walk',                  14.50, 1),
  (2, 'Midaq Alley',                  11.00, 1),
  (3, 'Nineteen Eighty-Four',         12.99, 2),
  (4, 'Animal Farm',                   9.50, 2),
  (5, 'One Hundred Years of Solitude',16.75, 3),
  (6, 'Love in the Time of Cholera',  15.20, 3),
  (7, 'Murder on the Orient Express', 10.80, 4),
  (8, 'And Then There Were None',     10.25, 4);
