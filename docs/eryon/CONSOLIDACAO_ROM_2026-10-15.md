# Consolidação da ROM Eryon — 15 de outubro de 2026

## Critérios observáveis

| Etapa | Estado verificado | Próxima validação |
|---|---|---|
| Registro regional | 42 mapas em `gMapGroup_Eryon` | Percorrer toda a região no Delta |
| Oito ginásios | IDs, equipes, scripts e insígnias registrados | Lutar contra cada líder e salvar |
| Liga | 8 classificatórias, Elite Four e Campeão em scripts | Testar ordem, derrota, recomeço e conclusão |
| Eclipse | Investigações, combate final e epílogo registrados | Testar flags em diferentes ordens de missão |
| Encontros | Rotas e encontros especiais cadastrados | Conferir metatile de grama, EXP e captura real |
| Evoluções | Mudanças até Kalos, com exceções de gerações anteriores | Revisar ramificações e níveis no jogo |
| Terrenos | Quatro cidades com colisões corrigidas a partir das plantas | Verificar metatiles visuais e travessia em Porymap/Delta |
| Arte | Tilesets, retratos e sprites provisórios registrados | Refinar identidade GBA própria |
| Build atual | Nenhuma execução Actions encontrada para os commits recentes até a auditoria | CI manual na branch atual |
| Emulador | Nenhum playtest completo demonstrado | Campanha integral no Delta |

## Caminho de compilação existente

O repositório já possui `.github/workflows/build.yml` com `workflow_dispatch`. O job `ROM (Eryon)` instala o compilador ARM em Ubuntu, executa `bash tools/build_eryon.sh`, roda validadores, limpa uma ROM antiga antes do build, compila `pokeeryon.gba`, testa cabeçalho e gera SHA-256. O job `eryon-validation` executa uma auditoria independente.

**Ação externa ainda necessária:** acionar manualmente o workflow `CI` em `eryon-development`. A integração usada para gravar código não oferece uma ação de disparo do workflow. O sucesso antigo de 14/10 não valida o HEAD novo.

1. Abra a aba **Actions** do repositório e selecione o workflow **CI**.
2. Use **Run workflow** e escolha a branch **eryon-development**.
3. Após a conclusão, confira todos os jobs. Em caso de falha, use o artefato **eryon-build-diagnostics** e os logs do job para corrigir o erro exato.
4. Se houver sucesso, baixe **eryon-gba** e confira a presença de `pokeeryon.gba` e o hash em `build/eryon-rom.sha256`.
5. Teste no Delta: novo jogo com Riolu, deslocamentos e colisões, capturas, EXP, oito ginásios, Eclipse, classificação da Liga, Elite Four e Campeão. Salve e recarregue em pontos críticos.

Este relatório **não** atesta ROM compilada nem prontidão para lançamento; documenta o caminho para evidências reproduzíveis.
