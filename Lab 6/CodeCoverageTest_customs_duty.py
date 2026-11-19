
import pytest
from customs_duty import duty_rate, total_duty, clearance_channel


# 1. Test all duty rate categories and origins
@pytest.mark.parametrize("category, origin, expected", [
    ("electronics", "FTA", 0.10),
    ("electronics", "US", 0.20),
    ("clothing", "FTA", 0.05),
    ("clothing", "US", 0.12),
    ("books", "US", 0),
    ("furniture", "US", 0.15),
])
def test_duty_rate_categories(category, origin, expected):
    assert duty_rate(category, origin) == expected


# 2. Test prohibited items
def test_prohibited_item_raises_error():
    with pytest.raises(ValueError, match="prohibited item"):
        duty_rate("weapons", "US")


# 3. Test negative declared value
def test_negative_value_raises_error():
    with pytest.raises(ValueError, match="negative value"):
        total_duty("books", -1, "US", False)


# 4. Test gift exemption
def test_low_value_gift_is_duty_free():
    assert total_duty("electronics", 5000, "US", True) == 0


# 5. Test gift above exemption limit
def test_high_value_gift_calculates_duty():
    assert total_duty("electronics", 6000, "FTA", True) == 100


# 6. Test non-gift exemption
def test_low_value_non_gift_is_duty_free():
    assert total_duty("electronics", 1000, "US", False) == 0


# 7. Test minimum duty
def test_minimum_duty_applies():
    assert total_duty("clothing", 5500, "FTA", True) == 50


# 8. Test prohibited item clearance
def test_clearance_refuses_prohibited_items():
    assert clearance_channel(100, "narcotics", True) == "refuse"


# 9. Test high-value item inspection
def test_clearance_inspects_high_value_items():
    assert clearance_channel(100001, "books", True) == "inspect"


# 10. Test inspection due to missing documents
def test_clearance_inspects_missing_documents():
    assert clearance_channel(20001, "books", False) == "inspect"


# 11. Test green clearance
def test_clearance_allows_valid_low_value_item():
    assert clearance_channel(20000, "books", True) == "green"
