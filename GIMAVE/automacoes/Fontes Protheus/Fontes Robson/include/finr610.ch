#ifdef SPANISH
	#define STR0001 "Este programa emite el informe de las"
	#define STR0002 "Comisiones por Pagar."
	#define STR0003 "Previs. de Comisiones"
	#define STR0004 "A Rayas"
	#define STR0005 "Administrac."
	#define STR0006 "PRF TITULO             PRC CODIGO  LJ  NOMBRE                FECHA DE    FECHA                VALOR        COMISION    COMISION    VALOR BASE %COMIS   VALOR TOTAL P/T"
	#define STR0007 "    PEDIDO                 CLIENTE                         EMISION    VENTO             TITULO       P/EMISION     P/BAJA      P/ BAJA  TOTAL   DE COMISION     "
	#define STR0008 "ANULADO POR EL OPERADOR"
	#define STR0009 "CODIGO : "
	#define STR0010 "NOMBRE:"
	#define STR0011 "TOTAL DEL VENDEDOR   --->"
	#define STR0012 "TOTAL  GENERAL       --->"
	#define STR0013 "SUBTOTAL DEL VENDEDOR--->"
	#define STR0014 "TOTAL IR VENDEDOR    --->"
	#define STR0015 "SUBTOTAL GENERAL     --->"
	#define STR0016 "TOTAL GENERAL IR     --->"
	#define STR0017 "PRF TITULO       PRC CODIGO               TD   NOMBRE               FCH. DE    FCH.               VALOR      COMISION      COMISION    VALOR BASE %COMIS   VALOR TOTAL P/T"
	#define STR0018 "    PEDIDO           CLIENTE                                        EMISION    VENCTO            TITULO     P/ EMISION       P/ BAJA      P/ BAJA  TOTAL   DE COMISION  "
	#define STR0019 "Salta Pag Vend."
	#define STR0020 "Si"
	#define STR0021 "No"
	#define STR0022 " en "
	#define STR0023 "Seleccionando Registros.."
	#define STR0024 "Registros"
	#define STR0025 "PRF"
	#define STR0026 "TITULO"
	#define STR0027 "PEDIDO"
	#define STR0028 "PRC"
	#define STR0029 "CODIGO"
	#define STR0030 "CLIENTE"
	#define STR0031 "TD"
	#define STR0032 "NOMB"
	#define STR0033 "DE FCH."
	#define STR0034 "EMISION"
	#define STR0035 "FCH."
	#define STR0036 "VENCTO"
	#define STR0037 "VALOR"
	#define STR0038 "TITULO"
	#define STR0039 "COMISION"
	#define STR0040 "P/ EMIS"
	#define STR0041 "P/ BAJA"
	#define STR0042 "VALOR BASE"
	#define STR0043 "%COMIS"
	#define STR0044 "TOTAL"
	#define STR0045 "VALOR TOTAL"
	#define STR0046 "DE COMISION"
	#define STR0047 "P/T"
