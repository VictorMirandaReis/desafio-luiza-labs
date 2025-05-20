import io
import pytest
from unittest.mock import MagicMock
from src.core.order.create_from_file import OrderFileProcessor
from src.db.models import User, Order, OrderProduct

@pytest.fixture
def db_session():
    return MagicMock()

@pytest.fixture
def processor(db_session):
    return OrderFileProcessor(db_session)

@pytest.fixture
def valid_line():
    return (
        "0000000123" +
        "João da Silva".ljust(45) +
        "0000000456" +
        "0000000789" +
        "000000012.34" +
        "20240501"
    )

@pytest.fixture
def line_short():
    return "invalida".encode()

@pytest.fixture
def line_empty():
    return b"\n"

@pytest.fixture
def line_invalid_price():
    return (
        "0000000123" +
        "Nome Teste".ljust(45) +
        "0000000456" +
        "0000000789" +
        "00INVALIDO12" +
        "20240501"
    )

@pytest.fixture
def line_negative_price():
    return (
        "0000000123" +
        "Nome Negativo".ljust(45) +
        "0000000456" +
        "0000000789" +
        "-00000012.00" +
        "20240501"
    )


@pytest.fixture
def line_invalid_date():
    return (
        "0000000123" +
        "Nome Data".ljust(45) +
        "0000000456" +
        "0000000789" +
        "000000012.00" +
        "20241399"
    )


@pytest.fixture
def line_empty_name():
    return (
        "0000000123" +
        "".ljust(45) +
        "0000000456" +
        "0000000789" +
        "000000012.00" +
        "20240501"
    )


@pytest.fixture
def line_invalid_user_id():
    return (
        "ABC0000123" +
        "Nome Teste".ljust(45) +
        "0000000456" +
        "0000000789" +
        "000000012.00" +
        "20240501"
    )


def make_dummy_file(*lines):
    content = "\n".join(lines).encode()
    class DummyFile:
        file = io.BytesIO(content)
    return DummyFile()

def test_valid_line_creates_order(processor, valid_line, db_session):
    db_session.execute.return_value.scalars.return_value.first.side_effect = [None, None, None]
    db_session.flush.side_effect = lambda: None

    file = make_dummy_file(valid_line)
    created, errors = processor.create_from_file(file)

    assert created == 1
    assert errors == 0


def test_short_line_raises_exception(processor, db_session):
    file = make_dummy_file("linha_curta")
    with pytest.raises(Exception, match="Line 1 too short or None"):
        processor.create_from_file(file)


def test_empty_line_is_ignored(processor, valid_line, db_session):
    db_session.execute.return_value.scalars.return_value.first.side_effect = [None, None, None]
    file = make_dummy_file("", valid_line)

    created, errors = processor.create_from_file(file)
    assert created == 1
    assert errors == 0


def test_invalid_price_is_counted_as_error(processor, line_invalid_price, db_session):
    file = make_dummy_file(line_invalid_price)
    created, errors = processor.create_from_file(file)
    assert created == 0
    assert errors == 1


def test_negative_price_is_counted_as_error(processor, line_negative_price):
    file = make_dummy_file(line_negative_price)
    created, errors = processor.create_from_file(file)
    assert created == 0
    assert errors == 1


def test_invalid_date_is_counted_as_error(processor, line_invalid_date):
    file = make_dummy_file(line_invalid_date)
    created, errors = processor.create_from_file(file)
    assert created == 0
    assert errors == 1


def test_empty_name_is_counted_as_error(processor, line_empty_name):
    file = make_dummy_file(line_empty_name)
    created, errors = processor.create_from_file(file)
    assert created == 0
    assert errors == 1


def test_invalid_user_id_is_counted_as_error(processor, line_invalid_user_id):
    file = make_dummy_file(line_invalid_user_id)
    created, errors = processor.create_from_file(file)
    assert created == 0
    assert errors == 1


def test_existing_user_and_order_does_not_create_twice(processor, valid_line, db_session):
    db_session.execute.return_value.scalars.return_value.first.side_effect = [
        User(id=1), Order(id=1), OrderProduct(id=1)
    ]
    file = make_dummy_file(valid_line)
    created, errors = processor.create_from_file(file)
    assert created == 0
    assert errors == 0


def test_multiple_lines_some_valid_some_invalid(processor, valid_line, line_invalid_price, db_session):
    db_session.execute.return_value.scalars.return_value.first.side_effect = [
        None, None, None,
        None, None, None
    ]
    file = make_dummy_file(valid_line, line_invalid_price, "", valid_line)
    created, errors = processor.create_from_file(file)
    assert created == 2
    assert errors == 1