ALTER TABLE pedidos_diarios CHANGE COLUMN vlt_emissaocrt vlr_emissaocrt float;

SELECT * FROM pedidos_diarios;

UPDATE pedidos_diarios SET grupo = "LICITACOES" WHERE cod_pedido IN ("74926","74933","74935","74937","74939","74977","75026","75030","75033","75051","75081","75082","75090","75091","75093","75101","75108","75122","75129");

DELETE FROM pedidos_diarios;

DESCRIBE pedidos_diarios;

ALTER TABLE pedidos_diarios DROP COLUMN created_at;

SELECT count(*) FROM pedidos_diarios;


