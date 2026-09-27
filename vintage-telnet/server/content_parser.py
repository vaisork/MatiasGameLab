"""
Parser de contenido público para Vintage Telnet (Issues #209 y #211).

Lee y estructura:
1. 'Conocer el Mundo' (KNOW_THE_WORLD_MENU.md)
   - Filtra metadatos internos, notas de diseño e instrucciones de frontend.
   - Inserta assets canónicos aprobados en sus marcadores.
   - Divide en 5 capítulos claros con soporte para índice y 'Leer todo'.
2. 'Guía del aventurero' (ENTRY_ADVENTURER_GUIDE.md)
   - Filtra metadatos editoriales de cabecera.
   - Extrae introducción y 15 secciones con encabezados aprobados.
   - Genera navegación cómoda por anclas / índice rápido.

Sin dependencias externas pesadas (usa únicamente la biblioteca estándar de Python).
"""

from dataclasses import dataclass
import html
from pathlib import Path
import re
from typing import Dict, List, Optional


@dataclass
class WorldChapter:
    num: int
    id: str
    slug: str
    title: str
    short_title: str
    html: str


@dataclass
class GuideSection:
    index: int
    id: str
    slug: str
    title: str
    html: str


CHAPTER_SHORT_TITLES = {
    1: "1. El Mundo",
    2: "2. Las Especies",
    3: "3. Las Regiones y los Pueblos",
    4: "4. Vaisgard",
    5: "5. Tu Lugar en la Historia",
}

APPROVED_IMAGES = {
    1: (
        '<figure class="world-art">\n'
        '  <img src="/assets/maps/region-inicial.webp" '
        'alt="Mapa de la Cuenca de Veyra y la región inicial" loading="lazy" decoding="async">\n'
        '  <figcaption>Cuenca de Veyra y la región conocida alrededor de Vaisgard.</figcaption>\n'
        '</figure>'
    ),
    2: (
        '<figure class="world-art">\n'
        '  <img src="/assets/species/comparativa-especies.webp" '
        'alt="Lámina canónica de las cinco especies" loading="lazy" decoding="async">\n'
        '  <figcaption>Las cinco especies de la región conocida.</figcaption>\n'
        '</figure>'
    ),
    3: "",  # No hay collage de pueblos aprobado todavía; omitir limpiamente.
    4: (
        '<figure class="world-art">\n'
        '  <img src="/assets/locations/vaisgard.webp" '
        'alt="Vaisgard, la ciudad central" loading="lazy" decoding="async">\n'
        '  <figcaption>Vaisgard, la ciudad antigua en el corazón de las Cinco Rutas.</figcaption>\n'
        '</figure>'
    ),
}


