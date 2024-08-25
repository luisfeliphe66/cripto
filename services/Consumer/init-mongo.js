// usa o banco de dados de administração
db = db.getSiblingDB('admin');

// Cria um usuário com privilégios de administrador
db.createUser({
  user: "myUser",
  pwd: "myPassword",
  roles: [{ role: "userAdminAnyDatabase", db: "admin" }]
});

// Cria um banco de dados e uma coleção
db = db.getSiblingDB('BTCBRL');

// Cria um usuário para o banco de dados BTCBRL com permissões de leitura e gravação
db.createUser({
  user: "admin",
  pwd: "password",
  roles: [{ role: "readWrite", db: "BTCBRL" }]
});

// Opcionalmente, você pode criar um documento inicial em uma coleção
db.BTC.insertOne({ initial: "data" });