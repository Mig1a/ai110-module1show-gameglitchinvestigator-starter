def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 1000  # FIXME: Logic breaks here | FIX: Hard range was 1-50, easier than Normal; Claude corrected it to 1-1000
    return 1, 100  # FIXME: Logic breaks here | FIX: Fallback return was missing entirely; Claude added it so unknown difficulties don't return None



def parse_guess(raw: str, low: int, high: int):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    if value < low or value > high:
        return False, None, f"Please guess within the range {low} to {high}."  # FIXME: Logic breaks here | FIX: Function had no range check; Claude added low/high params and out-of-range rejection

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"  # FIXME: Logic breaks here | FIX: Message said "Go HIGHER!" when guess was too high; Claude swapped to correct direction
        else:
            return "Too Low", "📈 Go HIGHER!"  # FIXME: Logic breaks here | FIX: Message said "Go LOWER!" when guess was too low; Claude swapped to correct direction
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"  # FIXME: Logic breaks here | FIX: Same swapped message bug in the TypeError fallback path; Claude fixed both
        return "Too Low", "📈 Go HIGHER!"  # FIXME: Logic breaks here | FIX: Same swapped message bug in the TypeError fallback path; Claude fixed both


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * attempt_number  # FIXME: Logic breaks here | FIX: Was attempt_number + 1, making first attempt score 80 instead of 90; Claude removed the +1 offset
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
