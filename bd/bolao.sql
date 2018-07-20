CREATE TABLE Usuario (
        nome varchar (255);
        email varchar(255) NOT NULL;
        descricao text;
        senha varchar(255) NOT  NULL;
        PRIMARY KEY (email)
);

CREATE TABLE Apostas (
        tipo varchar(255),
        classificacao varchar(255),
        id_aposta serial,
        valor float,
        bolao_aposta integer,
        email_usuario varchar(255),
        PRIMARY KEY (id_aposta),
        FOREIGN KEY (bolao_aposta) REFERENCES Bolao (id_bolao),
        FOREIGN KEY (email_usuario) REFERENCES Usuario (email)
);

CREATE TABLE Bolao(
        publico varchar (255),
        id_bolao serial,
        email_usuario varchar(255),
        data_inicio date,
        data_fim date,
        nome text,
        descricao text,
        valor_minimo float,
        PRIMARY KEY (id_bolao),
        FOREIGN KEY (email_usuario) REFERENCES Usuario (email)
);
