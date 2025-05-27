#Include "TOTVS.ch"
#Include "TopConn.ch"
#include "protheus.ch"
#include "rwmake.ch"                                         
#include "font.ch"
#include "colors.ch"   
#include "dbinfo.ch"  
#INCLUDE "tbiconn.ch"
#INCLUDE "TBICODE.CH"
#Include "aarray.ch"
  
//Comecar ler da posicao 0
Static nPosLjP := 2 //Coluna C no Excel
Static nPosCnpj := 3 //Coluna D no Excel
Static nPosDtVcto := 4 //Coluna E no Excel //Data Emissao
Static nPosCondPg := 5 //Coluna F no Excel
Static nPosVlr := 6 //Coluna G no Excel

//+------------------------------------------------------------------------+
//| Rotina | EUIMPCSV4 | Autor | Robson Herpich 	   | Data | 16.05.2024 |
//+------------------------------------------------------------------------+
//| Descr. | Importação de Pedidos de Venda - Cargas                       |
//+------------------------------------------------------------------------+

User Function EUIMPCSV4()

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
    Local cArqLog    := "zImpCSV2_" + dToS(Date()) + "_" + StrTran(Time(), ':', '-') + ".log"
    Local nTotLinhas := 0
    Local cLinAtu    := ""
    Local nLinhaAtu  := 0
    Local aLinha     := {}
    Local oArquivo
    Local aLinhas
    Local cCnpjCli := ""
    Local cCodCli   := ""
    Local cLojaCli   := ""
    Local cDtVcto   := ""
    Local cCondPgto := ""
    Local nValor := 0
    Local cLjParc := ""
    Private cDirLog    := GetTempPath() + "x_importacao2\"
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
                If ! "CPF" $ Upper(cLinAtu) //or Lower
  
                    //Zera as variaveis
                    cCnpjCli   := aLinha[nPosCnpj]
                    cDtVcto    := aLinha[nPosDtVcto]
                    cCondPgto  := aLinha[nPosCondPg]
                    nValor     := aLinha[nPosVlr]
                    cLjParc    := aLinha[nPosLjP]
  
                    DbSelectArea('SA1')
                    //SA1->(DbSetOrder(3)) // Filial + CNPJ(CGC) //Alterar para indice 14 (Indice E filial + cnpj + loja_parceiro)
                    SA1->(DbSetOrder(14))
  
                    //Se conseguir posicionar no Cliente
                    If SA1->(DbSeek(FWxFilial('SA1') + cCnpjCli + cLjParc))

                        //Prepara para implantacao do Pedido De venda.
                        cCodCli   := SA1->A1_COD
                        cLojaCli   := SA1->A1_LOJA

                        MontaCabec(cCodCli,cLojaCli,cDtVcto,cCondPgto,nValor)

                    Else
                        cLog += "- Lin" + cValToChar(nLinhaAtu) + ", Cliente [" + cCnpjCli + "] não encontrados no Protheus;" + CRLF
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



Static Function MontaCabec(cCodCli,cLojaCli,cDtVcto,cCondPgto,nValor)

    Local aCabec := {}
    Local aItens := {}
    Local aItem := {}
    Local cTes := "511"
    Local cProduto := "0641000002"
    Local nX
    Local cUm := "UN"
    Local cNumePedi := ""
    Local cEmissao :=  cDtVcto //Date()
    Local cHora := SubStr(Time(),1,5)
    Local cTabela := "422"
    Local cVend := "000001"
    Local cNatureza := "2152101005" 
    Local cNomeCli := ""
    Local cVlrTot := 0
    Private aHeader := {}
    Private aCols := {}

        DbSelectArea("SC6")
        SC6->(DBGoTop())

            DbSelectArea("SB1")
            SB1->(DBGoTop())
     
                cUm := POSICIONE("SB1",1,xFilial("SB1") + cProduto, "B1_UM")

            SB1->(DBCloseArea())
            aItem := {}

            //Tratamento do Valor
            nValor := Replace(nValor, ",", ".")

            AADD(aItem, {"C6_ITEM"   , '01'         		, NIL})
            AADD(aItem, {"C6_PRODUTO", cProduto 	        , NIL})
            AADD(aItem, {"C6_QTDVEN" , 1            		, NIL})
            AADD(aItem, {"C6_PRUNIT" , val(nValor)		    , NIL})
            AADD(aItem, {"C6_PRCVEN" , val(nValor)		    , NIL})
            AADD(aItem, {"C6_QTDLIB" , 1            	    , NIL})
            AADD(aItem, {"C6_UM"     , cUm 	                , NIL})
            AADD(aItem, {"C6_TES"    ,cTes                  , NIL})
            AADD(aItem, {"C6_LOCAL"  , "01"                 , NIL})
        
        SC6->(DbCloseArea())

       //Adiciona aItem ao Array de Itens
       AADD(aItens, aItem)  

       cNomeCli := POSICIONE("SA1",1,xFilial("SA1") + cCodCli + cLojaCli , "A1_NOME")


    dbSelectArea("SC5")
    SC5->(DBGoTop())
    
        //cNumePedi := GetSX8Num("SC5","C5_NUM") // Busca numero do Pedido

        //Monta Cabeçalho do Pedido
        aCabec := {}
        AADD(aCabec,{"C5_FILIAL"  , cFilAnt             ,Nil})
        AADD(aCabec,{"C5_TIPO"    ,"N"        	        ,NIL})
        AADD(aCabec,{"C5_TIPOCLI" ,"F"        	        ,NIL})
        AADD(aCabec,{"C5_X_NOME"  ,cNomeCli    	        ,NIL})
        AADD(aCabec,{"C5_X_VLTOT"  ,val(nValor)	        ,NIL})
        //AADD(aCabec,{"C5_NUM"	  , cNumePedi	        ,Nil})
        AADD(aCabec,{"C5_CLIENTE" ,cCodCli 	            ,NIL})
        AADD(aCabec,{"C5_LOJACLI" ,cLojaCli 	        ,NIL})
        AADD(aCabec,{"C5_EMISSAO" ,cToD(cEmissao)     	,NIL})
        AADD(aCabec,{"C5_HORA"    ,cHora    	        ,NIL})
        AADD(aCabec,{"C5_CONDPAG" ,cCondPgto    	    ,NIL})
        AADD(aCabec,{"C5_VEND1"   ,cVend        	    ,NIL})
        AADD(aCabec,{"C5_NATUREZ" ,cNatureza		    ,NIL})

    SC5->(DbCloseArea())

    //Chama Funcao de ExecAuto
    GERAPED(aCabec,aItens)

Return 


Static Function GERAPED(aCabec,aItens)

    Local nOpc := 3 //Inclusao
	Private lMostraErro := .F.
    Private lMsErroAuto := .F.

	Begin Transaction
		
			MSEXECAUTO({|X,Y,Z|MATA410(X,Y,Z)},aCabec, aItens, nOpc)

            //Mostraerro()

            If lMsErroAuto
                DisarmTransaction()
                Mostraerro()
            Else
                ConfirmSX8()
            EndIf			

    End Transaction

Return
