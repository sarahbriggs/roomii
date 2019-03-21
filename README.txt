You can initialize (or reset) the tables by running creatin_tables.py in either python 2 or 3.
You can insert a few fake datapoints by running useful_operations.py in either python 2 or 3.

All sql for creating the tables and associated constraints can be found in creatin_tables.sql.

We have decided to go ahead and wrap some of the queries that would otherwise go in test-sample.sql instead in useful_operations.py, and running it as main will run a few sample queries.  While we could have focused on writing *every query we'll need*, we decided instead to go ahead and begin integrating them with our Python backend.

All code for creating the sample data in XML can be found in data/datageneration.py.


