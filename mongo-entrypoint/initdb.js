db = db.getSiblingDB("sampledb");
db.users.drop();
db.createCollection('users');


