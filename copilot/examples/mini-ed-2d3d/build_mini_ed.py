"""Mini emergency department in 2D and 3D - generated AnyLogic model (reproducible example).

    python build_mini_ed.py [output folder]       # default: Desktop\\AnyLogic demos\\Mini ED 2D-3D

Patients arrive at the entrance, wait, are triaged by a nurse, wait again, are treated by a doctor in a bed
bay, then are admitted to a ward (25 %) or go home. They walk between areas in 2D and 3D. A dashboard shows
live counts, a time plot of the queues and staff utilisation. See brief.md for the assumptions.
Needs the template cache: python ../../../.claude/skills/anylogic-model-builder/scripts/alp_templates.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / ".claude" / "skills" / "anylogic-model-builder" / "scripts"))
from alp_builder import AlpModel  # noqa: E402

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "Documents" / "AnyLogic demos" / "Mini ED 2D-3D"

m = AlpModel("Mini ED 2D-3D", "mini_ed", time_unit="Minute")
m.agent_type("Patient", usage="ENTITY", figure="person")
m.agent_type("Nurse", usage="RESOURCE_UNIT", figure="nurse")
m.agent_type("Doctor", usage="RESOURCE_UNIT", figure="doctor")
rgb = m.rgb
GREY, WALL = rgb(220, 220, 220), rgb(245, 245, 245)
BLUE, GREEN, YELLOW, PINK, DARK = rgb(198, 226, 255), rgb(204, 235, 197), rgb(255, 242, 204), rgb(250, 218, 221), rgb(40, 60, 90)

# ---- floor plan (10 px = 1 m; building 47 m x 29 m at x 80-550, y 70-360)
m.shape(m.rect("buildingFloor", 80, 70, 470, 290, GREY, z=0, zh=1))
for nm, x, y, w, h, c in [("waitingRoomFloor", 120, 85, 140, 120, BLUE), ("triageFloor", 280, 85, 120, 120, GREEN),
                          ("doctorsFloor", 420, 85, 115, 120, YELLOW), ("doctorWaitingFloor", 120, 225, 140, 120, BLUE),
                          ("treatmentFloor", 280, 225, 255, 120, PINK)]:
    m.shape(m.rect(nm, x, y, w, h, c, z=1, zh=1))
# perimeter walls 1.2 m high, with gaps: entrance (left, y 200-235), exit (left, y 315-345), wards (right, y 270-300)
for i, (x, y, w, h) in enumerate([(80, 70, 470, 2), (80, 358, 470, 2), (80, 70, 2, 130), (80, 235, 2, 80),
                                  (80, 345, 2, 15), (548, 70, 2, 200), (548, 300, 2, 60)]):
    m.shape(m.rect(f"wall{i + 1}", x, y, w, h, WALL, z=0, zh=12, line=rgb(160, 160, 160)))
for nm, x, y, s in [("lblWaiting", 124, 88, "Waiting room (triage)"), ("lblTriage", 284, 88, "Triage"),
                    ("lblDoctors", 424, 88, "Doctors"), ("lblDocWaiting", 124, 228, "Waiting room (doctor)"),
                    ("lblTreatment", 284, 228, "Treatment bays"), ("lblEntrance", 22, 222, "Entrance"),
                    ("lblExit", 30, 350, "Exit"), ("lblWards", 554, 262, "To wards")]:
    m.shape(m.text(nm, x, y, s, size=10))

# ---- space markup: where agents are placed (nodes are invisible at run time; the floors show the rooms)
m.shape(m.point_node("entrance", 95, 217))
m.shape(m.point_node("exitHome", 65, 330))
m.shape(m.point_node("exitWard", 570, 285))
m.shape(m.rect_node("triageWaiting", 130, 100, 120, 95))
m.shape(m.rect_node("triageRoom", 290, 100, 100, 45, [(315, 125, 90.0), (365, 125, 90.0)]))
m.shape(m.rect_node("nurseHome", 290, 155, 100, 45, [(315, 180, 270.0), (365, 180, 270.0)]))
m.shape(m.rect_node("doctorHome", 430, 100, 95, 95, [(450, 125), (500, 125), (450, 172), (500, 172)]))
m.shape(m.rect_node("doctorWaiting", 130, 240, 120, 95))
BEDS = [318, 373, 428, 483]
m.shape(m.rect_node("treatmentBeds", 290, 240, 235, 95, [(bx, 310, 270.0) for bx in BEDS]))

# ---- 3D furniture from AnyLogic's library
k = 0
for yy in (120, 165, 260, 305):
    for xx in (145, 170, 195, 220, 245):
        k += 1
        m.shape(m.figure3d(f"chair{k}", "chair", xx, yy, rotation=180.0))
for i, xx in enumerate((315, 365)):
    m.shape(m.figure3d(f"triageDesk{i + 1}", "table", xx, 152))
    m.shape(m.figure3d(f"triageComputer{i + 1}", "computer_on", xx, 152, z=7.5))
m.shape(m.figure3d("doctorsDesk", "table", 475, 148))
m.shape(m.figure3d("doctorsComputer", "computer_on", 475, 148, z=7.5))
for i, bx in enumerate(BEDS):
    m.shape(m.figure3d(f"bed{i + 1}", "bed", bx, 275, rotation=90.0))
m.shape(m.figure3d("ambulance", "ambulance_car", 40, 140, rotation=90.0))

# ---- 3D view next to the floor plan, and the dashboard
m.shape(m.camera("camera", 315, 560, 280, 38.0, -90.0))
m.shape(m.window3d("window3d", 620, 70, 460, 290, "camera"))
m.shape(m.text("title", 20, 10, "Mini Emergency Department: 2D floor plan and 3D view", size=18, color=DARK, bold=True))
m.shape(m.text("clock", 860, 14, "clock", size=14, color=DARK,
               dyn='"Day " + (int)(time() / 1440 + 1) + ", " + String.format("%02d:%02d", (int)(time() % 1440 / 60), (int)(time() % 60))'))
m.shape(m.text("kpis", 20, 44, "kpis", size=12, color=rgb(30, 30, 30),
               dyn='"Arrived " + source.count() + "   |   waiting for triage " + seizeNurse.size()'
                   ' + "   |   waiting for a doctor " + seizeDoctor.size() + "   |   in treatment " + treatment.size()'
                   ' + "   |   admitted " + toWard.count() + "   |   gone home " + toHome.count()'
                   ' + "   |   average time in ED " + (timeOut.distribution.count() > 0'
                   ' ? String.format("%.0f min", timeOut.distribution.mean()) : "-")'))
m.shape(m.time_plot("queuePlot", 20, 375, 580, 190, [
    ("Waiting for triage", "dsWaitTriage", "seizeNurse.size()", rgb(30, 110, 220)),
    ("Waiting for a doctor", "dsWaitDoctor", "seizeDoctor.size()", rgb(235, 120, 20)),
    ("In treatment", "dsInTreatment", "treatment.size()", rgb(40, 160, 70))], window=12))
m.shape(m.bar_chart("staffChart", 620, 375, 460, 190, [
    ("Nurses busy (share of time)", "nurses.utilization()", rgb(40, 160, 70)),
    ("Doctors busy (share of time)", "doctors.utilization()", rgb(235, 120, 20))]))

# ---- parameters and the process flowchart (below the visible dashboard)
m.parameter("arrivalRate", "double", "8", "Patients arriving per hour", 20, 830)
m.parameter("numNurses", "int", "2", "Triage nurses", 220, 830)
m.parameter("numDoctors", "int", "4", "Doctors", 420, 830)
m.parameter("admitProbability", "double", "0.25", "Share admitted to a ward", 620, 830)
node = lambda n: {"destinationType": m.code("self.DEST_NODE"), "destinationNode": m.code(n), "straightMovement": m.code("true")}
flow = [
    ("Source", "source", {"rate": m.unit("arrivalRate", "RateUnits", "PER_HOUR"), "newEntity": m.entity("Patient"),
                          "locationType": m.code("self.LOCATION_NODE"), "locationNode": m.code("entrance"),
                          "speed": m.unit("uniform(0.6, 0.9)", "SpeedUnits", "MPS")}),
    ("TimeMeasureStart", "timeIn", {}),
    ("MoveTo", "walkToWaiting", node("triageWaiting")),
    ("Seize", "seizeNurse", {"seizeFromOnePool": m.code("true"), "resourcePool": m.code("nurses"),
                             "maximumCapacity": m.code("true"), "entityLocationQueue": m.code("triageWaiting")}),
    ("MoveTo", "walkToTriage", node("triageRoom")),
    ("Delay", "triage", {"delayTime": m.unit("triangular(4, 7, 12)", "TimeUnits", "MINUTE"),
                         "maximumCapacity": m.code("true"), "entityLocation": m.code("triageRoom")}),
    ("Release", "releaseNurse", {}),
    ("MoveTo", "walkToDoctorWaiting", node("doctorWaiting")),
    ("Seize", "seizeDoctor", {"seizeFromOnePool": m.code("true"), "resourcePool": m.code("doctors"),
                              "maximumCapacity": m.code("true"), "entityLocationQueue": m.code("doctorWaiting")}),
    ("MoveTo", "walkToBed", node("treatmentBeds")),
    ("Delay", "treatment", {"delayTime": m.unit("triangular(10, 20, 40)", "TimeUnits", "MINUTE"),
                            "maximumCapacity": m.code("true"), "entityLocation": m.code("treatmentBeds")}),
    ("Release", "releaseDoctor", {}),
    ("TimeMeasureEnd", "timeOut", {"startObjects": m.code("{ timeIn }")}),
    ("SelectOutput", "admitted", {"conditionIsProbabilistic": m.code("true"), "probability": m.code("admitProbability")}),
]
Y, STEP = 680, 100
for i, (cls, name, vals) in enumerate(flow):
    dy = 10 if cls in ("Source", "Sink", "SelectOutput") else 20          # line the ports up on y = 680
    m.block(cls, name, 20 + i * STEP, Y - dy, vals, label=(0, -12) if i % 2 == 0 else (0, 48))
xb = 20 + len(flow) * STEP
m.block("MoveTo", "walkToWard", xb, Y - 20, node("exitWard"))
m.block("Sink", "toWard", xb + STEP, Y - 10)
m.block("MoveTo", "walkHome", xb, Y + 60, node("exitHome"))
m.block("Sink", "toHome", xb + STEP, Y + 70)
m.block("ResourcePool", "nurses", 20 + 3 * STEP, 600, {"capacity": m.code("numNurses"), "newUnit": m.entity("Nurse"),
                                                       "homeNodes": m.code("{ nurseHome }")}, agent=None)
m.block("ResourcePool", "doctors", 20 + 8 * STEP, 600, {"capacity": m.code("numDoctors"), "newUnit": m.entity("Doctor"),
                                                        "homeNodes": m.code("{ doctorHome }")}, agent=None)
names = [n for _, n, _ in flow]
for a, b in zip(names, names[1:]):
    m.connect(a, "out", b)
m.connect("admitted", "outT", "walkToWard"); m.connect("walkToWard", "out", "toWard")
m.connect("admitted", "outF", "walkHome"); m.connect("walkHome", "out", "toHome")

path = m.write(OUT, frame=(1100, 580), stop_time=1440, real_time_scale=0.5)
print(f"written {path} ({path.stat().st_size:,} bytes); blocks {len(m.blocks)}, links {len(m.links)}, "
      f"shapes {len(m.shapes)}, 3D objects {sorted(m.used3d)}")
