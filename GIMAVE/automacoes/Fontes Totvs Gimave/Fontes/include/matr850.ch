#ifdef SPANISH
	#define STR0001 "Detalle de las ordenes de Produccion"
	#define STR0002 "Este programa imprime el detalle de las ordenes de Produccion"
	#define STR0003 "Por O.P.         "
	#define STR0004 "Por producto     "
	#define STR0005 "Por centro costo "
	#define STR0006 "A Rayas"
	#define STR0007 "Administracion"
	#define STR0008 " - Por O.P."
	#define STR0009 " - Por Producto"
	#define STR0010 " - Por Centro Costo"
	#define STR0011 "NUMERO         P R O D U C T O                                                CENTRO    EMISION     ENTREGA      ENTREGA         CANTIDAD          SALDO A      ST TP"
	#define STR0012 "                                                                               COSTO                PREVISTA        REAL         ORIGINAL         ENTREGAR"
	#define STR0013 "ANULADO POR EL OPERADOR"
	#define STR0014 "Total ---->"
	#define STR0015 "NUMERO         P R O D U C T O                                                CENTRO    EMISION     ENTREGA      ENTREGA         CANTIDAD          SALDO A      "
	#define STR0016 "NUMERO         P R O D U C .                                 CENTRO  EMISION  ENTREGA  ENTREGA     CANTIDAD          SALDO A ST TP"
	#define STR0017 "                                                           DE COSTO          PREVISTA     REAL       ORIGINAL       ENTREGAR"
	#define STR0018 "NUMERO         P R O D U C .                                 CENTRO  EMISION  ENTREGA  ENTREGA     CANTIDAD          SALDO A      "
	#define STR0019 "NUMERO"
	#define STR0020 "PRODUC."
	#define STR0021 "DESCRIPC."
	#define STR0022 "CENTRO COSTO"
	#define STR0023 "EMIS."
	#define STR0024 "FC.PREVISTA"
	#define STR0025 "FC. REAL"
	#define STR0026 "CANT. ORIGINAL"
	#define STR0027 "SALDO P ENTREGAR"
	#define STR0028 "ESTAT."
	#define STR0029 "TIPO"
	#define STR0030 "Ordenes de Prod. "
