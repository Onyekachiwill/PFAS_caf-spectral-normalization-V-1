import os
import numpy as np

from method_a import MethodA
from method_a_plot import MethodAPlotter
from method_a_result import MethodAResults


class MethodARunner:

    def __init__(self, output_folder):

        self.processor = MethodA()

        self.plotter = MethodAPlotter(output_folder)

        self.results = MethodAResults(output_folder)

        self.average_spectra = {}

        self.raw_spectra = {}

        # Keep a separate wavelength grid for each sample. Different sample
        # exports may contain slightly different numbers of wavelength points.
        self.wavelengths = {}


    def process_shot(
        self,
        wavelength,
        intensity,
        sample,
        shot
    ):

        if sample not in self.wavelengths:
            self.wavelengths[sample] = np.asarray(wavelength)
        else:
            reference_wavelength = self.wavelengths[sample]

            if (
                len(wavelength) != len(reference_wavelength)
                or not np.allclose(wavelength, reference_wavelength)
            ):
                raise ValueError(
                    f"Wavelength grid mismatch within sample '{sample}' "
                    f"at shot {shot}: expected {len(reference_wavelength)} "
                    f"points but found {len(wavelength)}."
                )

        output = self.processor.process(
            wavelength,
            intensity
        )

        self.results.add(

            sample=sample,

            shot=shot,

            acaf=output["ACaF"],

            aref=output["ARef"],

            ratio=output["Ratio"]

        )

        self.plotter.save_baseline_plot(

            wavelength,

            intensity,

            output["baseline"],

            output["corrected"],

            sample,

            shot

        )

        self.plotter.save_normalized_plot(

            wavelength,

            output["normalized"],

            sample,

            shot

        )

        if sample not in self.average_spectra:

            self.average_spectra[sample] = []

        if sample not in self.raw_spectra:

            self.raw_spectra[sample] = []

        self.average_spectra[sample].append(

            output["normalized"]

        )

        self.raw_spectra[sample].append(

            np.asarray(intensity)

        )
        
    def finish(self):

        averages = {}

        raw_averages = {}

        for sample, spectra in self.average_spectra.items():

            spectra = np.array(spectra)

            sample_wavelength = self.wavelengths[sample]

            self.plotter.save_average(

                sample_wavelength,

                spectra,

                sample

            )

            averages[sample] = np.mean(

                spectra,

                axis=0

            )

            raw_averages[sample] = np.mean(

                np.asarray(self.raw_spectra[sample]),

                axis=0

            )

        self.plotter.save_overlay(

            self.wavelengths,

            averages

        )

        self.plotter.save_comparison_overlays(

            self.wavelengths,

            self.raw_spectra,

            raw_averages

        )

        self.results.save()
