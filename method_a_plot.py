import os
import numpy as np
import matplotlib.pyplot as plt


class MethodAPlotter:

    COLORS = {
        "Chalk": "tab:blue",
        "PFAS1": "tab:orange",
        "PFAS 1": "tab:orange",
        "PFAS2": "tab:green",
        "PFAS 2": "tab:green"
    }

    def __init__(self, output_dir):

        self.output_dir = output_dir

        os.makedirs(output_dir, exist_ok=True)


    def save_baseline_plot(
        self,
        wavelength,
        raw,
        baseline,
        corrected,
        sample,
        shot,
        caf=(604.5,609.0),
        ref=(615.0,617.0)
    ):

        plt.figure(figsize=(9,5))

        mask = (wavelength>=600) & (wavelength<=617)

        x = wavelength[mask]

        raw = raw[mask]
        base = baseline[mask]
        corr = corrected[mask]

        plt.plot(x, raw,
                 color='black',
                 lw=1.2,
                 label='Raw')

        plt.plot(x, base,
                 '--',
                 color='red',
                 lw=2,
                 label='Baseline')

        plt.plot(x, corr,
                 color='blue',
                 lw=1.5,
                 label='Corrected')

        plt.fill_between(
            x,
            0,
            corr,
            where=(x>=caf[0])&(x<=caf[1]),
            color='green',
            alpha=.35,
            label='CaF Region'
        )

        plt.fill_between(
            x,
            0,
            corr,
            where=(x>=ref[0])&(x<=ref[1]),
            color='orange',
            alpha=.35,
            label='Reference Region'
        )

        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Intensity")
        plt.title(f"{sample}  Shot {shot}")

        plt.legend()

        plt.tight_layout()

        folder = os.path.join(
            self.output_dir,
            sample,
            "Baseline"
        )

        os.makedirs(folder,exist_ok=True)

        plt.savefig(
            os.path.join(
                folder,
                f"Shot_{shot:03d}.png"
            ),
            dpi=300
        )

        plt.close()

    def save_normalized_plot(
        self,
        wavelength,
        normalized,
        sample,
        shot
    ):

        mask = (wavelength>=604.5)&(wavelength<=609.0)

        plt.figure(figsize=(8,4))

        plt.plot(
            wavelength[mask],
            normalized[mask],
            color='blue',
            lw=2
        )

        plt.fill_between(
            wavelength[mask],
            0,
            normalized[mask],
            color='green',
            alpha=.35
        )

        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Corrected Intensity / ARef")

        plt.title(
            f"{sample}  Shot {shot}"
        )

        plt.tight_layout()

        folder = os.path.join(
            self.output_dir,
            sample,
            "Normalized"
        )

        os.makedirs(folder,exist_ok=True)

        plt.savefig(
            os.path.join(
                folder,
                f"Shot_{shot:03d}.png"
            ),
            dpi=300
        )

        plt.close()

    def save_average(
        self,
        wavelength,
        spectra,
        sample
    ):

        avg = np.mean(spectra,axis=0)
        std = np.std(spectra,axis=0)

        mask = (wavelength>=604.5)&(wavelength<=609.0)

        x = wavelength[mask]

        y = avg[mask]
        s = std[mask]

        plt.figure(figsize=(8,4))

        plt.plot(
            x,
            y,
            lw=2,
            color='blue'
        )

        plt.fill_between(
            x,
            y-s,
            y+s,
            alpha=.25
        )

        plt.fill_between(
            x,
            0,
            y,
            alpha=.30,
            color='green'
        )

        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Corrected Intensity / ARef")

        plt.title(f"{sample} Average")

        plt.tight_layout()

        folder = os.path.join(
            self.output_dir,
            "Average"
        )

        os.makedirs(folder,exist_ok=True)

        plt.savefig(
            os.path.join(
                folder,
                f"{sample}.png"
            ),
            dpi=300
        )

        plt.close()

    def save_overlay(
        self,
        wavelengths,
        averages
    ):

        plt.figure(figsize=(9,5))

        for sample,y in averages.items():

            wavelength = wavelengths[sample]
            mask = (wavelength>=604.5)&(wavelength<=609.0)

            x = wavelength[mask]

            plt.plot(
                x,
                y[mask],
                lw=2,
                label=sample
            )

        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Corrected Intensity / ARef")

        plt.title("Method A Overlay")

        plt.legend()

        plt.tight_layout()

        folder = os.path.join(
            self.output_dir,
            "Average"
        )

        os.makedirs(folder,exist_ok=True)

        plt.savefig(
            os.path.join(
                folder,
                "Overlay.png"
            ),
            dpi=300
        )

        plt.close()

    def save_comparison_overlays(
        self,
        wavelengths,
        raw_spectra,
        raw_averages
    ):

        """Save full-range and zoomed overlays of sample-mean spectra.

        Each raw shot is maximum-normalized within the displayed wavelength
        range before the normalized shots are averaged for each sample.
        This visualization pathway is independent of Method A calculations.
        """

        folder = os.path.join(
            self.output_dir,
            "Average_Overlays"
        )

        os.makedirs(folder, exist_ok=True)

        # Normalize every shot independently in the whole-spectrum window,
        # then average the normalized shots within each sample.
        whole_normalized_averages = self._average_max_normalized_shots(
            wavelengths,
            raw_spectra,
            200,
            900
        )

        # Repeat the operation independently in the zoomed window so its
        # normalization maximum is determined only from 500-700 nm.
        zoom_normalized_averages = self._average_max_normalized_shots(
            wavelengths,
            raw_spectra,
            500,
            700
        )

        self._save_average_overlay(
            wavelengths=wavelengths,
            averages=whole_normalized_averages,
            x_min=200,
            x_max=900,
            ylabel="Normalized Intensity",
            title="Whole LIBS Spectrum (Mean of All Shots)",
            filename=os.path.join(
                folder,
                "Normalized_Whole_200_900nm.png"
            )
        )

        self._save_average_overlay(
            wavelengths=wavelengths,
            averages=zoom_normalized_averages,
            x_min=500,
            x_max=700,
            ylabel="Normalized Intensity",
            title="Normalized LIBS Spectrum: 500-700 nm (Mean of All Shots)",
            filename=os.path.join(
                folder,
                "Normalized_Zoom_500_700nm.png"
            )
        )

        self._save_average_overlay(
            wavelengths=wavelengths,
            averages=raw_averages,
            x_min=200,
            x_max=900,
            ylabel="Raw Intensity",
            title="Raw Unprocessed LIBS Spectrum (Mean of All Shots)",
            filename=os.path.join(
                folder,
                "Raw_Averaged_Overlay_200_900nm.png"
            )
        )

    def _average_max_normalized_shots(
        self,
        wavelengths,
        raw_spectra,
        x_min,
        x_max
    ):

        normalized_averages = {}

        for sample, spectra in raw_spectra.items():

            wavelength = wavelengths[sample]
            mask = (wavelength >= x_min) & (wavelength <= x_max)
            spectra = np.asarray(spectra, dtype=float)

            normalized_shots = []

            for shot_spectrum in spectra:

                if np.any(mask):
                    shot_maximum = np.max(shot_spectrum[mask])
                else:
                    shot_maximum = np.nan

                if not np.isfinite(shot_maximum) or shot_maximum == 0:
                    normalized_shots.append(shot_spectrum.copy())
                else:
                    normalized_shots.append(shot_spectrum / shot_maximum)

            normalized_averages[sample] = np.mean(
                np.asarray(normalized_shots),
                axis=0
            )

        return normalized_averages

    def _save_average_overlay(
        self,
        wavelengths,
        averages,
        x_min,
        x_max,
        ylabel,
        title,
        filename
    ):

        plt.figure(figsize=(12, 7))

        for sample, spectrum in averages.items():

            wavelength = wavelengths[sample]
            spectrum = np.asarray(spectrum)
            mask = (wavelength >= x_min) & (wavelength <= x_max)

            plt.plot(
                wavelength[mask],
                spectrum[mask],
                lw=1.5,
                color=self.COLORS.get(sample),
                label=sample
            )

        plt.xlim(x_min, x_max)
        plt.xlabel("Wavelength (nm)")
        plt.ylabel(ylabel)
        plt.title(title)
        plt.grid(alpha=0.25)
        plt.legend()
        plt.tight_layout()
        plt.savefig(filename, dpi=300)
        plt.close()
