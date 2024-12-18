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

{description}
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

OUTPUT = "tutors/unit-2-clusters/"

def run(verbose=False):

    clusters = {}
    for ref,module in modules.items():
        group, cluster = module['group'], module['subgroup']
        if group not in clusters: clusters[group] = {}
        if cluster not in clusters[group]: clusters[group][cluster] = []
        clusters[group][cluster].append((module['ref'],module['name']))    

    clusters = dict(sorted(clusters.items()))
    for group in clusters:
        clusters[group] = dict(sorted(clusters[group].items()))
        for cluster in clusters[group]:
            clusters[group][cluster] = sorted(clusters[group][cluster], key=lambda x: x[1])

    # only upload for one group - the CM department              
    group = 'Computing and Mathematics'

    # cluster <-> topic
    for k, cluster in enumerate(clusters[group],1):

        topic = f"{OUTPUT}/topic-{k:02d}-{clean_filename(cluster)}"
        os.makedirs(topic, exist_ok=True)
        content = topic_content.format(title=cluster, description="")
        open(f"{topic}/topic.md", "wt").write(content)

        # module <-> talk
        for kk, (ref,title) in enumerate(clusters[group][cluster],1):
            
            target = f"talk-{kk:02d}-" + clean_filename(title)
            card = f"talk-{kk:02d}-{target}"
            if verbose: print(f"\t\t{card}")
            os.makedirs(f"{topic}/{card}", exist_ok=True)

            df_tmp = df.query(f"Module_Title=='{title}'")
            if df_tmp.shape[0]:
                icon = df_tmp.Icon.values[0]
                color = df_tmp.Color.values[0]
            else:
                icon = 'fa:desktop'
                color = 398126
            description = descriptors[ref]['aim'][:150] + " ... " 
            content = module_content.format(title=title, icon=icon, color=color, description=description)
            open(f"{topic}/{card}/{target}" + ".md", "wt").write(content)

            source = f"module_catalogue/descriptors/pdf/{ref}.pdf"
            shutil.copyfile(source, f"{topic}/{card}/{target}" + ".pdf")


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Generate a tutor course for module clusters in the module catalogue.')
                                    
    parser.add_argument('-v','--verbose', action="store_true", default=False, help='Verbose output')

args = parser.parse_args()
run(verbose=args.verbose)
