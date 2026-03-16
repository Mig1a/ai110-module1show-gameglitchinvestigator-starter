import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


# ── existing tests (fixed: check_guess returns a tuple) ──────────────────────

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# ── Bug 1: Hard range was 1–50 (easier than Normal) ──────────────────────────

def test_hard_range_is_harder_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, "Hard range must be wider than Normal"

def test_hard_range_is_1_to_1000():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1 and high == 1000


# ── Bug 2: Hint messages were backwards ──────────────────────────────────────

def test_too_high_message_says_go_lower():
    _, message = check_guess(80, 50)
    assert "LOWER" in message.upper(), f"Expected 'LOWER' in message, got: {message}"

def test_too_low_message_says_go_higher():
    _, message = check_guess(20, 50)
    assert "HIGHER" in message.upper(), f"Expected 'HIGHER' in message, got: {message}"


# ── Bug 3: parse_guess had no range validation ────────────────────────────────

def test_guess_above_range_is_rejected():
    ok, _, err = parse_guess("101", 1, 100)
    assert not ok
    assert err is not None

def test_guess_below_range_is_rejected():
    ok, _, err = parse_guess("0", 1, 100)
    assert not ok
    assert err is not None

def test_guess_at_boundary_low_is_accepted():
    ok, value, _ = parse_guess("1", 1, 100)
    assert ok and value == 1

def test_guess_at_boundary_high_is_accepted():
    ok, value, _ = parse_guess("100", 1, 100)
    assert ok and value == 100


# ── Bug 4: get_range_for_difficulty missing fallback return ───────────────────

def test_unknown_difficulty_returns_default_range():
    low, high = get_range_for_difficulty("Unknown")
    assert low == 1 and high == 100


# ── Bug 5: update_score used attempt_number + 1 (skipped first attempt) ──────

def test_score_on_first_attempt_is_90():
    # attempt_number=1 (first valid guess), win should give 100 - 10*1 = 90
    new_score = update_score(0, "Win", 1)
    assert new_score == 90, f"Expected 90, got {new_score}"

def test_score_does_not_use_plus_one_offset():
    # If +1 bug were present, attempt_number=1 would compute 100 - 10*2 = 80
    new_score = update_score(0, "Win", 1)
    assert new_score != 80, "Score still uses the +1 offset bug"
