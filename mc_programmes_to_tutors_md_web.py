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


def build_cluster_mapping(modules):
    """Build a mapping from module ref to cluster path."""
    mapping = {}

    # Organize modules by cluster
    clusters = {}
    for ref, module in modules.items():
        group, cluster = module['group'], module['subgroup']
        if group != 'Computing and Mathematics':
            continue
        if cluster not in clusters:
            clusters[cluster] = []
        clusters[cluster].append((ref, module['name']))

    # Sort clusters and modules
    clusters = dict(sorted(clusters.items()))
    for cluster in clusters:
        clusters[cluster] = sorted(clusters[cluster], key=lambda x: x[1])

    # Build the mapping with paths
    for k, cluster in enumerate(clusters, 1):
        clean_cluster = clean_filename(cluster)
        for kk, (ref, title) in enumerate(clusters[cluster], 1):
            clean_title = clean_filename(title)
            target = f"note-{kk:02d}-note-{kk:02d}-{clean_title}"
            cluster_path = f"/note/setu-comp-sci-modules-md/unit-2-clusters/topic-{k:02d}-{clean_cluster}/{target}"
            mapping[ref] = {
                'path': cluster_path,
                'title': title,
                'cluster': cluster
            }

    return mapping


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

web_link_content = """---
icon:
  type: {icon}
  color: {color}
---

{title}"""

# The following CSV stores the icons/colors for each module
# Columns Icon/Color were populated by Pete/chatGPT
df = pd.read_csv("module_display_settings.csv")

OUTPUT = "tutors-md/unit-1-programmes"

def run(programme_codes, verbose=False):

    # Build cluster mapping first
    cluster_mapping = build_cluster_mapping(modules)

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
            content = unit_content.format(title=title, description="TODO (semester)")
            open(f"{topic}/{unit}/topic.md", "wt").write(content)

            # module <-> web link
            for kk, module in enumerate(semester_modules['mandatory'] + semester_modules['elective'],1):
                ref = module['code']
                title = module['name']

                target = f"web-{kk:02d}-" + clean_filename(title)
                card = f"web-{kk:02d}-{target}"
                if verbose: print(f"\t\t{card}")
                os.makedirs(f"{topic}/{unit}/{card}", exist_ok=True)

                df_tmp = df.query(f"Module_Title=='{title}'")
                if df_tmp.shape[0]:
                    icon = df_tmp.Icon.values[0]
                    color = df_tmp.Color.values[0]
                else:
                    icon = 'fa:desktop'
                    color = 398126

                # Create web link to cluster view
                if ref in cluster_mapping:
                    cluster_path = cluster_mapping[ref]['path']

                    # Create link.md with frontmatter
                    link_content = web_link_content.format(title=title, icon=icon, color=color)
                    open(f"{topic}/{unit}/{card}/link.md", "wt").write(link_content)

                    # Create weburl file
                    open(f"{topic}/{unit}/{card}/weburl", "wt").write(cluster_path)
                else:
                    if verbose: print(f"\t\t\tWARNING: {ref} not found in cluster mapping")


CM_PROGRAMMES = "WD_KINFT_D WD_KINTE_B WD_KCRCO_B WD_KCOMC_D WD_KDEVP_B WD_KCOFO_B WD_KCMSC_B WD_KBUSY_G WD_KCOSC_G WD_KDAAN_G WD_KCESS_R WD_KISYP_R".split()

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Generate a tutor course for a set of programmes with web links to cluster view.')

    parser.add_argument('-v','--verbose', action="store_true", default=False, help='Verbose output')

    parser.add_argument('programme_codes', action="store", nargs='*', default=CM_PROGRAMMES)

    args = parser.parse_args()
    run(args.programme_codes, verbose=args.verbose)
