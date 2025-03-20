#include "protheus.ch"
#include "rwmake.ch"                                         
#include "font.ch"
#include "colors.ch"   
#include "dbinfo.ch"  
#include "topconn.ch"   
#INCLUDE "tbiconn.ch"
#INCLUDE "TBICODE.CH"
#Include "aarray.ch"

  
//Comecar ler da posicao 0
Static nPosCodCli   := 1 //Coluna A
Static nPosLjCli    := 2 //Coluna B
Static nPosDtEmiss  := 3 //Coluna C
Static nPosQtdLib   := 4 //Coluna D
Static nPosCongPg   := 5 //Coluna E
Static nPosMsgNf1   := 6 //Coluna F
Static nPosMsgNf2   := 7 //Coluna G
Static nPosPrd1	    := 8 //Coluna H
Static nPosTes1	    := 9 //Coluna I
Static nPosVlr1     := 10 //Coluna J
Static nPosDesc1    := 11 //Coluna K
Static nPosDtEntr   := 12 //Coluna L
Static nPosIss1     := 13 //Coluna M
Static nPosPrd2     := 14 //Coluna N
Static nPosTes2     := 15 //Coluna O
Static nPosVlr2     := 16 //Coluna P
Static nPosDesc2	:= 17 //Coluna Q
Static nPosIss2     := 18 //Coluna R
Static nPosPrd3     := 19 //Coluna S
Static nPosTes3     := 20 //Coluna T
Static nPosVlr3     := 21 //Coluna U
Static nPosDesc3    := 22 //Coluna V
Static nPosIss3     := 23 //Coluna W
Static nPosPrd4     := 24 //Coluna X
Static nPosTes4     := 25 //Coluna Y
Static nPosVlr4     := 26 //Coluna Z
Static nPosDesc4    := 27 //Coluna AA
Static nPosIss4     := 28 //Coluna AB
Static nPosPedOri   := 29 //Coluna AC

//+------------------------------------------------------------------------+
//| Rotina | IMPCSV05 | Autor | Robson Herpich 	       | Data | 10.07.2024 |
//+------------------------------------------------------------------------+
//| Descr. | Importação de Pedidos de Venda - Gimave                       |
//+------------------------------------------------------------------------+

User Function IMPCSV05()

    Local aArea     := GetArea()
    Private cArqOri := ""

    cArqOri := tFileDialog( "CSV files (*.csv) ", 'Seleção de Arquivos', , , .F., )
      
    If ! Empty(cArqOri)
          
        //Somente se existir o arquivo e for com a extensão CSV
        If File(cArqOri) .And. Upper(SubStr(cArqOri, RAt('.', cArqOri) + 1, 3)) == 'CSV'
            Processa({|| fImporta2() }, "Importando...")
        Else
            MsgStop("Arquivo e/ou extensão inválida!", "Atenção")
        EndIf
        
    EndIf
      
    RestArea(aArea)
Return
  
/*-------------------------------------------------------------------------------*
 | Func:  fImporta                                                               |
 | Desc:  Função que importa os dados                                            |
 *-------------------------------------------------------------------------------*/
  
