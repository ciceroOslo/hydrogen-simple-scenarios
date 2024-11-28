"""
Chemistry related help functions
"""

molar_mass_dict = {"H": 1.00784, "O": 15.999, "C": 12.011, "N": 14.0067}


def calculate_molar_mass_from_name_recursive(name_str, sum_so_far=0):
    """
    Calculate molar mass of chemical compound

    Method recursively works from the end of a formula

    Parameters
    ----------
    name_str : str
        Chemical formula yet to be considered
    sum_so_far: dict
        Sum of atoms of molar mass found so far

    Returns
    -------
    int
        The molar_mass for the formula for what has already been
        considered, what is considered here, and what is yet to be considered
    """
    count = 1
    len_cut = 1
    if name_str[-1].isdigit():
        count = count * int(name_str[-1])
        if name_str[-2].isdigit():
            count = count + 10 * int(name_str[-2])
            comp = name_str[-3]
            len_cut = 3
        else:
            comp = name_str[-2]
            len_cut = 2
    else:
        comp = name_str[-1]
    sum_so_far = sum_so_far + molar_mass_dict[comp] * count
    if len(name_str) <= len_cut:
        return sum_so_far
    return calculate_molar_mass_from_name_recursive(
        name_str[:-len_cut], sum_so_far=sum_so_far
    )


def calculate_number_of_atom_in_compound(name_str, atom_letter="N", sum_so_far=0):
    """
    Calculate number of atoms of a specific type in a chemical formula

    Method recursively works from the end of a formula

    Parameters
    ----------
    name_str : str
        Chemical formula yet to be considered
    atom_letter : char
        The chemical symbol of the atom to count
    sum_so_far: dict
        Sum of atoms of this kind found so far

    Returns
    -------
    int
        The sum of atoms of atom_letter for the formula for what has already been
        considered, what is considered here, and what is yet to be considered
    """
    count = 1
    len_cut = 1
    if name_str[-1].isdigit():
        count = count * int(name_str[-1])
        if name_str[-2].isdigit():
            count = count + 10 * int(name_str[-2])
            comp = name_str[-3]
            len_cut = 3
        else:
            comp = name_str[-2]
            len_cut = 2
    else:
        comp = name_str[-1]
    if comp == atom_letter:
        sum_so_far = sum_so_far + count
    if len(name_str) <= len_cut:
        return sum_so_far
    return calculate_number_of_atom_in_compound(
        name_str[:-len_cut], atom_letter=atom_letter, sum_so_far=sum_so_far
    )


def make_dict_of_atoms_and_numbers_in_formula(name_str, dict_so_far=None):
    """
    Make dictionary of atoms and their numbers from chemical formula

    Method recursively works from the end of a formula

    Parameters
    ----------
    name_str : str
        Chemical formula yet to be considered
    dict_so_far: dict
        Dictionary of the result from running through the parts of the
        formula in the parts of the string already considered

    Returns
    -------
    dict
        The full dictionary for the formula for what has already been
        considered, what is considered here, and what is yet to be considered
    """
    count = 1
    len_cut = 1
    if dict_so_far is None:
        dict_so_far = {}
    if name_str[-1].isdigit():
        count = count * int(name_str[-1])
        if name_str[-2].isdigit():
            count = count + 10 * int(name_str[-2])
            comp = name_str[-3]
            len_cut = 3
        else:
            comp = name_str[-2]
            len_cut = 2
    else:
        comp = name_str[-1]
    if comp in dict_so_far:
        dict_so_far[comp] = dict_so_far[comp] + count
    else:
        dict_so_far[comp] = count
    if len(name_str) <= len_cut:
        return dict_so_far
    return make_dict_of_atoms_and_numbers_in_formula(
        name_str[:-len_cut], dict_so_far=dict_so_far
    )


def calculate_mass_conversion_fraction(comp, total_unit="H2"):
    """
    Calculate a mass conversion fraction between two species

    Finding first the ratio between the comp and the total_unit
    species in a chemical reaction from one to the other and
    then multiplying that by the ratio of their molar masses

    Parameters
    ----------
    comp : str
        Chemical formula for the target compound
    total_unit : str
        CHemical formula for the original unit

    Returns
    -------
    float
        conversion number between mass of one species to the other
        to calculate leakage emissions
    """
    total_mm = calculate_molar_mass_from_name_recursive(total_unit)
    comp_mm = calculate_molar_mass_from_name_recursive(comp)
    dict_tunit = make_dict_of_atoms_and_numbers_in_formula(total_unit)
    dict_comp = make_dict_of_atoms_and_numbers_in_formula(comp)
    shared_keys = list(set(dict_tunit).intersection(dict_comp))
    if len(shared_keys) != 1:
        print(f"What to do with shared_keys {shared_keys}?")
        fraction = 1
    else:
        fraction = (
            dict_comp[shared_keys[0]] / dict_tunit[shared_keys[0]] * comp_mm / total_mm
        )
    return fraction
