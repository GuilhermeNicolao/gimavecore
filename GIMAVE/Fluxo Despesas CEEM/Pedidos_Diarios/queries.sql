ALTER TABLE pedidos_diarios CHANGE COLUMN vlt_emissaocrt vlr_emissaocrt float;
SELECT * FROM pedidos_diarios;
-- UPDATE pedidos_diarios SET grupo = "LICITACOES" WHERE cod_pedido IN ("74926","74933","74935","74937","74939","74977","75026","75030","75033","75051","75081","75082","75090","75091","75093","75101","75108","75122","75129");
-- DELETE FROM pedidos_diarios;
DESCRIBE pedidos_diarios;
ALTER TABLE pedidos_diarios DROP COLUMN created_at;
SELECT count(*) FROM pedidos_diarios;
SELECT SUM(vlr_pedido) AS total FROM pedidos_diarios;


SELECT * FROM cadastro;
DESCRIBE cadastro;
ALTER TABLE cadastro CHANGE COLUMN cnpj cnpj bigint;

CREATE TABLE cadastro (
    cod INT PRIMARY KEY,
    cnpj INT,
    razao_social varchar(255),
    produto varchar(255),
    dt_inicio date,
    dt_fim date,
    status_ctt varchar(255),
    taxa varchar(255),
    vlr_taxa float,
    tp_desconto varchar(255),
    vlr_desconto float,
    cond_pgto varchar(255),
    vlr_emissaocrt float,
    vlr_novavia float,
    cobranca int,
    dt_fechamento date,
    dt_apuracao varchar(255),
    freq_apuracao int,
    replica_limite varchar(255),
    reposicao_automatica varchar(255),
    tp_cartao varchar(255),
    dados_bancarios varchar(255),
    calculo_venc varchar(255),
    logradouro varchar(255),
    numero int,
    complemento varchar(255),
    bairro varchar(255),
    cidade varchar(255),
    estado varchar(255));
