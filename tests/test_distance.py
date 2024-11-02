from __future__ import annotations

import pathlib

import numpy as np
import pytest
from legendmeta import TextDB
from legendtestdata import LegendTestData
from pyg4ometry import geant4

from legendhpges import (
    make_hpge,
)
from legendhpges.materials import make_natural_germanium

reg = geant4.Registry()
natural_germanium = make_natural_germanium(reg)
configs = TextDB(pathlib.Path(__file__).parent.resolve() / "configs")


@pytest.fixture(scope="session")
def test_data_configs():
    ldata = LegendTestData()
    ldata.checkout("5f9b368")
    return ldata.get_path("legend/metadata/hardware/detectors/germanium/diodes")


def test_not_implemented():
    reg = geant4.Registry()
    ppc = make_hpge(configs.P00664B, registry=reg)

    with pytest.raises(NotImplementedError):
        ppc.distance_to_surface([[1, 0, 0]])


def test_bad_dimensions(test_data_configs):
    reg = geant4.Registry()
    gedet = make_hpge(test_data_configs + "/C99000A.json", registry=reg)

    with pytest.raises(ValueError):
        gedet.distance_to_surface([[1, 0, 0, 0]])


def test_output(test_data_configs):
    reg = geant4.Registry()
    gedet = make_hpge(test_data_configs + "/C99000A.json", registry=reg)

    assert np.shape(
        gedet.distance_to_surface([[0, 0, 0], [1, 3, 3], [0, 0, 0]]) == (3,)
    )
    assert np.all(gedet.distance_to_surface([[0, 0, 0], [1, 3, 3], [0, 0, 0]]) >= 0)
