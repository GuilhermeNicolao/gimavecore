#ifdef SPANISH
	#define STR0001 "Espere"
	#define STR0002 "Creacion de archivos para impresion..."
	#define STR0003 "¡Informe vacio! Verifique los parametros."
	#define STR0004 "Atencion"
	#define STR0005 "Pedido de compras "
	#define STR0006 "Impresion..."
	#define STR0007 "PEDIDO DE COMPRA:"
	#define STR0008 "EMISION:"
	#define STR0009 "CNPJ:"
	#define STR0010 "I.E:"
	#define STR0011 "CP:"
	#define STR0012 "TEL.:"
	#define STR0013 "FAX:"
	#define STR0014 "Proveedor"
	#define STR0015 "Dir:"
	#define STR0016 "Barrio:"
	#define STR0017 "Municipio/E/P/R:"
	#define STR0018 "Item"
	#define STR0019 "Ctd"
	#define STR0020 "Codigo"
	#define STR0021 "Cod. Prod. Proveed."
	#define STR0022 "Descripcion"
	#define STR0023 "Tab. Prov."
	#define STR0024 "Vlr. Unit."
	#define STR0025 "Vlr. Total"
	#define STR0026 "IPI"
	#define STR0027 "Desc:"
	#define STR0028 "ICMS:"
	#define STR0029 "IPI:"
	#define STR0030 "Valor total:"
	#define STR0031 "Plazo programado p/ entrega:"
	#define STR0032 "Direccion de entrega:"
	#define STR0033 "Ciudad / E/P/R:"
	#define STR0034 "Telefono:"
	#define STR0035 "¿De proveedor?"
	#define STR0036 "¿A proveedor?"
	#define STR0037 "¿De pedido?"
	#define STR0038 "¿A pedido?"
	#define STR0039 "¿De emision?"
	#define STR0040 "¿A emision?"
	#define STR0041 "Unidad"
	#define STR0042 "Fc. Entrega"
	#define STR0043 "Vlr.Flete:"
	#define STR0044 "Gastos:"
	#define STR0045 "Seguro:"
