import pinyin
import pinyin.cedict
import json
import random
from rich.console import Console
from rich import pretty
from rich.prompt import Prompt
from rich.panel import Panel

pretty.install()
console = Console()

def multipleChoice(question, options):
    options_str = "\n".join([f" ({a + 1}) - {options[a]}" for a in range(len(options))])
    console.print(f"{question}\n{options_str}")
    return Prompt.ask("Select an option", choices = [str(b + 1) for b in range(len(options))], console = console)

def selectMultipleChoice(question, options):
    selected_items = []
    while True:
        console.clear()
        console.print(question)
        count = 1
        for option in options:
            console.print(f" ([bold blue]{count}[/bold blue])[[bold green]{'✓' if option in selected_items else ' '}[/bold green]] - {option}")
            count += 1
        while True:
            console.print(f"Select units to study. When finished, press Enter. [bold magenta][{'/'.join([str(a + 1) for a in range(len(options))])}][/bold magenta]: ", end = '')
            selected = input()
            if (not selected and not selected_items) or (selected and selected not in [str(b + 1) for b in range(len(options))]):
                console.print("[red]Please select one of the available options")
            else:
                break
        if not selected:
            break
        else:
            if options[int(selected) - 1] in selected_items:
                selected_items.remove(options[int(selected) - 1])
            else:
                selected_items.append(options[int(selected) - 1])
    return selected_items

while True:
    console.clear()
    console.print(Panel.fit("Welcome to study.py!"))
    print()
    mode = multipleChoice("What would you like to do?", ["Study", "Add", "Edit", "Quit"])
    console.clear()

    if mode == "1":
        console.print("Study mode selected.")
        print()
        with open('chars copy.json', 'r', encoding = 'utf-8') as f:
            data = json.load(f)
        study_mode = multipleChoice("What would you like to study?", ["All", "Specific Units"])
        console.clear()
        studying_str = "Studying all characters"
        units = []
        chars = []

        if study_mode == "1":
            units = list(data['units'])

        elif study_mode == "2":
            units = selectMultipleChoice("Which units do you want to study?", list(data['units']))
            studying_str = f"Studying units {', '.join(units)}"

        for unit in units:
            for char in data['units'][unit]:
                chars.append(data['units'][unit][char])
        random.shuffle(chars)

        index = 0
        while True:
            if index == len(chars) - 1:
                index = 0
            console.clear()
            console.print(studying_str)
            print()
            console.print(Panel.fit(chars[index]['char']))
            print()
            action = multipleChoice("What would you like to do?", ["Next", "Show Answer", "Menu", "Quit"])
            print()
            
            if action == "1":
                index += 1
                continue
            elif action == "2":
                console.clear()
                console.print("Studying all characters")
                print()
                console.print(Panel.fit(chars[index]['char']))
                print()
                console.print(", ".join([p for p in chars[index]['pinyin']]))
                for definition in chars[index]["definition"]:
                    console.print(f" - {definition}")
                print()
                action2 = multipleChoice("What would you like to do?", ["Next", "Menu", "Quit"])
                if action2 == "1":
                    index += 1
                    continue
                elif action2 == "2":
                    break
                elif action2 == "3":
                    exit()
            elif action == "3":
                break
            elif action == "4":
                exit()

    elif mode == "2":
        console.print("Add mode selected.")
        print()
        with open('chars copy.json', 'r', encoding = 'utf-8') as f:
            data = json.load(f)
        unit = Prompt.ask("Enter unit name")
        data['units'][unit] = {}
        count = 1
        console.print("Enter characters:")
        line = input()
        while line:
            for char in line.split(' '):
                if char:
                    data['units'][unit][char] = {
                        "char": char,
                        "week": count,
                        "pinyin": [pinyin.get(char)],
                        "definition": pinyin.cedict.translate_word(char), 
                        "words": []
                    }
            line = input()
            count += 1
        with open('chars copy.json', 'w', encoding = 'utf-8') as f:
            json.dump(data, f, ensure_ascii = False, indent = 4)

    elif mode == "3":
        console.print("Edit mode selected.")
        print()

    elif mode == "4":
        exit()