"""$INSUNITS codes map to millimetre scale factors, with unknown units returning None."""

from drawing_analyzer.dxf.units import millimetres_per_unit


def test_supported_units_map_to_millimetres() -> None:
    assert millimetres_per_unit(4) == 1.0  # millimetres
    assert millimetres_per_unit(6) == 1000.0  # metres
    assert millimetres_per_unit(5) == 10.0  # centimetres
    assert millimetres_per_unit(1) == 25.4  # inches
    assert millimetres_per_unit(2) == 304.8  # feet


def test_unitless_and_unknown_codes_return_none() -> None:
    assert millimetres_per_unit(0) is None  # unitless
    assert millimetres_per_unit(999) is None  # not a real code
