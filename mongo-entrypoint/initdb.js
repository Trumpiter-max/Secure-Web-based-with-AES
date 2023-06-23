db = db.getSiblingDB("sampledb");
db.users.drop();
db.roles.drop();
db.permissions.drop();
db.documents.drop();
db.createCollection('users');
db.createCollection('roles');
db.createCollection('permissions');
db.createCollection('documents');


