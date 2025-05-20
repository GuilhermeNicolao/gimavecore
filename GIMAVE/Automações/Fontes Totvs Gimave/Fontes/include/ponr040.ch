#ifdef SPANISH
	#define STR0001 "Divergencias en marcaciones"
	#define STR0002 "Se imprimira de acuerdo con los parametros solicitados por el"
	#define STR0003 "usuario."
	#define STR0004 "Matricula"
	#define STR0005 "Centro de costo"
	#define STR0006 "Nombre"
	#define STR0007 "Turno"
	#define STR0008 "A Rayas"
	#define STR0009 "Administracion"
	#define STR0011 "Fecha  Marcaciones                                                                  Evento    "
	#define STR0015 "** No existe ageda               "
	#define STR0016 "** Numero de marcaciones impares   "
	#define STR0017 "** Menos marcac. que lo programado "
	#define STR0018 "** Mas marcac. que lo programado "
	#define STR0019 "** Hora extra no autorizada       "
	#define STR0020 " Intervalo menor que el programado"
	#define STR0021 " Intervalo mayor que el programado"
	#define STR0022 "** Marcaciones antes del ingreso  "
	#define STR0023 "** Marcaciones despues despido    "
	#define STR0024 "** Marcaciones durante vacaciones "
	#define STR0025 "** Marcaciones durante licencia   "
	#define STR0027 "Sucursal: "
	#define STR0028 " Turno: "
	#define STR0029 "    C.C: "
	#define STR0030 "C.Costo+Nomb"
	#define STR0031 "PLACA: "
	#define STR0032 "MATR: "
	#define STR0033 "NOMB: "
	#define STR0034 "Departamento"
	#define STR0035 "Seleccione la opcion de impresion: "
	#define STR0036 "Por Periodo"
	#define STR0037 "Por Fechas"
	#define STR0038 "DEPTO: "
	#define STR0039 "Proceso: "
	#define STR0040 "Periodo: "
	#define STR0041 "Procedim.: "
	#define STR0042 "Num. Pago.:"
	#define STR0043 "Este programa emite Relacion de los Funcionarios con Divergencias de Marcaciones"
	#define STR0044 "Empleados"
	#define STR0045 "Ocurrencias"
	#define STR0046 "Marcaciones"
	#define STR0047 "Fecha"
	#define STR0048 "C.Costo"
	#define STR0049 "Tno"
	#define STR0050 "Proceso"
	#define STR0051 "Periodo"
	#define STR0052 "Rot"
	#define STR0053 "NP"
	#define STR0054 "Depto"
