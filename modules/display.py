from rich import print
from rich.tree import Tree
from rich.console import Console
from modules.config import OUTLINE, SUBSYSTEMS, SUBSUBSYSTEMS_URLS, SUBSUBSYSTEMS

console = Console()

def display_subtopics():
    tree = Tree("\n [bold white]💥️ PHOTONICS CATALOG", guide_style="bold bright_black")
    for category, components in OUTLINE.items():
        category_branch = tree.add(f"[bold steel_blue3]{category}")

        for component in components:
            category_branch.add(f"[deep_sky_blue1]{component}")

    print(tree)

def get_url_from_subsystem(subsystem_name):
    for item in SUBSUBSYSTEMS_URLS:
        if item['item'] == subsystem_name:
            return item['url']

def get_subtopics_by_index(index):
    subsystem_names = list(OUTLINE.keys())

    if 0 <= index < len(subsystem_names):
        subsystem_name = subsystem_names[index]
        return OUTLINE[subsystem_name]
    else:
        raise IndexError("Subsystem index out of range.")

def select_subsystem():
    print("\n[bold white]💥 PHOTONICS CATALOG[/bold white]")
    for i, category in enumerate(OUTLINE):
        print(f"[bold steel_blue3]{i + 1}: {category}[/bold steel_blue3]")

    choice = console.input(f"[cyan]Please select an option (1-{(len(OUTLINE))}): [/cyan]")
    # TODO: sanitize input
    return int(choice) - 1

def select_subsystem_topic(subsystem_index):
    print("\n[bold white]💥️ CATALOG TOPICS[/bold white]")
    subsystem_name = list(OUTLINE.keys())[subsystem_index]
    subtopics = get_subtopics_by_index(subsystem_index)
    for i, category in enumerate(subtopics):
        print(f"[bold steel_blue3]{i + 1}: {category}[/bold steel_blue3]")
    choice = console.input(f"[cyan]Please select an option (1-{(len(subtopics))}): [/cyan]")
    return subtopics[int(choice) - 1]

def select_component(subsystem_index, components):
    print("\n[bold white]💥️ COMPONENTS[/bold white]")
    subsystem_name = list(OUTLINE.keys())[subsystem_index]
    subtopics = get_subtopics_by_index(subsystem_index)
    for i, category in enumerate(components):
        print(f"[bold steel_blue3]{i + 1}: {category['title']}[/bold steel_blue3]")
    choice = console.input(f"[cyan]Please select an option (1-{(len(components))}): [/cyan]")
    return components[int(choice) - 1]