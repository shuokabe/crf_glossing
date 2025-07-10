# Extract tokens and glosses from ELAN .eaf file
import pympi

eaf = pympi.Elan.Eaf("input.eaf")
token_data = eaf.get_annotation_data_for_tier("tokens")
gloss_data = eaf.get_annotation_data_for_tier("gloss")

def index_by_time(data):
    return {(start, end): text for start, end, text in data}

token_map = index_by_time(token_data)
gloss_map = index_by_time(gloss_data)

with open("pipeline_input.txt", "w", encoding="utf-8") as out:
    for key in sorted(token_map.keys()):
        tokens = token_map.get(key, "").split('\t')
        glosses = gloss_map.get(key, "").split('\t')
        if len(tokens) != len(glosses):
            print(f"Warning: mismatch at {key}, skipping.")
            continue
        for t, g in zip(tokens, glosses):
            out.write(f"{t}\t{g}\n")
        out.write("\n")
