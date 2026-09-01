"""
method_a_overlay.py

Overlay visualizations for Method A.

Generates

1. Raw spectral overlay
2. Chalk vs PFAS1 raw comparison
3. Chalk vs PFAS2 raw comparison
4. Normalized spectral overlay
5. Average spectra (Mean ± SD)

Author:
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


class MethodAOverlay:

    # --------------------------------------------
    # Spectral Regions
    # --------------------------------------------

    CAF_START = 604.5
    CAF_END = 609.0
    CA_LINE = 610.27

    COLORS = {
        "Chalk": "black",
        "PFAS1": "tab:blue",
        "PFAS2": "tab:red"
    }

    # --------------------------------------------

    def __init__(self, results_dir):

        self.results_dir = Path(results_dir)

        self.raw_dir = self.results_dir / "Raw_Overlay"
        self.raw_dir.mkdir(parents=True, exist_ok=True)

        self.overlay_dir = self.results_dir / "Sample_Comparison"
        self.overlay_dir.mkdir(parents=True, exist_ok=True)

    # ==========================================================
    # Helper
    # ==========================================================

    def _decorate_caf_region(self):

        plt.axvspan(
            self.CAF_START,
            self.CAF_END,
            color="limegreen",
            alpha=0.18,
            label="CaF Molecular Band"
        )

        plt.axvline(
            self.CA_LINE,
            linestyle="--",
            color="purple",
            linewidth=2,
            label="Ca I (610.27 nm)"
        )

        ymax = plt.ylim()[1]

        plt.text(
            (self.CAF_START + self.CAF_END)/2,
            ymax*0.93,
            "CaF Molecular Band",
            ha="center",
            color="darkgreen",
            fontsize=10
        )

        plt.text(
            self.CA_LINE + 0.06,
            ymax*0.78,
            "Ca I",
            rotation=90,
            fontsize=9,
            color="purple"
        )

    # ==========================================================
    # Figure 1
    # Raw Overlay
    # ==========================================================

    def save_raw_overlay(self, wavelengths, raw_spectra):

        plt.figure(figsize=(10,6))

        means = {}

        for sample, spectra in raw_spectra.items():

            means[sample] = np.mean(np.asarray(spectra), axis=0)

            plt.plot(
                wavelengths[sample],
                means[sample],
                lw=2,
                color=self.COLORS.get(sample),
                label=sample
            )

        plt.xlim(600,615)

        self._decorate_caf_region()

        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Raw Intensity")
        plt.title("Raw Spectral Overlay")

        plt.legend()

        plt.tight_layout()

        plt.savefig(
            self.raw_dir/"Raw_All.png",
            dpi=300
        )

        plt.close()

        # ----------------------------------------
        # Chalk vs PFAS1
        # ----------------------------------------

        if "Chalk" in means and "PFAS1" in means:

            plt.figure(figsize=(10,6))

            plt.plot(
                wavelengths["Chalk"],
                means["Chalk"],
                color="black",
                lw=2,
                label="Chalk"
            )

            plt.plot(
                wavelengths["PFAS1"],
                means["PFAS1"],
                color="tab:blue",
                lw=2,
                label="PFAS1"
            )

            plt.xlim(600,615)

            self._decorate_caf_region()

            plt.xlabel("Wavelength (nm)")
            plt.ylabel("Raw Intensity")
            plt.title("Raw Spectra: Chalk vs PFAS1")

            plt.legend()

            plt.tight_layout()

            plt.savefig(
                self.raw_dir/"Chalk_vs_PFAS1.png",
                dpi=300
            )

            plt.close()

        # ----------------------------------------
        # Chalk vs PFAS2
        # ----------------------------------------

        if "Chalk" in means and "PFAS2" in means:

            plt.figure(figsize=(10,6))

            plt.plot(
                wavelengths["Chalk"],
                means["Chalk"],
                color="black",
                lw=2,
                label="Chalk"
            )

            plt.plot(
                wavelengths["PFAS2"],
                means["PFAS2"],
                color="tab:red",
                lw=2,
                label="PFAS2"
            )

            plt.xlim(600,615)

            self._decorate_caf_region()

            plt.xlabel("Wavelength (nm)")
            plt.ylabel("Raw Intensity")
            plt.title("Raw Spectra: Chalk vs PFAS2")

            plt.legend()

            plt.tight_layout()

            plt.savefig(
                self.raw_dir/"Chalk_vs_PFAS2.png",
                dpi=300
            )

            plt.close()

    # ==========================================================
    # Figure 2
    # Normalized Overlay
    # ==========================================================

    def save_normalized_overlay(self,
                                wavelengths,
                                normalized_average):

        plt.figure(figsize=(10,6))

        for sample, spectrum in normalized_average.items():

            plt.plot(
                wavelengths[sample],
                spectrum,
                lw=2,
                color=self.COLORS.get(sample),
                label=sample
            )

        plt.xlim(603.5,611)

        self._decorate_caf_region()

        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Normalized Intensity")

        plt.title("Normalized Spectral Overlay")

        plt.legend()

        plt.tight_layout()

        plt.savefig(
            self.overlay_dir/"Normalized_Overlay.png",
            dpi=300
        )

        plt.close()

    # ==========================================================
    # Figure 3
    # Mean ± SD Overlay
    # ==========================================================

    def save_average_overlay(self,
                             wavelengths,
                             spectra_dict):

        plt.figure(figsize=(10,6))

        for sample, spectra in spectra_dict.items():

            spectra = np.asarray(spectra)

            mean = spectra.mean(axis=0)

            sd = spectra.std(axis=0)

            wl = wavelengths[sample]

            plt.plot(
                wl,
                mean,
                lw=2,
                color=self.COLORS.get(sample),
                label=sample
            )

            plt.fill_between(
                wl,
                mean-sd,
                mean+sd,
                alpha=0.20,
                color=self.COLORS.get(sample)
            )

        plt.xlim(603.5,611)

        self._decorate_caf_region()

        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Normalized Intensity")

        plt.title("Average Spectra (Mean ± SD)")

        plt.legend()

        plt.tight_layout()

        plt.savefig(
            self.overlay_dir/"Average_Overlay.png",
            dpi=300
        )

        plt.close()