import xml.etree.ElementTree as ET
from pathlib import Path

svg_file = Path(__file__).parent / "key-positions.svg"

tree = ET.parse(svg_file)
root: ET.Element = tree.getroot()

namespaces = {
    "svg": "http://www.w3.org/2000/svg",
    "inkscape": "http://www.inkscape.org/namespaces/inkscape",
}


def get_xy_transform(translate_transform: str | None) -> tuple[float, float]:
    """Gets the amount of translation (x and y) from a transform attribute"""
    if translate_transform is None:
        return 0, 0
    assert translate_transform.startswith("translate(")
    x, y = translate_transform.split("translate(")[1].rstrip(")").split(",")
    return float(x), float(y)


def get_xy_from_d(d: str) -> tuple[float, float]:
    """Gets the start and end coordinates from a path element's d attribute"""

    parts = d.split()
    assert len(parts) == 3  # Assuming this is a simple line.

    start_x, start_y = map(float, parts[1].split(","))
    end_x, end_y = map(float, parts[2].split(","))
    return start_x, start_y, end_x, end_y


def add_translate_to_line(start_x, start_y, end_x, end_y, xy_translate=(0, 0)):
    start_x += xy_translate[0]
    start_y += xy_translate[1]
    end_x += xy_translate[0]
    end_y += xy_translate[1]
    return start_x, start_y, end_x, end_y


def calculate_length(start_x, start_y, end_x, end_y):
    return ((end_x - start_x) ** 2 + (end_y - start_y) ** 2) ** 0.5


def get_length_of_a_path(path_element: ET.Element) -> float:
    """Gets the length of a path element (in pixels or whatever units used by
    inkscape)"""
    transform = path_element.get("transform")
    d = path_element.get("d")
    x_trans, y_trans = get_xy_transform(transform)
    start_x, start_y, end_x, end_y = get_xy_from_d(d)
    start_x, start_y, end_x, end_y = add_translate_to_line(
        start_x, start_y, end_x, end_y, (x_trans, y_trans)
    )
    return calculate_length(start_x, start_y, end_x, end_y)


def get_scale(root: ET.Element):

    # unit:  millimeters.
    measured_lengths = {
        "R3-horizontal": 109,
        "R4-horizontal": 109.5,
        "C4-vertical": 90,
    }
    scales = []
    for label, real_length in measured_lengths.items():
        path_element = root.find(
            f'.//svg:path[@inkscape:label="{label}"]', namespaces=namespaces
        )
        length = get_length_of_a_path(path_element)
        scale = real_length / length
        print(
            f"{label}, {length=:.2f} inkscape_mm, {real_length=:.2f} mm, {scale=:.2f}"
        )
        scales.append(scale)

    scale = sum(scales) / len(scales)
    print("Average scale:", f"{scale:.3f} (mm/inkscape_mm)")
    return scale


if __name__ == "__main__":
    get_scale(root)
