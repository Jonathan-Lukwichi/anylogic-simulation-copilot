"""Build an AnyLogic 8.9 model file (.alp) from Python, using formats copied from AnyLogic's own examples.

Templates come from ../.cache/templates.json (run alp_templates.py once per machine). The builder writes
the model in the reference model's file version (Bank Office tutorial, AlpVersion 8.9.6, with its converter
list); AnyLogic 8.9.10 upgrades it when it opens the file. Verified end to end on 2026-10-02 with the Mini ED
example (copilot/examples/mini-ed-2d3d): the file opened, built and ran in AnyLogic 8.9.10 PLE, in 2D and 3D.

Typical use (see copilot/examples/mini-ed-2d3d/build_mini_ed.py):

    m = AlpModel("Mini ED 2D-3D", "mini_ed", time_unit="Minute")
    m.agent_type("Patient", figure="person")
    m.agent_type("Nurse", usage="RESOURCE_UNIT", figure="nurse")
    m.parameter("arrivalRate", "double", "8", "Patients per hour", 20, 860)
    m.block("Source", "source", 20, 670, {"rate": m.unit("arrivalRate", "RateUnits", "PER_HOUR"),
                                          "newEntity": m.entity("Patient")})
    ...
    m.connect("source", "out", "timeIn")
    m.shape(m.rect("floor", 80, 70, 470, 290, m.rgb(220, 220, 220)))
    path = m.write(r"C:\\...\\Mini ED 2D-3D")        # copies the 3D files, runs the file checks

Units: canvas pixels with the default scale (10 px = 1 m); Z and heights in the same pixels.
"""
import json
import re
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE.parent / ".cache" / "templates.json"
PML = "com.anylogic.libraries.processmodeling"
MARKUP = "com.anylogic.libraries.modules.markup_descriptors"
AREA_PARAMS = ["appliedClass", "speedRestricted", "maxSpeed", "accessRestricted", "accessRestrictionType",
               "accessRestrictionCondition", "capacity", "throughput", "schedule", "avoidedIfClosed", "onEnter",
               "onEnterDenied", "onExit", "onOpen", "onClose"]
# Port offsets of the block icons (measured from AnyLogic's example connectors); default in (0,20), out (40,20).
PORTS = {("Source", "out"): (30, 10), ("Sink", "in"): (0, 10), ("SelectOutput", "in"): (10, 10),
         ("SelectOutput", "outT"): (30, 10), ("SelectOutput", "outF"): (20, 20),
         ("TimeMeasureStart", "in"): (0, 20), ("TimeMeasureStart", "out"): (10, 20),
         ("TimeMeasureEnd", "in"): (20, 20), ("TimeMeasureEnd", "out"): (30, 20)}


def cd(s):
    return f"<![CDATA[{s}]]>"


