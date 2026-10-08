# Eryon — encontros selvagens da abertura (proposta de implementação)

Este documento define tabelas de encontro para integração futura no sistema de encontros selvagens. **Não representa encontros já ativados na ROM.** Todas as espécies abaixo são oficiais, anteriores ou pertencentes à geração Kalos.

## Rota 01 — campo e capim (níveis 2–5)
| Espécie | Peso relativo | Função |
|---|---:|---|
| Pidgey | 25 | Primeiro voador |
| Bidoof | 20 | Normal comum |
| Sentret | 20 | Captura inicial |
| Shinx | 15 | Elétrico raro no começo |
| Caterpie | 15 | Evolução rápida |
| Ralts | 5 | Encontro incomum |

## Bosque de Lúmina — capim e clareiras (níveis 4–8)
| Espécie | Peso relativo | Função |
|---|---:|---|
| Wurmple | 20 | Inseto comum |
| Sewaddle | 20 | Vegetação densa |
| Oddish | 15 | Planta/veneno |
| Shroomish | 15 | Cogumelos e sombra |
| Scatterbug | 10 | Espécie de Kalos |
| Hoothoot | 10 | Mistério das luzes noturnas |
| Phantump | 5 | Raro nas árvores antigas |
| Pikachu | 5 | Raro, captura opcional |

## Rota 02 — colinas (níveis 6–10)
| Espécie | Peso relativo | Função |
|---|---:|---|
| Zigzagoon | 25 | Trilha aberta |
| Fletchling | 20 | Ave de Kalos |
| Nidoran♀ | 15 | Variedade de tipos |
| Nidoran♂ | 15 | Variedade de tipos |
| Budew | 15 | Preparação para Verdelume |
| Abra | 10 | Encontro raro |

## Regras de progressão
- Riolu nível 5 é entregue pelo Professor Elya; não aparece nas tabelas selvagens da abertura.
- Não usar espécies inventadas nem espécies posteriores a Kalos.
- Garantir variedade sem oferecer Pokémon evoluídos poderosos cedo demais.
- Reservar encontros noturnos específicos somente após confirmar suporte a relógio/períodos no motor.
- As porcentagens somam 100 em cada tabela; ajustar para os slots aceitos pelo formato real do projeto antes da integração.
- Colisões, tiles de capim e geometria original do Bosque de Lúmina são pré-requisitos para os encontros funcionarem.

## Estado de implementação
- [x] Planejamento de espécies e pesos da abertura
- [ ] Localizar e confirmar arquivo-fonte e formato de encontros no projeto
- [ ] Converter pesos em slots suportados
- [ ] Inserir tabelas na base e compilar
- [ ] Testar encontros, níveis e frequência no emulador
