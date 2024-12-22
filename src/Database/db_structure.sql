CREATE TABLE IF NOT EXISTS User(
    id INTEGER PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    isonline BOOLEAN NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS Chatroom(
    id INTEGER PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    createdby INTEGER,
    FOREIGN KEY (createdby) REFERENCES User(id)
);
CREATE TABLE IF NOT EXISTS Message(
    id INTEGER PRIMARY KEY,
    message text,
    timestamp DATETIME NOT NULL,
    userid INTEGER NOT NULL,
    chatroomid INTEGER NOT NULL,
    FOREIGN KEY (userid) REFERENCES User(id),
    FOREIGN KEY (chatroomid) REFERENCES Chatroom(id)
);