import numpy as np


class MethodA:

    def __init__(
        self,
        baseline_start=603.0,
        baseline_end=609.5,
        caf_start=604.5,
        caf_end=609.0,
        ref_start=615.0,
        ref_end=617.0,
    ):

        self.baseline_start = baseline_start
        self.baseline_end = baseline_end

        self.caf_start = caf_start
        self.caf_end = caf_end

        self.ref_start = ref_start
        self.ref_end = ref_end


    def integrate(self, wavelength, intensity, start, end):

        mask = (wavelength >= start) & (wavelength <= end)

        return np.trapz(
            intensity[mask],
            wavelength[mask]
        )


    def baseline_correct(self, wavelength, intensity):

        idx1 = np.argmin(np.abs(wavelength - self.baseline_start))
        idx2 = np.argmin(np.abs(wavelength - self.baseline_end))

        x1 = wavelength[idx1]
        y1 = intensity[idx1]

        x2 = wavelength[idx2]
        y2 = intensity[idx2]

        baseline = np.interp(
            wavelength,
            [x1, x2],
            [y1, y2]
        )

        corrected = intensity - baseline

        return corrected, baseline


    def process(self, wavelength, intensity):

        corrected, baseline = self.baseline_correct(
            wavelength,
            intensity
        )

        ACaF = self.integrate(
            wavelength,
            corrected,
            self.caf_start,
            self.caf_end
        )

        ARef = self.integrate(
            wavelength,
            intensity,
            self.ref_start,
            self.ref_end
        )

        if ARef == 0:
            ratio = 0
        else:
            ratio = ACaF / ARef

        normalized = corrected / ARef if ARef != 0 else corrected

        return {

            "baseline": baseline,

            "corrected": corrected,

            "normalized": normalized,

            "ACaF": ACaF,

            "ARef": ARef,

            "Ratio": ratio

        }