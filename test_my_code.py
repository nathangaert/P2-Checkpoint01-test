"""Test your Animon Battle Arena classes incrementally.

Run this script after implementing each file to check your work:

    python3 test_my_code.py

It tests each class in order and stops at the first failure so you
can fix one thing at a time.
"""


def test_animon_subclasses():
    print("Testing Animon subclasses...", end=" ")
    from animon import Animon, FireAnimon, WaterAnimon, GrassAnimon

    fire = FireAnimon("Flamey", 12, 4)
    assert isinstance(fire, Animon), "FireAnimon should inherit from Animon"
    assert fire.get_animon_type() == "Fire", f"Expected 'Fire', got '{fire.get_animon_type()}'"
    assert str(fire) == "[Fire] Flamey (Power: 12, Defense: 4)", f"Got: {str(fire)}"

    water = WaterAnimon("Splashy", 9, 6)
    assert water.get_animon_type() == "Water"

    grass = GrassAnimon("Leafy", 10, 8)
    assert grass.get_animon_type() == "Grass"

    # Fire vs Grass (1.5x): (12 - 8) * 1.5 = 6
    assert fire.calculate_damage(grass) == 6, f"Fire vs Grass: expected 6, got {fire.calculate_damage(grass)}"

    # Fire vs Water (0.5x): (12 - 6) * 0.5 = 3
    assert fire.calculate_damage(water) == 3, f"Fire vs Water: expected 3, got {fire.calculate_damage(water)}"

    # Water vs Fire (1.5x): (9 - 4) * 1.5 = 7
    assert water.calculate_damage(fire) == 7, f"Water vs Fire: expected 7, got {water.calculate_damage(fire)}"

    # Water vs Grass (0.5x): (9 - 8) * 0.5 = 0
    assert water.calculate_damage(grass) == 0, f"Water vs Grass: expected 0, got {water.calculate_damage(grass)}"

    # Grass vs Water (1.5x): (10 - 6) * 1.5 = 6
    assert grass.calculate_damage(water) == 6, f"Grass vs Water: expected 6, got {grass.calculate_damage(water)}"

    # Grass vs Fire (0.5x): (10 - 4) * 0.5 = 3
    assert grass.calculate_damage(fire) == 3, f"Grass vs Fire: expected 3, got {grass.calculate_damage(fire)}"

    # __eq__: same stats = equal, different stats = not equal
    fire_copy = FireAnimon("Flamey", 12, 4)
    assert fire == fire_copy, "Two Animon with same name/type/power/defense should be equal"
    assert fire != water, "Animon with different attributes should not be equal"
    assert fire != "not an animon", "Animon should not be equal to non-Animon types"

    # Subclass equality: a FireAnimon and base Animon with same stats are NOT equal (different type)
    base = Animon("Flamey", 12, 4)
    assert fire != base, "FireAnimon and base Animon should not be equal (different animon_type)"

    print("PASSED")


def test_deck_core():
    print("Testing Deck (core + protocols)...", end=" ")
    from deck import Deck
    from animon import Animon

    # owner_name default parameter
    d_default = Deck()
    d_named = Deck("Alex")

    d = Deck()
    assert d.size() == 0, f"New deck should have size 0, got {d.size()}"

    a1 = Animon("TestMon1", 10, 5)
    a2 = Animon("TestMon2", 8, 3)
    d.add_card(a1)
    d.add_card(a2)
    assert d.size() == 2, f"Expected size 2, got {d.size()}"

    # peek should return first card without removing it
    peeked = d.peek()
    assert peeked.get_name() == "TestMon1", f"peek() should return first card, got {peeked.get_name()}"
    assert d.size() == 2, "peek() should not change deck size"

    # draw should return first card and remove it (FIFO)
    drawn = d.draw_card()
    assert drawn.get_name() == "TestMon1", f"draw_card() should return first card, got {drawn.get_name()}"
    assert d.size() == 1, f"After draw, size should be 1, got {d.size()}"

    drawn = d.draw_card()
    assert drawn.get_name() == "TestMon2"

    # __str__
    d2 = Deck()
    d2.add_card(Animon("Mon", 5, 3))
    s = str(d2)
    assert "Deck:" in s, "__str__ should start with 'Deck:'"
    assert "[Normal] Mon" in s, f"__str__ should contain card info, got: {s}"

    # __len__: len(deck) should work
    d_len = Deck()
    assert len(d_len) == 0, f"len() of empty deck should be 0, got {len(d_len)}"
    d_len.add_card(Animon("A", 1, 1))
    d_len.add_card(Animon("B", 2, 2))
    assert len(d_len) == 2, f"len() should be 2, got {len(d_len)}"

    # __iter__: for card in deck should work
    names_from_iter = [card.get_name() for card in d_len]
    assert names_from_iter == ["A", "B"], f"Iterating should yield cards in order, got {names_from_iter}"

    # __contains__: card in deck should work (uses Animon.__eq__)
    search = Animon("A", 1, 1)
    assert search in d_len, "Animon('A', 1, 1) should be found in deck via 'in' operator"
    not_there = Animon("Z", 9, 9)
    assert not_there not in d_len, "Animon('Z', 9, 9) should not be found in deck"

    print("PASSED")


