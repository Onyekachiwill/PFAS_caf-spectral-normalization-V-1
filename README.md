# PFAS_caf-spectral-normalization-V-1
Python workflow for baseline correction, CaF molecular-band integration, reference-area normalization, visualization, statistics, and validation of chalk and PFAS-related optical emission spectra.

# Method A: CaF Spectral Normalization and Analysis

This repository contains a Python workflow for processing repeated optical-emission spectra from chalk and PFAS-containing samples. The method isolates the calcium fluoride (CaF) molecular-band region, applies a two-point linear baseline correction, normalizes the corrected signal to a reference-band area, generates per-shot and averaged plots, and exports descriptive statistics and validation checks.

The current example labels used by the plotting code are `Chalk`, `PFAS1`, and `PFAS2`, but the main processing workflow accepts any sample name represented by a subfolder in `Raw_Data/`.

## Method summary

For each spectrum, the workflow:

1. Reads wavelength and intensity values from a CSV file.
2. constructs a two-point linear baseline using the measured intensities nearest 603.0 and 609.5 nm;
3. subtracts the baseline from the raw spectrum;
4. integrates the baseline-corrected CaF signal from 604.5 to 609.0 nm;
5. integrates the raw reference signal from 615.0 to 617.0 nm;
6. divides the corrected spectrum and integrated CaF area by the reference area;
7. saves plots, tabulated measurements, summary statistics, and a validation report.

## Default parameters

| Parameter | Default | Purpose |
|---|---:|---|
| `baseline_start` | 603.0 nm | First anchor used to construct the linear baseline |
| `baseline_end` | 609.5 nm | Second anchor used to construct the linear baseline |
| `caf_start` | 604.5 nm | Lower boundary of the integrated CaF molecular-band region |
| `caf_end` | 609.0 nm | Upper boundary of the integrated CaF molecular-band region |
| `ref_start` | 615.0 nm | Lower boundary of the reference integration region |
| `ref_end` | 617.0 nm | Upper boundary of the reference integration region |
| `CA_LINE` | 610.27 nm | Ca I marker used only in overlay figures |
| Histogram bins | 20 | Number of bins used for each sample distribution |
| Outlier threshold | 3 standard deviations | Flags ratios more than three sample SDs from their sample mean |
| Figure resolution | 300 dpi | Resolution of saved PNG figures |

The spectral areas are calculated with trapezoidal numerical integration (`numpy.trapz`) over all recorded wavelength points inside the inclusive limits.

## Baseline correction

Let the spectrum be intensity \(I(\lambda)\). The program identifies the recorded wavelength points nearest the two requested baseline anchors:

- \(\lambda_1 \approx 603.0\ \text{nm}\)
- \(\lambda_2 \approx 609.5\ \text{nm}\)

It constructs a straight baseline \(B(\lambda)\) between the measured intensities at those points and calculates:

\[
I_{corrected}(\lambda)=I(\lambda)-B(\lambda).
\]

`numpy.interp` is evaluated across the complete wavelength array. Outside the two anchor wavelengths, it uses the corresponding endpoint baseline value rather than linearly extrapolating the baseline.

## Integration and normalization

### Corrected CaF area

The CaF molecular-band area is integrated from 604.5 to 609.0 nm using the baseline-corrected intensity:

\[
A_{CaF}=\int_{604.5}^{609.0} I_{corrected}(\lambda)\,d\lambda.
\]

### Reference area

The reference area is integrated from 615.0 to 617.0 nm using the **raw, uncorrected intensity**:

\[
A_{Ref}=\int_{615.0}^{617.0} I(\lambda)\,d\lambda.
\]

### Normalization outputs

The workflow creates two normalization outputs:

1. **Normalized spectrum**

   \[
   I_{normalized}(\lambda)=\frac{I_{corrected}(\lambda)}{A_{Ref}}.
   \]

   This full spectral array is used for the per-shot normalized plots, sample mean spectra, mean ± SD plots, and the average overlay.

2. **Normalized integrated response**

   \[
   R=\frac{A_{CaF}}{A_{Ref}}.
   \]

   This scalar is saved as `ACaF_ARef` in `MethodA_Results.csv` and is used for the summary statistics, histogram, box plot, violin plot, and outlier analysis.

If `ARef` is exactly zero, the code records the ratio as `0`. In that case, the value stored internally as the normalized spectrum is the corrected spectrum without division. The validation report separately counts reference areas satisfying `ARef <= 0`.

## Input data

Place spectra in sample-specific folders under `Raw_Data/`:

