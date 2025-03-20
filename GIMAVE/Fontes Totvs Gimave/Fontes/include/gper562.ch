#ifdef SPANISH
	#define STR0001 "Archivo Texto|*.TXT"
	#define STR0002 "Grabar Busqueda..."
	#define STR0003 "         DGII              | SECRETARIA DE ESTADO DE FINANZAS                                   "
	#define STR0004 "         IR-4              | DIRECCION GENERAL DE IMPUESTOS INTERNO                             "
	#define STR0005 "                           | FORMATO PARA EL CALCULO DE LAS RETENCIONES MENSUALES DEL ASALARIADO"
	#define STR0006 "Agente de Retencion"
	#define STR0007 "Periodo"
	#define STR0008 "Hoja"
	#define STR0009 "Mes: "
	#define STR0010 "Ano: "
	#define STR0011 "De: "
	#define STR0012 "No: "
	#define STR0013 "       IDENTIFICACION DEL ASALARIADO         |                                 REMUNERACIONES PERCIBIDAS                        |                   LIQUIDACION DEL IMPUESTO (LEY 11-92)"
	#define STR0014 "                              |              | SUELDOS PAG.   |REMUNERACIONES |OTRAS REM. PAG. |               |SUELDOS Y OTROS |               |                |SALDO A FAVOR DEL|SAL. FAVOR de LA"
	#define STR0015 "APELLIDOS Y NOMBRES           |   CEDULA O   | POR EL AGENTE  |PAGADAS  OTROS |POR EL   AGENTE | TOTAL PAGADO  |PAGOS SUJETOS A |  LIQUIDACION  |  SALDO A FAV.  |ASAL COMP FUT RET|DIRECCION GENERAL"
	#define STR0016 "      COMPLETOS               |   PASAPORTE  | DE  RETENCION  | EMPLEADORES   |DE RETENCION    |  EN EL MES    |   RETENCION    |    PERIODO    | DEL ASALARIADO |(Si H-1 es neg.) |(Si H-1 es pos.)"
	#define STR0017 "           A                  |      B       |        C       |       D       |        E       |        F      |        G       |       H       |       I        |        J        |        K       "
	#define STR0018 "(L)Numero asalariados      "
	#define STR0019 "(M)Sujetos a Retencion     "
	#define STR0020 "TOTALES(RD$)"
	#define STR0021 "Llevar a la casilla con la letra (A) del Form. IR-13"
	#define STR0022 "Llevar a la casilla con la letra (B) del Form IR-13"
	#define STR0023 "El Periodo debe informarse en el formato aaaadd"
