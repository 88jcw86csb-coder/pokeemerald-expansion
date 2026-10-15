# Verificação de compilação Eryon — 15/10/2026

Esta branch de validação deriva de `3674283e027fc2fd0d71ec1d4e428c78f18c76f3` de `eryon-development`.
Ela existe apenas para solicitar uma compilação no workflow
`Eryon GBA Build Verification` via pull request.

**Não substitui nem reinicia a branch principal.**
Não realizar merge automático. O job deve executar
`bash tools/build_eryon.sh`, produzir `pokeeryon.gba`,
validar o cabeçalho e anexar o hash SHA-256; se falhar, preservar
`eryon-pr-build-diagnostics` para corrigir o erro.
