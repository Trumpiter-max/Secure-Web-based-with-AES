db = db.getSiblingDB("sampledb");
db.users.drop();
db.createCollection('users');
db.createCollection('roles');
db.createCollection('permissions');
db.createCollection('documents');