Static Function fImporta2()

    Local aArea      := GetArea()
    Local cArqLog    := "zImpCSV05_" + dToS(Date()) + "_" + StrTran(Time(), ':', '-') + ".log"
    Local nTotLinhas := 0
    Local cLinAtu    := ""
    Local nLinhaAtu  := 0
    Local aLinha     := {}
    Local oArquivo
    Local aLinhas
    Local cCodCli   := "" 
    Local cLjCli    := ""
    Local dDtemissao := ""
    Local nQtdLib   := 0
    Local cCondPg   := ""
    Local cMsgNf1   := ""
    Local cMsgNf2   := ""
    Local cPrd1	    := ""
    Local cTes1	    := ""
    Local nVlr1     := 0
    Local nDesc1    := 0
    Local dDtEntr   := ""
    Local cPrd2     := ""
    Local cTes2     := ""
    Local nVlr2     := 0
    Local nDesc2	:= 0
    Local cPrd3     := ""
    Local cTes3     := ""
    Local nVlr3     := 0
    Local nDesc3    := 0	
    Local cPrd4     := ""
    Local cTes4     := ""
    Local nVlr4     := 0
    Local nDesc4    := 0
    Local cNatureza := ""
    Local cCodVend := ""
    Local cTipoCli := ""
    Local nAbatIss1 := 0
    Local nAbatIss2 := 0
    Local nAbatIss3 := 0
    Local nAbatIss4 := 0
    Local nPedOrig  := 0

    Private cDirLog    := GetTempPath() + "x_importacao5\"
    Private cLog       := ""
      
    //Se a pasta de log não existir, cria ela
    If ! ExistDir(cDirLog)
        MakeDir(cDirLog)
    EndIf
  
    //Definindo o arquivo a ser lido
    oArquivo := FWFileReader():New(cArqOri)
      
    If (oArquivo:Open())
  
        If ! (oArquivo:EoF())
  
            aLinhas := oArquivo:GetAllLines()
            nTotLinhas := Len(aLinhas)
            ProcRegua(nTotLinhas)
              
            oArquivo:Close()
            oArquivo := FWFileReader():New(cArqOri)
            oArquivo:Open()
  
            While (oArquivo:HasLine())
  
                //Incrementa na tela a mensagem
                nLinhaAtu++
                IncProc("Analisando linha " + cValToChar(nLinhaAtu) + " de " + cValToChar(nTotLinhas) + "...")
                  
                //Pegando a linha atual e transformando em array
                cLinAtu := oArquivo:GetLine()
                aLinha  := StrTokArr(cLinAtu, ";")
                  
                //Se não for o cabeçalho (encontrar o texto "Código" na linha atual)
                If ! "TES" $ Upper(cLinAtu) //or Lower
  
                    //Zera as variaveis
                    cCodCli   := aLinha[nPosCodCli]
                    cLjCli    := aLinha[nPosLjCli]
                    dDtemissao :=  aLinha[nPosDtEmiss]
                    nQtdLib := aLinha[nPosQtdLib]
                    cCondPg   := aLinha[nPosCongPg]
                    cMsgNf1   := aLinha[nPosMsgNf1]
                    cMsgNf2   := aLinha[nPosMsgNf2]
                    cPrd1	  := aLinha[nPosPrd1]
                    cTes1	  := aLinha[nPosTes1]
                    nVlr1     := aLinha[nPosVlr1]
                    nDesc1    := aLinha[nPosDesc1]
                    dDtEntr   := aLinha[nPosDtEntr]
                    nAbatIss1 := aLinha[nPosIss1]
                    cPrd2     := aLinha[nPosPrd2]
                    cTes2     := aLinha[nPosTes2]
                    nVlr2     := aLinha[nPosVlr2]
                    nDesc2	  := aLinha[nPosDesc2]
                    nAbatIss2 := aLinha[nPosIss2]
                    cPrd3     := aLinha[nPosPrd3]
                    cTes3     := aLinha[nPosTes3]
                    nVlr3     := aLinha[nPosVlr3]
                    nDesc3    := aLinha[nPosDesc3]
                    nAbatIss3 := aLinha[nPosIss3]
                    cPrd4     := aLinha[nPosPrd4]
                    cTes4     := aLinha[nPosTes4]
                    nVlr4     := aLinha[nPosVlr4]
                    nDesc4    := aLinha[nPosDesc4]
                    nAbatIss4 := aLinha[nPosIss4]
                    nPedOrig  := aLinha[nPosPedOri]
  
                    DbSelectArea('SA1')
                    //SA1->(DbSetOrder(1)) // Filial + Codigo + Loja
                    SA1->(DbSetOrder(1))
  
                    //Se conseguir posicionar no Cliente
                    If SA1->(DbSeek(FWxFilial('SA1') + cCodCli + cLjCli))

                        //Prepara para implantacao do Pedido De venda.
                        cCodCli   := SA1->A1_COD
                        cLjCli   := SA1->A1_LOJA
                        cNatureza := SA1->A1_NATUREZ
                        cCodVend := SA1->A1_VEND
                        cTipoCli := SA1->A1_TIPO

                        MontaCabec(cCodCli,cLjCli,dDtemissao,nQtdLib,cNatureza,cCodVend,cTipoCli,cCondPg,cMsgNf1,cMsgNf2,cPrd1,cTes1,nVlr1,nDesc1,dDtEntr,cPrd2,cTes2,nVlr2,nDesc2,cPrd3,cTes3,nVlr3,nDesc3,cPrd4,cTes4,nVlr4,nDesc4,nAbatIss1,nAbatIss2,nAbatIss3,nAbatIss4,nPedOrig)

                    Else
                        cLog += "- Lin" + cValToChar(nLinhaAtu) + ", Cliente: ["+cCodCli+' - Loja: ' + cLjCli +  "] não encontrados no Protheus;" + CRLF
                    EndIf
                      
                Else
                    cLog += "- Lin" + cValToChar(nLinhaAtu) + ", linha não processada - cabeçalho;" + CRLF
                EndIf
                  
            EndDo
  
            //Se tiver log, mostra ele
            If ! Empty(cLog)
                cLog := "Processamento finalizado, abaixo as mensagens de log: " + CRLF + cLog
                MemoWrite(cDirLog + cArqLog, cLog)
                ShellExecute("OPEN", cArqLog, "", cDirLog, 1)
            EndIf
  
        Else
            MsgStop("Arquivo não tem conteúdo!", "Atenção")
        EndIf
  
        //Fecha o arquivo
        oArquivo:Close()
    Else
        MsgStop("Arquivo não pode ser aberto!", "Atenção")
    EndIf
  
    RestArea(aArea)