```text
Raw_Data/
├── Chalk/
│   ├── spectrum_001.csv
│   └── spectrum_002.csv
├── PFAS1/
│   ├── spectrum_001.csv
│   └── spectrum_002.csv
└── PFAS2/
    ├── spectrum_001.csv
    └── spectrum_002.csv
```

Each CSV file must contain these exact, case-sensitive column names:

```csv
wavelength,intensity
603.000,125.4
603.010,127.1
```

Files are sorted by filename, and the workflow assigns shot numbers sequentially beginning at 1. Sample names are taken directly from the subfolder names.

All spectra processed in a single run should use the same wavelength grid. The program retains the wavelength array from the first successfully processed spectrum when it creates average plots.

## Installation

Python 3.9 or later is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install numpy pandas matplotlib
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Running the analysis

From the repository root, run:

```bash
python run_method_a.py
```

The default paths are defined near the top of `run_method_a.py`:

```python
INPUT_FOLDER = "Raw_Data"
OUTPUT_FOLDER = os.path.join("Results", "MethodA")
```

To change the spectral windows, edit the defaults in the `MethodA` constructor in `method_a.py`, or initialize `MethodA` with alternative values in `method_a_runner.py`.

## Outputs

The standard workflow writes the following files under `Results/MethodA/`:

```text
Results/MethodA/
├── MethodA_Results.csv
├── SummaryStatistics.csv
├── MethodA_Validation_Report.txt
├── Histogram.png
├── Boxplot.png
├── ViolinPlot.png
├── Average/
│   ├── <sample>.png
│   └── Overlay.png
└── <sample>/
    ├── Baseline/
    │   └── Shot_<number>.png
    └── Normalized/
        └── Shot_<number>.png
```

### `MethodA_Results.csv`

| Column | Meaning |
|---|---|
| `Sample` | Sample-folder name |
| `Shot` | Sequential file number within the sample |
| `ACaF` | Integrated baseline-corrected area from 604.5–609.0 nm |
| `ARef` | Integrated raw reference area from 615.0–617.0 nm |
| `ACaF_ARef` | Normalized integrated response, `ACaF / ARef` |

### `SummaryStatistics.csv`

For `ACaF_ARef`, the code reports the count, mean, median, sample standard deviation, minimum, and maximum for each sample.

### Validation report

`MethodA_Validation_Report.txt` reports:

- number of spectra and samples;
- missing values;
- non-positive reference areas;
- negative corrected CaF areas;
- infinite and missing ratios;
- sample-level ratio statistics; and
- potential within-sample outliers based on the mean ± 3 sample standard deviations rule.

The validation report identifies conditions for review; it does not remove spectra or outliers automatically.

## Optional overlay module

`method_a_overlay.py` defines additional raw and normalized comparison plots, including fixed colors for `Chalk`, `PFAS1`, and `PFAS2`. The standard `run_method_a.py` workflow does not currently instantiate this class, so its `Raw_Overlay/` and `Sample_Comparison/` figures are not produced unless the module is called separately.

## Repository files

| File | Role |
|---|---|
| `run_method_a.py` | Main entry point and input-folder traversal |
| `method_a.py` | Baseline correction, integration, and normalization |
| `method_a_runner.py` | Coordinates processing, plotting, and result collection |
| `method_a_plot.py` | Per-shot, average, and overlay figures |
| `method_a_result.py` | Shot-level CSV output |
| `method_a_statistics.py` | Descriptive statistics and distribution plots |
| `method_a_validation.py` | Quality-control and outlier report |
| `method_a_overlay.py` | Optional raw and normalized sample-comparison figures |

## Interpretation notes

- A larger `ACaF_ARef` value means that the integrated, baseline-corrected CaF-region signal is larger relative to the selected raw reference-region area.
- The result is a normalized analytical response; the code alone does not establish PFAS identity, concentration, detection limits, or statistical significance.
- Negative `ACaF` or `ACaF_ARef` values can occur when the corrected signal lies below the constructed baseline within the CaF integration window.
- The current method applies no smoothing, wavelength alignment, background model beyond the two-point baseline, blank subtraction, or automatic removal of invalid spectra.
- Spectral limits and the reference band should be justified for the instrument, samples, and analytical objective before scientific interpretation.

## Reproducibility

When reporting results, record the software version, dependency versions, wavelength grid, number of spectra per sample, acquisition conditions, baseline anchors, integration limits, reference window, and any exclusions made before or after this workflow.

## License

No license is included in the current files. Add a license before inviting reuse. If you want others to reuse and modify the code with attribution, the MIT or BSD 3-Clause license may be suitable; choose a license consistent with your institution's requirements.

## Citation

If this repository supports a publication, add the article or archived software citation here. A DOI-backed software release can be created by archiving a GitHub release with a service such as Zenodo.
