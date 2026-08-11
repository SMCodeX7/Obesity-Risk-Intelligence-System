CATEGORY_STYLES = {
    "Insufficient_Weight": {
        "color": "#0284C7",
        "background": "#F0F9FF",
        "border": "#BAE6FD",
    },
    "Normal_Weight": {
        "color": "#16A34A",
        "background": "#F0FDF4",
        "border": "#BBF7D0",
    },
    "Overweight_Level_I": {
        "color": "#CA8A04",
        "background": "#FEFCE8",
        "border": "#FEF08A",
    },
    "Overweight_Level_II": {
        "color": "#D97706",
        "background": "#FFF7ED",
        "border": "#FED7AA",
    },
    "Obesity_Type_I": {
        "color": "#EA580C",
        "background": "#FFF7ED",
        "border": "#FDBA74",
    },
    "Obesity_Type_II": {
        "color": "#DC2626",
        "background": "#FEF2F2",
        "border": "#FECACA",
    },
    "Obesity_Type_III": {
        "color": "#991B1B",
        "background": "#FEF2F2",
        "border": "#FCA5A5",
    },
}


DEFAULT_CATEGORY_STYLE = {
    "color": "#475569",
    "background": "#F8FAFC",
    "border": "#E2E8F0",
}


def get_category_style(class_name):
    return CATEGORY_STYLES.get(
        class_name,
        DEFAULT_CATEGORY_STYLE,
    )


def get_category_color(class_name):
    return get_category_style(
        class_name
    )["color"]


def get_category_background(class_name):
    return get_category_style(
        class_name
    )["background"]


def get_category_border(class_name):
    return get_category_style(
        class_name
    )["border"]