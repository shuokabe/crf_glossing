# Convert \t, \m, \g lines into SIGMORPHON format
import re

with open("toolbox_input.txt", "r", encoding="utf-8") as f:
    content = f.read()

blocks = re.split(r'\n(?=\\t)', content.strip())

with open("pipeline_input.txt", "w", encoding="utf-8") as out:
    for block in blocks:
        lines = block.strip().split("\n")
        m_line = next((l[3:].strip() for l in lines if l.startswith("\\m")), "")
        g_line = next((l[3:].strip() for l in lines if l.startswith("\\g")), "")
        tokens = m_line.split()
        glosses = g_line.split()
        if len(tokens) != len(glosses):
            print("Warning: token/gloss mismatch, skipping block.")
            continue
        for tok, gloss in zip(tokens, glosses):
            out.write(f"{tok}\t{gloss}\n")
        out.write("\n")
