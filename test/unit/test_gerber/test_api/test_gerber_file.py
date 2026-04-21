from __future__ import annotations

import pytest

from pygerber.gerber.api import FileTypeEnum, GerberFile


@pytest.mark.parametrize(
    ("function_name", "expected"),
    [
        ("Copper", FileTypeEnum.COPPER),
        ("Plated", FileTypeEnum.PLATED),
        ("NonPlated", FileTypeEnum.NON_PLATED),
        ("Profile", FileTypeEnum.PROFILE),
        ("Soldermask", FileTypeEnum.SOLDERMASK),
        ("Legend", FileTypeEnum.LEGEND),
        ("Component", FileTypeEnum.COMPONENT),
        ("Paste", FileTypeEnum.PASTE),
        ("Glue", FileTypeEnum.GLUE),
        ("Carbonmask", FileTypeEnum.CARBONMASK),
        ("Goldmask", FileTypeEnum.GOLDMASK),
        ("Heatsinkmask", FileTypeEnum.HEATSINKMASK),
        ("Peelablemask", FileTypeEnum.PEELABLEMASK),
        ("Silvermask", FileTypeEnum.SILVERMASK),
        ("Tinmask", FileTypeEnum.TINMASK),
        ("Depthrout", FileTypeEnum.DEPTHROUT),
        ("Vcut", FileTypeEnum.VCUT),
        ("Viafill", FileTypeEnum.VIAFILL),
        ("Pads", FileTypeEnum.PADS),
        ("Other", FileTypeEnum.OTHER),
        ("Drillmap", FileTypeEnum.DRILLMAP),
        ("FabricationDrawing", FileTypeEnum.FABRICATIONDRAWING),
        ("Vcutmap", FileTypeEnum.VCUTMAP),
        ("AssemblyDrawing", FileTypeEnum.ASSEMBLYDRAWING),
        ("ArrayDrawing", FileTypeEnum.ARRAYDRAWING),
        ("OtherDrawing", FileTypeEnum.OTHERDRAWING),
    ],
)
def test_file_type_from_attributes(function_name: str, expected: FileTypeEnum) -> None:
    gerber = GerberFile.from_str(f"""%TF.FileFunction,{function_name}*%""")
    assert gerber.file_type == FileTypeEnum.INFER
    assert gerber._get_file_type_from_attributes() == expected


def test_file_type_from_attributes_no_file_function() -> None:
    gerber = GerberFile.from_str("G04*")
    assert gerber.file_type == FileTypeEnum.INFER
    assert gerber._get_file_type_from_attributes() == FileTypeEnum.UNDEFINED


def test_zero_step_repeat_count_rejected_during_compile() -> None:
    gerber = GerberFile.from_str(
        """%FSLAX36Y36*%
%MOIN*%
%ADD10C,0.010*%
%SRX0Y1I0.0000J0.0000*%
D10*
X0Y0D03*
%SR*%
M02*"""
    )

    with pytest.raises(ValueError, match="SR X repeat count must be at least 1"):
        gerber._get_rvmc()
