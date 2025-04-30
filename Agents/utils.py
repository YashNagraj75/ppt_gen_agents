import json

from .schema import ContentOutput, SlideLayout


def parse_output(generations):
    slides_data = []

    for generation in generations:
        for gen in generation:
            layout_name = gen.layout_name.value if gen.layout_name else None

            slide_dict = {
                "title_content": gen.title_content,
                "slide_content": gen.slide_content,
                "image_url": gen.image_url,
                "layout_name": layout_name,
            }
            slides_data.append(slide_dict)

    return slides_data


def parse_content_output(generation):
    """
    Convert nested lists of ContentOutput models into a list of serializable dicts.
    """
    data = {
        "layout": generation.layout.value,
        "title": generation.title,
        "data": generation.data,
    }

    return data


def parse_data(generation):
    """
    Convert nested lists of ContentOutput models into a list of serializable dicts.
    """
    data = {
        "data": json.loads(generation.data),
    }

    return data


def parse_planner_output(generations):
    """
    Convert nested lists of PlannerOutput models into a list of serializable dicts.
    """
    slides_data = []
    for generation in generations:
        data = {
            "layout": generation.layout.name,
            "title": generation.title,
        }
        slides_data.append(data)
    return slides_data


def convert_to_content_output(json_str: str):
    parsed = json.loads(json_str)
    layout = parsed.pop("layout")
    title = parsed.pop("title")
    data = parsed  # Remaining fields
    return ContentOutput(layout=layout, title=title, data=data)