Return



Static Function MontaCabec(cCodCli,cLjCli,dDtemissao,nQtdLib,cNatureza,cCodVend,cTipoCli,cCondPg,cMsgNf1,cMsgNf2,cPrd1,cTes1,nVlr1,nDesc1,dDtEntr,cPrd2,cTes2,nVlr2,nDesc2,cPrd3,cTes3,nVlr3,nDesc3,cPrd4,cTes4,nVlr4,nDesc4,nAbatIss1,nAbatIss2,nAbatIss3,nAbatIss4,nPedOrig)

    Local aCabec := {}
    Local aItens := {}
    Local aItem := {}
    Local nX
    Local cUm := "UN"
    Local cEmissao :=  dDtEntr //Date()
    Local cHora := SubStr(Time(),1,5)
    Local cNomeCli := ""
    Local nVlrTot1 := 0
    Local nVlrTot2 := 0
    Local nVlrTot3 := 0
    Local nVlrTot4 := 0
    Local nVlrTotG := 0
    Local cMsgNota := ""
    Local aItens := {}
    Private aHeader := {}
    Private aCols := {}

        DbSelectArea("SC6")
        SC6->(DBGoTop())

            aItem := {}

            If alltrim(cPrd1) != "*"    

                DbSelectArea("SB1")
                SB1->(DBGoTop())
                    cUm := POSICIONE("SB1",1,xFilial("SB1") + cPrd1, "B1_UM")
                SB1->(DBCloseArea())

                //Tratamento do Valor
                nVlr1 := Replace(nVlr1, ".", "")
                nVlr1 := Replace(nVlr1, ",", ".")
                //Tratamento Desconto
                If alltrim(nDesc1) == ""
                    nDesc1 := 0
                Else 
                    nDesc1 := Replace(nDesc1, ".", "")
                    nDesc1 := Replace(nDesc1, ",", ".")                
                EndIf
                //Tratamento ISS
                If alltrim(nAbatIss1) == ""
                    nAbatIss1 := 0
                Else 
                    nAbatIss1 := Replace(nAbatIss1, ".", "")
                    nAbatIss1 := Replace(nAbatIss1, ",", ".")                
                EndIf

                AADD(aItem, {"C6_ITEM"   , '01'         		, NIL})
                AADD(aItem, {"C6_PRODUTO", cPrd1     	        , NIL})
                AADD(aItem, {"C6_QTDVEN" , 1            		, NIL})
                AADD(aItem, {"C6_PRUNIT" , val(nVlr1)		    , NIL})
                AADD(aItem, {"C6_PRCVEN" , val(nVlr1)		    , NIL})
                AADD(aItem, {"C6_QTDLIB" , val(nQtdLib)    	    , NIL})
                AADD(aItem, {"C6_UM"     , cUm 	                , NIL})
                AADD(aItem, {"C6_TES"    ,cTes1                 , NIL})
                AADD(aItem, {"C6_VALDESC", val(nDesc1)		    , NIL})
                AADD(aItem, {"C6_ENTREG" ,cToD(dDtEntr)      	, NIL})
                AADD(aItem, {"C6_LOCAL"  , "01"                 , NIL})
                AADD(aItem, {"C6_ABATISS", val(nAbatIss1)       , NIL})

                AADD(aItens, aItem)    
                nVlrTot1 := val(nVlr1) - val(nDesc1) 

            EndIf

            If alltrim(cPrd2) != "*"    

                DbSelectArea("SB1")
                SB1->(DBGoTop())
                    cUm := POSICIONE("SB1",1,xFilial("SB1") + cPrd2, "B1_UM")
                SB1->(DBCloseArea())

                //Tratamento do Valor
                nVlr2 := Replace(nVlr2, ".", "")
                nVlr2 := Replace(nVlr2, ",", ".")
                //Tratamento Desconto
                If alltrim(nDesc2) == ""
                    nDesc2 := 0
                Else 
                    nDesc2 := Replace(nDesc2, ".", "")
                    nDesc2 := Replace(nDesc2, ",", ".")                
                EndIf
                //Tratamento ISS
                If alltrim(nAbatIss2) == ""
                    nAbatIss2 := 0
                Else 
                    nAbatIss2 := Replace(nAbatIss2, ".", "")
                    nAbatIss2 := Replace(nAbatIss2, ",", ".")                
                EndIf

                aItem := {}
                AADD(aItem, {"C6_ITEM"   , '02'         		, NIL})
                AADD(aItem, {"C6_PRODUTO", cPrd2     	        , NIL})
                AADD(aItem, {"C6_QTDVEN" , 1            		, NIL})
                AADD(aItem, {"C6_PRUNIT" , val(nVlr2)		    , NIL})
                AADD(aItem, {"C6_PRCVEN" , val(nVlr2)		    , NIL})
                AADD(aItem, {"C6_QTDLIB" , val(nQtdLib)    	    , NIL})
                AADD(aItem, {"C6_UM"     , cUm 	                , NIL})
                AADD(aItem, {"C6_TES"    , cTes2                , NIL})
                AADD(aItem, {"C6_VALDESC", val(nDesc2)		    , NIL})                
                AADD(aItem, {"C6_ENTREG" ,cToD(dDtEntr)        	, NIL})                
                AADD(aItem, {"C6_LOCAL"  , "01"                 , NIL})
                AADD(aItem, {"C6_ABATISS", val(nAbatIss2)       , NIL})

                AADD(aItens, aItem)
                nVlrTot2 := val(nVlr2) - val(nDesc2) 

            EndIf

            If alltrim(cPrd3) != "*"    

                DbSelectArea("SB1")
                SB1->(DBGoTop())
                    cUm := POSICIONE("SB1",1,xFilial("SB1") + cPrd3, "B1_UM")
                SB1->(DBCloseArea())

                //Tratamento do Valor
                nVlr3 := Replace(nVlr3, ".", "")
                nVlr3 := Replace(nVlr3, ",", ".")
                //Tratamento Desconto
                If alltrim(nDesc3) == ""
                    nDesc3 := 0
                Else 
                    nDesc3 := Replace(nDesc3, ".", "")
                    nDesc3 := Replace(nDesc3, ",", ".")                
                EndIf
                //Tratamento ISS
                If alltrim(nAbatIss3) == ""
                    nAbatIss3 := 0
                Else 
                    nAbatIss3 := Replace(nAbatIss3, ".", "")
                    nAbatIss3 := Replace(nAbatIss3, ",", ".")                
                EndIf

                aItem := {}
                AADD(aItem, {"C6_ITEM"   , '03'         		, NIL})
                AADD(aItem, {"C6_PRODUTO", cPrd3     	        , NIL})
                AADD(aItem, {"C6_QTDVEN" , 1            		, NIL})
                AADD(aItem, {"C6_PRUNIT" , val(nVlr3)		    , NIL})
                AADD(aItem, {"C6_PRCVEN" , val(nVlr3)		    , NIL})
                AADD(aItem, {"C6_QTDLIB" , val(nQtdLib)    	    , NIL})
                AADD(aItem, {"C6_UM"     , cUm 	                , NIL})
                AADD(aItem, {"C6_TES"    , cTes3                , NIL})
                AADD(aItem, {"C6_VALDESC", val(nDesc3)		    , NIL})                
                AADD(aItem, {"C6_ENTREG" ,cToD(dDtEntr)        	, NIL})
                AADD(aItem, {"C6_LOCAL"  , "01"                 , NIL})
                AADD(aItem, {"C6_ABATISS", val(nAbatIss3)       , NIL})

                AADD(aItens, aItem)
                nVlrTot3 := val(nVlr3) - val(nDesc3) 

            EndIf

            If alltrim(cPrd4) != "*"    

                DbSelectArea("SB1")
                SB1->(DBGoTop())
                    cUm := POSICIONE("SB1",1,xFilial("SB1") + cPrd4, "B1_UM")
                SB1->(DBCloseArea())

                //Tratamento do Valor
                nVlr4 := Replace(nVlr4, ".", "")
                nVlr4 := Replace(nVlr4, ",", ".")
                //Tratamento Desconto
                If alltrim(nDesc4) == ""
                    nDesc4 := 0
                Else 
                    nDesc4 := Replace(nDesc4, ".", "")
                    nDesc4 := Replace(nDesc4, ",", ".")                
                EndIf
                //Tratamento ISS
                If alltrim(nAbatIss4) == ""
                    nAbatIss4 := 0
                Else 
                    nAbatIss4 := Replace(nAbatIss4, ".", "")
                    nAbatIss4 := Replace(nAbatIss4, ",", ".")                
                EndIf

                aItem := {}
                AADD(aItem, {"C6_ITEM"   , '04'         		, NIL})
                AADD(aItem, {"C6_PRODUTO", cPrd4     	        , NIL})
                AADD(aItem, {"C6_QTDVEN" , 1            		, NIL})
                AADD(aItem, {"C6_PRUNIT" , val(nVlr4)		    , NIL})
                AADD(aItem, {"C6_PRCVEN" , val(nVlr4)		    , NIL})
                AADD(aItem, {"C6_QTDLIB" , val(nQtdLib)    	    , NIL})
                AADD(aItem, {"C6_UM"     , cUm 	                , NIL})
                AADD(aItem, {"C6_TES"    , cTes4                , NIL})
                AADD(aItem, {"C6_VALDESC", val(nDesc4)		    , NIL})                
                AADD(aItem, {"C6_ENTREG" ,cToD(dDtEntr)     	, NIL})                
                AADD(aItem, {"C6_LOCAL"  , "01"                 , NIL})
                AADD(aItem, {"C6_ABATISS", val(nAbatIss4)       , NIL})

                AADD(aItens, aItem)
                nVlrTot4 := val(nVlr4) - val(nDesc4)

            EndIf

            //Total Geral do Pedido
            nVlrTotG := (nVlrTot1 + nVlrTot2 + nVlrTot3 + nVlrTot4)
   
        SC6->(DbCloseArea())

       cNomeCli := POSICIONE("SA1",1,xFilial("SA1") + cCodCli + cLjCli , "A1_NOME")

        If alltrim(cCodVend) == ""
            cCodVend = '000152' 
        EndIf 

        //Tratamento para Mensagem da Nota
        if cMsgNf1 != '*'
            cMsgNota = cMsgNf1
        EndIf 

        if cMsgNf2 != '*'
            cMsgNota += ' '+ cMsgNf2
        EndIf 

    dbSelectArea("SC5")
    SC5->(DBGoTop())
    
        //Monta Cabeçalho do Pedido
        aCabec := {}
        AADD(aCabec,{"C5_FILIAL"  , cFilAnt             ,Nil})
        AADD(aCabec,{"C5_TIPO"    ,"N"        	        ,NIL})
        AADD(aCabec,{"C5_TIPOCLI" ,cTipoCli    	        ,NIL})
        AADD(aCabec,{"C5_X_NOME"  ,cNomeCli    	        ,NIL})
        AADD(aCabec,{"C5_X_VLTOT"  ,nVlrTotG            ,NIL})
        AADD(aCabec,{"C5_CLIENTE" ,cCodCli 	            ,NIL})
        AADD(aCabec,{"C5_LOJACLI" ,cLjCli    	        ,NIL})
        AADD(aCabec,{"C5_EMISSAO" ,cToD(dDtemissao)    	,NIL})
        AADD(aCabec,{"C5_HORA"    ,cHora    	        ,NIL})
        AADD(aCabec,{"C5_CONDPAG" ,cCondPg      	    ,NIL})
        AADD(aCabec,{"C5_VEND1"   ,cCodVend        	    ,NIL})
        AADD(aCabec,{"C5_NATUREZ" ,cNatureza		    ,NIL})
        if (Alltrim(cMsgNota) != "")
            AADD(aCabec,{"C5_MENNOTA" ,cMsgNota		    ,NIL})
        EndIf
        AADD(aCabec,{"C5_X_PORIG" ,nPedOrig		        ,NIL})

    SC5->(DbCloseArea())

    //Chama Funcao de ExecAuto
    GERAPED(aCabec,aItens)