#else
	#ifdef ENGLISH
		#define STR0001 "Marks Divergences"
		#define STR0002 "It will be printed according to the parameters selected "
		#define STR0003 "by the User"
		#define STR0004 "Registr."
		#define STR0005 "Cost Center"
		#define STR0006 "Name"
		#define STR0007 "Shift"
		#define STR0008 "Z.Form"
		#define STR0009 "Management"
		#define STR0011 "Date   Markings                                                                        Occurrence"
		#define STR0015 "** There is no Calendar            "
		#define STR0016 "** Odd Number of Markings          "
		#define STR0017 "** Less Markings than Programmed   "
		#define STR0018 "** More Markings than Programmed   "
		#define STR0019 "** No Authorized Overtime          "
		#define STR0020 " Lower Interval than Programmed  "
		#define STR0021 " Higher Interval than Programmed "
		#define STR0022 "** Markings before Admission       "
		#define STR0023 "** Markings after Dismissal        "
		#define STR0024 "** Markings during Vacations       "
		#define STR0025 "** Markings during Absence         "
		#define STR0027 "Branch: "
		#define STR0028 " Shift: "
		#define STR0029 "    C.C: "
		#define STR0030 "C.Cent.+Name"
		#define STR0031 "PLATE: "
		#define STR0032 "REG.: "
		#define STR0033 "NAME: "
		#define STR0034 "Department"
		#define STR0035 "Select the printing option: "
		#define STR0036 "By Period"
		#define STR0037 "By Dates"
		#define STR0038 "DEP.: "
		#define STR0039 "Process: "
		#define STR0040 "Period: "
		#define STR0041 "Procedure: "
		#define STR0042 "Paym. Nbr.:"
		#define STR0043 "This program issues Employees Report with Selections Differences"
		#define STR0044 "Employees"
		#define STR0045 "Occurrences"
		#define STR0046 "Selections"
		#define STR0047 "Data"
		#define STR0048 "Cost Center"
		#define STR0049 "Tno"
		#define STR0050 "Process"
		#define STR0051 "Period"
		#define STR0052 "Rot"
		#define STR0053 "NP"
		#define STR0054 "Dept."
	#else
		#define STR0001 If( cPaisLoc $ "ANG|PTG", "Divergências Nas Marcações", "Divergencias nas Marcacoes" )
		#define STR0002 If( cPaisLoc $ "ANG|PTG", "Será impresso de acordo com os parâmetros solicitados pelo", "Será impresso de acordo com os parametros solicitados pelo" )
		#define STR0003 If( cPaisLoc $ "ANG|PTG", "Utilizador.", "usuario." )
		#define STR0004 If( cPaisLoc $ "ANG|PTG", "Registo", "Matricula" )
		#define STR0005 If( cPaisLoc $ "ANG|PTG", "Centro De Custo", "Centro de Custo" )
		#define STR0006 "Nome"
		#define STR0007 "Turno"
		#define STR0008 If( cPaisLoc $ "ANG|PTG", "Código de barras", "Zebrado" )
		#define STR0009 If( cPaisLoc $ "ANG|PTG", "Administração", "Administraçäo" )
		#define STR0011 If( cPaisLoc $ "ANG|PTG", "Data    Marcações                                                                     Ocorrência", "Data   Marcacoes                                                                       Ocorrencia" )
		#define STR0015 If( cPaisLoc $ "ANG|PTG", "** Não existe calendário**", "** Nao existe Calendario           " )
		#define STR0016 If( cPaisLoc $ "ANG|PTG", "** Número de marcações ímpar", "** Numero de Marcacoes Impar       " )
		#define STR0017 If( cPaisLoc $ "ANG|PTG", "** Menos Marcações Do Que O Programado", "** Menos Marcacoes que o Programado" )
		#define STR0018 If( cPaisLoc $ "ANG|PTG", "** Mais marcações do que o programado", "** Mais Marcacoes que o Programado " )
		#define STR0019 If( cPaisLoc $ "ANG|PTG", "** Hora extra não autorizada", "** Hora Extra Nao Autorizada       " )
		#define STR0020 If( cPaisLoc $ "ANG|PTG", " Intervalo Menor Do Que O Programado", " Intervalo Menor que o Programado" )
		#define STR0021 If( cPaisLoc $ "ANG|PTG", " Intervalo Maior Do Que O Programado", " Intervalo Maior que o Programado" )
		#define STR0022 If( cPaisLoc $ "ANG|PTG", "** Marcações antes da admissão", "** Marcacoes antes da Admisssao    " )
		#define STR0023 If( cPaisLoc $ "ANG|PTG", "** Marcações após demissão", "** Marcacoes apos Demissao         " )
		#define STR0024 If( cPaisLoc $ "ANG|PTG", "** Marcações durante as férias", "** Marcacoes durante as Ferias     " )
		#define STR0025 If( cPaisLoc $ "ANG|PTG", "** Marcações durante afastamento", "** Marcacoes durante Afastamento   " )
		#define STR0027 "Filial: "
		#define STR0028 If( cPaisLoc $ "ANG|PTG", "Turno:", " Turno: " )
		#define STR0029 "    C.C: "
		#define STR0030 If( cPaisLoc $ "ANG|PTG", "C. Custo+ Nome", "C.Custo+Nome" )
		#define STR0031 If( cPaisLoc $ "ANG|PTG", "Número: ", "CHAPA: " )
		#define STR0032 If( cPaisLoc $ "ANG|PTG", "Reg.:", "MATR: " )
		#define STR0033 If( cPaisLoc $ "ANG|PTG", "Nome: ", "NOME: " )
		#define STR0034 "Departamento"
		#define STR0035 If( cPaisLoc $ "ANG|PTG", "Seleccionar a opção  de impressao: ", "Selecione a opção de impressão: " )
		#define STR0036 "Por Período"
		#define STR0037 "Por Datas"
		#define STR0038 If( cPaisLoc $ "ANG|PTG", "Depto: ", "DEPTO: " )
		#define STR0039 "Processo: "
		#define STR0040 "Período: "
		#define STR0041 If( cPaisLoc $ "ANG|PTG", "Mapa: ", "Roteiro: " )
		#define STR0042 If( cPaisLoc $ "ANG|PTG", "Num. Pgt.:", "Num. Pagto.:" )
		#define STR0043 If( cPaisLoc $ "ANG|PTG", "Este programa emite Relação dos Colaboradores com Divergências de Marcações", "Este programa emite Relacao dos Funcionarios com Divergencias de Marcacoes" )
		#define STR0044 If( cPaisLoc $ "ANG|PTG", "Colaboradores", "Funcionarios" )
		#define STR0045 If( cPaisLoc $ "ANG|PTG", "Ocorrências", "Ocorrencias" )
		#define STR0046 "Marcações"
		#define STR0047 "Data"
		#define STR0048 "C.Custo"
		#define STR0049 "Tno"
		#define STR0050 "Processo"
		#define STR0051 If( cPaisLoc $ "ANG|PTG", "Período", "Periodo" )
		#define STR0052 "Rot"
		#define STR0053 "NP"
		#define STR0054 "Depto"
	#endif
#endif
