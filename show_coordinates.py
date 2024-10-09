import xml.etree.ElementTree as ET
from pathlib import Path
from pprint import pprint

svg_file = Path(__file__).parent / "key-positions.svg"

tree = ET.parse(svg_file)
root: ET.Element = tree.getroot()

namespaces = {
    "svg": "http://www.w3.org/2000/svg",
    "inkscape": "http://www.inkscape.org/namespaces/inkscape",
}

# This is calculated in calculate_scale.py
SCALE = 0.768  # mm / inkscape mm

# Difference of left and right halves of the keyboard
SIDE_SEPARATION = 40  # mm

# labels for 36 key layout (18 per side)
LABELS_36_keys = [
    "C5R3",
    "C5R4",
    "C5R5",
    "C4R3",
    "C4R4",
    "C4R5",
    "C3R3",
    "C3R4",
    "C3R5",
    "C2R3",
    "C2R4",
    "C2R5",
    "C1R3",
    "C1R4",
    "C1R5",
    "T4",
    "T5",
    "T6",
]
LABELS_42_keys = LABELS_36_keys + [
    "C6R3",
    "C6R4",
    "C6R5",
]
LABELS_80_keys = LABELS_42_keys + [
    "C1R2",
    "C2R1",
    "C2R2",
    "C3R1",
    "C3R2",
    "C4R1",
    "C4R2",
    "C5R1",
    "C5R2",
    "C6R1",
    "C6R2",
    "C2R6",
    "C3R6",
    "C4R6",
    "C5R6",
    "C6R6",
    "T1",
    "T2",
    "T3",
]

SELECTED = LABELS_36_keys

# Origin is at top left corner.
if SELECTED == LABELS_80_keys:
    TOP_LEFT_KEY = "C6R1"
elif SELECTED == LABELS_42_keys:
    TOP_LEFT_KEY = "C6R3"
elif SELECTED == LABELS_36_keys:
    TOP_LEFT_KEY = "C5R3"
else:
    raise ValueError("Unknown layout")

# Offset origin a bit from the top left corner key center, to make the whole layout to
# reside within positive coordinates.
ORIGIN_OFFSET = (10, 10)  # mm


assert len(set(LABELS_36_keys)) == 18
assert len(set(LABELS_42_keys)) == 21
assert len(set(LABELS_80_keys)) == 40


def get_coordinates(root: ET.Element) -> dict[str, tuple[float, float]]:
    coordinates = dict()
    for label in SELECTED:
        path_element = root.find(
            f'.//svg:circle[@inkscape:label="{label}"]', namespaces=namespaces
        )
        cx = float(path_element.get("cx"))
        cy = float(path_element.get("cy"))
        x = cx * SCALE
        y = cy * SCALE
        coordinates[label] = (x, y)

    offset_x, offset_y = coordinates[TOP_LEFT_KEY]
    offset_x -= ORIGIN_OFFSET[0]
    offset_y -= ORIGIN_OFFSET[1]
    for label, (x, y) in coordinates.items():
        coordinates[label] = (x - offset_x, y - offset_y)

    coordinates_right = get_right_side(coordinates)
    coordinates.update(coordinates_right)
    return coordinates


def get_right_side(
    coordinates: dict[str, tuple[float, float]]
) -> dict[str, tuple[float, float]]:
    # mirror the coordinates along the y-axis
    coordinates_right = dict()
    for label, (x, y) in coordinates.items():
        x_right = -x
        coordinates_right[label + "*"] = (x_right, y)

    max_x = max(x for x, _ in coordinates.values())
    for label, (x, y) in coordinates_right.items():
        coordinates_right[label] = (x + 2 * max_x + SIDE_SEPARATION, y)
    return coordinates_right


def plot(coordinates: dict[str, tuple[float, float]]):
    import matplotlib.pyplot as plt

    x, y = zip(*coordinates.values())
    plt.scatter(x, y)
    for label, (x, y) in coordinates.items():
        plt.text(x, y, label)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.gca().invert_yaxis()
    plt.xlabel("x (mm)")
    plt.ylabel("y (mm)")
    plt.show()


if __name__ == "__main__":
    coordinates = get_coordinates(root)
    pprint(coordinates)
    plot(coordinates)
