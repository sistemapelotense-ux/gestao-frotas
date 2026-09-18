# Gestão de Ativos em Obras

> Sistema web para controle diário de veículos alocados nas obras da empresa

## Problema
A empresa precisa controlar os veículos (ativos) que ficam alocados em obras diferentes, registrando diariamente onde cada ativo está e seu status de uso, e o administrador precisa verificar se todos os ativos estão alocados e detectar lançamentos duplicados (mesmo veículo em duas obras no mesmo dia)

_Hoje resolvem com_: Controle manual, sem sistema centralizado

## Decisões do dono (o que foi declarado completo)
- **Quem usa**: somente esses dois papéis: usuário da obra e administrador

## Papéis
- **Usuário da obra**: Faz lançamentos diários dos veículos da sua localidade; só vê os registros da sua obra
- **Administrador**: Acesso total: cadastros de ativos e usuários, visualização de todos os registros e verificação de alocação/duplicidade

## Entidades
- **Ativo (veículo)** (ativo): identificação, status
- **Obra (local)** (obra): nome, localização
- **Usuário** (usuario): nome, perfil, obra vinculada
- **Lançamento diário** (lancamento_diario): data, ativo, obra, status de uso, informações do dia, ativo (código), descrição, tipo, fabricante, modelo, horímetro inicial, horímetro final, total horas, km inicial, km final, total km, descritivo de manutenção e outros, status, condição climática
- **Arquivo de propriedade (lista de ativos da empresa)** (arquivo_de_propriedade): ativo, status

## Regras de Negócio
- [BR] quando um ativo cadastrado não estiver alocado em nenhuma obra no dia, então o sistema deve sinalizar isso ao administrador
- [BR] quando o mesmo veículo for lançado em duas obras no mesmo dia, então o sistema deve detectar e alertar a duplicidade
- [BR] quando um usuário de obra acessar os lançamentos, então só pode ver os registros da sua própria localidade
- [BR] quando o sistema consolidar os registros diários, então deve comparar a lista de ativos da empresa (arquivo de propriedade) com os registros do dia e apontar as divergências (ativo lançado em duas obras no mesmo dia; ativo da lista que não está registrado em nenhuma obra)
- [BR] quando a coluna "Status" do diário da obra estiver preenchida com O, D, P, C ou R, então o sistema considera o ativo como alocado na obra
- [BR] quando houver item no diário que não consta no arquivo de propriedade, então o sistema deve incluir o item no arquivo de propriedade identificado com status L (Locado)
- [BR] quando o usuário tentar salvar o registro diário, então o sistema só deve permitir se todos os campos estiverem preenchidos, exceto o campo "Descritivo de Manutenção e Outros", que não é obrigatório
- [BR] quando o sistema for consolidar (comparar ativos da empresa com os dias lançados), então só deve processar dias menores ou iguais ao dia anterior (ex.: sendo hoje 15/09/2026, processa apenas de 01/09/2026 até 15/09/2026)
- [BR] quando alguma obra não tiver efetuado o registro de um dia, então o sistema não pode processar esse dia (pois faltam informações para verificar a totalidade) e deve informar o usuário, identificando as obras sem lançamento

## Em Aberto (discovery)
- Como você imagina o visual das telas além da logo (cores, estilo, algo que devamos registrar)?

## Especificação: 96% completa