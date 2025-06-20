"""extract_and_clean_html"""

import re
import bleach
from dash import dcc

# Define allowed HTML tags for content cleaning, may need to add to this list
ALLOWED_TAGS = ["h1", "h2", "h3", "p", "a", "ul", "ol", "li", "strong", "em", "b", "i"]

# Define mapping for HTML tags to className
TAG_CLASS_MAPPING = {
    "<h1>": '<h1 className="govuk-heading-l">',
    "<h2>": '<h2 className="govuk-heading-m">',
    "<h3>": '<h3 className="govuk-heading-s">',
    "<p>": '<p className="govuk-body">',
    "<ul>": '<ul className="govuk-list--bullet">',
}

TAG_STYLE_MAPPING = {"<p>": '<p style="margin:auto;">'}


def extract_and_clean_section(
    html_content: str,
    section_marker: str,
    replace_tag_using_tag_class_mapping: bool = True,
    apply_auto_margin_style: bool = False,
) -> str:
    """
    Extracts and cleans a specific section from HTML content based on the start marker.
    The section ends at the beginning of the next section or at the end of the content.
    Args:
        html_content (str): The HTML content containing marked sections.
        section_marker (str): The unique identifier for the start of the section.
        replace_tag_using_tag_class_mapping (bool): Whether to replace tag using tag class mapping.
            Defaults to True.
        apply_auto_margin_style (bool): Whether to apply auto margin style. Defaults to False.
    Returns:
        str: The cleaned HTML content of the specified section.
    """
    start_marker = f"###START:{section_marker}###"
    start_index = html_content.find(start_marker)
    if start_index == -1:
        return ""
    start_index += len(start_marker)
    next_section_index = html_content.find("###START:", start_index)
    if next_section_index == -1:
        next_section_index = len(html_content)

    start_shift = 4  # these are needed to remove empty p's from display
    end_shift = 3
    section_content = html_content[
        start_index + start_shift : next_section_index - end_shift
    ].strip()
    clean_section = bleach.clean(section_content, tags=ALLOWED_TAGS, strip=True)
    if replace_tag_using_tag_class_mapping:
        for tag, replacement in TAG_CLASS_MAPPING.items():
            clean_section = clean_section.replace(tag, replacement)

    if apply_auto_margin_style:
        for tag, style in TAG_STYLE_MAPPING.items():
            clean_section = clean_section.replace(tag, style)

    return clean_section


def get_section_component(
    html_content,
    section_name,
    style: dict = None,
    div_id: str = "",
    replace_tag_using_tag_class_mapping: bool = True,
    apply_auto_margin_style: bool = False,
):
    """
    Generates a Dash HTML component for a specified section from the provided HTML content.
    Args:
        html_content (str): The full HTML content from which to extract the section.
        section_name (str): The unique identifier for the start of the section to be extracted.
        style (dict, optional): A dictionary defining CSS styles to be applied to the component.
        replace_tag_using_tag_class_mapping (bool): Whether to replace tag using tag class mapping.
            Defaults to True.
        apply_auto_margin_style (bool): Whether to apply auto margin style. Defaults to False.
    Returns:
        html.Div: A Dash HTML Div component containing the cleaned and formatted content
                  of the specified section, ready to be used in a Dash application layout.
    """
    clean_content = extract_and_clean_section(
        html_content,
        section_name,
        replace_tag_using_tag_class_mapping,
        apply_auto_margin_style,
    )
    return dcc.Markdown(
        clean_content, dangerously_allow_html=True, style=style, id=div_id
    )


def remove_html_tags(text: str) -> str:
    """Remove HTML tags from a given string, and return a string.
    eg. remove_html_tags('<p>Hello!</p>') retuns 'Hello!'
    """
    clean = re.compile("<.*?>")
    return re.sub(clean, "", text)
