# LinuxTrainer CLI – Interactive Linux Command Trainer

**LinuxTrainer CLI is a command-line application designed for beginners. It teaches basic Linux commands through interactive levels. This extended version includes 23 levels, coloured output, logging of your attempts, and helpful hints. It is designed for students who are learning Linux and want a practical, hands-on way to practise common commands.**

## Features

* **Interactive levels:** progress through 23 levels that cover core
  commands such as `pwd`, `ls`, `cd`, `mkdir`, `touch`, `cat`, `rm`,
  `mv`, `cp`, `nano`/`vi`, `head`, `tail`, `grep`, `find`, `man`,
  `echo`, `whoami`, `clear`, `chmod`, and `history`.
* **Hints on demand:** type `hint` at any prompt to receive a helpful
  clue tailored to the current task.
* **Coloured output:** success messages appear in green, errors in red
  and hints in yellow, making it easy to distinguish information.
* **Command logging:** every input you enter is recorded in
  `logs/commands.log` so you can review your progress or share it
  with an instructor.
* **Optional command execution:** for safe commands (like `pwd` and
  `ls`) the trainer will run the command and show its output.

## Project Structure

The project is organised into a clear directory structure inspired by
the sample project in the PDF:

```
LinuxTrainerCLI/
├── trainer.py        # Main script that runs the interactive CLI
├── checker.py        # Module that validates user commands
├── levels/           # JSON files defining each level
│   ├── level01.json  # Level 1 definition (pwd)
│   ├── level02.json  # Level 2 definition (ls)
│   └── …             # Further levels up to level23.json
├── logs/             # Directory where commands.log is written
├── requirements.txt  # Python dependencies (currently just colorama)
├── .gitignore        # Files and folders to be ignored by Git
└── README.md         # This documentation
```

Each JSON file in `levels/` contains keys like `number`, `title`,
`description`, `expected_command` and `hint`.  Splitting level
definitions into separate files makes it simple to add or modify
exercises without touching the Python code.

## Prerequisites

Before running the trainer you will need:

1. **Python 3** – Installable from python.org or via your package
   manager.  You can verify it with `python3 --version`.
2. **A terminal with Linux commands** – The trainer is meant to run on
   a system where commands like `pwd` and `ls` are available.  This
   includes most Linux distributions, macOS (in a terminal), or
   Windows with a Bash shell (e.g. WSL or Git Bash).
3. **Install dependencies** – run `pip install -r requirements.txt`
   from inside the project directory to install `colorama`.

## How to Run

1. **Clone or download** the repository to your machine.
2. Open a terminal and **navigate into** the `LinuxTrainerCLI` folder.
3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Launch the trainer with:

   ```bash
   python3 trainer.py
   ```

   If your system uses `python` as Python 3, you can use `python
   trainer.py` instead.

## How to Use the Trainer

When you start the program you will see a welcome message followed by
the first level description.  At the prompt (`>`), type the command
you believe solves the task and press Enter.  The trainer will tell
you if your answer is correct.  You can:

* Type **`hint`** to see a helpful tip for the current level.
* Type **`exit`** or **`quit`** to stop the session at any time.
* On success, the trainer may run the command (if it is safe) and
  show you the real output, then move on to the next level.

Below is an example session showing the first few levels:

```bash
$ python3 trainer.py
Welcome to LinuxTrainer CLI – Extended Version!
This interactive program helps you practise common Linux commands.
Type the command you think solves the current level, or type 'hint' for help.
You can leave the trainer at any time by typing 'exit' or 'quit'.

** Level 1: Print Working Directory **
Level 1: You are in a shell, but you don't know where. Use the command to print your current working directory (the folder you are in).
> ls
Oops, that's not the right command. Try again or type 'hint' for help.
> hint
Hint: Use the command that stands for 'print working directory'.
> pwd
/home/username/LinuxTrainerCLI
Correct! Well done.

** Level 2: List Files **
Level 2: List the files and directories in the current folder. This helps you see what's around you.
> ls
trainer.py  checker.py  levels  logs  README.md  requirements.txt
Correct! Well done.
```

Work through each level at your own pace.  If you make a mistake,
don’t worry – the trainer will prompt you to try again.

## Extending the Project

Adding new levels is easy and requires no changes to the Python code.
Simply create a new JSON file in the `levels/` directory following the
same structure as the existing ones.  Use the next consecutive
number, provide a clear `title`, a friendly `description`, the exact
`expected_command`, and a useful `hint`.  After saving the file,
re‑run `trainer.py` and your new level will appear automatically.

For example, to add a level that teaches the `uptime` command:

```json
{
  "number": 24,
  "title": "System Uptime",
  "description": "Check how long the system has been running.",
  "expected_command": "uptime",
  "hint": "Use the command that displays how long the system has been up."
}
```

Place this as `levels/level24.json` and you’re done.

## Contributing

Contributions are welcome!  Feel free to fork the repository, add
your own levels or enhancements, and open a pull request.  If you
notice any issues or have suggestions, please open an issue on
GitHub.
