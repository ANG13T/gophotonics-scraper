from rich.console import Console
from rich.panel import Panel
import re

console = Console()

def display_menu_prompt(items, color, expand):
    menu_lines = "\n".join([f"[bright_black]{item[0]}[/bright_black] [bold]{item[1]}[/bold]" for item in items])
    menu_panel = Panel(
        f"{menu_lines}",
        border_style=color,
        expand=expand,
    )
    console.print(menu_panel)
    choice = console.input(f"[cyan]Please select an option (1-{len(items)}): [/cyan]")
    return choice

def print_line(contents, style):
    console.print(f"[{style}]{contents}[/{style}]")

def print_input(contents, style):
    return console.input(f"[{style}]{contents}[/{style}]")

def print_styled_items(items):
    print("\n")
    for item in items:
        print_line("=" * 70, "bold steel_blue3")

        print(items)
        for key, value in item.items():
            if key == "details":
                for k, v in value.items():
                    console.print(f"[steel_blue3 bold]{k.upper()}[/steel_blue3 bold] {v}")
            else:
                console.print(f"[steel_blue3 bold]{key.upper()}[/steel_blue3 bold] {value}")

def highlight_keyword(text, keyword):
    return re.sub(f"({re.escape(keyword)})", r"[bold yellow]\1[/bold yellow]", text, flags=re.IGNORECASE)

def print_styled_items_with_keyword_highlights(items, keyword):
    print("\n")
    for item in items:
        console.print("=" * 70, style="bold steel_blue3")
        for key, value in item.items():
            if key == "details":
                for k, v in value.items():
                    highlighted_v = highlight_keyword(str(v), keyword)
                    console.print(f"[steel_blue3 bold]{k.upper()}[/steel_blue3 bold] {highlighted_v}")
            else:
                highlighted_value = highlight_keyword(str(value), keyword)
                console.print(f"[steel_blue3 bold]{key.upper()}[/steel_blue3 bold] {highlighted_value}")

def print_styled_component(component):
    print("\n")
    for key, value in component.items():
        if key == 'specs':
            for spec in value:
                console.print(f"\n[steel_blue bold][ {spec['title'].upper()} ]\n [/steel_blue bold]")
                for item in spec['items']:
                    console.print(f"   [steel_blue3 bold]{item['field'].upper()}:[/steel_blue3 bold] {item['value']}")
            continue

        if key != 'details':
            console.print(f"[steel_blue3 bold]{key.upper()}:[/steel_blue3 bold] {value}")