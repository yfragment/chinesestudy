from rich import print
from rich.console import RenderGroup
from rich.panel import Panel

panel_group = RenderGroup(
    Panel("Hello", style="blue"),
    Panel("World", style="red"),
)
print(Panel(panel_group))