def test_seed_determinism():
    print("Testing shuffle determinism...", end=" ")
    import random
    from deck import Deck
    from animon import Animon

    # Verify that seed 42 produces a known shuffle order.
    # If you call random functions elsewhere in your code, this will break.
    random.seed(42)
    d = Deck()
    names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    for n in names:
        d.add_card(Animon(n, 5, 5))
    d.shuffle()
    first = d.draw_card().get_name()
    second = d.draw_card().get_name()
    assert first == "H", (
        f"After seed(42) and shuffle, first card should be 'H', got '{first}'. "
        "Make sure you are not calling any random functions outside of main.py."
    )
    assert second == "D", (
        f"After seed(42) and shuffle, second card should be 'D', got '{second}'. "
        "Make sure you are not calling any random functions outside of main.py."
    )

    print("PASSED")


def test_invalid_stat_error():
    print("Testing InvalidStatError...", end=" ")
    from invalid_stat_error import InvalidStatError

    e = InvalidStatError("power", -5)
    assert isinstance(e, Exception), "InvalidStatError should inherit from Exception"
    assert str(e) == "Invalid power: -5 (must be non-negative)", f"Got: \"{str(e)}\""

    e2 = InvalidStatError("defense", -3)
    assert str(e2) == "Invalid defense: -3 (must be non-negative)", f"Got: \"{str(e2)}\""

    print("PASSED")


def test_deck_full_error():
    print("Testing DeckFullError...", end=" ")
    from deck_full_error import DeckFullError

    e = DeckFullError("Alex", 10)
    assert isinstance(e, Exception), "DeckFullError should inherit from Exception"
    assert str(e) == "Alex's deck is full! (max 10 cards)", f"Got: \"{str(e)}\""

    e2 = DeckFullError("Tim", 5)
    assert str(e2) == "Tim's deck is full! (max 5 cards)", f"Got: \"{str(e2)}\""

    print("PASSED")


def test_animon_validation():
    print("Testing Animon stat validation...", end=" ")
    from animon import Animon
    from invalid_stat_error import InvalidStatError

    try:
        Animon("Bad", -1, 5)
        assert False, "Should have raised InvalidStatError for negative power"
    except InvalidStatError as e:
        assert "power" in str(e), f"Error should mention 'power', got: {str(e)}"

    try:
        Animon("Bad", 5, -3)
        assert False, "Should have raised InvalidStatError for negative defense"
    except InvalidStatError as e:
        assert "defense" in str(e), f"Error should mention 'defense', got: {str(e)}"

    print("PASSED")


def test_deck_capacity():
    print("Testing Deck capacity...", end=" ")
    from deck import Deck
    from animon import Animon
    from deck_full_error import DeckFullError

    # DeckFullError: max_size defaults to 10
    d3 = Deck("Alex")
    for i in range(10):
        d3.add_card(Animon(f"Mon{i}", 5, 5))
    try:
        d3.add_card(Animon("OneMore", 5, 5))
        assert False, "Should have raised DeckFullError when adding 11th card"
    except DeckFullError as e:
        assert "Alex" in str(e), f"Error should mention owner name, got: {str(e)}"
        assert "10" in str(e), f"Error should mention max size, got: {str(e)}"

    # Custom max_size
    d4 = Deck("Tim", max_size=3)
    for i in range(3):
        d4.add_card(Animon(f"Mon{i}", 5, 5))
    try:
        d4.add_card(Animon("Extra", 5, 5))
        assert False, "Should have raised DeckFullError"
    except DeckFullError:
        pass  # expected

    print("PASSED")


