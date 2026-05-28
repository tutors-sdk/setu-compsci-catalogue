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


def generate_module_markdown(descriptor, module_info, icon='fa:desktop', color='398126'):
    """Generate markdown content for a module descriptor."""

    # Basic information
    code = descriptor.get('code', 'N/A')
    full_title = descriptor.get('full title', descriptor.get('name', 'N/A'))
    short_title = descriptor.get('short title', full_title)
    credits = descriptor.get('credits', 'N/A')
    level = descriptor.get('level', 'N/A')
    department = descriptor.get('department', 'N/A')
    author = module_info.get('author', 'N/A')
    subgroup = module_info.get('subgroup', 'N/A')

    # Build the markdown content with frontmatter
    md = f"""---
icon:
  type: {icon}
  color: {color}
---

# {full_title}

"""

    # Module Information Table
    md += "## Module Information\n\n"
    md += "| **Field** | **Details** |\n"
    md += "|-----------|-------------|\n"
    md += f"| **Module Code** | {code} |\n"
    md += f"| **Module Title** | {full_title} |\n"
    md += f"| **Short Title** | {short_title} |\n"
    md += f"| **Credits** | {credits} ECTS |\n"
    md += f"| **Level** | {level} (Level 8) |\n"
    md += f"| **Department** | {department} |\n"
    md += f"| **Module Author** | {author} |\n"
    md += f"| **Cluster** | {subgroup} |\n\n"
    md += "---\n\n"

    # Module Aim
    aim = descriptor.get('aim', 'No aim specified.')
    md += "## Module Aim\n\n"
    md += f"{aim}\n\n"
    md += "---\n\n"

    # Learning Outcomes
    learning_outcomes = descriptor.get('learning outcomes', [])
    if learning_outcomes:
        md += "## Learning Outcomes\n\n"
        md += "On successful completion of this module, learners will be able to:\n\n"
        for i, outcome in enumerate(learning_outcomes, 1):
            md += f"{i}. {outcome}\n"
        md += "\n---\n\n"

    # Indicative Content
    indicative_content = descriptor.get('indicative content', [])
    if indicative_content:
        md += "## Indicative Content\n\n"
        md += "The module covers the following topics:\n\n"
        for item in indicative_content:
            md += f"- {item}\n"
        md += "\n---\n\n"

    # Learning and Teaching Methods
    teaching_methods = descriptor.get('learning and teaching methods', [])
    if teaching_methods:
        md += "## Learning and Teaching Methods\n\n"
        for method in teaching_methods:
            md += f"{method}\n\n"

        # Contact Hours
        learning_modes = descriptor.get('learning modes', [])
        if learning_modes:
            md += "### Contact Hours\n\n"
            md += "| **Activity** | **Full Time Hours** | **Part Time Hours** |\n"
            md += "|--------------|---------------------|---------------------|\n"
            total_ft = 0
            total_pt = 0
            for mode in learning_modes:
                name = mode.get('name', 'N/A')
                ft = mode.get('full time', '-')
                pt = mode.get('part time', '-')
                md += f"| {name} | {ft} | {pt if pt else '-'} |\n"
                if isinstance(ft, (int, float)):
                    total_ft += ft
                if pt and isinstance(pt, (int, float)):
                    total_pt += pt
            md += f"| **Total** | **{total_ft}** | **{total_pt if total_pt else '-'}** |\n\n"

        md += "---\n\n"

    # Assessment Methods
    assessment_methods = descriptor.get('assessment methods', [])
    if assessment_methods:
        md += "## Assessment Methods\n\n"
        md += "| **Assessment Type** | **Learning Outcomes** | **Weighting** |\n"
        md += "|---------------------|----------------------|---------------|\n"

        for assessment in assessment_methods:
            name = assessment.get('name', 'N/A')
            lo = assessment.get('learning outcomes', 'All')
            weighting = assessment.get('weighting', 'N/A')
            is_main = assessment.get('main', False)

            if is_main:
                md += f"| **{name}** | {lo if lo else 'All'} | **{weighting}%** |\n"
            else:
                md += f"| - {name} | {lo if lo else 'All'} | {weighting}% |\n"

        md += "\n---\n\n"

    # Assessment Criteria
    assessment_criteria = descriptor.get('assessment criteria', [])
    if assessment_criteria:
        md += "## Assessment Criteria\n\n"

        grade_bands = [
            ("Fail (<40%)", 0),
            ("Pass (40%-49%)", 1),
            ("Credit (50%-59%)", 2),
            ("Distinction (60%-69%)", 3),
            ("High Distinction (70%-100%)", 4)
        ]

        for band_name, idx in grade_bands:
            if idx < len(assessment_criteria):
                md += f"### {band_name}\n"
                md += f"{assessment_criteria[idx]}\n\n"

        md += "---\n\n"

    # Pre-requisites and Co-requisites
    prereqs = descriptor.get('pre-requisites', [])
    coreqs = descriptor.get('co-requisites', [])

    md += "## Pre-requisites and Co-requisites\n\n"
    md += f"- **Pre-requisites:** {', '.join(prereqs) if prereqs else 'None'}\n"
    md += f"- **Co-requisites:** {', '.join(coreqs) if coreqs else 'None'}\n\n"
    md += "---\n\n"

    # Recommended Reading
    supp_material = descriptor.get('supplementary material', [])
    essential_material = descriptor.get('essential material', [])

    if supp_material or essential_material:
        md += "## Recommended Reading\n\n"

        if essential_material:
            md += "### Essential Material\n\n"
            for item in essential_material:
                md += f"- {item}\n"
            md += "\n"

        if supp_material:
            md += "### Supplementary Material\n\n"
            for item in supp_material:
                md += f"- {item}\n"
            md += "\n"

        md += "---\n\n"

    # Programme Information
    programmes = descriptor.get('programmes', [])
    if programmes:
        # Filter out null entries and get valid programmes
        valid_progs = [p for p in programmes if p and isinstance(p, dict)]

        if valid_progs:
            md += "## Programme Information\n\n"
            md += "This module is available on the following programmes:\n\n"
            md += "| **Programme Code** | **Programme Title** | **Stage** | **Semester** | **Status** |\n"
            md += "|-------------------|---------------------|-----------|--------------|------------|\n"

            for prog in valid_progs:
                prog_code = prog.get('programme', 'N/A')
                prog_title = prog.get('title', 'N/A')
                stage = prog.get('stage', 'N/A')
                semester = prog.get('semester', 'N/A')
                status = prog.get('status', 'N/A')
                status_text = "Mandatory" if status == 'M' else "Elective" if status == 'E' else status

                md += f"| {prog_code} | {prog_title} | {stage} | {semester} | {status_text} |\n"

            md += "\n---\n\n"

    # Resources Required
    resources = descriptor.get('requested resources', [])
    if resources:
        md += "## Resources Required\n\n"
        for resource in resources:
            md += f"- {resource}\n"
        md += "\n---\n\n"

    # Footer
    timetable = descriptor.get('timetable', module_info.get('timetable', 'N/A'))
    md += f"*Module Code: {code} | Timetable Code: {timetable}*\n"

    return md


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

