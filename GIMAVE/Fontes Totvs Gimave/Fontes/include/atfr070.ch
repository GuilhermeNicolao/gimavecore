#ifdef SPANISH
	#define STR0001 "Este programa emitira la situacion valorizada de"
	#define STR0002 "bienes hasta en 5 (cinco)mon."
	#define STR0003 "Situac. Valoriz. de Bienes "
	#define STR0004 " Sucursal        C. Costo             Cod. Base  Item Tp Descripcion sintetica                Adquisic.   Fch.Baja    Cantidad  Placa  Item.Ctb  Cl.Valor.   "
	#define STR0005 " Sucursal        Cuenta                Cod. Base  Item Tp Descripcion sintetica                Adquisic.   Fch.Baja    Cantidad  Placa  Item.Ctb  Cl.Valor.   "
	#define STR0006 "      VLR AMPLIACION    VALOR ORIGINAL    VALOR ACTUALIZADO  DEPREC AL MES  DEPREC.AL EJERC.    DEPREC. ACUMULADA   CORR.MON. MES  CORR. MON.EJERC.  CORR. MONET. ACUM.  CORR.DEPR. MES  CORR.DEPR.EJERC.  CORR. DEPR.  ACUM."
	#define STR0007 "Cuenta  : "
	#define STR0008 "C.Costo : "
	#define STR0009 "ANULADO POR EL OPERADOR"
	#define STR0010 "TOTAL "
	#define STR0011 "CANTIDAD  "
	#define STR0012 "* *   T O T A L   G E N E R A L  * *"
	#define STR0013 "CANTIDAD  "
	#define STR0014 "A Rayas"
	#define STR0015 "Administrac. "
	#define STR0016 "Cuen."
	#define STR0017 "C. Costo"
	#define STR0018 " por "
	#define STR0019 " - TIPO "
	#define STR0020 "Para utilizac. crear indice SN4 - Clave N4_FILIAL + N4_CBASE + N4_ITEM + N4_TIPO + N4_OCORR + DTOS(N4_DATA)."
	#define STR0021 "Item Contable"
	#define STR0022 "Clase de Valor"
	#define STR0023 " Sucursal        Cuenta                Cod. Base  Item Tp Descripcion sintetica                Adquisic.   Fch.Baja    Cantidad  Placa  C.Costo   Cl.Valor.   "
	#define STR0024 " Sucursal        Cuenta                Cod. Base  Item Tp Descripcion sintetica                Adquisic.   Fch.Baja    Cantidad  Placa  Item Ctb  C.Costo     "
	#define STR0025 "Valor Original"
	#define STR0026 "Valor Actualiz. "
	#define STR0027 "Deprec.del mes"
	#define STR0028 "Deprec.del Ejerc."
	#define STR0029 "Deprec. Acumulada"
	#define STR0030 "Valores de Total Geral de Baja "
	#define STR0031 "* * *  B  A  J  A  S* * *"
	#define STR0032 "* * *   T O T A L   * * *"
	#define STR0033 "BAJAS "
	#define STR0034 "TOTAL"
	#define STR0035 "Ente Contable"
	#define STR0036 "Datos del Ente"
	#define STR0037 "Valores"
	#define STR0038 "Simb. Moneda"
	#define STR0039 "Texto Subtotal"
	#define STR0040 "Valores Subtotal"
	#define STR0041 "Texto Baja"
	#define STR0042 "Ente"
	#define STR0043 "Cantidad"
	#define STR0044 "Baja"
	#define STR0045 "Valores de baja"
	#define STR0046 "Texto Total de Bajas"
	#define STR0047 "Val. del Total de Bajas"
	#define STR0048 "Texto Total Gral."
	#define STR0049 "Val. del Total Gral."
	#define STR0050 "Texto Total Gral. de Baja"
	#define STR0051 "Total Gral. de Baja"
	#define STR0052 "Texto Total + Baja"
	#define STR0053 "Total + Baja"
	#define STR0054 "Valores del Total + Baja"
	#define STR0055 "Total de Bajas"
	#define STR0056 "Total Gral."
	#define STR0057 "Sucursal:"
