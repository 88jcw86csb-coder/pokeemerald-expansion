# Pokémon Eryon — estado real do desenvolvimento (13/10/2026)

Este diretório reúne os projetos e arquivos de documentação dos mapas de Eryon. O jogo está **em desenvolvimento**, sem teste completo confirmado no emulador Delta.

## Região implementada no repositório

- **41 mapas registrados** no grupo Eryon, com layouts e arquivos binários próprios. Estão incluídos Vila Aurora, Bosque de Lumina, Verdelume, Neonara, Frostheim, Arkhara, Umbra, Ignivar, Lunaris, Drakonia, Gruta das Estrelas e Caminho da Liga.
- Os cinco mapas de abertura que ainda reutilizavam blocos de Hoenn (Vila Aurora, Rota 01, Rota 02, Verdelume e Rota 03) receberam terrenos exclusivos com dimensões corrigidas e acessos a pé verificados por testes estáticos.
- A Cidade de Arkhara ocupa o quarto ginásio, sob responsabilidade de Tessa (Pedra, Armaldo); sua investigação Eclipse e ligações leste-oeste já existem, mas seu combate oficial ainda não foi implementado.
- Todos os mapas possuem algum NPC ou ponto investigável, mas vários encontros e sistemas de progressão ainda estão incompletos.
- O plano é usar **Riolu como inicial, sem fakemon**, e oferecer espécies oficiais até Kalos.

## Limitações funcionais detectadas

- **Ginásios:** somente Kael, de Verdelume, possui confronto de líder e concessão de insígnia nos scripts atuais. Os outros **sete** ainda precisam de batalhas, insígnias e interiores.
- **Encontros selvagens:** **18 de 21** áreas registradas como rotas ou cavernas não possuem tabelas `land_mons`. As distribuições em `distribuicao_pokemon_rotas.md` não estão todas codificadas no jogo.
- **Liga:** Caminho da Liga é explorável no esquema de terreno, mas o edifício, Elite Four, campeão e final não estão implementados.
- **Arte:** os metatiles e cenários são provisórios, não representam uma região inteiramente desenhada no Porymap.
- **HMs:** a progressão principal não deve exigir Cut, Rock Smash, Strength, Surf, Waterfall, Dive ou Flash. O código possui validações para scripts e colisões, mas é necessário testar esses acessos no emulador.
- **Game testing:** compilação e testes estáticos não substituem jogar do início ao fim, testar capturas, salvamento, batalhas, transições e estabilidade no Delta.

## Para acompanhar os trabalhos

- `docs/eryon/AUDITORIA_TECNICA_2026-10-13.md`: defeitos encontrados, correções e pendências.
- `docs/eryon/SEM_HMS_OBRIGATORIAS.md`: regra de progressão sem HMs.
- `tools/eryon_readiness_report.py`: contagem automática de mapas, ginásios e capturas por implementar.
- `tools/test_eryon_opening_terrain.py`: verificação de tamanhos e acessibilidade dos cinco mapas iniciais.
- `tools/build_eryon.sh`: validações, compilação e teste básico do arquivo GBA.

**Critério de conclusão:** entregar uma ROM somente após oito ginásios jogáveis, história completa da Eclipse, Liga, encontros distribuídos e teste final no emulador. Os próximos passos devem reduzir essas pendências reais.

## Nova Liga Central

A Liga possui uma cidade de 96×72 blocos, edifício central com recepção, arena de oito adversários visíveis e sala de recuperação. A classificação exige oito insígnias e oito vitórias consecutivas; cada derrota segue a penalidade normal de dinheiro do combate e a entrada seguinte na arena reinicia a série. Os ginásios restantes e as salas de combate da Elite Four ainda precisam ser implementados e testados.
