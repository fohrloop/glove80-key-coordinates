"""Convert coordinates to the format used by the https://github.com/dariogoetz/keyboard_layout_optimizer/"""

REST_LEFT_PINKY = "C5R4"
REST_LEFT_RING = "C4R4"
REST_LEFT_MIDDLE = "C3R4"
REST_LEFT_INDEX = "C2R4"
REST_LEFT_THUMB = "T5"
REST_RIGHT_PINKY = "C5R4*"
REST_RIGHT_RING = "C4R4*"
REST_RIGHT_MIDDLE = "C3R4*"
REST_RIGHT_INDEX = "C2R4*"
REST_RIGHT_THUMB = "T5*"

# fmt: off
LAYOUT_36_KEYS = [
    ["C5R3", "C4R3", "C3R3", "C2R3", "C1R3", "C1R3*", "C2R3*", "C3R3*", "C4R3*", "C5R3*"],
    ["C5R4", "C4R4", "C3R4", "C2R4", "C1R4", "C1R4*", "C2R4*", "C3R4*", "C4R4*", "C5R4*"],
    ["C5R5", "C4R5", "C3R5", "C2R5", "C1R5", "C1R5*", "C2R5*", "C3R5*", "C4R5*", "C5R5*"],
    ["T4", "T5", "T6", "T6*", "T5*", "T4*"],
]
# fmt: on

COORDINATES_36_KEYS = {
    "C1R3": (84.512044288, 3.0541335040000064),
    "C1R3*": (203.934441728, 3.0541335040000064),
    "C1R4": (84.558070528, 20.12562150400001),
    "C1R4*": (203.888415488, 20.12562150400001),
    "C1R5": (84.594650368, 35.702834944),
    "C1R5*": (203.851835648, 35.702834944),
    "C2R3": (66.996153088, 2.7075397120000133),
    "C2R3*": (221.450332928, 2.7075397120000133),
    "C2R4": (67.268462848, 19.610846464000005),
    "C2R4*": (221.17802316799998, 19.610846464000005),
    "C2R5": (67.413637888, 35.32335846400002),
    "C2R5*": (221.032848128, 35.32335846400002),
    "C3R3": (47.47361612799999, 2.5458795520000166),
    "C3R3*": (240.972869888, 2.5458795520000166),
    "C3R4": (47.33003084799999, 19.439605504000014),
    "C3R4*": (241.11645516800002, 19.439605504000014),
    "C3R5": (47.684347648, 35.017894143999996),
    "C3R5*": (240.762138368, 35.017894143999996),
    "C4R3": (28.406751999999997, 2.6239498240000074),
    "C4R3*": (260.039734016, 2.6239498240000074),
    "C4R4": (28.26335488000001, 19.81383654400001),
    "C4R4*": (260.183131136, 19.81383654400001),
    "C4R5": (28.545021183999992, 35.547376384),
    "C4R5*": (259.901464832, 35.547376384),
    "C5R3": (10.0, 10.0),
    "C5R3*": (278.446486016, 10.0),
    "C5R4": (9.568298751999997, 26.70873318400001),
    "C5R4*": (278.87818726399996, 26.70873318400001),
    "C5R5": (9.873859071999995, 42.90782694400002),
    "C5R5*": (278.57262694400004, 42.90782694400002),
    "T4": (92.262492928, 63.632038144000006),
    "T4*": (196.183993088, 63.632038144000006),
    "T5": (109.983017728, 73.24805862400001),
    "T5*": (178.463468288, 73.24805862400001),
    "T6": (124.223243008, 88.022435584),
    "T6*": (164.223243008, 88.022435584),
}
LAYOUT, COORDINATES = LAYOUT_36_KEYS, COORDINATES_36_KEYS

print("  positions:")
for row in LAYOUT:
    items = []
    for key in row:
        x, y = COORDINATES[key]
        item = f"[{x:.1f}, {y:.1f}]"
        items.append(item)
    print(f'    - [{", ".join(items)}]')


frp_template = """
  finger_resting_positions:
    Left:
      Pinky: {left_pinky}
      Ring: {left_ring}
      Middle: {left_middle}
      Index: {left_index}
      Thumb: {left_thumb}
    Right:
      Pinky: {right_pinky}
      Ring:  {right_ring}
      Middle: {right_middle}
      Index: {right_index}
      Thumb: {right_thumb}
"""


def formatted_coordinate(key):
    x = COORDINATES[key]
    return f"[{x[0]:.1f}, {x[1]:.1f}]"


finger_resting_positions = frp_template.format(
    left_pinky=formatted_coordinate(REST_LEFT_PINKY),
    left_ring=formatted_coordinate(REST_LEFT_RING),
    left_middle=formatted_coordinate(REST_LEFT_MIDDLE),
    left_index=formatted_coordinate(REST_LEFT_INDEX),
    left_thumb=formatted_coordinate(REST_LEFT_THUMB),
    right_pinky=formatted_coordinate(REST_RIGHT_PINKY),
    right_ring=formatted_coordinate(REST_RIGHT_RING),
    right_middle=formatted_coordinate(REST_RIGHT_MIDDLE),
    right_index=formatted_coordinate(REST_RIGHT_INDEX),
    right_thumb=formatted_coordinate(REST_RIGHT_THUMB),
)

print(finger_resting_positions)
