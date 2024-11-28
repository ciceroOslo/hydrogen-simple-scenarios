import numpy as np

from hydrogen_simple_scenarios import chem_help_functions


def test_calculate_molar_mass_from_name_recursive():
    assert np.allclose(
        chem_help_functions.calculate_molar_mass_from_name_recursive("H2"), 2 * 1.00784
    )
    assert np.allclose(
        chem_help_functions.calculate_molar_mass_from_name_recursive("CO2"),
        44.01,
        atol=1e-2,
    )
    assert np.allclose(
        chem_help_functions.calculate_molar_mass_from_name_recursive("CH4"),
        16.04,
        atol=1e-2,
    )
    assert np.allclose(
        chem_help_functions.calculate_molar_mass_from_name_recursive("NH3"),
        17.031,
        atol=1e-2,
    )
    assert np.allclose(
        chem_help_functions.calculate_molar_mass_from_name_recursive("C6H12O6"),
        180.156,
        atol=1e-3,
    )


def test_calculate_number_of_atom_in_compound():
    assert chem_help_functions.calculate_number_of_atom_in_compound("H2") == 0
    assert (
        chem_help_functions.calculate_number_of_atom_in_compound("CO2", atom_letter="C")
        == 1
    )
    assert chem_help_functions.calculate_number_of_atom_in_compound("N2O") == 2
    assert chem_help_functions.calculate_number_of_atom_in_compound("CH3COOH", "O") == 2
    assert chem_help_functions.calculate_number_of_atom_in_compound("CH3COOH") == 0
    assert chem_help_functions.calculate_number_of_atom_in_compound("CH3COOH", "H") == 4
    assert chem_help_functions.calculate_number_of_atom_in_compound("CH3COOH", "C") == 2
    assert (
        chem_help_functions.calculate_number_of_atom_in_compound("C6H12O6", "H") == 12
    )


def test_make_dict_of_atoms_and_numbers_in_formula():
    h2_dict = chem_help_functions.make_dict_of_atoms_and_numbers_in_formula("H2")
    nh3_dict = chem_help_functions.make_dict_of_atoms_and_numbers_in_formula("NH3")
    acetic_acid_dict = chem_help_functions.make_dict_of_atoms_and_numbers_in_formula(
        "CH3COOH"
    )
    assert len(h2_dict) == 1
    assert len(nh3_dict) == 2
    assert len(acetic_acid_dict) == 3
    assert set(h2_dict.keys()) == set(["H"])
    assert set(nh3_dict.keys()) == set(["H", "N"])
    assert set(acetic_acid_dict.keys()) == set(["H", "O", "C"])
    assert h2_dict["H"] == 2
    assert nh3_dict["H"] == 3
    assert nh3_dict["N"] == 1
    assert acetic_acid_dict["C"] == 2
    assert acetic_acid_dict["O"] == 2
    assert acetic_acid_dict["H"] == 4
    assert (
        chem_help_functions.make_dict_of_atoms_and_numbers_in_formula("C6H12O6")["H"]
        == 12
    )


def test_calculate_mass_conversion_fraction():
    print(4.0 / (3.0 * 17))
    assert np.allclose(
        chem_help_functions.calculate_mass_conversion_fraction("H2", "NH3"),
        4.0 / (3.0 * 17),
        rtol=1e-2,
    )
    assert chem_help_functions.calculate_mass_conversion_fraction("CO2", "H2") == 1
    assert chem_help_functions.calculate_mass_conversion_fraction("H2", "H2") == 1
