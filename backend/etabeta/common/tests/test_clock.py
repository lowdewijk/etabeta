from etabeta.common.Clock import Clock

def test_get_timetamp():
    clock = Clock(lambda: 123)
    assert clock.get_timestamp() == 123

def test_set_fixed_timestamp():
    clock = Clock(lambda: 123)
    clock.set_fixed_timestamp(456)
    assert clock.get_timestamp() == 456
