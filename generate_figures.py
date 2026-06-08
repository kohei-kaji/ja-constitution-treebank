import subprocess
from pathlib import Path


def parse_conllu(path: Path) -> list[dict]:
    sentences = []
    current: dict = {"id": None, "text": "", "tokens": []}

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# sent_id"):
            current["id"] = line.split("=", 1)[1].strip()
        elif line.startswith("# text"):
            current["text"] = line.split("=", 1)[1].strip()
        elif line == "":
            if current["tokens"]:
                sentences.append(current)
            current = {"id": None, "text": "", "tokens": []}
        elif not line.startswith("#") and line.strip():
            parts = line.split("\t")
            if len(parts) >= 8 and parts[0].isdigit():
                current["tokens"].append({
                    "id": int(parts[0]),
                    "form": parts[1],
                    "upos": parts[3],
                    "head": int(parts[6]),
                    "deprel": parts[7],
                })

    if current["tokens"]:
        sentences.append(current)

    return sentences


def escape_latex(text: str) -> str:
    for char, repl in [
        ("\\", "\\textbackslash{}"),
        ("&", "\\&"),
        ("%", "\\%"),
        ("$", "\\$"),
        ("#", "\\#"),
        ("_", "\\_"),
        ("{", "\\{"),
        ("}", "\\}"),
        ("^", "\\^{}"),
        ("~", "\\~{}"),
    ]:
        text = text.replace(char, repl)
    return text


def make_tex(sent: dict) -> str:
    tokens = sent["tokens"]
    n = len(tokens)

    if n > 60:
        col_sep, font_cmd = "0.3em", "\\fontsize{5pt}{6pt}\\selectfont"
    elif n > 30:
        col_sep, font_cmd = "0.5em", "\\small"
    else:
        col_sep, font_cmd = "1em", "\\normalsize"

    # pgf overflows when max_span * edge_unit_distance exceeds ~370pt;
    # cap edge_unit_distance so the tallest arc stays under 250pt.
    max_span = max(
        (abs(t["head"] - t["id"]) for t in tokens if t["head"] != 0),
        default=1,
    )
    edge_step_pt = min(250 / max_span, 12)
    edge_unit_dist = f"{edge_step_pt:.1f}pt"

    forms = " \\& ".join(escape_latex(t["form"]) for t in tokens)
    upos  = " \\& ".join(escape_latex(t["upos"])  for t in tokens)

    root_line = ""
    edge_lines = []
    for t in tokens:
        if t["deprel"].upper() == "ROOT":
            root_line = f"    \\deproot{{{t['id']}}}{{ROOT}}"
        else:
            edge_lines.append(
                f"    \\depedge{{{t['head']}}}{{{t['id']}}}{{{escape_latex(t['deprel'])}}}"
            )

    return (
        "\\documentclass[tikz,border=5pt]{standalone}\n"
        "\\usepackage{luatexja}\n"
        "\\usepackage{tikz-dependency}\n"
        "\n"
        "\\begin{document}\n"
        f"{font_cmd}\n"
        f"\\begin{{dependency}}[edge unit distance={edge_unit_dist}]\n"
        f"    \\begin{{deptext}}[column sep={col_sep}]\n"
        f"        {forms}\\\\\n"
        f"        {upos}\\\\\n"
        "    \\end{deptext}\n"
        f"{root_line}\n"
        + "\n".join(edge_lines) + "\n"
        "\\end{dependency}\n"
        "\\end{document}\n"
    )


def main():
    conllu_path = Path("preamble-gold.conllu")
    figure_dir = Path("figure")
    figure_dir.mkdir(exist_ok=True)

    sentences = parse_conllu(conllu_path)
    print(f"{len(sentences)} sentences found")

    for sent in sentences:
        num = sent["id"]
        tex_path = figure_dir / f"{num}.tex"
        tex_path.write_text(make_tex(sent), encoding="utf-8")
        print(f"  wrote {tex_path}")

    print("\nCompiling PDFs...")
    for sent in sentences:
        num = sent["id"]
        print(f"  lualatex {num}.tex ...", end=" ", flush=True)
        result = subprocess.run(
            ["lualatex", "-interaction=nonstopmode", f"{num}.tex"],
            cwd=figure_dir,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print("OK")
        else:
            print("FAILED")
            for line in result.stdout.splitlines()[-30:]:
                print("   ", line)


if __name__ == "__main__":
    main()
