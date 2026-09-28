# Pattern card — AnyLogic Cloud API: running uploaded models from Python (and Java, JS, REST)
- **Source:** AnyLogic video "AnyLogic Cloud" (https://youtu.be/F93iENzUcWc) — distilled, original wording
- **Paradigm:** Method
- **Problem it solves:** Scripting scenario sweeps, replications and file-driven runs of a Cloud model, and getting the results back as data instead of reading them off the dashboard.

## Mechanism
- **Provenance.** The video shows only the web UI. The API facts here are supplementary, taken from AnyLogic Cloud Help 2.6.0/2.6.1 (Dec 2025) and AnyLogic's Cloud API blog posts, and read on 2026-09-28.
- **Access:** subscribers and Private Cloud users only, with User or Developer rights on the model. The key is in the Cloud profile; REST calls send it as the header `Authorization: <API key>`. AnyLogic publishes a demo key and demo models (e.g. "Service System Demo") for evaluation.
- **Clients:** Python (synchronous); Java (synchronous and asynchronous); JavaScript, which can also embed an animated run in your own page; plain REST at `https://cloud.anylogic.com/api/open/8.5.0`.
- **Object chain:** `CloudClient` → model → version → `Inputs` → `ModelRun` → outputs. A `ModelRun` is a simulation, parameter variation, variation with replications, or Monte Carlo run.
- **The result store is the same as the UI's.** A run executes only when that (version, inputs) pair has no stored result.

## Resources
n/a

## Key settings worth copying
```python
# pip install https://cloud.anylogic.com/files/api-8.5.0/clients/anylogiccloudclient-8.5.0-py3-none-any.whl
from anylogiccloudclient.client.cloud_client import CloudClient
client = CloudClient(API_KEY)                  # Private Cloud: CloudClient(API_KEY, CLOUD_URL)
version = client.get_latest_model_version("Fleet model")
inputs = client.create_inputs_from_experiment(version, "Baseline")  # or create_default_inputs(version)
inputs.set_input("Fleet size", 40)             # Cloud labels; names are case-insensitive
out = client.create_simulation(inputs).get_outputs_and_run_if_absent()
print(out.names()); print(out.value(out.find_name_including("delivery")))
```
- **Sweeps and replications:**
  - `inputs.set_range_input(name, min, max, step)`, then `client.create_parameter_variation(inputs)`.
  - Add `inputs.set_number_of_replications(n)` (default 3) and call `create_parameter_variation_with_replications(inputs)` instead.
  - Monte Carlo 1st order: `set_number_of_replications(n)`, then `create_monte_carlo(inputs)`.
- **Multi-run outputs:**
  - Name the outputs you want, e.g. `get_outputs_and_run_if_absent(["Utilization|Server utilization"])`. If you name none, only scalar outputs come back.
  - Read them with `get_values_of_input()`, `get_values_of_output()` or `get_raw_data()` (a table with a header row).
- **System inputs** have braced names and exist in every model, e.g. `{STOP_TIME}`. AnyLogic's 2018 API deck also shows `{STOP_MODE}` and `{MAX_MEMORY_MB}`. List all inputs with `inputs.names()`.
- **Files:**
  - Input: `h = client.upload_file("data.xlsx")` returns a hash; pass it with `inputs.set_input("Data", h)`.
  - Output: a file comes back as a resource. Use `f = out.value("Data")`, then `client.download_file(f, "out_" + f.name)`.
- **Async control:**
  - `run()` does not wait.
  - `wait_for_completion(polling_period)` polls; the default period is 5000 ms.
  - Also `get_status()`, `get_progress()["total"]` and `stop()`.
  - `get_outputs()` fails with 404 if the run does not exist.

## KPIs instrumented
n/a. The script reads whatever scalar Outputs the model exports (see `videos/cloud-run-semantics-and-access.md`).

## Pitfalls
- **Output names are composite labels** such as `"Chart|Item"`, and an Output often appears as `"X|X"`. Look names up with `names()` or `find_name_including()` rather than guessing.
- **`set_input()` validates nothing.** A misspelt input name fails only when the run starts.
- **Identical inputs return the stored run.** A custom optimizer that re-scores a candidate gets the same single sample again. Variability comes only from replication-type runs.
- **Monte Carlo 2nd order** (distribution-type inputs) is not available through the API as of Help 2.6.0. Run it in the web UI.
- **The function name varies.** The Help reference table spells it `create_parameter_variation_with_replication`, but its example uses `..._replications`. Check `dir(client)` for your client version.
- **Polling traffic.** Each parallel `wait_for_completion()` polls over HTTP; raise `polling_period` for large batches.
- **Free accounts lack full API access.** Do not plan a thesis pipeline on it without a subscription or Private Cloud.

## Reusable idea
Script the experiment design (factors, levels, replications) against one fixed model version, and pull the results as tables. The result store makes re-running the analysis free and reproducible.

## When the co-pilot should use this
| Need | Route |
|---|---|
| External code runs many scenarios or replications of a finished model, with results going to Python, R or BI | Cloud API (subscription or Private Cloud) |
| Step-wise control or RL training from Python | Alpyne (`templates/rl-pipeline/`) |
| The running model must call Python (ML predictor, solver) | Pypeline (`basicmodels/basic-functionality-interactive.md`) |
| Embedding in on-premises software with no Cloud | Standalone export and a custom launcher (`basicmodels/launching-anylogic-model-from-external-application.md`) |
| PLE or thesis-scale study | Desktop Parameter Variation / Monte Carlo experiments |
