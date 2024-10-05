import pytest

from server.utils.text import camel_to_snake


@pytest.mark.parametrize(
    ["input_text", "output_text"],
    [
        ["Example", "example"],
        ["SecondExample", "second_example"],
        ["", ""],
    ],
)
def test_camel_to_snake_works_sufficiently(input_text: str, output_text: str):
    assert camel_to_snake(input_text) == output_text
