"""
checker.py
==========

This module provides simple functions to check whether a user's input
matches the expected command for a level.  Separating this logic from
``trainer.py`` keeps the code modular and easier to test or extend.

At its core, ``check_command`` performs a straightforward comparison
between the user's input and the expected command defined in the level
JSON file.  As an enhancement over the base project in the PDF, we
include a few accepted variations for certain commands (like ``ls``
with optional arguments) to make the trainer a bit more forgiving and
realistic.  Comments throughout the code explain the thought process
and can guide a beginner on how to adjust or expand the rules.
"""

from typing import Optional


def normalise_command(cmd: str) -> str:
    """Return a normalised version of a command string.

    Normalisation currently trims whitespace and collapses multiple
    consecutive spaces into a single space.  This function can be
    extended later to perform more sophisticated parsing or casing
    adjustments.  Keeping normalisation separate makes it easier to
    tweak behaviour in one place.

    Args:
        cmd: The raw command entered by the user or defined in the level.

    Returns:
        A simplified command string.
    """
    # Split on whitespace and join with single spaces; this removes extra
    # spaces without affecting intended arguments.
    return " ".join(cmd.strip().split())


def check_command(user_input: str, expected_command: Optional[str]) -> bool:
    """Check whether the user's input satisfies the expected command.

    The simplest check is an exact match (after normalisation).  Some
    commands allow for small variations (e.g., ``ls`` may accept
    optional flags or a ``.`` argument), so we implement a few
    specific rules.  Beginners can use this as a template to add
    further exceptions if needed.

    Args:
        user_input: The command string the user typed.
        expected_command: The exact command string defined for the level.

    Returns:
        True if ``user_input`` is deemed correct for the level; False otherwise.
    """
    if not expected_command:
        # Without an expected command, there's nothing to compare; default to False.
        return False

    # Normalise both commands to reduce the effect of extra whitespace.
    user_norm = normalise_command(user_input)
    expected_norm = normalise_command(expected_command)

    # Rule 1: Exact match after normalisation.
    if user_norm == expected_norm:
        return True

    # Extract base commands (e.g., 'ls' from 'ls -l').
    user_parts = user_norm.split()
    expected_parts = expected_norm.split()
    user_base = user_parts[0] if user_parts else ""
    expected_base = expected_parts[0] if expected_parts else ""

    # Rule 2: Accept variations for 'ls'.  If the expected command is
    # exactly 'ls', we allow additional arguments like '.', '-l', or
    # '--all', since they still perform a directory listing.
    if expected_norm == "ls" and user_base == "ls":
        return True

    # Rule 3: Accept variations for 'history'.  The `history` command
    # can accept numerical arguments (e.g., 'history 5'), which limit
    # the number of lines shown.  We consider those correct too.
    if expected_norm == "history" and user_base == "history":
        return True

    # Rule 4: Accept either 'nano filename' or 'vi filename' when
    # expected is 'nano filename'.  Many users prefer vi; for a
    # beginner both are acceptable ways to open a file in a text editor.
    if expected_base == "nano" and user_base in {"nano", "vi"}:
        # Additionally ensure that the filename matches (second argument).
        if len(expected_parts) > 1 and len(user_parts) > 1:
            expected_file = expected_parts[1]
            user_file = user_parts[1]
            return expected_file == user_file

    # By default, anything else is treated as incorrect.
    return False