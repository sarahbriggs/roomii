FINAL INSTRUCTIONS:
You need to install a few packages, namely flask, flask-materialize, and flask-login.
Then, you need to go to roomii/data/ and run datageneration.py.  Shouldn't take too long.
Then, navigate to roomii/app/db_related and run first creatin_tables.py then add_data_to_db.py. (this might take a minute)
At which point, you can run the app on your local machine by running main.py from the app folder.

At the page index, you get a login screen.  None of the fake users have passwords, so you can't get in there, you'll have to register an account.
Registering an account is the same as you'd expect.
Once you register, you're brought to a survey.  Follow the instructions.
Once you do the survey, submitting will take a sec.  That's ok, it just takes some time to compute your matches.
You can visit other people's accounts and write reviews and stuff.





Milestone 1:
You can initialize (or reset) the tables by running creatin_tables.py in either python 2 or 3.
You can insert a few fake datapoints by running useful_operations.py in either python 2 or 3.

All sql for creating the tables and associated constraints can be found in creatin_tables.sql.

We have decided to go ahead and wrap some of the queries that would otherwise go in test-sample.sql instead in useful_operations.py, and running it as main will run a few sample queries.  While we could have focused on writing *every query we'll need*, we decided instead to go ahead and begin integrating them with our Python backend.

All code for creating the sample data in XML can be found in data/datageneration.py.

Milestone 2:
All of the app and database logic can be found under ./app/

To generate the database, navigate to db_related and run, in this order, creatin_tables.py, useful_operations.py, and add_data_to_db.py.  add_data_to_db.py, so far, just adds some answers to questions.  However, it contains most of the infrastructure we need to extend it to other relations that need populating.

Again, in lieu of test_production.sql and test_production.out, we've hard-coded a lot of the important queries into our python, specifically in useful_operations and useful_queries.  After running creatin_tables and useful_operations, you can test out a few queries by running useful_queries.

Included in this rendition of the app is a proof-of-concept, demonstrating that we are able to load data into jinja templates.  You can run the program from the app folder with python app.py, and, if the database has been initialized with a set of questions and answers, it should be able to display whatever question is in index 0, along with associated answers.  