def test_trainer():
    print("Testing Trainer...", end=" ")
    from trainer import Trainer
    from animon import FireAnimon, WaterAnimon

    t = Trainer("Alex", 100)
    assert t.get_name() == "Alex"
    assert t.get_health() == 100
    assert t.is_alive()
    assert str(t) == "Alex (HP: 100, Deck: 0 cards)", f"Got: {str(t)}"

    t.take_damage(30)
    assert t.get_health() == 70

    t.take_damage(200)
    assert t.get_health() == 0, f"HP should floor at 0, got {t.get_health()}"
    assert not t.is_alive()

    # Deck operations
    t2 = Trainer("Tim", 50)
    t2.add_card_to_deck(FireAnimon("Mon1", 10, 5))
    t2.add_card_to_deck(WaterAnimon("Mon2", 8, 6))
    assert str(t2) == "Tim (HP: 50, Deck: 2 cards)", f"Got: {str(t2)}"

    drawn = t2.draw_card()
    assert drawn.get_name() == "Mon1"

    # heal() restores HP, capped at starting HP
    t3 = Trainer("Nurse", 100)
    t3.take_damage(50)
    assert t3.get_health() == 50

    t3.heal(20)
    assert t3.get_health() == 70, f"After 50 damage and 20 heal, expected 70, got {t3.get_health()}"

    t3.heal(999)
    assert t3.get_health() == 100, (
        f"Heal should not exceed starting HP (100), got {t3.get_health()}"
    )

    # heal on a KO'd trainer still caps at max
    t4 = Trainer("Revive", 80)
    t4.take_damage(80)
    assert t4.get_health() == 0
    t4.heal(30)
    assert t4.get_health() == 30, f"Healing from 0 by 30 should give 30, got {t4.get_health()}"
    t4.heal(100)
    assert t4.get_health() == 80, f"Heal should cap at starting HP (80), got {t4.get_health()}"

    print("PASSED")


def test_deck_empty_error():
    print("Testing DeckEmptyError + deck empty handling...", end=" ")
    from deck_empty_error import DeckEmptyError
    from deck import Deck
    from animon import Animon

    # Test the error class format
    e = DeckEmptyError("Alex")
    assert isinstance(e, Exception), "DeckEmptyError should inherit from Exception"
    assert str(e) == "Alex's deck is empty!", f"Expected \"Alex's deck is empty!\", got \"{str(e)}\""

    e2 = DeckEmptyError("Tim")
    assert str(e2) == "Tim's deck is empty!", f"Expected \"Tim's deck is empty!\", got \"{str(e2)}\""

    # Test that Deck raises DeckEmptyError on draw from empty deck
    d = Deck("Alex")
    d.add_card(Animon("Mon", 5, 5))
    d.draw_card()
    try:
        d.draw_card()
        assert False, "Should have raised DeckEmptyError on empty deck"
    except DeckEmptyError:
        pass  # expected

    # Test that peek raises DeckEmptyError on empty deck
    d2 = Deck("Tim")
    try:
        d2.peek()
        assert False, "Should have raised DeckEmptyError on peek of empty deck"
    except DeckEmptyError:
        pass  # expected

    # Test that error message includes the owner name
    d3 = Deck("Misty")
    try:
        d3.draw_card()
    except DeckEmptyError as e:
        assert "Misty" in str(e), f"Error should mention owner name, got: {str(e)}"

    print("PASSED")


