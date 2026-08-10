CREATE DATABASE Avengers;
USE Avengers;

SET SQL_SAFE_UPDATES = 0;

CREATE TABLE superhero (
    superhero_id INT NOT NULL,
    superhero_name VARCHAR(50),
    superhero_strength INT,
    superhero_realname VARCHAR(50),
    PRIMARY KEY(superhero_id)
);

INSERT INTO superhero VALUES(1, 'Iron Man', 1000, 'Tony Stark');
INSERT INTO superhero VALUES(2, 'Captain America', 800, 'Steve Rogers');
INSERT INTO superhero VALUES(3, 'Thor', 1200, 'Thor Odinson');
INSERT INTO superhero VALUES(4, 'Hulk', 900, 'Bruce Banner');
INSERT INTO superhero VALUES(5, 'Black Widow', 600, 'Natasha Romanoff');
INSERT INTO superhero VALUES(6, 'Hawkeye', 500, 'Clint Barton');

SELECT * FROM superhero;

DELIMITER && 

CREATE PROCEDURE super_hero() 
BEGIN 
    SELECT superhero_name, superhero_strength, superhero_realname 
    FROM superhero 
    WHERE superhero_strength > 800; 
END && 

DELIMITER ;
CALL super_hero();

UPDATE superhero SET superhero_strength = 1000 WHERE superhero_name = 'Captain America';
SELECT * FROM superhero;

DELIMITER &&

CREATE PROCEDURE update_superhero_power(IN power INT, IN superheroes VARCHAR(50)) 
BEGIN 
    UPDATE superhero 
    SET superhero_strength = power 
    WHERE superhero_realname = superheroes;
END && 

DELIMITER ;

CALL update_superhero_power(5000, 'Thor Odinson');
CALL update_superhero_power(4000, 'Tony Stark');
CALL update_superhero_power(3000, 'Steve Rogers');
CALL update_superhero_power(2000, 'Bruce Banner');
SELECT * FROM superhero;

DELIMITER &&

CREATE PROCEDURE get_superhero_count(OUT total_strength INT)
BEGIN
    SELECT count(*) FROM superhero INTO total_strength;
END &&

DELIMITER ;

CALL get_superhero_count(@total_count);

SELECT @total_count;