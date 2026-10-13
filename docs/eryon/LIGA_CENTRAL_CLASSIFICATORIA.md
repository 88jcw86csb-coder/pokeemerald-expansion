# Liga Pokémon de Eryon — Cidade, classificatória e Elite Four

## Cidade e edifício

A Liga fica numa **capital de 96 × 72 blocos**, acessível a pé pelo Caminho da Liga. O edifício principal está no centro da praça, em (48, 36). A fachada dá acesso a uma **recepção**; a recepcionista só registra treinadores com as oito insígnias de Eryon.

## Classificatória obrigatória — oito fases

Uma inscrição válida leva a uma arena única com **oito sprites distintos**, um por adversário. O jogador pode conversar com os oponentes, mas cada combate só é liberado depois de ganhar todas as fases anteriores. Não existe atalho de warp contornando a inscrição.

| Fase | Competidor | Equipe | Níveis |
|---|---|---|---|
| 1 | Ivo | Luxray, Staraptor, Floatzel | 62–64 |
| 2 | Marta | Roserade, Milotic, Gardevoir | 63–65 |
| 3 | Pedro | Golem, Camerupt, Rhyperior | 64–66 |
| 4 | Noah | Alakazam, Espeon, Reuniclus | 65–67 |
| 5 | Ravi | Lucario, Conkeldurr, Mienshao | 66–68 |
| 6 | Luna | Togekiss, Whimsicott, Sylveon | 67–69 |
| 7 | Dante | Flygon, Kingdra, Haxorus | 68–70 |
| 8 | Elisa | Aegislash, Volcarona, Metagross | 69–71 |

Todos os Pokémon são oficiais até Kalos; nenhum fakemon e nenhuma HM para acessar o prédio.

### Regras do torneio

- Cada vitória registra uma flag de fase; a oitava registra a aprovação.
- Na **derrota**, a batalha normal do motor GBA aplica a penalidade de dinheiro e a mecânica de *whiteout*. Ao retornar para a arena, as oito vitórias e flags de treinadores são reiniciadas e a nova tentativa começa na fase 1.
- **Sair antes de completar** as oito fases também encerra a tentativa: ao reentrar, volta à fase 1. Isso evita sequências parciais indevidas e simplifica a recuperação após derrotas.
- Para não sobrepor os flags de insígnias, os oito novos treinadores usam flags reservadas separadas do intervalo legado de flags de treinadores.
- Depois de oito vitórias consecutivas, o jogador recebe acesso à **sala de recuperação**, onde pode curar todos os Pokémon e preparar o time.
- A aprovação não é removida ao visitar novamente a cidade. Ao regressar à recepção, o jogador aprovado pode ir diretamente para a sala de recuperação.

## Elite Four — etapa seguinte

A **antecâmara** está planejada como ligação da recuperação para quatro salas individuais e a sala do Campeão, tudo no mesmo complexo. **As quatro batalhas e a sala do Campeão ainda não estão implementadas nesta etapa.** A entrada da Elite Four permanece bloqueada por diálogo em vez de conduzir a uma sala falsa ou criar um bloqueio de HM.

## Validação

O repositório possui testes estáticos de oito sprites, oito IDs/parties distintas, oito flags de vitória, ordem das fases, exigência das oito insígnias, resets no evento de transição e sala de cura. Esses testes não substituem verificação no emulador, especialmente para penalidade monetária, whiteout, reinício após perder, salvamento e recarga.