#else
	#ifdef ENGLISH
		#define STR0001 "Wait"
		#define STR0002 "Creating files for printing..."
		#define STR0003 "Empty report! Check parameters."
		#define STR0004 "Attention"
		#define STR0005 "Purchase Order "
		#define STR0006 "Printing..."
		#define STR0007 "PURCHASE ORDER:"
		#define STR0008 "ISSUE:"
		#define STR0009 "CNPJ:"
		#define STR0010 "I.E:"
		#define STR0011 "Zip Code:"
		#define STR0012 "PHONE:"
		#define STR0013 "Fax Number:"
		#define STR0014 "Supplier"
		#define STR0015 "Addr.:"
		#define STR0016 "District:"
		#define STR0017 "City/State:"
		#define STR0018 "Item"
		#define STR0019 "Qty."
		#define STR0020 "Code"
		#define STR0021 "Supp. Prod. Code"
		#define STR0022 "Description"
		#define STR0023 "Supp. Tab."
		#define STR0024 "Unit Vl."
		#define STR0025 "Total Vl."
		#define STR0026 "IPI"
		#define STR0027 "Disc:"
		#define STR0028 "ICMS:"
		#define STR0029 "IPI:"
		#define STR0030 "Total Value:"
		#define STR0031 "Term Programmed f/ Delivery:"
		#define STR0032 "Delivery Address:"
		#define STR0033 "City/State:"
		#define STR0034 "Telephone:"
		#define STR0035 "From Supplier?"
		#define STR0036 "To Supplier?"
		#define STR0037 "From Order?"
		#define STR0038 "To Order?"
		#define STR0039 "From Issue?"
		#define STR0040 "To Issue?"
		#define STR0041 "Unit"
		#define STR0042 "Delivery Dt."
		#define STR0043 "Freight Amt.:"
		#define STR0044 "Expenses:"
		#define STR0045 "Insurance:"
	#else
		#define STR0001 "Aguarde"
		#define STR0002 If( cPaisLoc $ "ANG|PTG", "A criar ficheiros para impressão...", "Criando arquivos para impressão..." )
		#define STR0003 If( cPaisLoc $ "ANG|PTG", "Relatório vazio. Verifique os parâmetros.", "Relatório vazio! Verifique os parâmetros." )
		#define STR0004 "Atenção"
		#define STR0005 If( cPaisLoc $ "ANG|PTG", "Pedido de compras ", "Pedido de Compras " )
		#define STR0006 If( cPaisLoc $ "ANG|PTG", "A imprimir...", "Imprimindo..." )
		#define STR0007 "PEDIDO DE COMPRA:"
		#define STR0008 "EMISSÃO:"
		#define STR0009 If( cPaisLoc $ "ANG|PTG", "No.Contrib.:", "CNPJ:" )
		#define STR0010 If( cPaisLoc $ "ANG|PTG", "I.D:", "I.E:" )
		#define STR0011 If( cPaisLoc $ "ANG|PTG", "CP:", "CEP:" )
		#define STR0012 "TEL.:"
		#define STR0013 "FAX:"
		#define STR0014 "Fornecedor"
		#define STR0015 If( cPaisLoc $ "ANG|PTG", "Mor.:", "End:" )
		#define STR0016 If( cPaisLoc $ "ANG|PTG", "Freguesia:", "Bairro:" )
		#define STR0017 If( cPaisLoc $ "ANG|PTG", "Municipio/Distrito:", "Municipio/UF:" )
		#define STR0018 "Item"
		#define STR0019 If( cPaisLoc $ "ANG|PTG", "Qtd.", "Qtde" )
		#define STR0020 "Código"
		#define STR0021 "Cód. Prod. Fornec."
		#define STR0022 "Descrição"
		#define STR0023 "Tab. Fornec."
		#define STR0024 If( cPaisLoc $ "ANG|PTG", "Vlr. Unit.", "Vl. Unit." )
		#define STR0025 If( cPaisLoc $ "ANG|PTG", "Vlr. Total", "Vl. Total" )
		#define STR0026 "IPI"
		#define STR0027 "Desc:"
		#define STR0028 "ICMS:"
		#define STR0029 "IPI:"
		#define STR0030 If( cPaisLoc $ "ANG|PTG", "Valor total:", "Valor Total:" )
		#define STR0031 If( cPaisLoc $ "ANG|PTG", "Prazo programado p/ entrega:", "Prazo Programado p/ Entrega:" )
		#define STR0032 If( cPaisLoc $ "ANG|PTG", "Morada de entrega:", "Endereço de Entrega:" )
		#define STR0033 If( cPaisLoc $ "ANG|PTG", "Município / Distrito:", "Cidade / UF:" )
		#define STR0034 "Telefone:"
		#define STR0035 If( cPaisLoc $ "ANG|PTG", "Do fornecedor?", "Do Fornecedor?" )
		#define STR0036 If( cPaisLoc $ "ANG|PTG", "Até o fornecedor?", "Até o Fornecedor?" )
		#define STR0037 If( cPaisLoc $ "ANG|PTG", "Do pedido?", "Do Pedido?" )
		#define STR0038 If( cPaisLoc $ "ANG|PTG", "Até o pedido?", "Até o Pedido?" )
		#define STR0039 If( cPaisLoc $ "ANG|PTG", "Da emissão?", "Da Emissão?" )
		#define STR0040 If( cPaisLoc $ "ANG|PTG", "Até a emissão?", "Até Emissão?" )
		#define STR0041 "Unidade"
		#define STR0042 "Dt. Entrega"
		#define STR0043 If( cPaisLoc $ "ANG|PTG", "Vlr. Frete:", "Vlr Frete:" )
		#define STR0044 "Despesas:"
		#define STR0045 "Seguro:"
	#endif
#endif
