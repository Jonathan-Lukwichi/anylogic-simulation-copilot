# Pattern card — Reading Agent Parameters from a CSV File
- **Source:** AnyLogic example model "Reading Agent Parameters from a CSV File" (bigbookmodels), AnyLogic 8.9.10 — distilled, original wording
- **Paradigm:** ABM
- **Problem it solves:** Create agents from a delimited text file, replace a lookup curve from a text file while the model runs, and keep a plain-text run log, using the Text File element instead of a database.

## Structure
Companions: *Reading Table Function from a Text File*, *Using Text File as a Log* and *Working with Clipboard*. The file-chooser read loop itself is Big Book ch. 13 Ex. 13.6, already in the KB text.
- **File → agents.**
  - Text File `file`: Read mode on `data.csv`. Its separators are line break, `;` and `,`; the demo file is in fact semicolon-separated and has no header row.
  - Main's On startup loops while `file.canReadMore()`: `readString()` twice (registration, type), `readDouble()` twice (x, y). It then calls `add_airplanes(reg, type)`, which takes the parameters in declared order, and `plane.setXY(x, y)`.
  - The population starts empty. The picture's scale and a label depend on `type`.
- **File → table function.**
  1. A File Chooser's action points the element at the chosen file: `file.setFile(value, TextFile.READ)`.
  2. It reads (argument, value) pairs into two `ArrayList<Double>` until `canReadMore()` is false.
  3. It copies them into `double[]` arrays and calls `tableFunction.setArgumentsAndValues(args, vals)`.
- **Log file.**
  - Text File `log` in Write mode; a function `writeToLog(String)` calls `log.println(info)`.
  - On startup writes a header line stamped with the computer's clock (`new Date()`); a Rate event (once per minute on average) adds lines stamped with `time()`.
- **Clipboard.**
  - "Copy" builds a string from a polyline's points and calls AnyLogic's `copyToClipboard(s)`.
  - "Paste" reads `java.awt.Toolkit.getDefaultToolkit().getSystemClipboard()` and checks `DataFlavor.stringFlavor` first. Main's Imports carry `java.awt.datatransfer.*`.

## Resources
n/a

## Key settings worth copying
From Help 8.9.10 *Text file* and the Javadoc:
- **Modes.** Read; Write, which overwrites; Write/Append, which adds. A file taken from a URL or packed inside the model can only be read.
- **Separators** (Read mode) are check boxes plus a custom field. Include the line break, or a `readString()` can run across lines.
- **Readers.** `readString`, `readInt`, `readDouble`, `readBoolean` and `readLine` each advance one token and skip the separators after it.
  - `getLineNumber()` is 1-based: 0 before the first read, −1 at end of file.
  - `skipTokens(n)` and `skipChars(n)` jump over headers.
- **Opening.** The file opens at the first read or write; `close()` puts it back to "not open".
- **`setArgumentsAndValues(double[], double[])`** needs equal lengths and no duplicate arguments; unsorted arguments are sorted (Javadoc).
- **`copyToClipboard(String)`** is a built-in AnyLogic function; in a browser run the copy may ask for permission first (Help).

## KPIs instrumented
n/a (data-exchange demos).

## Pitfalls
- **Headers and number formats.** With a header row, skip it first (`readLine()`), or the first `readDouble()` throws. Because `,` is also a separator here, a decimal comma ("50,00") splits into two tokens, and quoted fields that contain separators break the reader. Clean such files first, or import them into the built-in database *(judgement)*.
- **Write mode starts over.** A Write-mode file is rewritten from the first write after it opens. Calling `close()` and then writing again starts a fresh file *(inferred from the two Help statements)*. Keep the log open for the whole run, or use Write/Append plus a run header.
- **Two clocks.** `new Date()` is wall-clock time; model time is `time()` or `date()`. Label which one a log line carries.
- **Mid-run table swap.** Only later look-ups see the new curve. Anything already scheduled from the old curve, such as a timeout, keeps its value (compare G56).

## Reusable idea
For small, flat inputs and plain logs the Text File element is enough: stream tokens into `add_<population>(…)` or into arrays, then give the arrays to a table function. Keep large or structured data in the built-in database.

## When the co-pilot should use this
- A user supplies a delimited file of entities (vehicles, sites, staff), or a two-column curve (arrival profile, efficiency curve), and wants it read without setting up a database.
- A run log outside the console, or letting users swap a lookup curve at runtime through a file chooser.
- Related: `basicmodels/feeding-a-collection-from-access-database.md` (external database rows → agents), `videos/excel-round-trip-results-and-cloud.md` (built-in database route), G19 (execution log).
