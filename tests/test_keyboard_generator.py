from utils.keyboard_generators import GeneratorKb


def test_structure_generate_for_choose_period():
    builder = GeneratorKb.generate_for_choose_period()
    keyboard = builder.as_markup().inline_keyboard
    assert len(keyboard) == 3
    assert len(keyboard[0]) == 2
    assert len(keyboard[1]) == 1
    assert len(keyboard[2]) == 2
    assert keyboard[0][0].callback_data.startswith('period_')


def test_structure_generate_years():
    builder = GeneratorKb.generate_years(['2022', '2021', '2020'])
    keyboard = builder.as_markup().inline_keyboard
    assert len(keyboard) == 2
    assert len(keyboard[0]) == 2
    assert len(keyboard[1]) == 1
    assert keyboard[0][0].callback_data.startswith('all_periods_year_')


def test_structure_generate_months():
    builder = GeneratorKb.generate_months(['02', '05', '08', '11', '12'])
    keyboard = builder.as_markup().inline_keyboard
    assert len(keyboard) == 3
    assert len(keyboard[0]) == 2
    assert len(keyboard[1]) == 2
    assert len(keyboard[2]) == 1
    assert keyboard[0][0].callback_data.startswith('all_periods_month_')
