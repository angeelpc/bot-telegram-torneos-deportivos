import pytest
from services.bracket_service import bracket_service

def test_get_next_power_of_2():
    assert bracket_service.get_next_power_of_2(2) == 2
    assert bracket_service.get_next_power_of_2(3) == 4
    assert bracket_service.get_next_power_of_2(4) == 4
    assert bracket_service.get_next_power_of_2(5) == 8
    assert bracket_service.get_next_power_of_2(10) == 16
    assert bracket_service.get_next_power_of_2(32) == 32

def test_get_round_name():
    assert bracket_service.get_round_name(4, 4) == "Final"
    assert bracket_service.get_round_name(3, 4) == "Semifinal"
    assert bracket_service.get_round_name(2, 4) == "Cuartos de final"
    assert bracket_service.get_round_name(1, 4) == "Octavos de final"
    
    # Para 32 equipos (5 rondas)
    assert bracket_service.get_round_name(1, 5) == "Ronda 1"
    assert bracket_service.get_round_name(2, 5) == "Octavos de final"