#else
	#ifdef ENGLISH
		#define STR0001 "Report of Production Orders"
		#define STR0002 "This program will print the list of Production Orders "
		#define STR0003 "By P.O.       "
		#define STR0004 "By Product    "
		#define STR0005 "By Cost Center"
		#define STR0006 "Z.Form"
		#define STR0007 "Management"
		#define STR0008 " - By P.O."
		#define STR0009 " - By Product"
		#define STR0010 " - By Cost Center"
		#define STR0011 "NUMBER         P R O D U C T                                                    COST      ISSUE     EXPECTED   EFFECTIVE         ORIGINAL       BALANCE TO      ST TP"
		#define STR0012 "                                                                              CENTER                DELIVERY    DELIVERY         QUANTITY          DELIVER"
		#define STR0013 "CANCELLED BY THE OPERATOR"
		#define STR0014 "Total ---->"
		#define STR0015 "NUMBER         P R O D U C T                                                    COST      ISSUE     EXPECTED   EFFECTIVE         ORIGINAL       BALANCE TO      "
		#define STR0016 "NUMBER         P R O D U C T                                 CENTER   ISSUE   DELIV.   DELIV.      QUANTITY          BLNCE A ST TP"
		#define STR0017 "                                                            COST             ESTIMATED    REAL       ORIGINAL       DELIVER "
		#define STR0018 "NUMBER         P R O D U C T                                 CENTER    ISSUE  DELIV.   DELIV.      QUANTITY          BALANCE      "
		#define STR0019 "NUMBER"
		#define STR0020 "PRODUCT"
		#define STR0021 "DESCRIPT."
		#define STR0022 "COST CENTER "
		#define STR0023 "ISSUE  "
		#define STR0024 "ESTIM. DATE"
		#define STR0025 "REALDATE"
		#define STR0026 "ORIGINAL QTY.  "
		#define STR0027 "AMOUNT TO DELIV."
		#define STR0028 "STATUS"
		#define STR0029 "TYPE"
		#define STR0030 "Production Orders "
	#else
		#define STR0001 If( cPaisLoc $ "ANG|PTG", "Relação Das Ordens De Produção", "Relacao Das Ordens de Producao" )
		#define STR0002 If( cPaisLoc $ "ANG|PTG", "Este programa irá imprimir a Relação das Ordens de Produção.", "Este programa ira imprimir a Relaçäo das Ordens de Produçäo." )
		#define STR0003 If( cPaisLoc $ "ANG|PTG", "Por o.p.       ", "Por O.P.       " )
		#define STR0004 If( cPaisLoc $ "ANG|PTG", "Por produto    ", "Por Produto    " )
		#define STR0005 If( cPaisLoc $ "ANG|PTG", "Por C. De Custo", "Por C. de Custo" )
		#define STR0006 If( cPaisLoc $ "ANG|PTG", "Código de barras", "Zebrado" )
		#define STR0007 If( cPaisLoc $ "ANG|PTG", "Administração", "Administracao" )
		#define STR0008 If( cPaisLoc $ "ANG|PTG", " - Por O.p.", " - Por O.P." )
		#define STR0009 " - Por Produto"
		#define STR0010 If( cPaisLoc $ "ANG|PTG", " - Por Centro De Custo", " - Por Centro de Custo" )
		#define STR0011 If( cPaisLoc $ "ANG|PTG", "Número         P R O D U T O                                                  Centro    Emissão      Entrega     Entrega       Quantidade          Saldo A      St Tp", "NUMERO         P R O D U T O                                                  CENTRO    EMISSAO      ENTREGA     ENTREGA       QUANTIDADE          SALDO A      ST TP" )
		#define STR0012 If( cPaisLoc $ "ANG|PTG", "                                                                            De Custo                Prevista        Real         Original         Entregar", "                                                                            DE CUSTO                PREVISTA        REAL         ORIGINAL         ENTREGAR" )
		#define STR0013 If( cPaisLoc $ "ANG|PTG", "Cancelado Pelo Operador", "CANCELADO PELO OPERADOR" )
		#define STR0014 "Total ---->"
		#define STR0015 If( cPaisLoc $ "ANG|PTG", "Número         p r o d u t o                                                  centro    emissão      entrega     entrega       quantidade          saldo a      ", "NUMERO         P R O D U T O                                                  CENTRO    EMISSAO      ENTREGA     ENTREGA       QUANTIDADE          SALDO A      " )
		#define STR0016 If( cPaisLoc $ "ANG|PTG", "Número         Produto                                 Centro  Emissão  Entrega  Entrega     Quantidade        Saldo A St Tp", "NUMERO         P R O D U T O                                 CENTRO  EMISSAO  ENTREGA  ENTREGA     QUANTIDADE        SALDO A ST TP" )
		#define STR0017 If( cPaisLoc $ "ANG|PTG", "                                                           De Custo          Prevista     Real       Original       Entregar", "                                                           DE CUSTO          PREVISTA     REAL       ORIGINAL       ENTREGAR" )
		#define STR0018 If( cPaisLoc $ "ANG|PTG", "Número         produto                                 centro  emissão  entrega  entrega     quantidade        saldo a      ", "NUMERO         P R O D U T O                                 CENTRO  EMISSAO  ENTREGA  ENTREGA     QUANTIDADE        SALDO A      " )
		#define STR0019 If( cPaisLoc $ "ANG|PTG", "Número", "NUMERO" )
		#define STR0020 If( cPaisLoc $ "ANG|PTG", "Produto", "PRODUTO" )
		#define STR0021 If( cPaisLoc $ "ANG|PTG", "Descrição", "DESCRIÇÃO" )
		#define STR0022 If( cPaisLoc $ "ANG|PTG", "Centro De Custo", "CENTRO CUSTO" )
		#define STR0023 If( cPaisLoc $ "ANG|PTG", "Emissão", "EMISSÃO" )
		#define STR0024 If( cPaisLoc $ "ANG|PTG", "Dt. prevista", "DT.PREVISTA" )
		#define STR0025 If( cPaisLoc $ "ANG|PTG", "Dt. Real", "DT. REAL" )
		#define STR0026 If( cPaisLoc $ "ANG|PTG", "Quant. Original", "QUANT. ORIGINAL" )
		#define STR0027 If( cPaisLoc $ "ANG|PTG", "Saldo A Entregar", "SALDO A ENTREGAR" )
		#define STR0028 If( cPaisLoc $ "ANG|PTG", "Estado", "STATUS" )
		#define STR0029 If( cPaisLoc $ "ANG|PTG", "Tipo", "TIPO" )
		#define STR0030 If( cPaisLoc $ "ANG|PTG", "Ordens de produção", "Ordens de Produção" )
	#endif
#endif
