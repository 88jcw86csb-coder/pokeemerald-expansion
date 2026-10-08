# Eryon — Identidade de Rotas e Áreas

## Regra principal
Nenhuma rota de Eryon deve ser apenas uma troca de nome de uma rota de Hoenn. Os mapas serão tratados como áreas com identidade própria de terreno, geometria, exploração, encontros e narrativa.

## Primeira região jogável

### Vila Aurora
- Pequena vila cercada por colinas e campos de flores.
- Saída principal por uma trilha de terra para leste.
- Laboratório da Professora Elya em posição central, sem copiar a estrutura de Littleroot.
- Pequena praça, mirante e acesso futuro a uma trilha secundária.

### Rota 01 — Trilha dos Ventos
- Corredor irregular e mais largo, com três faixas de terreno: campo baixo, encosta e margem de riacho.
- Pequenas bifurcações permitem atalhos, mas nenhum caminho é uma linha reta.
- Primeiros treinadores opcionais ficam fora do caminho principal.
- Pokémon iniciais de campo e aves comuns, sem copiar a distribuição de Route 101.
- Ao norte existe uma passagem bloqueada que será revisitada mais tarde.

### Bosque de Lúmina
- Área florestal grande e obrigatória entre Rota 01 e Rota 02.
- Estrutura de labirinto leve, com clareiras conectadas por trilhas.
- Árvores densas, pequenos cursos d'água, pedras, cogumelos e áreas de sombra.
- Uma clareira central serve como ponto de descanso.
- Área com encontros próprios e maior variedade de Pokémon.
- Primeira manifestação clara da anomalia ligada ao Eclipse.
- Exploração lateral e itens escondidos são parte do desenho.

### Rota 02 — Caminho das Águas
- Não será outra faixa reta de grama.
- O caminho acompanha um rio, alternando margens, pontes baixas e pequenas áreas elevadas.
- Uma passagem opcional leva a uma área de pesca e item escondido.
- Treinadores ficam distribuídos em posições que incentivam exploração.
- O jogador chega a Verdelume por uma entrada diferente da saída do Bosque.

### Verdelume
- Cidade construída em torno de jardins, canais e uma antiga árvore central.
- O Ginásio de Kael integra-se ao ambiente natural.
- Ruas não serão uma grade simples: praça central, vielas laterais e área residencial elevada.

## Identidade das regiões posteriores

### Neonara
Cidade elétrica/industrial com cabos, subestações e passarelas. Rotas próximas usam postes, campos abertos e instalações técnicas.

### Frostheim
Região montanhosa fria. Rotas usam desníveis, neve, cavernas e caminhos alternativos. Evitar qualquer rota plana e linear.

### Arkhara
Região arqueológica. Rotas são secas e pedregosas, com cânions, ruínas e caminhos parcialmente soterrados.

### Umbra
Pântanos, neblina, cavernas e trilhas noturnas. Rotas têm navegação por pontos de referência e áreas opcionais.

### Ignivar
Região vulcânica. Rotas alternam lava, cinzas, encostas e túneis. Algumas áreas mudam visualmente durante a história.

### Lunaris
Região elevada ligada ao observatório. Trilhas abertas, campos noturnos, ruínas celestes e caminhos para pontos panorâmicos.

### Drakonia
Vales, rios e montanhas. Rotas são longas, com rios atravessáveis, pontes naturais, cavernas laterais e áreas de treinamento.

## Regras de variedade
1. Evitar sequência repetitiva de cidade → corredor reto → cidade.
2. Alternar direção, largura e estrutura dos caminhos.
3. Cada rota deve possuir pelo menos uma característica visual/navegacional própria.
4. Pelo menos algumas rotas terão caminhos opcionais e retornos.
5. Florestas, cavernas, rios, montanhas e áreas abertas terão layouts distintos.
6. A progressão deve privilegiar exploração; a história não deve empurrar o jogador diretamente para a próxima cidade.
7. Encontros Pokémon devem acompanhar o ecossistema da área.
8. Áreas revisitadas devem mudar depois de eventos importantes.
9. O Bosque de Lúmina é uma área completa, não um corredor curto entre duas rotas.
10. Mapas de Hoenn existentes são referência técnica apenas; a identidade espacial de Eryon será construída separadamente.

## Implementação
A engine usa arquivos JSON de mapas e layouts para gerar os dados durante a compilação. As conexões, eventos e encontros serão definidos para Eryon, e os layouts serão substituídos progressivamente por layouts próprios.
