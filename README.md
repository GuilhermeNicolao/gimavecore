⁉️ **Seja bem-vindo! Este repositório é dividido em duas pastas principais.**



➡ **Automações**: As automações disponíveis no repositório contemplam um sistema interno utilizado na empresa onde trabalho e o Protheus. I) A automação 'Baixa Credenciados' foi criada utilizando Selenium para navegar pelo Protheus até o módulo de Contas a Pagar e realizar a montagem de borderôs. O script compara o número do título que está no Protheus com o número do título que está em uma planilha que o usuário irá informar o diretório, se der 'match' ele marca a flag e quando chegar a 100 títulos ele salva o borderô dentro do Protheus e informa dentro da planilha quais títulos pertencem a qual número de borderô. A baixa destes borderôs continua sendo manual. II) As 'Fontes Protheus' são fontes disponibilizadas por um consultor externo que realizou algumas integrações para a empresa, crédito a ele, Sr. Robson e futuramente fontes de minha criação.


Seguindo para as III) 'Liberações TEDs' é uma automação que procura quais transferências liberar dentro de uma planilha e compara os dados com um sistema interno da empresa que faz liberação de transferências eletrônicas. Por fim, as IV) 'Nfs Sucesso' é um script criado pelo autor Adryan Luiz que busca as notas fiscais nas prefeituras e as disponibiliza para o time de 'Sucesso' da empresa para que possam estar repassando aos usuários.

        



➡ **ERP**: O ERP foi uma criação minha que surgiu para suprir uma necessidade do time de Compras: Controle de orçamentos. O módulo 'Compras' foi o primeiro a ser criado e conta com cadastros de fornecedores, produtos, categorias e por fim, orçamentos. O sistema permite a criação de orçamentos, a comparação entre eles para validação e um dashboard mostrando a economia realizada dentro de um determinado período. Por fim outros dois módulos foram criados: Comercial e Financeiro. O Comercial conta com uma tela de parâmetros comerciais, uma tela de simulação de propostas e uma tela de relatórios analíticos para três produtos oferecidos pela empresa. O modulo financeiro, até o momento, contempla apenas um dashboard com todas as contas bancárias do ecossistema e em qual data cada uma está conciliada.

• **Linguagens utilizadas neste repositório**: Python, Html, CSS e JS.
