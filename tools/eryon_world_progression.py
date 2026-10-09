#!/usr/bin/env python3
"""Eryon overworld progression: interleave routes, villages and gyms.

Planning only: graph edges do NOT install map warps in the GBA engine.
"""
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGES = [
    ("vila_aurora", "village"),
    ("rota_01", "route"),
    ("bosque_de_lumina", "forest"),
    ("rota_02", "route"),
    ("verdelume", "gym"),
    ("estrada_dos_pomares", "route"),
    ("vila_dos_pomares", "village"),
    ("rota_03", "route"),
    ("neonara", "gym"),
    ("colinas_da_neblina", "route"),
    ("vila_da_neblina", "village"),
    ("trilha_glacial", "route"),
    ("frostheim", "gym"),
    ("serra_dos_cristais", "mountain"),
    ("refugio_cristal", "village"),
    ("passagem_rochosa", "mountain"),
    ("arkhara", "gym"),
    ("estrada_oriental", "route"),
    ("posto_oriental", "village"),
    ("vale_dos_ventos", "valley"),
    ("umbra", "gym"),
    ("rota_das_cachoeiras", "route"),
    ("vila_das_aguas", "village"),
    ("deserto_de_solaris", "desert"),
    ("ignivar", "gym"),
    ("floresta_dos_ecos", "forest"),
    ("aldeia_dos_ecos", "village"),
    ("trilha_lunar", "route"),
    ("lunaris", "gym"),
    ("trilha_dos_dragoes", "route"),
    ("vila_do_pico", "village"),
    ("drakonia", "gym"),
    ("caminho_da_liga", "route"),
    ("liga_eryon", "league"),
]
GYMS = ["verdelume", "neonara", "frostheim", "arkhara",
        "umbra", "ignivar", "lunaris", "drakonia"]


def validate():
    names = [name for name, _ in STAGES]
    assert len(names) == len(set(names)), "duplicate stage"
    assert [n for n, k in STAGES if k == "gym"] == GYMS
    for left, right in zip(STAGES, STAGES[1:]):
        assert not (left[1] == right[1] == "gym"), "adjacent gyms"
    for i, (_, kind) in enumerate(STAGES):
        if kind == "gym" and i:
            assert STAGES[i-1][1] != "gym"
    assert any(k == "forest" for _, k in STAGES[1:4])
    return True


def render():
    validate()
    lines = [
        "# Pokémon Eryon — ordem regional planejada",
        "",
        "Este documento é um roteiro de conexões, não warps já implementados.",
        "As cidades dos oito ginásios seguem a lista oficial aprovada.",
        "Cada seta representa uma conexão FUTURA a implementar/testar no motor.",
        "",
        "| Ordem | Local | Categoria | Próximo destino |",
        "|---:|---|---|---|",
    ]
    for i, (name, kind) in enumerate(STAGES):
        nxt = STAGES[i+1][0] if i+1 < len(STAGES) else "fim"
        lines.append(f"| {i+1} | {name.replace('_', ' ').title()} | {kind} | {nxt.replace('_', ' ').title()} |")
    lines += [
        "",
        "## Critérios de implementação",
        "- Não colocar cidades de ginásio consecutivas.",
        "- Inserir trilhas, biomas, vilas de descanso e encontros selvagens entre marcos.",
        "- Manter Bosque de Lumina entre a primeira rota e Verdelume.",
        "- Preservar saídas já registradas: Serra → Passagem → Estrada → Vale.",
        "- Refúgio Cristal e Posto Oriental são desvios laterais planejados; a tabela é ordem narrativa, não exige quebrar os warps diretos existentes.",
        "- Os novos locais são propostas de expansão; não alegar que possuem map.json, layout ou warp.",
        "- Confirmar em Porymap e no emulador cada transição antes de liberar a ROM.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    out = ROOT / "docs/eryon/progressao_regional.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(), encoding="utf-8")
    print(f"Validated {len(STAGES)} sequential locations and {len(GYMS)} gyms")
