##Udacity FSND P2 - Tournament APP

###Description
The tournament app is a tool for managing Swiss style tournaments. It is capable of managing multiple tournaments at once.  You can use it to generate match pairs, record match results and retrieve player standings.

###Requirements
Before you can run the tournament app, your will need to install:
- PostgreSQL
- Python
- psycopg2
- psycopg2

###Running the App
After downloading the files, open PostgreSQL and create a database for your tournaments and import `tournament.sql`.

**Important** You must create a tournament before any app functions will work. 

You can create a tournament either in PostgreSQL with
    `INSERT INTO tournaments(tournament_name) VALUES [tournament_name];`
or in Python using:
    `import tournament`
    `tournament.create([tournament_name])`