Return 


Static Function GERAPED(aCabec,aItens)

    Local nOpc := 3 //Inclusao
    Local aHeader := {}
    Local xx    
    Local nCountIt
	Private lMostraErro := .F.
    Private lMsErroAuto := .F.


    aHeader := fxOrdenaSX3(aCabec)
    for xx := 1 to Len(aItens)
        nCountIt++
        if (nCountIt <= xx ) 
            aItens := fxOrdenaSX3(aItens[xx])
        EndIf
    next xx

	Begin Transaction
		
			MSEXECAUTO({|X,Y,Z|MATA410(X,Y,Z)},aHeader, aItens, nOpc)

            If lMsErroAuto
                DisarmTransaction()
                Mostraerro()
            Else
                ConfirmSX8()
            EndIf		

    End Transaction

Return



Static Function fxOrdenaSX3(aCampos)

	Local aWithPos := {}
	Local aOrdenado := {}
	Local a
    
    //Le o array passado como parametro e coloca a posição de cada campo
    For a:= 1 to len(aCampos)
        aadd(aWithPos,{aCampos[a,1],aCampos[a,2], aCampos[a,3], fxPos(aCampos[a,1])})
    Next            

    //Ordena o array de acordo com a posição dos campos
    ASORT(aWithPos, , , { | x,y | x[4] < y[4] } )

    //Monta o novo array somente com os campos originais, mas agora ordenado
    For a:=1 to Len(aWithPos)
        aadd(aOrdenado,{aWithPos[a,1],aWithPos[a,2], aWithPos[a,3]})	
    Next

Return aOrdenado


Static Function fxPos(cCampo)
	Local nPos  := 0

	nPos := POSICIONE("SX3", 2, cCampo, "X3_ORDEM")

Return nPos
