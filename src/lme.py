import subprocess
from .settings import d

def lme():
    print('Resampling extracted features to conduct linear mixed-effects analysis')
    call_string_resample = "Rscript " + d + "/src/lme_models/resample_for_lme.R"
    resample_lme = subprocess.call(call_string_resample, shell=True)
    resample_lme

    print('Generating plots to analyse assumptions of linear mixed-effects models')
    call_string_assumptions = "Rscript " + d + "/src/lme_models/assumptions.R"
    assumptions_lme = subprocess.call(call_string_assumptions, shell=True)
    assumptions_lme

    print('Generating plots to analyse assumptions of linear mixed-effects models')
    call_string_assumptions = "Rscript " + d + "/src/lme_models/fixed_effects_plots.R"
    plots_lme = subprocess.call(call_string_assumptions, shell=True)
    plots_lme

    print('Conducting linear mixed-effects models analysis')
    call_string_assumptions = "Rscript " + d + "/src/lme_models/lme_analysis.R"
    lme_analysis = subprocess.call(call_string_assumptions, shell=True)
    lme_analysis

if __name__ == "__main__":
    lme()