#else
	#ifdef ENGLISH
		#define STR0001 "This program will print the valuation position "
		#define STR0002 "of the Assets in up to 5 (five) Currencies."
		#define STR0003 "Valuated position of Assets"
		#define STR0004 " Branch  C. Center             Code Base  Item Tp Summar. Description                 Acquis.   Dt.WriteOff    Amount  Reg.No.  Acc.Item  ValueCl.   "
		#define STR0005 " Branch        Account                Code Base  Item Tp Summar. Description                 Acquis.   Dt.WriteOff    Amount  Reg.No.  Acc.Item  ValueCl.   "
		#define STR0006 "      ENLARGEMENT VALUE  ORIGINAL AMOUNT   VALUATED AMOUNT   MONTH DEPREC   YEAR DEPREC         ACCUMUL DEPREC      MONET.ADJ MONTH MON.ADJ.YEAR     ACCUM.MONET.ADJ.    MONTH DEPR.ADJ. YEAR DEPR ADJ     ACCUM MONET ADJ.  "
		#define STR0007 "Account : "
		#define STR0008 "C.Center: "
		#define STR0009 "CANCELLED BY THE OPERATOR  "
		#define STR0010 "TOTAL "
		#define STR0011 "QUANTITY  "
		#define STR0012 "* * *  G R A N D   T O T A L * * *"
		#define STR0013 "QUANTITY  "
		#define STR0014 "Z.Form "
		#define STR0015 "Management   "
		#define STR0016 "Accnt"
		#define STR0017 "C Center"
		#define STR0018 " per "
		#define STR0019 " - TYPE "
		#define STR0020 "To use it, create index SN4 - Key N4_FILIAL + N4_CBASE + N4_ITEM + N4_TIPO + N4_OCORR + DTOS(N4_DATA).          "
		#define STR0021 "Account. Item"
		#define STR0022 "Class of Value"
		#define STR0023 " Branch        Account                Code Base  Item Tp Summar. Description                 Acquis.   Dt.WriteOff    Amount  Reg.No.  C.Center   ValueCl.   "
		#define STR0024 " Branch        Account                Code Base  Item Tp Summar. Description                 Acquis.   Dt.WriteOff    Amount  Reg.No.  Acc. Item  C.Center     "
		#define STR0025 "Original Value"
		#define STR0026 "Updated Value   "
		#define STR0027 "Deprec.in month"
		#define STR0028 "Deprec.in Fisc.Yr"
		#define STR0029 "Deprec. Accrued  "
		#define STR0030 "Values of Posting Grand Total  "
		#define STR0031 "* * *P O S T I N G S* * *"
		#define STR0032 "* * *   T O T A L   * * *"
		#define STR0033 "POSTS."
		#define STR0034 "TOTAL"
		#define STR0035 "Accounting Entity"
		#define STR0036 "Entity info      "
		#define STR0037 "Amounts"
		#define STR0038 "Currency symb"
		#define STR0039 "Sub-total text "
		#define STR0040 "Sub-total Amounts"
		#define STR0041 "Pstg. Text "
		#define STR0042 "Entity  "
		#define STR0043 "Quantity  "
		#define STR0044 "Pstng"
		#define STR0045 "Posting amounts "
		#define STR0046 "Pstngs GrandTotal Txt"
		#define STR0047 "Posting total amounts     "
		#define STR0048 "Grand Total Text "
		#define STR0049 "Grand total amounts   "
		#define STR0050 "Posting Grand Total Text  "
		#define STR0051 "Posting grand total   "
		#define STR0052 "Total Text +Posting"
		#define STR0053 "Total+Posting"
		#define STR0054 "Total amounts + Posting "
		#define STR0055 "Posting total  "
		#define STR0056 "Grand total"
		#define STR0057 "Branch"
	#else
		#define STR0001 If( cPaisLoc $ "ANG|PTG", "Este programa irá emitir a posição valorizada dos", "Este programa irá emitir a posiçäo valorizada dos" )
		#define STR0002 If( cPaisLoc $ "ANG|PTG", "Bens em até 5 (cinco) moedas.", "bens em ate 5 (cinco) moedas." )
		#define STR0003 If( cPaisLoc $ "ANG|PTG", "Posição Valorizada Dos Bens", "Posicao Valorizada dos Bens" )
		#define STR0004 If( cPaisLoc $ "ANG|PTG", " Filial        C. Custo             Cód. Base  Elem. Tp. Descrição sintética                 Aquisic.   Dt.Liquid.  Quantidade  Chapa  Elem.Ctb  Cl.Valor.   ", " Filial        C. Custo             Cod. Base  Item Tp Descricao sintetica                 Aquisic.   Dt.Baixa    Quantidade  Chapa  Item.Ctb  Cl.Valor.   " )
		#define STR0005 If( cPaisLoc $ "ANG|PTG", " Filial        Conta                Cód. Base  Elem.Tp.Descrição sintética                 Aquisic.   Dt.Liquid.  Quantidade  Chapa  Elem.Ctb  Cl.Valor.   ", " Filial        Conta                Cod. Base  Item Tp Descricao sintetica                 Aquisic.   Dt.Baixa    Quantidade  Chapa  Item.Ctb  Cl.Valor.   " )
		#define STR0006 If( cPaisLoc $ "ANG|PTG", "      Vlr Ampliação      Valor Original    Valor Actualizado  Deprec. No Mês Deprec. No Exerc.   Deprec. Acumulada   Corr.mon. Mes  Corr. Mon.exerc.  Corr. Monet. Acum.  Corr.depr. Mes  Corr.depr.exerc.  Corr. Depr.  Acum.", "      VLR AMPLIACAO      VALOR ORIGINAL    VALOR ATUALIZADO  DEPREC. NO MES DEPREC. NO EXERC.   DEPREC. ACUMULADA   CORR.MON. MES  CORR. MON.EXERC.  CORR. MONET. ACUM.  CORR.DEPR. MES  CORR.DEPR.EXERC.  CORR. DEPR.  ACUM." )
		#define STR0007 "Conta   : "
		#define STR0008 If( cPaisLoc $ "ANG|PTG", "C.custo : ", "C.Custo : " )
		#define STR0009 If( cPaisLoc $ "ANG|PTG", "Cancelado Pelo Operador", "CANCELADO PELO OPERADOR" )
		#define STR0010 If( cPaisLoc $ "ANG|PTG", "Total ", "TOTAL " )
		#define STR0011 If( cPaisLoc $ "ANG|PTG", "Quantidade", "QUANTIDADE" )
		#define STR0012 If( cPaisLoc $ "ANG|PTG", "* * *   t o t a l   g e r a l   * * *", "* * *   T O T A L   G E R A L   * * *" )
		#define STR0013 If( cPaisLoc $ "ANG|PTG", "Quantidade", "QUANTIDADE" )
		#define STR0014 If( cPaisLoc $ "ANG|PTG", "Código de barras", "Zebrado" )
		#define STR0015 If( cPaisLoc $ "ANG|PTG", "Administração", "Administracao" )
		#define STR0016 "Conta"
		#define STR0017 "C Custo"
		#define STR0018 " por "
		#define STR0019 If( cPaisLoc $ "ANG|PTG", " - tipo ", " - TIPO " )
		#define STR0020 If( cPaisLoc $ "ANG|PTG", "Para Utilização Criar índice Sn4 - Chave N4_filial + N4_cbase + N4_item + N4_tipo + N4_ocorr + Dtos(n4_data).", "Para utilizacao criar indice SN4 - Chave N4_FILIAL + N4_CBASE + N4_ITEM + N4_TIPO + N4_OCORR + DTOS(N4_DATA)." )
		#define STR0021 If( cPaisLoc $ "ANG|PTG", "Item Contab.", "Item Contabil" )
		#define STR0022 If( cPaisLoc $ "ANG|PTG", "Classe De Valor", "Classe de Valor" )
		#define STR0023 If( cPaisLoc $ "ANG|PTG", " Filial        Conta                Cód. Base  Elem.Tp.Descrição sintética                 Aquisic.   Dt.Liquid.  Quantidade  Chapa  C.Custo   Cl.Valor.   ", " Filial        Conta                Cod. Base  Item Tp Descricao sintetica                 Aquisic.   Dt.Baixa    Quantidade  Chapa  C.Custo   Cl.Valor.   " )
		#define STR0024 If( cPaisLoc $ "ANG|PTG", " Filial        Conta                Cód. Base  Elem.Tp.Descrição sintética                 Aquisic.   Dt.Liquid.  Quantidade  Chapa  Elem.Ctb. C.Custo     ", " Filial        Conta                Cod. Base  Item Tp Descricao sintetica                 Aquisic.   Dt.Baixa    Quantidade  Chapa  Item Ctb  C.Custo     " )
		#define STR0025 "Valor Original"
		#define STR0026 If( cPaisLoc $ "ANG|PTG", "Valor Actualizado", "Valor Atualizado" )
		#define STR0027 "Deprec. no mês"
		#define STR0028 If( cPaisLoc $ "ANG|PTG", "Deprec. No Exerc.", "Deprec. no Exerc." )
		#define STR0029 "Deprec. Acumulada"
		#define STR0030 If( cPaisLoc $ "ANG|PTG", "Valores De Total Crial De Liquidação", "Valores de Total Geral de Baixa" )
		#define STR0031 If( cPaisLoc $ "ANG|PTG", "* * *  b a i x a s  * * *", "* * *  B A I X A S  * * *" )
		#define STR0032 If( cPaisLoc $ "ANG|PTG", "* * *   t o t a l   * * *", "* * *   T O T A L   * * *" )
		#define STR0033 If( cPaisLoc $ "ANG|PTG", "Liquidações", "BAIXAS" )
		#define STR0034 If( cPaisLoc $ "ANG|PTG", "Total", "TOTAL" )
		#define STR0035 If( cPaisLoc $ "ANG|PTG", "Entidade Contabilística", "Entidade Contabil" )
		#define STR0036 If( cPaisLoc $ "ANG|PTG", "Dados Da Entidade", "Dados da Entidade" )
		#define STR0037 "Valores"
		#define STR0038 If( cPaisLoc $ "ANG|PTG", "Símbolo Moeda", "Simbolo Moeda" )
		#define STR0039 If( cPaisLoc $ "ANG|PTG", "Texto Subtotal", "Texto Sub-total" )
		#define STR0040 If( cPaisLoc $ "ANG|PTG", "Valores Subtotal", "Valores Sub-total" )
		#define STR0041 If( cPaisLoc $ "ANG|PTG", "Texto Liquidação", "Texto Baixa" )
		#define STR0042 "Entidade"
		#define STR0043 "Quantidade"
		#define STR0044 If( cPaisLoc $ "ANG|PTG", "Liquidação", "Baixa" )
		#define STR0045 If( cPaisLoc $ "ANG|PTG", "Valores de liquidação", "Valores de baixa" )
		#define STR0046 If( cPaisLoc $ "ANG|PTG", "Texto Total De Liquidações", "Texto Total de Baixas" )
		#define STR0047 If( cPaisLoc $ "ANG|PTG", "Valores Do Total De Liquidações", "Valores do Total de Baixas" )
		#define STR0048 "Texto Total Geral"
		#define STR0049 If( cPaisLoc $ "ANG|PTG", "Valores Do Total Geral", "Valores do Total Geral" )
		#define STR0050 If( cPaisLoc $ "ANG|PTG", "Texto Total Geral De Liquidação", "Texto Total Geral de Baixa" )
		#define STR0051 If( cPaisLoc $ "ANG|PTG", "Total Geral De Liquidação", "Total Geral de Baixa" )
		#define STR0052 If( cPaisLoc $ "ANG|PTG", "Texto Total + Liquidação", "Texto Total + Baixa" )
		#define STR0053 If( cPaisLoc $ "ANG|PTG", "Total + Liquidação", "Total + Baixa" )
		#define STR0054 If( cPaisLoc $ "ANG|PTG", "Valores Do Total + Liquidação", "Valores do Total + Baixa" )
		#define STR0055 If( cPaisLoc $ "ANG|PTG", "Total De Liquidações", "Total de Baixas" )
		#define STR0056 If( cPaisLoc $ "ANG|PTG", "Total crial", "Total geral" )
		#define STR0057 "Filial"
	#endif
#endif
