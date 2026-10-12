"""Tests for the anylogic-model-builder skill: the .alp generator and the file checker.

Generator tests need the local template cache (built from the user's AnyLogic install by alp_templates.py);
they are skipped on machines without it. The checker tests run everywhere.
"""
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[2] / ".claude" / "skills" / "anylogic-model-builder" / "scripts"
sys.path.insert(0, str(SKILL))
import verify_alp  # noqa: E402

HAS_CACHE = (SKILL.parent / ".cache" / "templates.json").is_file()
needs_cache = pytest.mark.skipif(not HAS_CACHE, reason="template cache not built on this machine")


def tiny_model():
    from alp_builder import AlpModel
    m = AlpModel("Tiny Queue", "tiny_queue", time_unit="Minute")
    m.agent_type("Customer", figure="person")
    m.parameter("rate", "double", "6", "Arrivals per hour", 20, 300)
    m.block("Source", "source", 20, 90, {"rate": m.unit("rate", "RateUnits", "PER_HOUR"),
                                         "newEntity": m.entity("Customer")}, agent="Customer")
    m.block("Delay", "service", 120, 80, {"delayTime": m.unit("exponential(1.0/5)", "TimeUnits", "MINUTE")},
            agent="Customer")
    m.block("Sink", "sink", 220, 90, agent="Customer")
    m.connect("source", "out", "service")
    m.connect("service", "out", "sink")
    m.shape(m.rect("floor", 0, 0, 300, 200, m.rgb(220, 220, 220)))
    return m


@needs_cache
def test_generated_model_passes_the_file_checks(tmp_path):
    path = tiny_model().write(tmp_path)
    problems, notes = verify_alp.check(path)
    assert problems == []
    root = ET.parse(path).getroot()
    assert [c.find("Name").text for c in root.find("Model/ActiveObjectClasses")] == ["Main", "Customer"]
    assert (tmp_path / "3d" / "person.dae").is_file()


@needs_cache
def test_unknown_block_parameter_is_refused():
    from alp_builder import AlpModel
    m = AlpModel("X", "x")
    with pytest.raises(KeyError, match="unknown parameters"):
        m.block("Delay", "d", 0, 0, {"delayTme": m.code("1")})


@needs_cache
def test_write_refuses_when_autosave_is_newer(tmp_path):
    import os
    import time
    m = tiny_model()
    path = m.write(tmp_path)
    auto = path.with_name(path.name + ".autosave")
    auto.write_text("stale")
    os.utime(auto, (time.time() + 60, time.time() + 60))
    with pytest.raises(SystemExit, match="autosave"):
        tiny_model().write(tmp_path)


def test_checker_flags_absolute_paths_and_ignores_parameter_value_references(tmp_path):
    alp = tmp_path / "m.alp"
    alp.write_text("""<?xml version="1.0" encoding="UTF-8"?>
<AnyLogicWorkspace AlpVersion="8.9.6"><Model><ActiveObjectClasses><ActiveObjectClass><Name>Main</Name>
<Variables><Variable Class="Parameter"><Id>11</Id></Variable></Variables>
<StartupCode><![CDATA[new java.io.FileReader("C:/Users/someone/OneDrive/Desktop/a/very/long/folder/name/data.csv");]]></StartupCode>
</ActiveObjectClass></ActiveObjectClasses>
<Experiments><ParamVariationExperiment><FreeformParamValue><Id>11</Id></FreeformParamValue></ParamVariationExperiment></Experiments>
</Model></AnyLogicWorkspace>""", encoding="utf-8")
    problems, _ = verify_alp.check(alp)
    assert any("absolute path" in p for p in problems)
    assert not any("duplicate ids" in p for p in problems)
