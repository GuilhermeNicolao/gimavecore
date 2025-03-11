ALTER TABLE pedidos_diarios CHANGE COLUMN vlt_emissaocrt vlr_emissaocrt float;
SELECT * FROM pedidos_diarios;
-- UPDATE pedidos_diarios SET grupo = "LICITACOES" WHERE cod_pedido IN ("74926","74933","74935","74937","74939","74977","75026","75030","75033","75051","75081","75082","75090","75091","75093","75101","75108","75122","75129");
-- DELETE FROM pedidos_diarios;
DESCRIBE pedidos_diarios;
ALTER TABLE pedidos_diarios DROP COLUMN created_at;
SELECT count(*) FROM pedidos_diarios;
SELECT SUM(vlr_pedido) AS total FROM pedidos_diarios;

SET SQL_SAFE_UPDATES = 0;

ALTER TABLE cadastro_orc ADD COLUMN status varchar(255);
UPDATE cadastro_orc SET status = NULL WHERE STATUS = 'REPROVADO';
SELECT * FROM cadastro_orc;
DELETE FROM cadastro_orc where cod = '16';
DESCRIBE cadastro;
ALTER TABLE cadastro CHANGE COLUMN cnpj cnpj bigint;

CREATE TABLE cadastro_orc(
    cod INT PRIMARY KEY auto_increment,
    dt date not null,
    produto varchar(255) not null,
    fornecedor varchar(255) not null,
    vlr_orcamento float not null,
    observacao varchar(255));
