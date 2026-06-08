import argparse
import spacy
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("input", help="Input text file")
parser.add_argument("output", help="Output CoNLL-U file")

def to_conllu(doc) -> str:
    lines = []
    for sent_i, sent in enumerate(doc.sents, 1):
        lines.append(f"# sent_id = {sent_i}")
        lines.append(f"# text = {sent.text}")
        for token in sent:
            token_id = token.i - sent.start + 1
            head_id = token.head.i - sent.start + 1 if token.head != token else 0
            deprel = token.dep_
            lines.append(
                "\t".join([
                    str(token_id),
                    token.text,
                    token.lemma_,
                    token.pos_,
                    token.tag_,
                    "_",
                    str(head_id),
                    deprel,
                    "_",
                    "_",
                ])
            )
        lines.append("")
    return "\n".join(lines)


def main():
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        text = f.read()

    nlp = spacy.load("ja_ginza", config={"components": {"compound_splitter": {"split_mode": "C"}}})
    doc = nlp(text)

    output = to_conllu(doc)
    print(output)

    out_path = Path(args.output)
    out_path.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
