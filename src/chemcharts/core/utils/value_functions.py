from chemcharts.core.utils.enums import PlottingEnum
_PE = PlottingEnum


def generate_value(chemdata_list, parameters: dict, idx: int = None) -> tuple:
    value_input = chemdata_list.get_values() if idx is None else chemdata_list[idx].get_values()
    value_column_input = parameters.get(_PE.PARAMETERS_VALUECOLUMN, None)
    if value_column_input is None or value_column_input not in list(value_input):
        raise ValueError(f"No values specified (3rd dimension) so generation of "
                         f"{parameters.get(_PE.PARAMETERS_PLOT_TITLE, '<no plot title given>')} "
                         f"is not possible.")
    value_column = value_input[value_column_input]
    value_name = parameters.get(_PE.PARAMETERS_VALUENAME, "Value")

    return value_column, value_name
