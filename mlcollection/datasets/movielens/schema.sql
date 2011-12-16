CREATE TABLE  MOVIE (
       Movie_Id INT PRIMARY KEY,
       Movie_Title VARCHAR(1024),
       Movie_ReleaseYear INT);

CREATE TABLE  GENRE (
       Genre_Id INT PRIMARY KEY,
       Genre_Name VARCHAR(200));

CREATE TABLE REVIEWER (
       Reviewer_Id INT PRIMARY KEY,
       Reviewer_Age INT,
       Reviewer_Gender VARCHAR(30),
       Reviewer_Occupation VARCHAR(50),
       Reviewer_Zipcode VARCHAR(30));

CREATE TABLE  MOVIE_GENRE (
       Movie_ID INT REFERENCES MOVIE (Movie_Id),
       Genre_ID INT REFERENCES GENRE (Genre_Id),
       PRIMARY KEY (Movie_Id, Genre_Id));

CREATE TABLE  RATING (
       Movie_Id INT REFERENCES MOVIE (Movie_Id),
       Reviewer_Id INT REFERENCES REVIEWER (Reviewer_Id),
       Rating INT NOT NULL,
       Rating_Timestamp INT,
       PRIMARY KEY (Reviewer_Id, Movie_id));

       

       