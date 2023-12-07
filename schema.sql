CREATE TABLE swimmers (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR
(64),
    age INT
);

CREATE TABLE events (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    distance VARCHAR
(64),
    stroke VARCHAR
(64)
);

CREATE TABLE times
(
    swimmer_id INT NOT NULL,
    events_id INT NOT NULL,
    time VARCHAR(64),
    ts TIMESTAMP,
    PRIMARY KEY (swimmer_id, events_id)
);
