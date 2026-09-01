import os
import glob
import pandas as pd

from method_a_runner import MethodARunner
from method_a_statistics import MethodAStatistics
from method_a_validation import MethodAValidation


##############################################################
# USER SETTINGS
##############################################################

INPUT_FOLDER = "Raw_Data"
OUTPUT_FOLDER = os.path.join("Results", "MethodA")

##############################################################


def main():

    print("\n" + "=" * 60)
    print("METHOD A ANALYSIS")
    print("=" * 60)

    # Create output folder
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Initialize runner
    runner = MethodARunner(OUTPUT_FOLDER)

    ##########################################################
    # Process all samples
    ##########################################################

    groups = sorted(os.listdir(INPUT_FOLDER))

    total_files = 0

    for sample in groups:

        sample_folder = os.path.join(INPUT_FOLDER, sample)

        if not os.path.isdir(sample_folder):
            continue

        print(f"\nProcessing Sample : {sample}")

        files = sorted(
            glob.glob(
                os.path.join(sample_folder, "*.csv")
            )
        )

        print(f"Total Spectra : {len(files)}")

        for shot, file in enumerate(files, start=1):

            print(f"   Shot {shot:03d} : {os.path.basename(file)}")

            try:

                df = pd.read_csv(file)

                # Read spectrum
                wavelength = df["wavelength"].to_numpy()
                intensity = df["intensity"].to_numpy()

                # Process one spectrum
                runner.process_shot(

                    wavelength=wavelength,
                    intensity=intensity,
                    sample=sample,
                    shot=shot

                )

                total_files += 1

            except Exception as e:

                print(f"      ERROR : {file}")
                print(e)

    ##########################################################
    # Finish processing
    ##########################################################

    runner.finish()

    ##########################################################
    # Statistics
    ##########################################################

    results_file = os.path.join(
        OUTPUT_FOLDER,
        "MethodA_Results.csv"
    )

    if os.path.exists(results_file):

        results = pd.read_csv(results_file)

        print("\nGenerating Statistics...")

        statistics = MethodAStatistics(OUTPUT_FOLDER)

        statistics.generate(results)

        print("Statistics Complete")

        ######################################################
        # Validation
        ######################################################

        print("\nRunning Validation...")

        validator = MethodAValidation(OUTPUT_FOLDER)

        validator.validate(results)

        print("Validation Complete")

    else:

        print("\nERROR:")
        print("MethodA_Results.csv was not created.")

    ##########################################################
    # Summary
    ##########################################################

    print("\n" + "=" * 60)
    print("METHOD A COMPLETE")
    print("=" * 60)

    print(f"Total Spectra Processed : {total_files}")
    print(f"Output Folder           : {OUTPUT_FOLDER}")

    print("=" * 60)


##############################################################

if __name__ == "__main__":

    main()