def slugify(text: str) -> str:
    """Convierte un título a slug seguro para IDs HTML y anclas."""
    text = text.lower().strip()
    text = re.sub(r"[áàä]", "a", text)
    text = re.sub(r"[éèë]", "e", text)
    text = re.sub(r"[íìï]", "i", text)
    text = re.sub(r"[óòö]", "o", text)
    text = re.sub(r"[úùü]", "u", text)
    text = re.sub(r"ñ", "n", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def render_markdown(text: str) -> str:
    """Convierte Markdown básico estructurado a HTML seguro y semántico.
    
    Escapa HTML para prevenir XSS y soporta encabezados, negrita, cursiva,
    saltos de línea (<br>), listas no ordenadas y ordenadas, y separadores.
    Preserva bloques HTML preformados como <figure>.
    """
    lines = text.strip().splitlines()
    html_parts: List[str] = []
    in_list: Optional[str] = None  # 'ul' o 'ol'
    paragraph_lines: List[str] = []

    def flush_p() -> None:
        nonlocal paragraph_lines
        if paragraph_lines:
            lines_formatted = []
            for l in paragraph_lines:
                has_br = l.endswith("  ")
                escaped = html.escape(l.strip())
                escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
                escaped = re.sub(r"_(.+?)_", r"<em>\1</em>", escaped)
                if has_br:
                    escaped += "<br>"
                lines_formatted.append(escaped)
            
            p_text = " ".join(lines_formatted) if not any(l.endswith("<br>") for l in lines_formatted) else "".join(
                f"{l} " if not l.endswith("<br>") else l for l in lines_formatted
            )
            html_parts.append(f"<p>{p_text.strip()}</p>")
            paragraph_lines = []

    def flush_list() -> None:
        nonlocal in_list
        if in_list:
            html_parts.append(f"</{in_list}>")
            in_list = None

    for line in lines:
        s = line.rstrip()
        stripped = s.strip()
        if not stripped:
            flush_p()
            flush_list()
            continue

        if stripped == "---":
            flush_p()
            flush_list()
            html_parts.append('<div class="divider" role="separator"></div>')
            continue

        # Permitir bloques HTML preformados (como las figuras de imágenes canónicas)
        if (
            stripped.startswith("<figure")
            or stripped.startswith("</figure>")
            or stripped.startswith("<img")
            or stripped.startswith("<figcaption")
            or stripped.startswith("</figcaption>")
        ):
            flush_p()
            flush_list()
            html_parts.append(stripped)
            continue

        m_h = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if m_h:
            flush_p()
            flush_list()
            level = len(m_h.group(1))
            # Ajustar nivel: # pasa a h2, ## a h3, ### a h4
            htag = f"h{min(level + 1, 6)}"
            htext = html.escape(m_h.group(2))
            htext = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", htext)
            html_parts.append(f"<{htag}>{htext}</{htag}>")
            continue

        m_ul = re.match(r"^[-*]\s+(.+)$", stripped)
        if m_ul:
            flush_p()
            if in_list != "ul":
                flush_list()
                html_parts.append("<ul>")
                in_list = "ul"
            item_text = html.escape(m_ul.group(1))
            item_text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", item_text)
            html_parts.append(f"<li>{item_text}</li>")
            continue

        m_ol = re.match(r"^\d+\.\s+(.+)$", stripped)
        if m_ol:
            flush_p()
            if in_list != "ol":
                flush_list()
                html_parts.append("<ol>")
                in_list = "ol"
            item_text = html.escape(m_ol.group(1))
            item_text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", item_text)
            html_parts.append(f"<li>{item_text}</li>")
            continue

        flush_list()
        paragraph_lines.append(s)

    flush_p()
    flush_list()
    return "\n".join(html_parts)


def get_world_file_path() -> Path:
    return Path(__file__).resolve().parent.parent / "KNOW_THE_WORLD_MENU.md"


def get_guide_file_path() -> Path:
    return Path(__file__).resolve().parent.parent / "ENTRY_ADVENTURER_GUIDE.md"


_world_cache: Optional[Dict] = None
_guide_cache: Optional[Dict] = None


def get_world_content(file_path: Optional[Path] = None, reload: bool = False) -> Dict:
    """Lee y estructura 'Conocer el Mundo' garantizando que no se filtren metadatos internos."""
    global _world_cache
    if _world_cache is not None and not reload and file_path is None:
        return _world_cache

    path = file_path or get_world_file_path()
    raw = path.read_text(encoding="utf-8")

    # Localizar inicio del contenido público (# 1. EL MUNDO)
    m_start = re.search(r"^#\s*1\.\s+EL\s+MUNDO", raw, re.MULTILINE | re.IGNORECASE)
    if not m_start:
        raise ValueError(f"No se encontró el inicio de los capítulos en {path}")

    # Localizar fin del contenido público (antes de '## Reglas de implementación para UI/Frontend')
    m_end = re.search(r"^##\s*Reglas de implementaci[oó]n", raw, re.MULTILINE | re.IGNORECASE)
    body = raw[m_start.start():m_end.start() if m_end else len(raw)]

    # Sustituir / omitir los bloques de NOTA DE DISEÑO / IMAGEN
    def replace_image_note(m: re.Match) -> str:
        try:
            num = int(m.group(1))
            img = APPROVED_IMAGES.get(num, "")
            return f"\n\n{img}\n\n" if img else "\n\n"
        except (ValueError, TypeError):
            return "\n\n"

    body = re.sub(
        r"###\s*NOTA DE DISE[ÑN]O / IMAGEN\s*(\d).*?(?=(?:\n#|\Z))",
        replace_image_note,
        body,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # Dividir en capítulos
    chapter_chunks = re.split(r"\n(?=#\s*[1-5]\.\s+)", body)
    chapter_chunks = [c for c in chapter_chunks if c.strip()]

    chapters: List[WorldChapter] = []
    for i, chunk in enumerate(chapter_chunks, 1):
        lines = chunk.strip().splitlines()
        first_line = lines[0].strip() if lines else f"Capítulo {i}"
        raw_title = re.sub(r"^#\s*", "", first_line).strip()
        
        # En el capítulo 5, quitar '# Cierre de presentación' para fluir directo a 'Bienvenido a Vintage Telnet'
        chunk_clean = chunk
        if i == 5:
            chunk_clean = re.sub(r"^#\s*Cierre de presentaci[oó]n\s*", "", chunk_clean, flags=re.MULTILINE)

        # Quitar la línea del título principal del chunk porque se renderiza en la cabecera del capítulo
        body_lines = [l for l in chunk_clean.strip().splitlines()]
        if body_lines and body_lines[0].strip().startswith("#"):
            body_text = "\n".join(body_lines[1:]).strip()
        else:
            body_text = "\n".join(body_lines).strip()

        rendered_html = render_markdown(body_text)

        chapters.append(
            WorldChapter(
                num=i,
                id=f"capitulo-{i}",
                slug=slugify(CHAPTER_SHORT_TITLES.get(i, f"capitulo-{i}")),
                title=raw_title,
                short_title=CHAPTER_SHORT_TITLES.get(i, f"Capítulo {i}"),
                html=rendered_html,
            )
        )

    result = {
        "title": "Conocer el Mundo",
        "subtitle": "Ambientación y territorio conocido de Vintage Telnet",
        "chapters": chapters,
    }
    if file_path is None:
        _world_cache = result
    return result


def get_guide_content(file_path: Optional[Path] = None, reload: bool = False) -> Dict:
    """Lee y estructura 'Guía del aventurero' filtrando metadatos editoriales."""
    global _guide_cache
    if _guide_cache is not None and not reload and file_path is None:
        return _guide_cache

    path = file_path or get_guide_file_path()
    raw = path.read_text(encoding="utf-8")

    # Localizar inicio del contenido público (# GUÍA DEL AVENTURERO)
    m_start = re.search(r"^#\s*GU[IÍ]A\s+DEL\s+AVENTURERO", raw, re.MULTILINE | re.IGNORECASE)
    if not m_start:
        raise ValueError(f"No se encontró el encabezado de la guía en {path}")

    public_text = raw[m_start.start():]

    # Separar introducción y secciones por '## '
    parts = re.split(r"\n(?=##\s+)", public_text)
    intro_raw = parts[0].strip()
    intro_lines = intro_raw.splitlines()
    if intro_lines and intro_lines[0].startswith("#"):
        intro_body = "\n".join(intro_lines[1:]).strip()
    else:
        intro_body = intro_raw

    intro_html = render_markdown(intro_body)

    sections: List[GuideSection] = []
    for idx, sec_raw in enumerate(parts[1:], 1):
        lines = sec_raw.strip().splitlines()
        first_line = lines[0].strip() if lines else f"Sección {idx}"
        sec_title = re.sub(r"^##\s*", "", first_line).strip()
        sec_body = "\n".join(lines[1:]).strip()
        sec_html = render_markdown(sec_body)
        slug = slugify(sec_title)

        sections.append(
            GuideSection(
                index=idx,
                id=slug,
                slug=slug,
                title=sec_title,
                html=sec_html,
            )
        )

    result = {
        "title": "Guía del aventurero",
        "subtitle": "Aprender a observar, explorar, combatir y viajar en Vintage Telnet",
        "intro_html": intro_html,
        "sections": sections,
    }
    if file_path is None:
        _guide_cache = result
    return result
