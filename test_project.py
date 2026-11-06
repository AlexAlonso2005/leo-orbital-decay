import pytest
from project import (
    get_ballistic_coefficient,
    get_density,
    get_deorbit_deltav,
    simulate_decay,
)

def test_get_ballistic_coefficient():
    assert get_ballistic_coefficient(10, 2, 2.5) == 2.0
    assert get_ballistic_coefficient(4, 0.04, 2.0) == 50.0
    with pytest.raises(ValueError):
        get_ballistic_coefficient(-6, 2, 2.2)
    with pytest.raises(ValueError):
        get_ballistic_coefficient(6, 0, 2.2)

def test_get_density():
    assert get_density(120000) == pytest.approx(2.0e-8)
    assert get_density(250000) == pytest.approx(6.0e-11)
    assert get_density(450000) == pytest.approx(7.0e-13)
    with pytest.raises(ValueError):
        get_density(50000)
    with pytest.raises(ValueError):
        get_density(1300000)

def test_get_deorbit_deltav():
    assert get_deorbit_deltav(400000) == pytest.approx(81.55, rel=1e-2)
    with pytest.raises(ValueError):
        get_deorbit_deltav(90000)
    with pytest.raises(ValueError):
        get_deorbit_deltav(1300000)

def test_simulate_decay():
    years, days_list, alt_list = simulate_decay(300000, 50)
    assert years > 0
    assert alt_list[-1] == 120000.0
    assert len(days_list) == len(alt_list)
    with pytest.raises(ValueError):
        simulate_decay(300000, -20)
    with pytest.raises(ValueError):
        simulate_decay(90000, 50)
