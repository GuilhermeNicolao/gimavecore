#ifdef SPANISH
	#define STR0001 "Informe de las ocurrencias por empleado. Por medio de los parametros "
	#define STR0002 "el usuario podra filtrar las ocurrencias que desea imprimir."
	#define STR0003 "A Rayas"
	#define STR0004 "Administracion"
	#define STR0005 "Ocurrencias por Empleado"
	#define STR0006 "¿De Sucursal?"
	#define STR0007 "¿De Centro de Costo?"
	#define STR0008 "¿A Centro de Costo?"
	#define STR0009 "De Empleado"
	#define STR0010 "A Empleado"
	#define STR0011 "¿De Fecha ?"
	#define STR0012 "¿A Fecha ?"
	#define STR0013 "Orden de ocurrrncias por:"
	#define STR0014 "Matricula"
	#define STR0015 "C.C. y Matr."
	#define STR0016 "N° ocurrencia"
	#define STR0017 "Sucursal        Nombre                             Matricula   Empleado                      C. Costo             Descripcion C. Costo"
	#define STR0018 "       Ocurrencia  Fecha      Gravedad              Descripc. Ocurrencia"
	#define STR0019 "Sucursal        Nombre                       C. Costo             Descripcion C. costo"
	#define STR0020 "Matricula:"
	#define STR0021 "      Ocurrencia  Fecha      Gravedad             Descripc. Ocurrencia"
	#define STR0022 "Ocurrencia   Descripc. Ocurrencia"
	#define STR0023 "         Matricula   Empleado                      C. Costo            Descripcion C. Costo         Fecha       Gravedad"
	#define STR0024 "No hay nada para imprimir en el informe."
	#define STR0025 "Advertencia Verbal"
	#define STR0026 "Advertencia Escrita"
	#define STR0027 "Suspension"
	#define STR0028 "Despido"
	#define STR0029 "Nombre Empleado: "
	#define STR0030 "¿A Sucursal?"
	#define STR0031 "Sucursal:"
	#define STR0032 "Nombre Sucursal:"
	#define STR0033 "Nombre"
	#define STR0034 "C.C. y Nombre"
	#define STR0035 "Matricula   Empleado                      C. Costo            Descripcion C. Costo "
	#define STR0036 "       Ocurrencia  Fecha      Gravedad              Descripc. Ocurrencia"
	#define STR0037 "C. Costo              Descripc. C. Costo"
	#define STR0038 "      Ocurrencia  Fecha      Gravedad             Descripc. Ocurrencia"
	#define STR0039 "Ocurrencia   Descripc. Ocurrencia"
	#define STR0040 "         Matricula   Empleado                      C. Costo            Descripcion C. Costo         Fecha       Gravedad"
	#define STR0041 "Cliente/Tda.: "
	#define STR0042 "¿Ordenar ocurrencias por: ?"
	#define STR0043 "¿A Fecha          ?"
	#define STR0044 "¿A Empleado ?"
	#define STR0045 "De Empleado."
	#define STR0046 "Tienda"
	#define STR0047 "¿De Cliente ?"
	#define STR0048 "¿A Cliente ?"
