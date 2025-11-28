"""
trainer.py
============

This script is the main entry point for the LinuxTrainer CLI project.  It
loads level definitions from JSON files, presents each level to the user,
prompts for input, checks the user’s answer against the expected command,
provides hints on request, logs all input, optionally executes safe commands
to show real output, and uses coloured text to make messages clear and
friendly.  The design and implementation here are based on the example
project described in the accompanying PDF, but extended with more levels,
additional features and thorough inline comments to aid beginners.

The code is kept modular: loading levels is handled by a separate
function, and the actual command checking lives in the ``checker`` module.
Logging is performed to a separate file under ``logs/``, and colour
styling is provided by the ``colorama`` library.
"""

import json
import os
import subprocess
from datetime import datetime

from colorama import init, Fore, Style  # colour printing support

import checker  # our own module that handles checking user commands


def load_levels() -> list:
    """Load all level definitions from the ``levels`` directory.

    The function reads every JSON file located in the ``levels/`` directory
    relative to this script.  Each JSON file defines one training level
    (containing keys like ``number``, ``title``, ``description``,
    ``expected_command`` and ``hint``).  Levels are sorted by their
    numerical ``number`` key so they are presented in order.

    Returns:
        A list of dictionaries, one per level, sorted by the ``number`` key.
    """
    # Determine the absolute path to the levels directory.  We use
    # ``os.path.dirname(__file__)`` so that this function works regardless
    # of where the script is executed from.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    levels_dir = os.path.join(base_dir, "levels")

    # Get all JSON files in the directory.  Files that don't end with
    # ``.json`` are ignored.  We use ``sorted`` on the filenames here,
    # but we'll sort again later by the ``number`` field for robustness.
    level_files = [f for f in os.listdir(levels_dir) if f.lower().endswith(".json")]

    levels = []
    for filename in level_files:
        path = os.path.join(levels_dir, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                levels.append(data)
        except (IOError, json.JSONDecodeError) as e:
            # If a file can't be read or parsed, we inform the user but
            # continue loading the rest.  Beginners might accidentally
            # introduce syntax errors in JSON files; this helps diagnose it.
            print(Fore.RED + f"Error reading level file {filename}: {e}" + Style.RESET_ALL)

    # Sort the list by the 'number' field; if missing, default to 0 to
    # ensure consistent ordering.  Sorting by the numeric field rather
    # than filename lets authors name files however they like.
    levels.sort(key=lambda level: level.get("number", 0))
    return levels


def main() -> None:
    """Run the LinuxTrainer interactive CLI.

    This function orchestrates the interactive session: it welcomes the
    user, loads the levels, iterates through them, prompts for user
    input, checks correctness using the ``checker`` module, provides
    hints, logs all input to a file, optionally executes safe commands to
    demonstrate their output, and prints a congratulatory message upon
    completion.  It also handles graceful exiting when the user types
    ``exit`` or ``quit``.
    """
    # Initialise colourama.  Without calling ``init()``, colours may
    # not render correctly on some terminals (especially Windows).  We
    # set ``autoreset=True`` so that colour settings reset after each
    # print call; this avoids needing to append ``Style.RESET_ALL`` to
    # every message manually.
    init(autoreset=True)

    # Prepare logging.  We'll append to a log file in the ``logs``
    # directory.  If the directory doesn't exist, create it.  Logging
    # lets students or instructors review what was entered during a
    # session.  Each run writes a start and end timestamp.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(base_dir, "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    log_path = os.path.join(logs_dir, "commands.log")
    log_file = open(log_path, "a", encoding="utf-8")
    log_file.write(f"Session started at {datetime.now().isoformat()}\n")

    # Load all levels.  If no levels are loaded, exit early.
    levels = load_levels()
    if not levels:
        print(Fore.RED + "No levels found. Please create JSON files in the 'levels' directory." + Style.RESET_ALL)
        log_file.write("No levels loaded. Exiting.\n")
        log_file.close()
        return

    # Welcome message explaining how the tool works.  We keep the tone
    # friendly and descriptive since this project targets beginners.
    print(Style.BRIGHT + "Welcome to LinuxTrainer CLI – Extended Version!" + Style.RESET_ALL)
    print("This interactive program helps you practise common Linux commands.")
    print("Type the command you think solves the current level, or type 'hint' for help.")
    print("You can leave the trainer at any time by typing 'exit' or 'quit'.\n")

    # Define a set of commands that we consider safe to execute.  For
    # demonstration purposes, when a correct command belongs to this set
    # we will run it using ``subprocess.run`` and display its output.
    # Commands that modify the filesystem (e.g., rm, mv, cp) or launch
    # editors are not executed automatically for safety.
    safe_commands = {"pwd", "ls", "whoami", "echo", "clear", "date", "history"}

    try:
        # Iterate through each level in order.
        for level in levels:
            number = level.get("number")
            title = level.get("title", f"Level {number}")
            description = level.get("description", "")
            expected_command = level.get("expected_command")
            hint = level.get("hint", "")

            # Display the level header with bold styling.  The Style.BRIGHT
            # attribute makes the text bright/bold.
            print(Style.BRIGHT + f"** Level {number}: {title} **" + Style.RESET_ALL)
            print(description)

            # Prompt until the correct command is entered or the user quits.
            while True:
                user_input = input("> ").strip()
                # Record every input to the log with the level number.
                log_file.write(f"Level {number} input: {user_input}\n")

                # If the user wants to quit, log it and return from main().
                if user_input.lower() in {"exit", "quit"}:
                    print("Exiting the LinuxTrainer. Goodbye!")
                    log_file.write("User exited the session.\n")
                    return

                # If the user requests a hint, print it in yellow.  We
                # ``continue`` so the loop prompts again without checking.
                if user_input.lower() == "hint":
                    if hint:
                        print(Fore.YELLOW + f"Hint: {hint}")
                    else:
                        print(Fore.YELLOW + "No hint available for this level.")
                    continue

                # Check the command using our checker module.  We pass
                # ``user_input`` and ``expected_command``; the checker
                # returns True if the user's command is acceptable.
                if checker.check_command(user_input, expected_command):
                    # Success message in green.
                    print(Fore.GREEN + "Correct! Well done.")

                    # If the command appears in our safe list, attempt to
                    # execute it to show real output.  We split the
                    # command into parts (e.g., "ls -l" -> ["ls", "-l"]) to
                    # pass to subprocess.run().  Setting
                    # ``capture_output=True`` captures stdout/stderr.  We
                    # ignore non-zero return codes (check=False) so the
                    # program continues even if the command errors.
                    base = user_input.split()[0] if user_input else ""
                    if base in safe_commands:
                        try:
                            result = subprocess.run(user_input.split(), capture_output=True, text=True, check=False)
                            output = result.stdout.strip()
                            error_output = result.stderr.strip()
                            # Only print output if it's not empty.
                            if output:
                                print(output)
                            # If there was error output, print it in red.
                            if error_output:
                                print(Fore.RED + error_output)
                        except Exception as e:
                            # We silently ignore exceptions during command execution
                            # because we don't want to crash the trainer if
                            # something unexpected happens.  Logging could be
                            # added here for debugging.
                            pass
                    else:
                        # For commands not in the safe list, inform the
                        # user that execution has been skipped.  This
                        # encourages safety and prevents unintended side effects.
                        print(Fore.CYAN + "(Command execution skipped for safety.)")

                    # Break out of the input loop and proceed to the next level.
                    break
                else:
                    # Incorrect command; encourage the user to try again.  We
                    # colour the message red to clearly indicate an error.
                    print(Fore.RED + "Oops, that's not the right command. Try again or type 'hint' for help.")

            # After a correct command, print a blank line to separate levels.
            print()

        # When the for-loop completes normally, the user has finished all levels.
        print(Style.BRIGHT + Fore.GREEN + "Congratulations! You have completed all the levels!" + Style.RESET_ALL)
        print("You've learned a variety of Linux commands. Keep practising!")
    finally:
        # Make sure we always record the end of the session and close the log.
        log_file.write(f"Session ended at {datetime.now().isoformat()}\n")
        log_file.close()


if __name__ == "__main__":
    main()