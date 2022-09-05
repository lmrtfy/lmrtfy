#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lmrtfy import  variable, result


def compound_interest(principal: float, annual_interest: float, years: int):
    """
    Compute the compound interest for `years` when starting from `principal` with `annual interest`.

    compound interest = principal * (1 + annual_interest)^years - principal

    """

    return principal * (1. + annual_interest/100.)**years - principal


if __name__ == "__main__":
    ci = result(
            compound_interest(
                principal=variable(10000., name="principal", min=0),
                annual_interest=variable(0.06, name="annual_interest", min=0, max=100, unit="%"),
                years=variable(10, name="years", min=0)
            ),
            name="compound_interest"
    )