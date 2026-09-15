"""
test_db.py
database.py ke functions ka automatic test.
Chalane se har function check hoga aur PASS/FAIL batayega.
"""

from database import *

passed = 0
failed = 0


def test(name, actual, expected):
    """
    Helper function — actual aur expected compare karta hai.
    Match ho to PASS, warna FAIL print karta hai.
    """
    global passed, failed
    if actual == expected:
        print(f"PASS: {name}")
        passed += 1
    else:
        print(f"FAIL: {name}")
        print(f"      Expected: {expected}")
        print(f"      Actual:   {actual}")
        failed += 1


print("=" * 60)
print("DATABASE.PY — AUTOMATIC TESTS")
print("=" * 60)


# SETUP — test user banao
print("\n--- SETUP ---")
create_user("eman", "pass123")
user = get_user("eman")
print(f"Test user: {user['username']} (ID: {user['id']})")



# USER TESTS
print("\n--- USER TESTS ---")

test("New User Creation",
     create_user("ahmed", "pass456"),
     True)

test("Duplicate username check",
     create_user("eman", "different"),
     False)

test("Existing user find",
     get_user("eman")['username'],
     "eman")

test("Nonexistent user return None",
     get_user("ghost_user"),
     None)


# ============================================================
# PASSWORD TESTS
# ============================================================
print("\n--- PASSWORD TESTS ---")

test("verifying password",
     verify_password(user, "pass123"),
     True)

test("wrong password fails",
     verify_password(user, "wrongpass"),
     False)


# ============================================================
# EXPENSE TESTS
# ============================================================
print("\n--- EXPENSE TESTS ---")

# 3 expenses add karo
exp1 = add_expense(user['id'], 500.50, "Food", "Lunch", "2026-09-14")
exp2 = add_expense(user['id'], 1200.00, "Bills", "Electricity", "2026-09-13")
exp3 = add_expense(user['id'], 300.00, "Travel", "Auto fare", "2026-09-14")
exp4 = add_expense(user['id'], 600.50, "Food", "Dinner", "2026-09-14")


test("Expense add return id",
     exp1 > 0,
     True)

test("no. of expenses added",
     len(get_expenses(user['id'])),
     4)

test("Total calculation check(500.50 + 1200 + 300 + 600.50 = 2601.0)",
     get_total(user['id']),
     2601.0)

test("Single expense return",
     get_expense(exp1, user['id'])['category'],
     "Food")

test("Nonexistent expense return None",
     get_expense(9999, user['id']),
     None)


# ============================================================
# UPDATE TESTS
# ============================================================
print("\n--- UPDATE TESTS ---")

test("Existing expense update",
     update_expense(exp1, user['id'], 999.99, "Food", "Updated", "2026-09-14"),
     True)

test("Nonexistent expense update fail",
     update_expense(9999, user['id'], 100, "X", "X", "2026-01-01"),
     False)


# ============================================================
# DELETE TESTS
# ============================================================
print("\n--- DELETE TESTS ---")

test("Existing expense delete",
     delete_expense(exp1, user['id']),
     True)

test("Deleted expense cannot be deleted again",
     delete_expense(exp1, user['id']),
     False)


# ============================================================
# SECURITY TESTS — sabse important
# ============================================================
print("\n--- SECURITY TESTS ---")

# Ali banao (doosra user)
create_user("ali_security", "ali123")
ali = get_user("ali_security")

# Ali apna ek expense add kare
ali_exp = add_expense(ali['id'], 500, "Food", "Ali's lunch", "2026-09-14")

test("Doosre user ka expense update nahi hota",
     update_expense(ali_exp, user['id'], 999, "X", "Hacked", "2026-01-01"),
     False)

test("Doosre user ka expense delete nahi hota",
     delete_expense(ali_exp, user['id']),
     False)

test("Doosre user ka expense dekh nahi sakte",
     get_expense(ali_exp, user['id']),
     None)


# ============================================================
# RESULTS
# ============================================================
print("\n" + "=" * 60)
print(f"RESULTS: {passed} pass, {failed} fail")
print("=" * 60)

if failed == 0:
    print("Database.py all tests passed.")
else:
    print(f"{failed} tests FAILED - CHECK ABOVE OUTPUT FOR DETAILS.")