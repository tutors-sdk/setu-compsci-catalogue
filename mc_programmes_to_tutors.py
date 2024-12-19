#!/usr/bin/env python

import os, shutil, glob
import yaml
import pandas as pd
import argparse


def clean_filename(s):
    return (s.replace(" ","_").replace("&","and")
            .replace(",","").replace(".","")
            .replace("(","").replace(")","")
    )


def load(folder='descriptors', id="*"):
    files = sorted(glob.glob(f"module_catalogue/{folder}/yaml/{id}.yaml"))

    return {file.rsplit("/")[-1].split(".")[0]:yaml.safe_load(open(file)) for file in files}


modules = load(folder="modules")
descriptors = load(folder="descriptors")
programmes = load(folder="programmes")
schedules = load(folder="schedules")

topic_content = """# {title}

Programme leader: {leader}
"""

unit_content = """# {title}

{description}
"""

module_content = """---
icon:
  type: {icon}
  color: {color}
---
{title}

{description}
"""

# The following CSV stores the icons/colors for each module 
# Columns Icon/Color were populated by Pete/chatGPT
df = pd.read_csv("module_display_settings.csv")

OUTPUT = "tutors/unit-1-programmes"

def run(programme_codes, verbose=False):

    # programme <-> topic
    for k, code in enumerate(programme_codes):

        programme = programmes[code]
        schedule = schedules[code]

        topic = f"{OUTPUT}/topic-{k:02d}-{code}"
        if verbose: print(f"{topic}")
        os.makedirs(topic, exist_ok=True)
        content = topic_content.format(title=programme['full title'], leader=programme['leader'])
        open(f"{topic}/topic.md", "wt").write(content)

        # semester <-> unit
        for semester, semester_modules in schedule['semesters'].items():

            unit = f"unit-{semester}" 
            if verbose: print(f"\t{unit}")
            os.makedirs(f"{topic}/{unit}", exist_ok=True)
            title = f"Semester {semester}"
            content = unit_content.format(title=title, description="TODO (semster)")
            open(f"{topic}/{unit}/topic.md", "wt").write(content)

            # module <-> talk
            for kk, module in enumerate(semester_modules['mandatory'] + semester_modules['elective'],1):  
                ref = module['code']
                title = module['name']

                # TODO if we want to jump to cluster view  
                # group = modules[ref]['group']
                # subgroup = modules[ref]['subgroup']

                target = f"talk-{kk:02d}-" + clean_filename(title)
                card = f"talk-{kk:02d}-{target}"
                if verbose: print(f"\t\t{card}")
                os.makedirs(f"{topic}/{unit}/{card}", exist_ok=True)

                df_tmp = df.query(f"Module_Title=='{title}'")
                if df_tmp.shape[0]:
                    icon = df_tmp.Icon.values[0]
                    color = df_tmp.Color.values[0]
                else:
                    icon = 'fa:desktop'
                    color = 398126
                description = descriptors[ref]['aim'][:150] + " ... " 
                content = module_content.format(title=title, icon=icon, color=color, description=description)
                open(f"{topic}/{unit}/{card}/{target}" + ".md", "wt").write(content)

                source = f"module_catalogue/descriptors/pdf/{ref}.pdf"
                shutil.copyfile(source, f"{topic}/{unit}/{card}/{target}" + ".pdf")


CM_PROGRAMMES = "WD_KINFT_D WD_KINTE_B WD_KCRCO_B WD_KCOMC_D WD_KDEVP_B WD_KCOFO_B WD_KCMSC_B WD_KBUSY_G WD_KCOSC_G WD_KDAAN_G WD_KCESS_R WD_KISYP_R".split()

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Generate a tutor course for a set of programmes in the module catalogue.')
                                    
    parser.add_argument('-v','--verbose', action="store_true", default=False, help='Verbose output')

    # TODO Need to talk to EdeL about numbering in tutors
    parser.add_argument('programme_codes', action="store", nargs='*', default=CM_PROGRAMMES)

args = parser.parse_args()
run(args.programme_codes, verbose=args.verbose)