class AlpModel:
    def __init__(self, name, package, time_unit="Minute", id_base=1790700000000):
        if not CACHE.is_file():
            raise SystemExit(f"template cache missing: run {HERE / 'alp_templates.py'} first")
        self.T = json.loads(CACHE.read_text(encoding="utf-8"))
        self.name, self.pkg, self.time_unit = name, package, time_unit
        self._id = id_base
        self.types = {}                      # agent type name -> dict(ids, usage, speed, figure)
        self.params, self.blocks, self.links, self.shapes = [], [], [], []
        self.pos = {}                        # block name -> (x, y, class)
        self.used3d = set()
        self._att = 0
        self.agent_type("Main", usage="ENTITY", speed=10)

    # ------------------------------------------------------------------ small helpers
    def nid(self):
        self._id += 1
        return self._id

    @staticmethod
    def rgb(r, g, b, a=255):
        v = (a << 24) | (r << 16) | (g << 8) | b
        return v - (1 << 32) if v >= (1 << 31) else v

    @staticmethod
    def code(v):
        return f'<Value Class="CodeValue"><Code>{cd(v)}</Code></Value>'

    @staticmethod
    def unit(v, unit_class, u):
        """unit_class: TimeUnits / RateUnits / SpeedUnits / LengthUnits; u: MINUTE, PER_HOUR, MPS, METER ..."""
        return f'<Value Class="CodeUnitValue"><Code>{cd(v)}</Code><Unit Class="{unit_class}">{cd(u)}</Unit></Value>'

    def entity(self, type_name):
        """Value of a Source 'newEntity' or ResourcePool 'newUnit' parameter: an agent of type_name."""
        src = self.T["blocks"]["Source"]
        x = re.search(r'<Value Class="EntityCodeValue">.*?</EntityEmbeddedObject>\s*</Value>', src, re.S).group(0)
        x = re.sub(r"<Id>\d+</Id>", lambda m: f"<Id>{self.nid()}</Id>", x)
        x = re.sub(r"(<ActiveObjectClass>\s*<PackageName>)<!\[CDATA\[\w+\]\]>(</PackageName>\s*<ClassName>)"
                   r"<!\[CDATA\[\w+\]\]>", lambda m: f"{m.group(1)}{cd(self.pkg)}{m.group(2)}{cd(type_name)}", x)
        x = re.sub(r"(<GenericParameterSubstituteReference>\s*<PackageName>)<!\[CDATA\[\w+\]\]>(</PackageName>\s*"
                   r"<ClassName>)<!\[CDATA\[\w+\]\]>(</ClassName>\s*<ItemName>)<!\[CDATA\[\d+\]\]>",
                   lambda m: f"{m.group(1)}{cd(self.pkg)}{m.group(2)}{cd(type_name)}{m.group(3)}"
                             f"{cd(self.types[type_name]['gen'])}", x)
        return x

    # ------------------------------------------------------------------ agent types
    def agent_type(self, name, usage="ENTITY", speed=1, figure=None, figure_scale=1.0):
        """usage: ENTITY (flows through blocks) or RESOURCE_UNIT (ResourcePool units). figure: 3D library object."""
        self.types[name] = {"id": self.nid(), "gen": self.nid(), "level": self.nid(), "link": self.nid(),
                            "usage": usage, "speed": speed, "figure": figure, "scale": figure_scale}

    # ------------------------------------------------------------------ Main contents
    def parameter(self, name, typ, default, label, x, y):
        self.params.append(f"""<Variable Class="Parameter">
<Id>{self.nid()}</Id>
<Name>{cd(name)}</Name>
<X>{x}</X><Y>{y}</Y>
<Label><X>20</X><Y>-20</Y></Label>
<PublicFlag>false</PublicFlag>
<PresentationFlag>true</PresentationFlag>
<ShowLabel>true</ShowLabel>
<Properties SaveInSnapshot="true" ModificatorType="STATIC">
<Type>{cd(typ)}</Type>
<UnitType>{cd("NONE")}</UnitType>
<SdArray>false</SdArray>
<DefaultValue Class="CodeValue"><Code>{cd(default)}</Code></DefaultValue>
<ParameterEditor>
<Id>{self.nid()}</Id>
<Label>{cd(label)}</Label>
<EditorContolType>TEXT_BOX</EditorContolType>
<MinSliderValue>{cd(0)}</MinSliderValue>
<MaxSliderValue>{cd(100)}</MaxSliderValue>
<DelimeterType>NO_DELIMETER</DelimeterType>
</ParameterEditor>
</Properties>
</Variable>""")

    def block(self, cls, name, x, y, values=None, agent="Patient", label=(0, -10)):
        """A Process Modeling Library block. values: {parameter name: m.code(...)/m.unit(...)/m.entity(...)};
        any parameter not given keeps AnyLogic's default. agent: the flowchart agent type (None for pools)."""
        if cls not in self.T["blocks"]:
            raise KeyError(f"no template for {cls}; known: {sorted(self.T['blocks'])}")
        t = self.T["blocks"][cls].replace("\r\n", "\n")
        i0, i1 = t.index("<Parameters>"), t.rindex("</Parameters>")
        head, mid, tail = t[:i0], t[i0 + len("<Parameters>"):i1], t[i1 + len("</Parameters>"):]
        mid = re.sub(r'<Value Class="EntityCodeValue">.*?</EntityEmbeddedObject>\s*</Value>', "", mid, flags=re.S)
        names = re.findall(r"<Parameter>\s*<Name><!\[CDATA\[(\w+)\]\]></Name>", mid)
        values = values or {}
        bad = set(values) - set(names)
        if bad:
            raise KeyError(f"{cls} '{name}': unknown parameters {sorted(bad)}; valid: {names}")
        params = "\n".join(f"<Parameter><Name>{cd(n)}</Name>{values.get(n, '')}</Parameter>" for n in names)
        head = re.sub(r"<Id>\d+</Id>", f"<Id>{self.nid()}</Id>", head, count=1)
        head = re.sub(r"<Name><!\[CDATA\[[^\]]*\]\]></Name>", f"<Name>{cd(name)}</Name>", head, count=1)
        head = re.sub(r"<X>[^<]*</X>\s*<Y>[^<]*</Y>", f"<X>{x}</X><Y>{y}</Y>", head, count=1)
        head = re.sub(r"<Label>\s*<X>[^<]*</X>\s*<Y>[^<]*</Y>\s*</Label>",
                      f"<Label><X>{label[0]}</X><Y>{label[1]}</Y></Label>", head, count=1)
        head = re.sub(r"\s*<GenericParameterSubstituteValue.*?</GenericParameterSubstituteValue>", "", head, flags=re.S)
        if agent:
            head = head.replace("</GenericParameterSubstituteReference>",
                                "</GenericParameterSubstituteReference>\n<GenericParameterSubstituteValue "
                                f"Class=\"CodeValue\"><Code>{cd(agent)}</Code></GenericParameterSubstituteValue>", 1)
        tail = re.sub(r"<Id>\d+</Id>", lambda m: f"<Id>{self.nid()}</Id>", tail)
        self.pos[name] = (x, y, cls)
        self.blocks.append(head + "<Parameters>\n" + params + "\n</Parameters>" + tail)

    def connect(self, src, port, dst, dport="in"):
        self.links.append((src, port, dst, dport))

    def _connector(self, i, src, sport, dst, dport):
        (sx, sy, scls), (dx, dy, dcls) = self.pos[src], self.pos[dst]
        ox, oy = PORTS.get((scls, sport), (40, 20))
        ix, iy = PORTS.get((dcls, dport), (0, 20))
        x0, y0 = sx + ox, sy + oy
        x1, y1 = dx + ix - x0, dy + iy - y0
        pts = [(0, 0)] + ([(0, y1)] if (x1 and y1) else []) + [(x1, y1)]
        ref = lambda kind, item, pkg, cls: (f"<{kind}><PackageName>{cd(pkg)}</PackageName><ClassName>{cd(cls)}"
                                             f"</ClassName><ItemName>{cd(item)}</ItemName></{kind}>")
        return f"""<Connector>
<Id>{self.nid()}</Id>
<Name>{cd("connector" + str(i))}</Name>
<X>{x0}</X><Y>{y0}</Y>
<Label><X>10</X><Y>0</Y></Label>
<PublicFlag>false</PublicFlag>
<PresentationFlag>true</PresentationFlag>
<ShowLabel>false</ShowLabel>
{ref("SourceEmbeddedObjectReference", src, self.pkg, "Main")}
{ref("SourceConnectableItemReference", sport, PML, scls)}
{ref("TargetEmbeddedObjectReference", dst, self.pkg, "Main")}
{ref("TargetConnectableItemReference", dport, PML, dcls)}
<Points>{"".join(f"<Point><X>{px}</X><Y>{py}</Y></Point>" for px, py in pts)}</Points>
</Connector>"""

    def shape(self, xml):
        self.shapes.append(xml)

    # ------------------------------------------------------------------ presentation and space markup
    def rect(self, name, x, y, w, h, fill, z=0, zh=1, line=None, mode="SHAPE_DRAW_2D3D"):
        """Filled rectangle; with mode 2D3D it is a box of height zh in 3D (floors zh=1, walls zh=12 = 1.2 m)."""
        return f"""<Rectangle>
<Id>{self.nid()}</Id>
<Name>{cd(name)}</Name>
<X>{x}</X><Y>{y}</Y>
<Label><X>10</X><Y>10</Y></Label>
<PublicFlag>true</PublicFlag>
<PresentationFlag>true</PresentationFlag>
<ShowLabel>false</ShowLabel>
<DrawMode>{mode}</DrawMode>
<EmbeddedIcon>false</EmbeddedIcon>
<Z>{z}</Z>
<ZHeight>{zh}</ZHeight>
<LineWidth>1</LineWidth>
{f"<LineColor>{line}</LineColor>" if line is not None else "<LineColor/>"}
<LineMaterial>null</LineMaterial>
<LineStyle>SOLID</LineStyle>
<Width>{w}</Width>
<Height>{h}</Height>
<Rotation>0.0</Rotation>
<FillColor>{fill}</FillColor>
<FillMaterial>null</FillMaterial>
</Rectangle>"""

    def text(self, name, x, y, s, size=11, color=-12566464, bold=False, dyn=None, mode="SHAPE_DRAW_2D"):
        """Static text, or dynamic when dyn is a Java expression (evaluated every frame)."""
        return f"""<Text>
<Id>{self.nid()}</Id>
<Name>{cd(name)}</Name>
<X>{x}</X><Y>{y}</Y>
<Label><X>0</X><Y>-10</Y></Label>
<PublicFlag>true</PublicFlag>
<PresentationFlag>true</PresentationFlag>
<ShowLabel>false</ShowLabel>
<DrawMode>{mode}</DrawMode>
<EmbeddedIcon>false</EmbeddedIcon>
<Z>0</Z>
<Rotation>0.0</Rotation>
<Color>{color}</Color>
<Text>{cd(s)}</Text>
{f"<TextCode>{cd(dyn)}</TextCode>" if dyn else ""}
<Font>
<Name>SansSerif</Name>
<Size>{size}</Size>
<Style>{1 if bold else 0}</Style>
</Font>
<Alignment>LEFT</Alignment>
</Text>"""

    def point_node(self, name, x, y):
        return f"""<PointNode>
<Id>{self.nid()}</Id>
<Name>{cd(name)}</Name>
<X>{x}</X><Y>{y}</Y>
<Label><X>10</X><Y>0</Y></Label>
<PublicFlag>true</PublicFlag>
<PresentationFlag>true</PresentationFlag>
<ShowLabel>false</ShowLabel>
<DrawMode>SHAPE_DRAW_2D3D</DrawMode>
<Z>0</Z>
<FakeNode>false</FakeNode>
<Lock>false</Lock>
<Color>-14774017</Color>
<Radius>1</Radius>
<SpeedLimit>false</SpeedLimit>
<SpeedLimitValue Class="UnitValue">
<Value Class="Double">10</Value>
<Unit Class="SpeedUnits">{cd("MPS")}</Unit>
</SpeedLimitValue>
</PointNode>"""

    def _area_descriptor(self):
        params = "\n".join(f"<Parameter><Name>{cd(p)}</Name></Parameter>" for p in AREA_PARAMS)
        xyz = "".join(f'<{t} Class="CodeValue"><Code>{cd(0)}</Code></{t}>' for t in
                      ("XCode", "YCode", "ZCode", "ColumnCode", "RowCode", "LatitudeCode", "LongitudeCode"))
        return f"""<EmbeddedObject>
<Id>{self.nid()}</Id>
<ActiveObjectClass>
<PackageName>{cd(MARKUP)}</PackageName>
<ClassName>{cd("AreaNodeDescriptor")}</ClassName>
</ActiveObjectClass>
<GenericParameterSubstitute>
<GenericParameterSubstituteReference>
<PackageName>{cd(MARKUP)}</PackageName>
<ClassName>{cd("AreaNodeDescriptor")}</ClassName>
<ItemName>{cd("1574694148121")}</ItemName>
</GenericParameterSubstituteReference>
</GenericParameterSubstitute>
<Parameters>
{params}
</Parameters>
<ReplicationFlag>false</ReplicationFlag>
<Replication Class="CodeValue"><Code>{cd(100)}</Code></Replication>
<CollectionType>ARRAY_LIST_BASED</CollectionType>
<InitialLocationType>AT_ANIMATION_POSITION</InitialLocationType>
{xyz}
<LocationNameCode Class="CodeValue"><Code>{cd('""')}</Code></LocationNameCode>
<InitializationType>SPECIFIED_NUMBER</InitializationType>
<InitializationDatabaseTableQuery>
<Id>{self.nid()}</Id>
<TableReference>
</TableReference>
</InitializationDatabaseTableQuery>
<InitializationDatabaseType>ONE_AGENT_PER_DATABASE_RECORD</InitializationDatabaseType>
<QuantityColumn>
</QuantityColumn>
</EmbeddedObject>"""

    def rect_node(self, name, x, y, w, h, attractors=(), visible=False):
        """Rectangular node (an area agents are placed in). attractors: [(x, y[, rotationDeg]), ...] absolute."""
        items = []
        for ax, ay, *rot in attractors:
            self._att += 1
            items.append(f"""<Attractor>
<Id>{self.nid()}</Id>
<Name>{cd("attractor" + str(self._att))}</Name>
<X>{ax}</X><Y>{ay}</Y>
<Label><X>10</X><Y>0</Y></Label>
<PublicFlag>true</PublicFlag>
<PresentationFlag>true</PresentationFlag>
<ShowLabel>false</ShowLabel>
<DrawMode>SHAPE_DRAW_2D3D</DrawMode>
<Z>0</Z>
<Rotation>{rot[0] if rot else 0.0}</Rotation>
</Attractor>""")
        atts = ("<Presentation>\n" + "\n".join(items) + "\n</Presentation>") if items else ""
        return f"""<RectangleNode>
<Id>{self.nid()}</Id>
<Name>{cd(name)}</Name>
<X>{x}</X><Y>{y}</Y>
<Label><X>10</X><Y>0</Y></Label>
<PublicFlag>true</PublicFlag>
<PresentationFlag>{str(visible).lower()}</PresentationFlag>
<ShowLabel>false</ShowLabel>
<DrawMode>SHAPE_DRAW_2D3D</DrawMode>
<Z>0</Z>
{self._area_descriptor()}
<LineColor>-14774017</LineColor>
<FillColor/>
<LineWidth>2</LineWidth>
<LineMaterial>null</LineMaterial>
<FillMaterial>null</FillMaterial>
<LineStyle>DASHED</LineStyle>
<AttractorsLayout>random</AttractorsLayout>
{atts}
<Sloped>false</Sloped>
<Slope>
<Id>{self.nid()}</Id>
<Name>{cd(name)}</Name>
<X>0</X><Y>10</Y>
<PublicFlag>false</PublicFlag>
<PresentationFlag>true</PresentationFlag>
<ShowLabel>true</ShowLabel>
<Dx>20</Dx>
<Dy>0</Dy>
<Dz>0</Dz>
<AngleX>30</AngleX>
<AngleZ>0</AngleZ>
<SlopeType>angle</SlopeType>
</Slope>
<Width>{w}</Width>
<Height>{h}</Height>
<Rotation>0.0</Rotation>
</RectangleNode>"""

    def figure3d(self, name, obj, x, y, z=0, rotation=0.0, scale=1.0):
        """A 3D object from AnyLogic's library (file name without .dae, e.g. 'bed', 'doctor'); copied on write."""
        if obj not in self.T["figures"]:
            raise KeyError(f"3D object '{obj}' has no template (not used in any example); pick another")
        self.used3d.add(obj)
        f = self.T["figures"][obj]
        return f"""<Figure3D>
<Id>{self.nid()}</Id>
<Name>{cd(name)}</Name>
<X>{x}</X><Y>{y}</Y>
<Label><X>0</X><Y>-10</Y></Label>
<PublicFlag>true</PublicFlag>
<PresentationFlag>true</PresentationFlag>
<ShowLabel>false</ShowLabel>
<DrawMode>SHAPE_DRAW_2D3D</DrawMode>
<X>{x}</X><Y>{y}</Y><Z>{z}</Z>
<Label><X>0</X><Y>-10</Y></Label>
<ResourceReference>
<PackageName>{cd(self.pkg)}</PackageName>
<ClassName>{cd("3d/" + obj + ".dae")}</ClassName>
</ResourceReference>
{f["colorTable"]}
<AutoScale>false</AutoScale>
<Scale>{scale}</Scale>
<Rotation>{rotation}</Rotation>
<AxisOrder>{f["AxisOrder"]}</AxisOrder>
<ApplyShading>true</ApplyShading>
<InternalLighting>OFF</InternalLighting>
<IgnoreSceneLights>false</IgnoreSceneLights>
</Figure3D>"""

    def camera(self, name, x, y, z, rot_x, rot_z):
        """rot_x = tilt down (deg); rot_z = -90 looks towards smaller Y (up the 2D canvas)."""
        return f"""<Camera3D>
<Id>{self.nid()}</Id>
<Name>{cd(name)}</Name>
<X>{x}</X><Y>{y}</Y><Z>{z}</Z>
<Label><X>0</X><Y>-10</Y></Label>
<ShowLabel>false</ShowLabel>
<RotationX>{rot_x}</RotationX>
<RotationZ>{rot_z}</RotationZ>
</Camera3D>"""

    def window3d(self, name, x, y, w, h, camera):
        return f"""<Control Type="Window3D">
<Id>{self.nid()}</Id>
<Name>{cd(name)}</Name>
<X>{x}</X><Y>{y}</Y>
<Width>{w}</Width>
<Height>{h}</Height>
<MakeDefaultViewArea>false</MakeDefaultViewArea>
<Label><X>0</X><Y>-10</Y></Label>
<ShowLabel>false</ShowLabel>
<FollowCamera>false</FollowCamera>
<NavigationType>limitedToZAboveZero</NavigationType>
<FarClippingDistance>2000</FarClippingDistance>
<Camera>{camera}</Camera>
</Control>"""

    def _recurrence(self, every):
        u = self.time_unit.upper()
        return f"""<RecurrenceProperties>
<Id>{self.nid()}</Id>
<OccurrenceAtTime>true</OccurrenceAtTime>
<OccurrenceDate>1417766400000</OccurrenceDate>
<OccurrenceTime Class="CodeUnitValue"><Code>{cd(0)}</Code><Unit Class="TimeUnits">{cd(u)}</Unit></OccurrenceTime>
<RecurrenceCode Class="CodeUnitValue"><Code>{cd(every)}</Code><Unit Class="TimeUnits">{cd(u)}</Unit></RecurrenceCode>
</RecurrenceProperties>"""

    @staticmethod
    def _chart_parts(x, y, w, h, area, legend_place, legend_size):
        ax, ay, aw, ah = area
        top = f"""<X>{x}</X><Y>{y}</Y>
<Label><X>0</X><Y>-10</Y></Label>
<PublicFlag>true</PublicFlag>
<PresentationFlag>true</PresentationFlag>
<ShowLabel>false</ShowLabel>
<DrawMode>SHAPE_DRAW_2D3D</DrawMode>"""
        mid = f"""<EmbeddedIcon>false</EmbeddedIcon>
<Width>{w}</Width>
<Height>{h}</Height>
<BackgroundColor/>
<BorderColor/>
<ChartArea>
<XOffset>{ax}</XOffset>
<YOffset>{ay}</YOffset>
<Width>{aw}</Width>
<Height>{ah}</Height>
<BackgroundColor>-1</BackgroundColor>
<BorderColor>-16777216</BorderColor>
<GridColor>-12566464</GridColor>
</ChartArea>
<Legend>
<Place>{legend_place}</Place>
<TextColor>-16777216</TextColor>
<Size>{legend_size}</Size>
</Legend>
<Labels>
<HorLabelsPosition>DEFAULT</HorLabelsPosition>
<VerLabelsPosition>DEFAULT</VerLabelsPosition>
<TextColor>-12566464</TextColor>
</Labels>
<ShowLegend>true</ShowLegend>"""
        return top, mid

    def time_plot(self, name, x, y, w, h, items, window, window_units="HOUR", every=5, area=None, legend=("EAST", 140)):
        """items: [(title, internal dataset name, Java value expression, colour)] sampled every `every` time units.
        area: (x offset, y offset, width, height) of the plot area inside the chart; legend: (place, size)."""
        top, mid = self._chart_parts(x, y, w, h, area or (50, 15, w - 200, h - 45), *legend)
        ds = "\n".join(f"""<DatasetExpression>
<Title>{cd(title)}</Title>
<Id>{self.nid()}</Id>
<Expression>{cd(dsname)}</Expression>
<Color>{color}</Color>
<Expression2>{cd(expr)}</Expression2>
<Expression2Flag>true</Expression2Flag>
<PointStyle>NONE</PointStyle>
<LineWidth>2.0</LineWidth>
</DatasetExpression>""" for title, dsname, expr, color in items)
        return f"""<TimePlot>
<Id>{self.nid()}</Id>
<Name>{cd(name)}</Name>
{top}
<AutoUpdate>true</AutoUpdate>
{self._recurrence(every)}
{mid}
<TimeWindowsMovementType>MOVEMENT_WITH_TIME</TimeWindowsMovementType>
<TimeWindowUnits>{window_units}</TimeWindowUnits>
<VerScaleFromExpression>{cd(0)}</VerScaleFromExpression>
<VerScaleToExpression>{cd(1)}</VerScaleToExpression>
<VerScaleType>AUTO</VerScaleType>
<DrawLine>true</DrawLine>
<Interpolation>STEP</Interpolation>
{ds}
<SamplesToKeep>300</SamplesToKeep>
<TimeWindowExpression>{cd(window)}</TimeWindowExpression>
<FillAreaUnderLine>false</FillAreaUnderLine>
<LabelFormat>MODEL_TIME_UNITS</LabelFormat>
</TimePlot>"""

    def bar_chart(self, name, x, y, w, h, items, every=5, area=None, legend=("EAST", 200)):
        """items: [(title, Java value expression, colour)]. area/legend as in time_plot."""
        top, mid = self._chart_parts(x, y, w, h, area or (40, 20, 160, h - 50), *legend)
        di = "\n".join(f"""<DataItem>
<Id>{self.nid()}</Id>
<Expression>{cd(expr)}</Expression>
<Color>{color}</Color>
<Title>{cd(title)}</Title>
</DataItem>""" for title, expr, color in items)
        return f"""<BarChart>
<Id>{self.nid()}</Id>
<Name>{cd(name)}</Name>
{top}
<AutoUpdate>true</AutoUpdate>
{self._recurrence(every)}
{mid}
{di}
<ScaleFromExpression>{cd(0)}</ScaleFromExpression>
<ScaleToExpression>{cd(1)}</ScaleToExpression>
<ScaleType>AUTO</ScaleType>
<Bars>
<Direction>UP</Direction>
<RelativeWidth>0.8</RelativeWidth>
</Bars>
</BarChart>"""

    # ------------------------------------------------------------------ assembly
    def _level(self, level_id, shapes):
        return f"""<Presentation>
<Level>
<Id>{level_id}</Id>
<Name>{cd("level")}</Name>
<X>0</X><Y>0</Y>
<Label><X>10</X><Y>0</Y></Label>
<PublicFlag>true</PublicFlag>
<PresentationFlag>true</PresentationFlag>
<ShowLabel>false</ShowLabel>
<DrawMode>SHAPE_DRAW_2D3D</DrawMode>
<Z>0</Z>
<LevelVisibility>ALWAYS_SHOW</LevelVisibility>
<Presentation>
{shapes}
</Presentation>
</Level>
</Presentation>"""

    def _class(self, name, body, space=(500, 500)):
        t = self.types[name]
        main = name == "Main"
        step = "DAY" if main else "SECOND"
        return f"""<ActiveObjectClass>
<Id>{t["id"]}</Id>
<Name>{cd(name)}</Name>
<Generic>false</Generic>
<GenericParameter>
<Id>{t["gen"]}</Id>
<Name>{cd(t["gen"])}</Name>
<GenericParameterValue Class="CodeValue"><Code>{cd("T" if main else "T extends Agent")}</Code></GenericParameterValue>
<GenericParameterLabel>{cd("Generic parameters:" if main else "Generic parameter:")}</GenericParameterLabel>
</GenericParameter>
<FlowChartsUsage>{t["usage"]}</FlowChartsUsage>
<SamplesToKeep>100</SamplesToKeep>
<LimitNumberOfArrayElements>false</LimitNumberOfArrayElements>
<ElementsLimitValue>100</ElementsLimitValue>
<MakeDefaultViewArea>{"false" if main else "true"}</MakeDefaultViewArea>
<SceneGridColor/>
<SceneBackgroundColor>-4144960</SceneBackgroundColor>
<SceneSkybox>null</SceneSkybox>
<AgentProperties>
<EnvironmentDefinesInitialLocation>true</EnvironmentDefinesInitialLocation>
<RotateAnimationTowardsMovement>true</RotateAnimationTowardsMovement>
<RotateAnimationVertically>false</RotateAnimationVertically>
<VelocityCode Class="CodeUnitValue"><Code>{cd(t["speed"])}</Code><Unit Class="SpeedUnits">{cd("MPS")}</Unit></VelocityCode>
<PhysicalLength Class="CodeUnitValue"><Code>{cd(1)}</Code><Unit Class="LengthUnits">{cd("METER")}</Unit></PhysicalLength>
<PhysicalWidth Class="CodeUnitValue"><Code>{cd(1)}</Code><Unit Class="LengthUnits">{cd("METER")}</Unit></PhysicalWidth>
<PhysicalHeight Class="CodeUnitValue"><Code>{cd(1)}</Code><Unit Class="LengthUnits">{cd("METER")}</Unit></PhysicalHeight>
</AgentProperties>
<EnvironmentProperties>
<EnableSteps>false</EnableSteps>
<StepDurationCode Class="CodeUnitValue"><Code>{cd("1.0")}</Code><Unit Class="TimeUnits">{cd(step)}</Unit></StepDurationCode>
<SpaceType>CONTINUOUS</SpaceType>
<WidthCode>{cd(space[0])}</WidthCode>
<HeightCode>{cd(space[1])}</HeightCode>
<ZHeightCode>{cd(0)}</ZHeightCode>
<ColumnsCountCode>{cd(100)}</ColumnsCountCode>
<RowsCountCode>{cd(100)}</RowsCountCode>
<NeigborhoodType>MOORE</NeigborhoodType>
<LayoutType>USER_DEF</LayoutType>
<NetworkType>USER_DEF</NetworkType>
<ConnectionsPerAgentCode>{cd(2)}</ConnectionsPerAgentCode>
<ConnectionsRangeCode>{cd(50)}</ConnectionsRangeCode>
<NeighborLinkFractionCode>{cd("0.95")}</NeighborLinkFractionCode>
<MCode>{cd(10)}</MCode>
</EnvironmentProperties>
<DatasetsCreationProperties>
<AutoCreate>true</AutoCreate>
<Id>{self.nid()}</Id>
<OccurrenceAtTime>true</OccurrenceAtTime>
<OccurrenceDate>1417766400000</OccurrenceDate>
<OccurrenceTime Class="CodeUnitValue"><Code>{cd(0)}</Code><Unit Class="TimeUnits">{cd(step)}</Unit></OccurrenceTime>
<RecurrenceCode Class="CodeUnitValue"><Code>{cd(1)}</Code><Unit Class="TimeUnits">{cd(step)}</Unit></RecurrenceCode>
</DatasetsCreationProperties>
<ScaleRuler>
<Id>{self.nid()}</Id>
<Name>{cd("scale")}</Name>
<X>0</X><Y>-150</Y>
<PublicFlag>false</PublicFlag>
<PresentationFlag>false</PresentationFlag>
<ShowLabel>false</ShowLabel>
<DrawMode>SHAPE_DRAW_2D3D</DrawMode>
<Length>100</Length>
<Rotation>0</Rotation>
<ScaleType>BASED_ON_LENGTH</ScaleType>
<ModelLength>10</ModelLength>
<LengthUnits>METER</LengthUnits>
<Scale>10</Scale>
<InheritedFromParentAgentType>true</InheritedFromParentAgentType>
</ScaleRuler>
<CurrentLevel>{t["level"]}</CurrentLevel>
<ConnectionsId>{t["link"]}</ConnectionsId>
{body}
<AgentLinks>
<AgentLink>
<Id>{t["link"]}</Id>
<Name>{cd("connections")}</Name>
<X>50</X><Y>-50</Y>
<Label><X>15</X><Y>0</Y></Label>
<PublicFlag>false</PublicFlag>
<PresentationFlag>true</PresentationFlag>
<ShowLabel>true</ShowLabel>
<HandleReceiveInConnections>false</HandleReceiveInConnections>
<AgentLinkType>COLLECTION_OF_LINKS</AgentLinkType>
<AgentLinkBidirectional>true</AgentLinkBidirectional>
<MessageType>{cd("Object")}</MessageType>
<LineStyle>SOLID</LineStyle>
<LineWidth>1</LineWidth>
<LineColor>-16777216</LineColor>
<LineZOrder>UNDER_AGENTS</LineZOrder>
<LineArrow>NONE</LineArrow>
<LineArrowPosition>END</LineArrowPosition>
</AgentLink>
</AgentLinks>
{self._main_tail() if main else self._level(t["level"], self.figure3d(t["figure"], t["figure"], 0, 0, scale=t["scale"]) if t["figure"] else "")}
</ActiveObjectClass>"""

    def _main_tail(self):
        return ("<EmbeddedObjects>\n" + "\n".join(self.blocks) + "\n</EmbeddedObjects>\n"
                + self._level(self.types["Main"]["level"], "\n".join(self.shapes)))

    def build(self, frame=(1100, 580), stop_time=1440, real_time_scale=0.5, start=datetime(2026, 1, 5),
              space=(1100, 900)):
        """Assemble the whole .alp text. stop_time in model time units (None = run until stopped)."""
        connectors = "\n".join(self._connector(i + 1, *l) for i, l in enumerate(self.links))
        body_main = ("<Variables>\n" + "\n".join(self.params) + "\n</Variables>\n<Connectors>\n" + connectors
                     + "\n</Connectors>")
        classes = [self._class("Main", body_main, space)] + [self._class(n, "") for n in self.types if n != "Main"]
        start_ms = int(start.replace(tzinfo=timezone.utc).timestamp() * 1000)
        unit_ms = {"Second": 1e3, "Minute": 6e4, "Hour": 3.6e6, "Day": 8.64e7}[self.time_unit]
        stop = "Stop at specified time" if stop_time is not None else "Never"
        final = stop_time if stop_time is not None else 100
        time_props = f"""<ModelTimeProperties>
<StopOption>{cd(stop)}</StopOption>
<InitialDate>{cd(start_ms)}</InitialDate>
<InitialTime>{cd("0.0")}</InitialTime>
<FinalDate>{cd(int(start_ms + final * unit_ms))}</FinalDate>
<FinalTime>{cd(float(final))}</FinalTime>
</ModelTimeProperties>"""
        resources = "\n".join(f"""<Resource>
<Id>{self.nid()}</Id>
<Path>{cd("3d/" + o + ".dae")}</Path>
<ReferencedFromUserCode>false</ReferencedFromUserCode>
<Location>FILE_SYSTEM</Location>
</Resource>""" for o in sorted(self.used3d))
        main_id = self.types["Main"]["id"]
        return f"""{self.T["header"]}<Model>
<Id>{self.nid()}</Id>
<Name>{cd(self.name)}</Name>
<EngineVersion>6</EngineVersion>
<JavaPackageName>{cd(self.pkg)}</JavaPackageName>
<ModelTimeUnit>{cd(self.time_unit)}</ModelTimeUnit>
<Folders>
</Folders>
<ActiveObjectClasses>
{chr(10).join(classes)}
</ActiveObjectClasses>
<DifferentialEquationsMethod>EULER</DifferentialEquationsMethod>
<MixedEquationsMethod>RK45_NEWTON</MixedEquationsMethod>
<AlgebraicEquationsMethod>MODIFIED_NEWTON</AlgebraicEquationsMethod>
<AbsoluteAccuracy>1.0E-5</AbsoluteAccuracy>
<FixedTimeStep>0.01</FixedTimeStep>
<RelativeAccuracy>1.0E-5</RelativeAccuracy>
<TimeAccuracy>1.0E-5</TimeAccuracy>
<InspectionWindowColorTheme>DEFAULT</InspectionWindowColorTheme>
<Frame>
<Id>{self.nid()}</Id>
<Width>{frame[0]}</Width>
<Height>{frame[1]}</Height>
</Frame>
<Database>
<Id>{self.nid()}</Id>
<Logging>false</Logging>
<AutoExport>false</AutoExport>
<ShutdownCompact>false</ShutdownCompact>
<ImportSettings>
</ImportSettings>
<ExportSettings>
</ExportSettings>
</Database>
<RunConfiguration ActiveObjectClassId="{main_id}">
<Id>{self.nid()}</Id>
<Name>{cd("RunConfiguration")}</Name>
<MaximumMemory>512</MaximumMemory>
{time_props}
<AnimationProperties>
<StopNever>{"true" if stop_time is None else "false"}</StopNever>
<ExecutionMode>realTimeScaled</ExecutionMode>
<RealTimeScale>{real_time_scale}</RealTimeScale>
<EnableZoomAndPanning>true</EnableZoomAndPanning>
<EnableDeveloperPanel>false</EnableDeveloperPanel>
<ShowDeveloperPanelOnStart>false</ShowDeveloperPanelOnStart>
</AnimationProperties>
<Inputs>
</Inputs>
<Outputs>
</Outputs>
</RunConfiguration>
<Experiments>
<SimulationExperiment ActiveObjectClassId="{main_id}">
<Id>{self.nid()}</Id>
<Name>{cd("Simulation")}</Name>
<CommandLineArguments>{cd("")}</CommandLineArguments>
<MaximumMemory>512</MaximumMemory>
<RandomNumberGenerationType>fixedSeed</RandomNumberGenerationType>
<CustomGeneratorCode>new Random()</CustomGeneratorCode>
<SeedValue>1</SeedValue>
<SelectionModeForSimultaneousEvents>LIFO</SelectionModeForSimultaneousEvents>
<VmArgs>{cd("")}</VmArgs>
<LoadRootFromSnapshot>false</LoadRootFromSnapshot>
<Presentation>
{self.text("text", 40, 30, self.name, size=24)}
</Presentation>
<Parameters>
</Parameters>
<PresentationProperties>
<EnableZoomAndPanning>true</EnableZoomAndPanning>
<ExecutionMode>{cd("realTimeScaled")}</ExecutionMode>
<Title>{cd(self.name + " : Simulation")}</Title>
<EnableDeveloperPanel>true</EnableDeveloperPanel>
<ShowDeveloperPanelOnStart>false</ShowDeveloperPanelOnStart>
<RealTimeScale>{real_time_scale}</RealTimeScale>
</PresentationProperties>
{time_props}
<BypassInitialScreen>true</BypassInitialScreen>
</SimulationExperiment>
</Experiments>
<ModelResources>
{resources}
</ModelResources>
{chr(10).join(self.T["libraries"])}
</Model>
{self.T["converters"]}
</AnyLogicWorkspace>
"""

    def write(self, out_dir, **build_args):
        """Write <out_dir>/<name>.alp (+ 3d/ files) and run the file checks. Refuses to overwrite a model
        that has an .autosave newer than the file (it may be open in AnyLogic - gotcha G125)."""
        out = Path(out_dir)
        alp = out / f"{self.name}.alp"
        auto = alp.with_name(alp.name + ".autosave")
        if alp.exists() and auto.exists() and auto.stat().st_mtime > alp.stat().st_mtime:
            raise SystemExit(f"{auto.name} is newer than the model: it may be open in AnyLogic. Close it first.")
        text = self.build(**build_args)
        root = ET.fromstring(text.encode("utf-8"))          # well-formed or raise
        ids = [e.text for e in root.iter("Id")]
        dup = {i for i in ids if ids.count(i) > 1}
        if dup:
            raise ValueError(f"duplicate ids: {sorted(dup)[:5]}")
        out.mkdir(parents=True, exist_ok=True)
        (out / "3d").mkdir(exist_ok=True)
        lib3d = Path(self.T["lib3d"])
        for o in sorted(self.used3d):
            src = lib3d / f"{o}.dae"
            shutil.copy2(src, out / "3d" / src.name)
            for tex in re.findall(r"<init_from>([^<]+)</init_from>", src.read_text(encoding="utf-8", errors="replace")):
                if (lib3d / tex).is_file():
                    shutil.copy2(lib3d / tex, out / "3d" / Path(tex).name)
        alp.write_bytes(text.replace("\n", self.T["eol"]).encode("utf-8"))
        return alp
