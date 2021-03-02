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

console.print(Panel.fit("Welcome to study.py!"))
print()
mode = multipleChoice("What would you like to do?", ["Study", "Add", "Edit", "Quit"])
console.clear()

if mode == "1":
    console.print("Study mode selected.")
    print()
    with open('chars.json', 'r', encoding = 'utf-8') as f:
        data = json.load(f)
    study_mode = multipleChoice("What would you like to study?", ["All", "Specific Units"])
    console.clear()

    if study_mode == "1":
        while True:
            console.clear()
            console.print("Studying all characters")
            print()
            unit = random.choice(list(data['units'].values()))
            week = random.choice(unit)
            char = random.choice(week)
            console.print(Panel.fit(char['char']))
            print()
            action = multipleChoice("What would you like to do?", ["Next", "Show Answer", "Quit"])
            print()
            
            if action == "1":
                continue
            elif action == "2":
                console.clear()
                console.print("Studying all characters")
                print()
                console.print(Panel.fit(char['char']))
                print()
                console.print(char['pinyin'])
                for d in char["definition"]:
                    console.print(f" - {d}")
                print()
                action2 = multipleChoice("What would you like to do?", ["Next", "Quit"])
                if action2 == "1":
                    continue
                elif action2 == "2":
                    exit()
            elif action == "3":
                exit()        

elif mode == "2":
    console.print("Add mode selected.")
    print()
    with open('chars.json', 'r', encoding = 'utf-8') as f:
        data = json.load(f)
    unit = Prompt.ask("Enter unit name")
    data['units'][unit] = []
    count = 0
    console.print("Enter characters:")
    line = input()
    while line:
        data['units'][unit].append([])
        for c in line.split(' '):
            if c:
                data['units'][unit][count].append(
                    {
                        "char": c,
                        "pinyin": pinyin.get(c),
                        "definition": pinyin.cedict.translate_word(c), 
                        "words": []
                    }
                )
        line = input()
        count += 1
    with open('chars.json', 'w', encoding = 'utf-8') as f:
        json.dump(data, f, ensure_ascii = False, indent = 4)

elif mode == "3":
    console.print("Edit mode selected.")
    print()

elif mode == "4":
    exit()