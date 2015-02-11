import enum

import numpy as np
from pygenie import init; init._make_initialized()
from pygenie.lib import check_for_error
from pygenie.lib.params._par_type import PARAM_GENERATOR, Parameter, ParamAliasBase


class ParamAlias(ParamAliasBase):

    NUMBER_OF_CHANNELS = "L_CHANNELS"
    TIME_LIVE = "X_ELIVE"
    TIME_REAL = "X_EREAL"


class SampleDescription(ParamAliasBase):

    TITLE = "T_STITLE"
    ID = "T_SIDENT"

    DESCRIPTION = PARAM_GENERATOR.get_serial_parametr("T_SDESC{}")

class EnergyCalibration(ParamAliasBase):

    TYPE = "T_ECALTYPE"
    UNIT = "T_ECALUNITS"

    TERMS = "L_ECALTERMS"

    # Next we assume that calibration has form:
    # \Sum_{i=0..N} n_i * x^0
    POLYNOMIAL_N0 = "F_ECOFFSET"
    POLYNOMIAL_N1 = "F_ECSLOPE"
    POLYNOMIAL_N2 = "F_ECQUAD"
    POLYNOMIAL_N3 = "F_ECALFAC1"
    POLYNOMIAL_N4 = "F_ECALFAC2"
    POLYNOMIAL_N5 = "F_ECALFAC3"

    POLY_COEFFS = PARAM_GENERATOR.get_composite_parameter(
        ['F_ECOFFSET', 'F_ECSLOPE', 'F_ECQUAD', 'F_ECALFAC1',
         'F_ECALFAC2', 'F_ECALFAC3'])

_CALIBRATION_PARAMS = [
    EnergyCalibration.POLYNOMIAL_N0,

]


def get_parameter(dsc, parameter, record=1, entry=1):
    """
    A wrapper to SadGetParam
    :param dsc: Object obtained from create_vdm_connection
    :param parameter: Instance of ParamEnum or ParamAlias
    :param record: This is 1 based as in S650 library
    :param entry:
    :return:
    """
    if isinstance(parameter, ParamAliasBase):
        parameter = parameter.param
    pvalue = parameter.type.from_python()
    check_for_error(dsc, init.SAD_LIB.SadGetParam(
        dsc, parameter.id, record, entry,
        pvalue,
        parameter.type.get_field_size_in_bytes()))
    return parameter.type.to_python(pvalue)


def set_parameter(dsc, parameter, value,  record=1, entry=1):
    if isinstance(parameter, ParamAliasBase):
        parameter = parameter.param
    pvalue = parameter.type.from_python(value)
    check_for_error(dsc, init.SAD_LIB.SadPutParam(
        dsc, parameter.id, record, entry,
        pvalue,
        parameter.type.get_field_size_in_bytes()))

def get_calibration(dsc):
    calibration_type  = get_parameter(dsc, EnergyCalibration.TYPE)
    if calibration_type != b"POLY":
        raise ValueError(
            "We can only interpret polynomial calibration. Calibration type used was {}".format(calibration_type))

    degree = get_parameter(dsc, EnergyCalibration.TERMS)
    params = [
        get_parameter(dsc, par) for ii, par in zip(range(degree), EnergyCalibration.POLY_COEFFS)
    ]

    calibration_poly = np.asarray(list(reversed(params)))
    return calibration_poly

