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
    console.print(f"[bold yellow]?[/bold yellow] {question}\n{options_str}")
    return Prompt.ask("Select an option", choices = [str(b + 1) for b in range(len(options))], console = console)

def selectMultipleChoice(question, options):
    selected_items = []
    while True:
        console.clear()
        console.print(f"[bold yellow]?[/bold yellow] {question}")
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

def edit(data, char):
    char_data = None
    for unit in data['units']:
        if char in data['units'][unit]:
            char_data = data['units'][unit][char]
            break
    if not char_data:
        return -1
    def print_stuff():
        console.clear()
        console.print("[bold]Editing character")
        print()
        console.print(Panel.fit(char))
        print()
        console.print(f"pinyin: {char_data['pinyin']}")
        console.print(f"definitions: {char_data['definitions']}")
        console.print(f"words: {char_data['words']}")
        console.print(f"week: {char_data['week']}")
        print()
    while True:
        print_stuff()
        edit = multipleChoice("What would you like to edit?", ["Delete", "Edit Pinyin", "Edit Words", "Back"])
        if edit == "1":
            data['units'][unit].pop(char)
            with open('chars.json', 'w', encoding = 'utf-8') as f:
                json.dump(data, f, ensure_ascii = False, indent = 4)
            return 1
        elif edit == "2":
            print_stuff()
            pinyin = Prompt.ask("Enter pinyin", console = console)
            data['units'][unit][char]['pinyin'] = pinyin.split(' ')
            with open('chars.json', 'w', encoding = 'utf-8') as f:
                json.dump(data, f, ensure_ascii = False, indent = 4)
        elif edit == "3":
            print_stuff()
            words = Prompt.ask("Enter words", console = console)
            data['units'][unit][char]['words'] = words.split(' ')
            with open('chars.json', 'w', encoding = 'utf-8') as f:
                json.dump(data, f, ensure_ascii = False, indent = 4)
        elif edit == "4":
            return 0

while True:
    console.clear()
    console.print(Panel.fit("[bold]Welcome to study.py!"))
    print()
    mode = multipleChoice("What would you like to do?", ["Study", "Search", "Add", "Edit", "Quit"])
    console.clear()

    if mode == "1":
        console.print("[bold]Study mode selected")
        print()
        with open('chars.json', 'r', encoding = 'utf-8') as f:
            data = json.load(f)
        study_mode = multipleChoice("What would you like to study?", ["All", "Specific Units"])
        studying_str = "[bold]Studying all characters"
        units = []
        chars = []

        if study_mode == "1":
            units = list(data['units'])

        elif study_mode == "2":
            units = selectMultipleChoice("Which units do you want to study?", list(data['units']))
            studying_str = f"[bold]Studying units {', '.join(units)}"
        
        console.clear()
        console.print("[bold]Study mode selected")
        print()
        order = multipleChoice("How would you like to study?", ["Random", "In Order"])

        for unit in units:
            for char in data['units'][unit]:
                chars.append(data['units'][unit][char])
        if order == "1":
            random.shuffle(chars)

        index = 0
        show = False
        while True:
            if index == len(chars):
                if order == "1":
                    random.shuffle(chars)
                index = 0
            if index < 0:
                index = 0
            console.clear()
            console.print(studying_str)
            print()
            console.print(f"[[bold blue]{index + 1}[/bold blue]/[bold blue]{len(chars)}[/bold blue]]")
            print()
            console.print(Panel.fit(chars[index]['char']))
            print()
            if show:
                console.print(", ".join([p for p in chars[index]['pinyin']]))
                console.print(', '.join(chars[index]['definitions']))
                console.print(', '.join(chars[index]['words']))
                print()
            action = multipleChoice("What would you like to do?", ["Next", "Previous", "Edit", "Exit"] if show else ["Next", "Previous", "Show Answer", "Edit", "Exit"])
            print()
            if show and action == "4":
                action = "5"
            show = False

            if action == "1":
                index += 1
                continue
            elif action == "2":
                index -= 1
                continue
            elif action == "3":
                show = True
                continue
            elif action == "4":
                result = edit(data, chars[index]['char'])
                if result == 1:
                    chars = chars[:index] + chars[index + 1:]
                with open('chars.json', 'r', encoding = 'utf-8') as f:
                    data = json.load(f)
            elif action == "5":
                break

    elif mode == "2":
        char_data = None
        while True:
            with open('chars.json', 'r', encoding = 'utf-8') as f:
                data = json.load(f)
            console.clear()
            if char_data:
                console.print("[bold]Showing search results")
                print()
                console.print(Panel.fit(char_data['char']))
                print()
                console.print(", ".join([p for p in char_data['pinyin']]))
                console.print(', '.join(char_data['definitions']))
                console.print(', '.join(char_data['words']))
                print()
            else:
                console.print("[bold]Search mode selected")
            print()
            char = Prompt.ask("[bold yellow]?[/bold yellow] What character would you like to search for? (Press Enter to return to main menu)")
            if not char:
                break
            for unit in data['units']:
                if char in data['units'][unit]:
                    char_data = data['units'][unit][char]
            if not char_data:
                continue

    elif mode == "3":
        with open('chars.json', 'r', encoding = 'utf-8') as f:
            data = json.load(f)
        console.print("[bold]Add mode selected")
        print()
        unit = Prompt.ask("What is the name of the unit?")
        data['units'][unit] = {}
        count = 1
        console.print("Enter characters below:")
        line = input()
        while line:
            for char in line.split(' '):
                if char:
                    data['units'][unit][char] = {
                        "char": char,
                        "week": count,
                        "pinyin": [pinyin.get(char)],
                        "definitions": pinyin.cedict.translate_word(char), 
                        "words": []
                    }
            line = input()
            count += 1
        with open('chars.json', 'w', encoding = 'utf-8') as f:
            json.dump(data, f, ensure_ascii = False, indent = 4)

    elif mode == "4":
        while True:
            with open('chars.json', 'r', encoding = 'utf-8') as f:
                data = json.load(f)
            console.clear()
            console.print("Edit mode selected")
            print()
            char = Prompt.ask("[bold yellow]?[/bold yellow] What character would you like to edit? (Press Enter to return to main menu)")
            if not char:
                break
            result = edit(data, char)
            if result < 0:
                continue


    elif mode == "5":
        exit()