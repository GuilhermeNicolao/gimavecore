#include "protheus.ch"
#include "rwmake.ch"                                         
#include "font.ch"
#include "colors.ch"   
#include "dbinfo.ch"  
#include "topconn.ch"   
#INCLUDE "tbiconn.ch"
#INCLUDE "TBICODE.CH"
#Include "aarray.ch"

 
/*------------------------------------------------------------------------------------------------------*
 | P.E.:  M460FIM                                                                                       |
 | Desc:  Gravação dos dados após gerar NF de Saída                                                     |
 | Links: http://tdn.totvs.com/pages/releaseview.action?pageId=6784180                                  |
 *------------------------------------------------------------------------------------------------------*/
//15.01.2025 - Robson 
User Function M460FIM()

    Local cPedido  := ''
    Local cPedOrig   := ''
    Local aAreaSF2 := SF2->(GetArea())
    Local aAreaSD2 := sd2->(GetArea())
    Local aAreaSC5 := sc5->(GetArea())
    Local aAreaSE1 := sE1->(GetArea())
    Local aAreaSA1 := sA1->(GetArea())
     
    If cEmpAnt == "06" //Gimave

        //Pega o pedido
        DbSelectArea("SD2")
        SD2->(DbSetorder(3))
        If SD2->(DbSeek(SF2->(F2_FILIAL+F2_DOC+F2_SERIE+F2_CLIENTE+F2_LOJA)))
            cPedido := SD2->D2_PEDIDO
        Endif          
        
        //Se tiver pedido
        If !Empty(cPedido)
            DbSelectArea("SC5")
            SC5->(DbSetorder(1))
            
            //Se posiciona pega o tipo de pagamento
            If SC5->(DbSeek(FWxFilial('SC5')+cPedido))
                cPedOrig := SC5->C5_X_PORIG //Pedido Original - Importado através da planilha
            Endif
        Endif
        
        //Filtra títulos dessa nota
        cSql := "SELECT R_E_C_N_O_ AS REC FROM "+RetSqlName("SE1")
        cSql += " WHERE E1_FILIAL = '"+xFilial("SE1")+"' AND D_E_L_E_T_<>'*' "
        cSql += " AND E1_PREFIXO = '"+SF2->F2_SERIE+"' AND E1_NUM = '"+SF2->F2_DOC+"' "
        cSql += " AND E1_TIPO = 'NF' "
        TcQuery ChangeQuery(cSql) New Alias "_QRY"
        
        //Enquanto tiver dados na query
        While !_QRY->(eof())
            DbSelectArea("SE1")
            SE1->(DbGoTo(_QRY->REC))
            
            //Se tiver dado
            If !SE1->(EoF())
                RecLock("SE1",.F.)
                    Replace E1_X_PORIG WITH cPedOrig  //Atualiza o campo com o Pedido de Venda original que estava informado na planilha
                MsUnlock()
            EndIf
            
            _QRY->(DbSkip())
        Enddo
        _QRY->(DbCloseArea())

    EndIf        
     
    RestArea(aAreaSF2)
    RestArea(aAreaSD2)
    RestArea(aAreaSC5)
    RestArea(aAreaSE1)
    RestArea(aAreaSA1)
    
Return
