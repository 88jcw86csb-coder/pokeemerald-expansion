# Eryon — auditoria estática de transições da abertura

Data: 2026-10-08. Escopo: os cinco primeiros mapas na branch `eryon-development`.

## Cadeia de ida e volta

| Origem | Warp | Coordenada | Destino | Warp destino | Retorno correspondente |
|---|---:|---|---|---:|---|
| Vila Aurora | 0 | (19,10) | Rota 01 | 0 | Sim |
| Rota 01 | 0 | (0,10) | Vila Aurora | 0 | Sim |
| Rota 01 | 1 | (19,10) | Bosque de Lúmina | 0 | Sim |
| Bosque de Lúmina | 0 | (0,22) | Rota 01 | 1 | Sim |
| Bosque de Lúmina | 1 | (47,22) | Rota 02 | 0 | Sim |
| Rota 02 | 0 | (0,10) | Bosque de Lúmina | 1 | Sim |
| Rota 02 | 1 | (49,10) | Verdelume | 0 | Sim |
| Verdelume | 0 | (0,30) | Rota 02 | 1 | Sim |

## Limites declarados

| Mapa | Dimensões | Eventos de warp dentro dos limites? |
|---|---|---|
| Vila Aurora | 20 × 20 | Sim |
| Rota 01 | 20 × 20 | Sim |
| Bosque de Lúmina | 48 × 44 | Sim |
| Rota 02 | 50 × 20 | Sim |
| Verdelume | 40 × 60 | Sim |

## Bloqueios ainda presentes

1. **Limite de mapa não equivale a tile atravessável.** Os warps estão nas bordas extremas e podem estar sobre tiles bloqueados ou inacessíveis.
2. Os cinco layouts ainda reutilizam blocos de mapas de Hoenn, não terrenos originais de Eryon.
3. A existência de pares de warps não comprova que o motor permitirá a transição.
4. Não há nenhuma execução do GitHub Actions registrada para a branch no momento da auditoria (`total_count: 0`). Nenhuma ROM compilada ou teste no Delta está confirmado.
5. Antes de adicionar novos warps, criar os layouts originais e verificar o ponto de chegada em cada sentido no emulador.

## Resultado

**Verificado estaticamente:** todos os oito warps estão dentro dos limites declarados e apontam para índices existentes com retorno correspondente.

**Não verificado:** colisões, tiles, acessibilidade, geração de mapas, compilação e comportamento em tempo de execução.