def test_arena():
    print("Testing Arena...", end=" ")
    from trainer import Trainer
    from animon import Animon, FireAnimon, WaterAnimon
    from arena import Arena

    # --- play_round format checks ---
    t1 = Trainer("Alice", 100)
    t2 = Trainer("Bob", 100)
    t1.add_card_to_deck(FireAnimon("Flamey", 10, 3))
    t2.add_card_to_deck(WaterAnimon("Splashy", 8, 5))

    arena = Arena(t1, t2)
    summary = arena.play_round(1)
    lines = summary.split("\n")

    # Line 1: "Round 1:"
    assert lines[0] == "Round 1:", (
        f"First line should be exactly 'Round 1:' but got: '{lines[0]}'"
    )

    # Line 2-3: "  Alice sends out [Fire] Flamey ..."
    assert len(lines) >= 5, (
        f"Round summary should have 5 lines separated by \\n, got {len(lines)}.\n"
        f"Full summary:\n{summary}"
    )
    assert lines[1].startswith("  "), (
        f"'sends out' lines should start with two spaces for indentation.\n"
        f"Got: '{lines[1]}'"
    )
    assert "Alice sends out" in lines[1], (
        f"Line 2 should have trainer 1 sending out, got: '{lines[1]}'"
    )
    assert "[Fire] Flamey" in lines[1], (
        f"'sends out' line should use Animon's __str__ (with type and stats).\n"
        f"Got: '{lines[1]}'"
    )
    assert "Bob sends out" in lines[2], (
        f"Line 3 should have trainer 2 sending out, got: '{lines[2]}'"
    )

    # Line 4-5: damage lines use get_name() not __str__
    assert "Flamey deals" in lines[3], (
        f"Damage line should use get_name() (just 'Flamey'), not __str__.\n"
        f"Got: '{lines[3]}'"
    )
    assert "[Fire]" not in lines[3], (
        f"Damage line should use get_name() (just the name), not __str__ (with [type]).\n"
        f"Got: '{lines[3]}'"
    )

    # Damage values: Fire vs Water = int((10-5) * 0.5) = 2, Water vs Fire = int((8-3) * 1.5) = 7
    assert "2 damage to Bob" in lines[3], (
        f"Fire vs Water: int((10-5) * 0.5) = 2 damage. Got: '{lines[3]}'"
    )
    assert "7 damage to Alice" in lines[4], (
        f"Water vs Fire: int((8-3) * 1.5) = 7 damage. Got: '{lines[4]}'"
    )

    # Line 6: HP status with pipe separator
    assert " | " in lines[5], (
        f"HP line should have ' | ' separating the two trainers.\n"
        f"Got: '{lines[5]}'"
    )
    assert "Alice: 93 HP" in lines[5], (
        f"Alice took 7 damage, should have 93 HP. Got: '{lines[5]}'"
    )
    assert "Bob: 98 HP" in lines[5], (
        f"Bob took 2 damage, should have 98 HP. Got: '{lines[5]}'"
    )

    # Battle log should contain the summary
    log = arena.get_battle_log()
    assert len(log) >= 1, "Battle log should have at least one entry after play_round"

    # --- play_game checks ---
    t3 = Trainer("Cid", 100)
    t4 = Trainer("Dawn", 100)
    t3.add_card_to_deck(Animon("A", 10, 3))
    t4.add_card_to_deck(Animon("B", 8, 5))

    arena2 = Arena(t3, t4)
    result = arena2.play_game()
    log2 = arena2.get_battle_log()
    assert len(log2) >= 2, "Battle log should have round(s) + winner/draw"
    assert "wins!" in log2[-1] or "draw" in log2[-1].lower(), (
        f"Last log entry should be a winner or draw announcement, got: '{log2[-1]}'"
    )

    # --- get_statistics checks ---
    stats = arena2.get_statistics()
    assert "Rounds played: 1" in stats, (
        f"Statistics should show 'Rounds played: 1', got:\n{stats}"
    )
    assert "Cid total damage dealt:" in stats, (
        f"Statistics should mention Cid's damage, got:\n{stats}"
    )
    assert "Dawn total damage dealt:" in stats, (
        f"Statistics should mention Dawn's damage, got:\n{stats}"
    )
    # A(10,3) vs B(8,5): damage to Dawn = max(0,10-5) = 5, damage to Cid = max(0,8-3) = 5
    assert "Cid total damage dealt: 5" in stats, (
        f"Cid should deal 5 damage (10 power - 5 defense), got:\n{stats}"
    )

    print("PASSED")


if __name__ == "__main__":
    print("=" * 40)
    print("Animon Battle Arena - Self-Test")
    print("=" * 40)
    print()

    tests = [
        ("1. Animon subclasses (tests 1.1-1.5)", test_animon_subclasses),
        ("2. Deck core + protocols (tests 1.6-1.9)", test_deck_core),
        ("3. Shuffle determinism (test 3.12)", test_seed_determinism),
        ("4. InvalidStatError (test 2.5)", test_invalid_stat_error),
        ("5. DeckFullError (test 2.8)", test_deck_full_error),
        ("6. Animon stat validation (tests 2.6-2.7)", test_animon_validation),
        ("7. Deck capacity (test 2.9)", test_deck_capacity),
        ("8. Trainer (tests 2.1-2.4)", test_trainer),
        ("9. DeckEmptyError + deck empty handling (test 3.1)", test_deck_empty_error),
        ("10. Arena (tests 3.2-3.10)", test_arena),
    ]

    passed = 0
    for name, test_fn in tests:
        try:
            test_fn()
            passed += 1
        except ImportError as e:
            print(f"SKIPPED - {e}")
            print(f"  (Implement {name} before running this test)")
            break
        except AssertionError as e:
            print(f"FAILED")
            print(f"  {e}")
            break
        except Exception as e:
            print(f"ERROR - {type(e).__name__}: {e}")
            break

    print()
    print(f"{passed}/{len(tests)} test groups passed")
    if passed == len(tests):
        print("All tests passed! Try running main.py next.")