#else
	#ifdef ENGLISH
		#define STR0001 "Text File|*.TXT"
		#define STR0002 "Save Search..."
		#define STR0003 "         DGII              | SECRETARIA DE ESTADO DE FINANZAS                                   "
		#define STR0004 "         IR-4              | DIRECCION GENERAL DE IMPUESTOS INTERNO                             "
		#define STR0005 "                           | FORMATO PARA EL CALCULO DE LAS RETENCIONES MENSUALES DEL ASALARIADO"
		#define STR0006 "Agente de Retencion"
		#define STR0007 "Periodo"
		#define STR0008 "Hoja"
		#define STR0009 "Mes: "
		#define STR0010 "Ano: "
		#define STR0011 "De: "
		#define STR0012 "No: "
		#define STR0013 "       IDENTIFICACION DEL ASALARIADO         |                                 REMUNERACIONES PERCIBIDAS                        |                   LIQUIDACION DEL IMPUESTO (LEY 11-92)"
		#define STR0014 "                              |              | SUELDOS PAG.   |REMUNERACIONES |OTRAS REM. PAG. |               |SUELDOS Y OTROS |               |                |SALDO A FAVOR DEL|SAL. FAVOR DE LA"
		#define STR0015 "APELLIDOS Y NOMBRES           |   CEDULA O   | POR EL AGENTE  |PAGADAS  OTROS |POR EL   AGENTE | TOTAL PAGADO  |PAGOS SUJETOS A |  LIQUIDACION  |  SALDO A FAV.  |ASAL.COMP.FUT.RET|DIRECION GENERAL"
		#define STR0016 "      COMPLETOS               |  PASSAPORTE  | DE  RETENCION  | EMPLEADORES   |DE RETENCION    |  EN EL MES    |   RETENCION    |    PERIODO    | DEL ASALARIADO |(Si H-1 es neg.) |(Si H-1 es pos.)"
		#define STR0017 "           A                  |      B       |        C       |       D       |        E       |        F      |        G       |       H       |       I        |        J        |        K       "
		#define STR0018 "(L)Numero asalariados      "
		#define STR0019 "(M)Sujetos a Retencion     "
		#define STR0020 "TOTALES(RD$)"
		#define STR0021 "Llevar a la casilla con la letra (A) del Form.IR-13 "
		#define STR0022 "Llevar a la casilla con la letra (B) del Form.IR-13"
		#define STR0023 "El periodo deve ser informado en el formato aaaadd"
	#else
		#define STR0001 If( cPaisLoc $ "ANG|PTG", "Ficheiro Texto|*.txt", "Arquivo Texto|*.TXT" )
		#define STR0002 If( cPaisLoc $ "ANG|PTG", "Gravar Pesquisa...", "Salvar Pesquisa..." )
		#define STR0003 If( cPaisLoc $ "ANG|PTG", "         DGII              | SECRETARIA DE ESTADO DE FINANÇAS                                   ", "         DGII              | SECRETARIA DE ESTADO DE FINANZAS                                   " )
		#define STR0004 If( cPaisLoc $ "ANG|PTG", "         IR-4              | DIREÇÃO GERAL DE IMPOSTOS INTERNOS                            ", "         IR-4              | DIRECCION GENERAL DE IMPUESTOS INTERNO                             " )
		#define STR0005 If( cPaisLoc $ "ANG|PTG", "                           | Formato Para O Cálculo Das Retenções Mensais Do Assalariado", "                           | FORMATO PARA EL CALCULO DE LAS RETENCIONES MENSUALES DEL ASALARIADO" )
		#define STR0006 If( cPaisLoc $ "ANG|PTG", "Agente De Retenção", "Agente de Retencion" )
		#define STR0007 If( cPaisLoc $ "ANG|PTG", "Período", "Periodo" )
		#define STR0008 If( cPaisLoc $ "ANG|PTG", "Folha", "Hoja" )
		#define STR0009 "Mes: "
		#define STR0010 "Ano: "
		#define STR0011 "De: "
		#define STR0012 "No: "
		#define STR0013 If( cPaisLoc $ "ANG|PTG", "       identificacion del asalariado         |                                 remuneraciones percibidas                        |                   liquidacion del impuesto (ley 11-92)", "       IDENTIFICACION DEL ASALARIADO         |                                 REMUNERACIONES PERCIBIDAS                        |                   LIQUIDACION DEL IMPUESTO (LEY 11-92)" )
		#define STR0014 If( cPaisLoc $ "ANG|PTG", "                              |              | Salários Pag.   |remunerações |outras Rem. Pag. |               |salários E Otros |               |                |saldo A Favor Do|sal. Favor Da", "                              |              | SUELDOS PAG.   |REMUNERACIONES |OTRAS REM. PAG. |               |SUELDOS Y OTROS |               |                |SALDO A FAVOR DEL|SAL. FAVOR DE LA" )
		#define STR0015 If( cPaisLoc $ "ANG|PTG", "Apelidos E Nomes           |   Cédula Ou   | Pelo Agente  |pagas  Outros |pelo Agente | Total Pago  |pagamentos Sujeitos A |  Liquidação  |  Saldo A Fav.  |assal. Comp. Fut. Ret|direcção Geral", "APELLIDOS Y NOMBRES           |   CEDULA O   | POR EL AGENTE  |PAGADAS  OTROS |POR EL   AGENTE | TOTAL PAGADO  |PAGOS SUJETOS A |  LIQUIDACION  |  SALDO A FAV.  |ASAL.COMP.FUT.RET|DIRECION GENERAL" )
		#define STR0016 If( cPaisLoc $ "ANG|PTG", "      completos               |  passaporte  | de  retenção  | empregadores   |de retenção    |  no mês    |   retenção    |    período    | do assalariado |(se h-1 é neg.) |(se h-1 é pos.)", "      COMPLETOS               |  PASSAPORTE  | DE  RETENCION  | EMPLEADORES   |DE RETENCION    |  EN EL MES    |   RETENCION    |    PERIODO    | DEL ASALARIADO |(Si H-1 es neg.) |(Si H-1 es pos.)" )
		#define STR0017 If( cPaisLoc $ "ANG|PTG", "           a                  |      b       |        c       |       d       |        e       |        f      |        g       |       h       |       i        |        j        |        k       ", "           A                  |      B       |        C       |       D       |        E       |        F      |        G       |       H       |       I        |        J        |        K       " )
		#define STR0018 If( cPaisLoc $ "ANG|PTG", "(l) número assalariados      ", "(L)Numero asalariados      " )
		#define STR0019 If( cPaisLoc $ "ANG|PTG", "(m)sujeitos a retenção    ", "(M)Sujetos a Retencion     " )
		#define STR0020 If( cPaisLoc $ "ANG|PTG", "Totais(rd€)", "TOTALES(RD$)" )
		#define STR0021 If( cPaisLoc $ "ANG|PTG", "Llevar a la casilla con la letra (a) del form.ir-13 ", "Llevar a la casilla con la letra (A) del Form.IR-13 " )
		#define STR0022 If( cPaisLoc $ "ANG|PTG", "Llevar A La Casilla Con La Letra (b) Del Form.ir-13", "Llevar a la casilla con la letra (B) del Form.IR-13" )
		#define STR0023 If( cPaisLoc $ "ANG|PTG", "O período deve ser introduzido em formato aaaadd", "El periodo deve ser informado en el formato aaaadd" )
	#endif
#endif
