CREATE DATABASE db_pet;
USE db_pet;

CREATE TABLE user
(
	id int auto_increment primary key,
    nome varchar(45) not null,
    telefone varchar(15),
    endereco varchar(255)
);

CREATE TABLE animal
(
	id int auto_increment primary key,
    nome varchar(100) not null,
    especie varchar(50),
    idade int,
    user_id int,
    data_vacinacao date,
    local_vacinacao varchar(255),
    foreign key (user_id) references user(id)
);

CREATE TABLE login
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);