#else
	#ifdef ENGLISH
		#define STR0001 "This report will print the Forecast of  "
		#define STR0002 "Commissions to be Paid. "
		#define STR0003 "Forecast of Commission"
		#define STR0004 "Z.Form "
		#define STR0005 "Management   "
		#define STR0006 "BILL PRF             PRC CODE  ST.  NAME                DATE FROM    DATE                VALUE        COMMISSION    COMMISSION    BASE VALUE COMMIS%   TOTAL VALUE P/T"
		#define STR0007 "    ORDER                  CLUSTOMER                       ISSUE      DUE DT             BILL         FOR ISSUE     FOR W.O.     FOR TOTAL W.O.    FROM COMMISSION     "
		#define STR0008 "CANCELLED BY THE OPERATOR  "
		#define STR0009 "CODE   : "
		#define STR0010 "NAME : "
		#define STR0011 "TOTAL OF REPRESENT.  --->"
		#define STR0012 "GRAND TOTAL          --->"
		#define STR0013 "SUBTOTAL OF REPRESEN.--->"
		#define STR0014 "TOTAL IR REPRESENTAT.--->"
		#define STR0015 "GRAND SUBTOTAL       --->"
		#define STR0016 "GRAND TOTAL IR       --->"
		#define STR0017 "PRF ORDER        PRC CUSTOMER             UN   NAME                 ISSUE      DUE                 BILL    COMMISSION    COMMISSION    BASE VALUE  TOTAL    TOTAL VALUE BY"
		#define STR0018 "    TITLE            CODE                                           DATE       DATE               VALUE      BY ISSUE  BY POSTING    BY POSTING   %COMM.      COMMISSION T"
		#define STR0019 "Sl.Repr. by Page"
		#define STR0020 "Yes"
		#define STR0021 "No"
		#define STR0022 " in "
		#define STR0023 "Selecting Records..."
		#define STR0024 "Records  "
		#define STR0025 "PRF"
		#define STR0026 "BILL  "
		#define STR0027 "ORDER "
		#define STR0028 "PRC"
		#define STR0029 "CODE  "
		#define STR0030 "CUSTOM."
		#define STR0031 "ST"
		#define STR0032 "NAME"
		#define STR0033 "FROM DT"
		#define STR0034 "ISSUE  "
		#define STR0035 "DATE"
		#define STR0036 "DUE DT"
		#define STR0037 "AMNT."
		#define STR0038 "BILL  "
		#define STR0039 "COMMISS."
		#define STR0040 "F/ISSUE  "
		#define STR0041 "F/PSTNG"
		#define STR0042 "BASE AMNT."
		#define STR0043 "COMM.%"
		#define STR0044 "TOTAL"
		#define STR0045 "TOTAL AMNT."
		#define STR0046 "OF COMMISS."
		#define STR0047 "P/T"
	#else
		#define STR0001 "Este relatorio irá emitir a Previsäo das"
		#define STR0002 If( cPaisLoc $ "ANG|PTG", "Comissões a serem pagas.", "Comissöes a Serem pagas." )
		#define STR0003 If( cPaisLoc $ "ANG|PTG", "Previsão De Comissões", "Previsao de Comissoes" )
		#define STR0004 If( cPaisLoc $ "ANG|PTG", "Código de barras", "Zebrado" )
		#define STR0005 If( cPaisLoc $ "ANG|PTG", "Administração", "Administracao" )
		#define STR0006 "PRF TITULO       PRC CODIGO LJ NOME                 DATA DE    DATA               VALOR      COMISSAO      COMISSAO    VALOR BASE %COMIS   VALOR TOTAL P/T"
		#define STR0007 "    PEDIDO           CLIENTE                        EMISSAO    VENCTO            TITULO     P/EMISSAO       P/BAIXA      P/ BAIXA  TOTAL   DA COMISSAO     "
		#define STR0008 If( cPaisLoc $ "ANG|PTG", "Cancelado Pelo Operador", "CANCELADO PELO OPERADOR" )
		#define STR0009 If( cPaisLoc $ "ANG|PTG", "Código : ", "CODIGO : " )
		#define STR0010 If( cPaisLoc $ "ANG|PTG", "Nome : ", "NOME : " )
		#define STR0011 If( cPaisLoc $ "ANG|PTG", "Total do vendedor    --->", "TOTAL DO VENDEDOR    --->" )
		#define STR0012 If( cPaisLoc $ "ANG|PTG", "Total  geral         --->", "TOTAL  GERAL         --->" )
		#define STR0013 If( cPaisLoc $ "ANG|PTG", "Subtotal do vendedor --->", "SUBTOTAL DO VENDEDOR --->" )
		#define STR0014 If( cPaisLoc $ "ANG|PTG", "Total ir vendedor    --->", "TOTAL IR VENDEDOR    --->" )
		#define STR0015 If( cPaisLoc $ "ANG|PTG", "Subtotal crial       --->", "SUBTOTAL GERAL       --->" )
		#define STR0016 If( cPaisLoc $ "ANG|PTG", "Total crial irs       --->", "TOTAL GERAL IR       --->" )
		#define STR0017 If( cPaisLoc $ "ANG|PTG", "Prf Título       Prc Código               Lj   Nome                 Data De    Data               Valor      Emissão      Emissão    Valor Base %comis   Valor Total P/t", "PRF TITULO       PRC CODIGO               LJ   NOME                 DATA DE    DATA               VALOR      COMISSAO      COMISSAO    VALOR BASE %COMIS   VALOR TOTAL P/T" )
		#define STR0018 If( cPaisLoc $ "ANG|PTG", "    pedido           cliente                                        emissão    vencto            título     p/emissão       p/liquidação      p/ liquidação  total   da emissão    ", "    PEDIDO           CLIENTE                                        EMISSAO    VENCTO            TITULO     P/EMISSAO       P/BAIXA      P/ BAIXA  TOTAL   DA COMISSAO    " )
		#define STR0019 "Salta Pag Vend."
		#define STR0020 "Sim"
		#define STR0021 If( cPaisLoc $ "ANG|PTG", "Não", "Nao" )
		#define STR0022 " em "
		#define STR0023 If( cPaisLoc $ "ANG|PTG", "A Seleccionar Registos...", "Selecionando Registros..." )
		#define STR0024 If( cPaisLoc $ "ANG|PTG", "Registos", "Registros" )
		#define STR0025 If( cPaisLoc $ "ANG|PTG", "Prf", "PRF" )
		#define STR0026 If( cPaisLoc $ "ANG|PTG", "Título", "TITULO" )
		#define STR0027 If( cPaisLoc $ "ANG|PTG", "Pedido", "PEDIDO" )
		#define STR0028 If( cPaisLoc $ "ANG|PTG", "Prc", "PRC" )
		#define STR0029 If( cPaisLoc $ "ANG|PTG", "Código", "CODIGO" )
		#define STR0030 If( cPaisLoc $ "ANG|PTG", "Cliente", "CLIENTE" )
		#define STR0031 If( cPaisLoc $ "ANG|PTG", "Loja", "LJ" )
		#define STR0032 If( cPaisLoc $ "ANG|PTG", "Nome", "NOME" )
		#define STR0033 If( cPaisLoc $ "ANG|PTG", "Da Data", "DATA DE" )
		#define STR0034 If( cPaisLoc $ "ANG|PTG", "Emissão", "EMISSAO" )
		#define STR0035 If( cPaisLoc $ "ANG|PTG", "Data", "DATA" )
		#define STR0036 If( cPaisLoc $ "ANG|PTG", "Vencto", "VENCTO" )
		#define STR0037 If( cPaisLoc $ "ANG|PTG", "Valor", "VALOR" )
		#define STR0038 If( cPaisLoc $ "ANG|PTG", "Título", "TITULO" )
		#define STR0039 If( cPaisLoc $ "ANG|PTG", "Comissão", "COMISSAO" )
		#define STR0040 If( cPaisLoc $ "ANG|PTG", "P/emissão", "P/EMISSAO" )
		#define STR0041 If( cPaisLoc $ "ANG|PTG", "P/liquidação", "P/BAIXA" )
		#define STR0042 If( cPaisLoc $ "ANG|PTG", "Valor Base", "VALOR BASE" )
		#define STR0043 If( cPaisLoc $ "ANG|PTG", "%comis", "%COMIS" )
		#define STR0044 If( cPaisLoc $ "ANG|PTG", "Total", "TOTAL" )
		#define STR0045 If( cPaisLoc $ "ANG|PTG", "Valor Total", "VALOR TOTAL" )
		#define STR0046 If( cPaisLoc $ "ANG|PTG", "Da Comissão", "DA COMISSAO" )
		#define STR0047 If( cPaisLoc $ "ANG|PTG", "P/t", "P/T" )
	#endif
#endif
