import argparse
import spacy

parser = argparse.ArgumentParser()
parser.add_argument("input", help="Input text file")
parser.add_argument("output", help="Output CoNLL-U file")

def to_conllu(doc, start_sent_id=1) -> tuple[str, int]:
    lines = []
    sent_i = start_sent_id

    for sent in doc.sents:
        lines.append(f"# sent_id = {sent_i}")
        lines.append(f"# text = {sent.text}")
        for token in sent:
            token_id = token.i - sent.start + 1
            head_id = token.head.i - sent.start + 1 if token.head != token else 0
            deprel = token.dep_
            inflection = token.morph.get("Inflection")
            if inflection:
                inflection = "Inf=" + inflection[0].replace(";", ",") + "|"
            else:
                inflection = ""
            reading = token.morph.get("Reading")
            if reading:
                reading = reading[0]
            else:
                reading = ""
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
                    f"SpaceAfter=No|{inflection}Reading={reading}",
                ])
            )
        lines.append("")
        sent_i += 1

    return "\n".join(lines), sent_i

def main():
    args = parser.parse_args()

    nlp = spacy.load("ja_ginza_electra", config={"components": {"compound_splitter": {"split_mode": "C"}}})

    with open(args.input, "r", encoding="utf-8") as fin, open(args.output, "w", encoding="utf-8") as fout:

        current_sent_id = 1

        for line in fin:
            line = line.strip()
            if not line:
                continue

            doc = nlp(line)

            output_str, current_sent_id = to_conllu(doc, start_sent_id=current_sent_id)

            if output_str:
                fout.write(output_str + "\n")
                print(output_str)

if __name__ == "__main__":
    main()
