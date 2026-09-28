# Pattern card — Custom flowchart block from a repeated block chain
- **Source:** AnyLogic video "How to create concise process flowcharts" (https://youtu.be/0Nu1a9Te6ac) — distilled, original wording
- **Paradigm:** DES (Process Modeling Library)
- **Problem it solves:** A flowchart repeats one block sequence with only a node, pool or time changed, so it sprawls and every fix must be made several times. Collapse the chain into one reusable, parameterised block.

## Block chain
- **Before.** The Wholesale Warehouse loading logic appears twice: `Seize` (forklift + loader from pool `loader`) → `MoveTo` (loading-zone node) → `Delay` (loading time) → `Release`. The two copies differ only in the node, `loadingZone1Rect` vs `loadingZone2Rect`.
- **Refactor.**
  1. Select one copy.
  2. Right-click a selected block and choose **Create custom flowchart block**. The older UI in the video labels it *Create Flowchart Block*.
  3. Name the new agent type in the New agent dialog (`LoadPallets`).
- **After.** AnyLogic creates the type, moves the blocks inside it, and leaves one `LoadPallets` instance in their place.
  - Replace the second copy with a copy of that instance, so its values carry over, and reconnect its ports.
  - Change only the node.
- **Ports (per AnyLogic Help):** the custom block takes the input ports of the chain's first block and the output ports of its last block.

## Resources
The pools stay on Main, and the block reaches them only through parameters: *Seized resource* and *Released resources*, both set to `loader` on each instance.

## Key settings worth copying
- **Generated interface.**
  - Each essential property of an enclosed block becomes a parameter named `<innerBlock>_<property>`, already linked to that field. Examples: `seizeLoader1_resourcePool`, `moveToLoadingZone1_destinationNode`.
  - The instance is pre-filled with the blocks' original values.
  - The parameters are needed because, inside the new type, the blocks can no longer see Main's `loader` or `loadingZone1Rect` directly.
- **Readable property sheet.** Set each parameter's **Label** (and **Control type** if useful) in its *Value editor* section, e.g. *Loading zone* or *Loading time*. Instances display the label, while code keeps the original name.
- **Per-instance values.**
  - Loading time: `uniform(loadingTimeMin, loadingTimeMax)`, with the bounds taken from Main's parameters.
  - Loading zone: `loadingZone1Rect` on one instance, `loadingZone2Rect` on the other.
- **Custom icon.**
  - Delete the default blue rectangle and draw shapes or an **Image** in its place.
  - Tick **Icon** on every icon element.
  - Put the in/out ports exactly on the icon's edge.
- **Clickable at runtime.** Put `return true;` in the icon shape's *Advanced → On click*. Per Help, a single click then opens the block's inspect window and a double click takes you inside it.
- **Live counters on the icon.**
  - Add Text elements with the dynamic values `seizeLoader1.in.count()` (entered) and `releaseLoadingTransferPerson1.out.count()` (left).
  - Right-align them so they clear the icon, and tick **Icon**.

## KPIs instrumented
- Cumulative in/out counts on the icon. In minus out = agents currently inside the block (its WIP).
- From Main, reach inner blocks through the instance, e.g. `loadPallets.seizeLoader1.in.count()`.

## Pitfalls
- **Per-agent properties must stay dynamic.**
  - A parameter that feeds a per-agent field (delay time, a condition) must be a *Dynamic* parameter. It is recomputed on every access and is read as `name()`.
  - A plain parameter samples `uniform(...)` once, so every pallet gets the same time.
  - Check the generated parameters. Whether the command always makes them dynamic is *(unverified)*.
- **Enclose a clean chain.** Choose a contiguous run whose only outside links are the first block's input and the last block's output(s). How side ports of middle blocks (timeout, preemption, a branch leaving the chain) are handled is *(unverified)*: test, or keep those blocks outside.
- **Icon visibility.** An element without **Icon** ticked is not drawn in the parent flowchart. Ports placed off the icon edge look detached.
- **Runtime debugging.** Without the `return true;` click handler you cannot open the block during a run.

## Reusable idea
Treat a recurring chain like a function: extract it once and pass the differences in as parameters. All copies then behave the same, and a fix inside the type reaches every instance.

## When the co-pilot should use this
- **When a spec repeats itself.** A spec or flowchart has two or more identical chains (per dock, zone, station or line) that differ only in values. Suggest the refactor once the logic is verified, not while it is still changing.
- **When a flowchart is unreadable.** Suggest it when a user says their flowchart is hard to read, or that edits must be repeated in several places.
- **When not to use it.** Skip it when chains differ in *structure* rather than values, or for a one-off chain.
- **Documenting it.** `LoadPallets` is not a palette block, so a written model spec should list its inner PML blocks for each instance (with that instance's parameter values) and use the custom type's name only as a label.
- **Related cards.**
  - `models/wholesale-warehouse.md`: the source model.
  - `basicmodels/interconnected-call-centers-web-app.md`: a different encapsulation, where whole Source→Sink sites become agents joined by Exit/Enter.
