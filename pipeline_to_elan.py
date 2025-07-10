# Convert pipeline output (predictions) into an ELAN .eaf file
import pympi

eaf = pympi.Elan.Eaf()
eaf.add_tier('tokens')
eaf.add_tier('gloss')

with open("pipeline_output.txt", "r", encoding="utf-8") as f:
    block = []
    time = 0
    step = 1000
    for line in f:
        if line.strip() == "":
            if block:
                start, end = time, time + step
                tokens = [w for w, _ in block]
                glosses = [g for _, g in block]
                eaf.add_annotation('tokens', start, end, '\t'.join(tokens))
                eaf.add_annotation('gloss', start, end, '\t'.join(glosses))
                block = []
                time += step
        else:
            w, g = line.strip().split('\t')
            block.append((w, g))

eaf.to_file("predicted.eaf")
print("ELAN file saved: predicted.eaf")
