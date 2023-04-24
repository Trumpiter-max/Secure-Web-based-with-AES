db = db.getSiblingDB("test");
db.animal_tb.drop();
db.users.drop();

db.users.insert(
    {
        "id": 1,
        "username": "test",
        "password": "test",
        "email": "test@test.com"
    }
);

db.animal_tb.insertMany([
    {
        "id": 1,
        "name": "Lion",
        "type": "wild"
    },
    {
        "id": 2,
        "name": "Cow",
        "type": "domestic"
    },
    {
        "id": 3,
        "name": "Tiger",
        "type": "wild"
    },
]);
