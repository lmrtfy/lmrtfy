#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lmrtfy.annotation import variable, result


def compound_interest(principal: float, annual_interest: float, years: int):
    """
    Compute the compound interest for `years` when starting from `principal` with `annual interest`.

    compound interest = principal * (1 + annual_interest)^years - principal

    """

    return principal * (1. + annual_interest/100.)**years - principal


if __name__ == "__main__":
    principal = variable(10000., name="principal", min=0)
    annual_interest = variable(6.0, name="annual_interest", min=0, max=100, unit="%")
    years = variable(10, name="years", min=0)

    ci = result(compound_interest(principal, annual_interest, years), name="compound_interest")
