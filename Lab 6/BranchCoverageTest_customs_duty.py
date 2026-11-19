
import pytest
from customs_duty import duty_rate, total_duty, clearance_channel


# 1. Test all duty rate branches
@pytest.mark.parametrize("category, origin, expected", [
    ("electronics", "FTA", 0.10),
    ("electronics", "US", 0.20),
    ("clothing", "FTA", 0.05),
    ("clothing", "US", 0.12),
    ("books", "US", 0),
    ("furniture", "US", 0.15),
])
def test_all_duty_rate_branches(category, origin, expected):
    assert duty_rate(category, origin) == expected


# 2. Test both prohibited categories
@pytest.mark.parametrize("category", ["weapons", "narcotics"])
def test_each_prohibited_category(category):
    with pytest.raises(ValueError, match="prohibited item"):
        duty_rate(category, "US")


# 3. Test negative value branch
def test_negative_value_branch():
    with pytest.raises(ValueError, match="negative value"):
        total_duty("electronics", -1, "FTA", False)


# 4. Test gift threshold
def test_gift_at_threshold():
    assert total_duty("electronics", 5000, "FTA", True) == 0


# 5. Test gift above threshold
def test_gift_above_threshold():
    assert total_duty("electronics", 6000, "FTA", True) == 100


# 6. Test non-gift threshold
def test_non_gift_at_threshold():
    assert total_duty("electronics", 1000, "FTA", False) == 0


# 7. Test minimum duty branch
def test_gift_triggers_minimum_duty():
    assert total_duty("clothing", 5500, "FTA", True) == 50


# 8. Test duty exactly equal to 50
def test_duty_exactly_fifty_does_not_need_minimum_adjustment():
    assert total_duty("clothing", 6000, "FTA", True) == 50


# 9. Test duty greater than 50
def test_duty_greater_than_fifty():
    assert total_duty("electronics", 2000, "US", False) == 400


# 10. Test prohibited item clearance
def test_clearance_prohibited_branch():
    assert clearance_channel(100, "weapons", True) == "refuse"


# 11. Test value greater than 100000
def test_clearance_value_over_100000_branch():
    assert clearance_channel(100001, "books", True) == "inspect"


# 12. Test value exactly 100000
def test_clearance_value_at_100000_with_documents():
    assert clearance_channel(100000, "books", True) == "green"


# 13. Test value above 20000 without documents
def test_clearance_over_20000_without_documents():
    assert clearance_channel(20001, "books", False) == "inspect"


# 14. Test value above 20000 with documents
def test_clearance_over_20000_with_documents():
    assert clearance_channel(20001, "books", True) == "green"


# 15. Test value exactly 20000 without documents
def test_clearance_at_20000_without_documents():
    assert clearance_channel(20000, "books", False) == "green"
