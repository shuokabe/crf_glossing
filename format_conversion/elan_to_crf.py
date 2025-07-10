# elan_to_crf.py
from pympi.Elan import Eaf
import argparse

def convert_eaf_to_crf(eaf_path, output_path):
    eaf = Eaf(eaf_path)
    tiers = eaf.get_tier_names()
    
    # Example: pick tiers manually (edit as needed)
    transcription_tier = 'transcription'
    morph_tier = 'morphemes'
    gloss_tier = 'gloss'

    with open(output_path, 'w', encoding='utf-8') as out_f:
        for annotation in eaf.get_annotation_data_for_tier(transcription_tier):
            start, end, text = annotation
            morphs = eaf.get_annotation_data_between_times(morph_tier, start, end)
            glosses = eaf.get_annotation_data_between_times(gloss_tier, start, end)
            
            # Ensure aligned counts
            if len(morphs) != len(glosses):
                continue
            
            for m, g in zip(morphs, glosses):
                _, _, morph = m
                _, _, gloss = g
                out_f.write(f"{morph}\t{gloss}\n")
            out_f.write("\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('eaf_file', help='Path to input EAF file')
    parser.add_argument('output_file', help='Path to output CRF format file')
    args = parser.parse_args()
    
    convert_eaf_to_crf(args.eaf_file, args.output_file)
