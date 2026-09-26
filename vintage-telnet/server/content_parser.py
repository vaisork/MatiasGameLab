import re
from pathlib import Path
import markdown

def parse_adventurer_guide(base_path: Path):
    guide_path = base_path / "ENTRY_ADVENTURER_GUIDE.md"
    if not guide_path.exists():
        return []
    content = guide_path.read_text(encoding="utf-8")

    parts = re.split(r'^# GUÍA DEL AVENTURERO', content, flags=re.MULTILINE)
    if len(parts) > 1:
        content = "# Guía del aventurero" + parts[1]

    return parse_sections(content)

def parse_know_the_world(base_path: Path):
    world_path = base_path / "KNOW_THE_WORLD_MENU.md"
    if not world_path.exists():
        return []
    content = world_path.read_text(encoding="utf-8")

    # Strip frontmatter: public content starts exactly at "# 1. EL MUNDO"
    parts = re.split(r'^# 1\. EL MUNDO', content, flags=re.MULTILINE)
    if len(parts) > 1:
        content = "# 1. El Mundo\n" + parts[1]

    # Remove internal notes and guidelines
    content = re.sub(r'^### NOTA DE DISEÑO.*?$', '', content, flags=re.MULTILINE)
    # Remove everything after "---" that separates internal notes at the end
    content = re.split(r'^## Reglas de implementación para UI/Frontend', content, flags=re.MULTILINE)[0]

    # Replace image markers with div placeholders (as requested)
    def replacer(match):
        return '<div class="art-placeholder" aria-hidden="true" style="margin: 20px 0;"></div>'

    content = re.sub(r'^\*\*\[INSERTAR IMAGEN CANÓNICA AQUÍ.*?$', replacer, content, flags=re.MULTILINE)
    content = re.sub(r'^Si todavía no existe.*?$', '', content, flags=re.MULTILINE)

    return parse_sections(content)

def parse_sections(content):
    """Simple parser to extract headings and their paragraphs and format as HTML"""
    sections = []
    current_section = None

    for line in content.split('\n'):
        line = line.strip()
        if not line:
            if current_section:
                current_section["body"] += "\n\n"
            continue

        if line.startswith('# '):
            if current_section:
                sections.append(current_section)
            # Remove prefix numbers like "1. El Mundo" -> "El Mundo"
            title = line[2:].strip()
            title = re.sub(r'^\d+\.\s*', '', title)
            current_section = {"title": title.title() if title.isupper() else title, "body": ""}
        else:
            if not current_section:
                current_section = {"title": "Introducción", "body": ""}
            current_section["body"] += line + "\n"

    if current_section:
        sections.append(current_section)

    for s in sections:
        # Convert markdown body to html
        s["body"] = markdown.markdown(s["body"].strip())

    return sections