#else
	#ifdef ENGLISH
		#define STR0001 "Report of events by employee. Through the parameters              "
		#define STR0002 "the user can filter the events to be printed.              "
		#define STR0003 "Z.form "
		#define STR0004 "Management "
		#define STR0005 "Events by employee         "
		#define STR0006 "From branch?"
		#define STR0007 "From cost center?   "
		#define STR0008 "To cost center?      "
		#define STR0009 "From employee "
		#define STR0010 "To employee    "
		#define STR0011 "From date?"
		#define STR0012 "To date?  "
		#define STR0013 "Sort events by:         "
		#define STR0014 "Registr. "
		#define STR0015 "C.C.and Reg."
		#define STR0016 "Event number "
		#define STR0017 "Branch        Name                             Reg. No.   Employee Name                      Cost C.             Cost C. Description"
		#define STR0018 "       Occurrence  Date       Seriousness           Occurrence descript."
		#define STR0019 "Branch        Branch Name                             Cost C.             Cost C. Description"
		#define STR0020 "Registr.: "
		#define STR0021 "      Occurrence  Date       Seriousness          Occurrence descript."
		#define STR0022 "Event        Description of event"
		#define STR0023 "         Reg. No.   Employee Name                      Cost C.             Cost C. Description         Date       Severity"
		#define STR0024 "Nothing to be printed on the report.   "
		#define STR0025 "Oral warning      "
		#define STR0026 "Written warning    "
		#define STR0027 "Suspension"
		#define STR0028 "Dismissal"
		#define STR0029 "Employee name:   "
		#define STR0030 "To branch?  "
		#define STR0031 "Branch:"
		#define STR0032 "Branch name:"
		#define STR0033 "Name"
		#define STR0034 "C.C.andName"
		#define STR0035 "Reg. No.   Employee Name                      Cost C.              Cost C. Description"
		#define STR0036 "       Occurrence  Date       Gravity               Occurrence Description"
		#define STR0037 "C. Center             C. Center Description"
		#define STR0038 "      Occurrence  Date       Gravity              Occurrence Description"
		#define STR0039 "Occurrence   Occurrence Description"
		#define STR0040 "         Reg. No.                      Employee Name              Cost C.         Cost C. Description          Date       Severity"
		#define STR0041 "Customer/Store: "
		#define STR0042 "Order occurrences by ?"
		#define STR0043 "To Date?"
		#define STR0044 "To Employee?"
		#define STR0045 "From Employee?"
		#define STR0046 "Unit"
		#define STR0047 "From Customer?"
		#define STR0048 "To Customer?"
	#else
		#define STR0001 "Relatório das ocorrências por funcionário. Através dos parâmetros "
		#define STR0002 If( cPaisLoc $ "ANG|PTG", "O utilizador poderá filtrar quais ocorrencias deseja imprimir.", "o usuário poderá filtrar quais ocorrências deseja imprimir." )
		#define STR0003 If( cPaisLoc $ "ANG|PTG", "Código de barras", "Zebrado" )
		#define STR0004 If( cPaisLoc $ "ANG|PTG", "Administração", "Administracao" )
		#define STR0005 If( cPaisLoc $ "ANG|PTG", "Ocorrencias por empregado", "Ocorrências por Funcionário" )
		#define STR0006 If( cPaisLoc $ "ANG|PTG", "De filial ?", "De Filial ?" )
		#define STR0007 If( cPaisLoc $ "ANG|PTG", "De centro de custo ?", "De Centro de Custo ?" )
		#define STR0008 If( cPaisLoc $ "ANG|PTG", "Até centro de custo ?", "Até Centro de Custo ?" )
		#define STR0009 If( cPaisLoc $ "ANG|PTG", "De empregado", "De Funcionário" )
		#define STR0010 If( cPaisLoc $ "ANG|PTG", "Até funcionário", "Até Funcionário" )
		#define STR0011 If( cPaisLoc $ "ANG|PTG", "De data ?", "De Data ?" )
		#define STR0012 If( cPaisLoc $ "ANG|PTG", "Até data ?", "Até Data ?" )
		#define STR0013 If( cPaisLoc $ "ANG|PTG", "Ordenar ocorrências por:", "Ordenar Ocorrências por:" )
		#define STR0014 "Matrícula"
		#define STR0015 If( cPaisLoc $ "ANG|PTG", "C.c. E Matr.", "C.C. e Matr." )
		#define STR0016 If( cPaisLoc $ "ANG|PTG", "N.° de ocorrência", "N° ocorrência" )
		#define STR0017 "Filial        Nome                             Matrícula   Funcionário                      C. Custo             Descrição C. Custo"
		#define STR0018 If( cPaisLoc $ "ANG|PTG", "       ocorrencia  data       gravidade             descrição ocorrencia", "       Ocorrência  Data       Gravidade             Descrição Ocorrência" )
		#define STR0019 "Filial        Nome                             C. Custo             Descrição C. Custo"
		#define STR0020 If( cPaisLoc $ "ANG|PTG", "Registo:", "Matrícula:" )
		#define STR0021 If( cPaisLoc $ "ANG|PTG", "      ocorrência  data       gravidade            descrição ocorrência", "      Ocorrência  Data       Gravidade            Descrição Ocorrência" )
		#define STR0022 If( cPaisLoc $ "ANG|PTG", "Ocorrência   descrição ocorrência", "Ocorrência   Descrição Ocorrência" )
		#define STR0023 "         Matrícula   Funcionário                      C. Custo             Descrição C. Custo         Data       Gravidade"
		#define STR0024 If( cPaisLoc $ "ANG|PTG", "Não existe informação para imprimir no relatório.", "Não há nada para imprimir no relatório." )
		#define STR0025 If( cPaisLoc $ "ANG|PTG", "Advertência verbal", "Advertência Verbal" )
		#define STR0026 If( cPaisLoc $ "ANG|PTG", "Adverteência escrita", "Advertência Escrita" )
		#define STR0027 "Suspensão"
		#define STR0028 "Demissão"
		#define STR0029 If( cPaisLoc $ "ANG|PTG", "Nome empregado:", "Nome Funcionário:" )
		#define STR0030 If( cPaisLoc $ "ANG|PTG", "Ate filial ?", "Até Filial ?" )
		#define STR0031 "Filial:"
		#define STR0032 "Nome Filial:"
		#define STR0033 "Nome"
		#define STR0034 If( cPaisLoc $ "ANG|PTG", "C.c. E Nome", "C.C. e Nome" )
		#define STR0035 "Matrícula   Funcionário                      C. Custo              Descrição C. Custo"
		#define STR0036 If( cPaisLoc $ "ANG|PTG", "       ocorrencia  data       gravidade             descrição ocorrencia", "       Ocorrência  Data       Gravidade             Descrição Ocorrência" )
		#define STR0037 If( cPaisLoc $ "ANG|PTG", "C. Custo      Descrição  C. Custo", "C. Custo              Descrição C. Custo" )
		#define STR0038 If( cPaisLoc $ "ANG|PTG", "      ocorrência  data       gravidade            descrição ocorrência", "      Ocorrência  Data       Gravidade            Descrição Ocorrência" )
		#define STR0039 If( cPaisLoc $ "ANG|PTG", "Ocorrência   descrição ocorrência", "Ocorrência   Descrição Ocorrência" )
		#define STR0040 "         Matrícula   Funcionário                      C. Custo              Descrição C. Custo         Data       Gravidade"
		#define STR0041 If( cPaisLoc $ "ANG|PTG", "Cliente/loja: ", "Cliente/Loja: " )
		#define STR0042 "Ordenar Ocorrências por ?"
		#define STR0043 If( cPaisLoc $ "ANG|PTG", "Até Data ?", "Ate Data ?" )
		#define STR0044 If( cPaisLoc $ "ANG|PTG", "Até Empregado ?", "Até Funcionário ?" )
		#define STR0045 If( cPaisLoc $ "ANG|PTG", "De Empregado ?", "De Funcionário ?" )
		#define STR0046 "Loja"
		#define STR0047 "De Cliente ?"
		#define STR0048 "Até Cliente ?"
	#endif
#endif