OUTPUT = "tutors-md/unit-1-programmes"

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
            content = unit_content.format(title=title, description="TODO (semester)")
            open(f"{topic}/{unit}/topic.md", "wt").write(content)

            # module <-> note
            for kk, module in enumerate(semester_modules['mandatory'] + semester_modules['elective'],1):
                ref = module['code']
                title = module['name']

                target = f"note-{kk:02d}-" + clean_filename(title)
                card = f"note-{kk:02d}-{target}"
                if verbose: print(f"\t\t{card}")
                os.makedirs(f"{topic}/{unit}/{card}", exist_ok=True)

                df_tmp = df.query(f"Module_Title=='{title}'")
                if df_tmp.shape[0]:
                    icon = df_tmp.Icon.values[0]
                    color = df_tmp.Color.values[0]
                else:
                    icon = 'fa:desktop'
                    color = 398126

                # Generate markdown version of module descriptor with frontmatter
                if ref in descriptors and ref in modules:
                    markdown_content = generate_module_markdown(descriptors[ref], modules[ref], icon, color)
                    open(f"{topic}/{unit}/{card}/{target}" + ".md", "wt").write(markdown_content)


CM_PROGRAMMES = "WD_KINFT_D WD_KINTE_B WD_KCRCO_B WD_KCOMC_D WD_KDEVP_B WD_KCOFO_B WD_KCMSC_B WD_KBUSY_G WD_KCOSC_G WD_KDAAN_G WD_KCESS_R WD_KISYP_R".split()

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Generate a tutor course for a set of programmes in the module catalogue (markdown version).')

    parser.add_argument('-v','--verbose', action="store_true", default=False, help='Verbose output')

    parser.add_argument('programme_codes', action="store", nargs='*', default=CM_PROGRAMMES)

    args = parser.parse_args()
    run(args.programme_codes, verbose=args.verbose)
