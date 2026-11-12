# Atrial Fibrillation Monitoring Ontology (AFMO)

[![DOI](https://zenodo.org/badge/711852941.svg)](https://doi.org/10.5281/zenodo.24157942)

The Atrial Fibrillation Monitoring Ontology (AFMO) is an ontology for AI-based monitoring of atrial fibrillation (AF). It extends the [Personal Health Monitoring Ontology (PHMO)](https://mbithenzomo.github.io/phmo/), a reusable general ontology for AI-based personal health monitoring applications. The PHMO defines how personal health monitoring concepts are modelled. The AFMO defines which concepts are modelled for AF.

The AFMO supports three main functionalities for AF: AF risk assessment, AF episode prediction, and intervention recommendation. AF risk is assessed by a hybrid Bayesian network, using risk factors such as age group, comorbidities, ECG characteristics, and lifestyle factors. AF episodes are predicted from ECG observations by a deep neural network. The expected utility of recommended interventions, such as alcoholism counselling or angiotensin receptor blocker therapy, is calculated by a Bayesian decision network. Each output is linked to the model that generated it, the inputs it was based on, and the datasets used to train and test the model. AF risk relationships and interventions are also linked to supporting scientific evidence, such as clinical guidelines and systematic reviews.

| | |
|---|---|
| **Ontology IRI** | `http://purl.org/afmo` |
| **Current version** | 3.0 (`http://purl.org/afmo/3.0`) |
| **Previous version** | 2.2 (`http://purl.org/afmo/2.2`) |
| **Imports** | [PHMO](https://mbithenzomo.github.io/phmo/) 1.0 (`http://purl.org/phmo/1.0`) |
| **Documentation** | https://mbithenzomo.github.io/afmo |
| **Creator** | Mbithe Nzomo |
| **Licence** | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

## Scope

The AFMO adds the following AF-specific concepts to the PHMO:

- **AF outputs:** AF risk assessments and risk statuses, and AF episodes, episode predictions, and prediction statuses.
- **AF risk factors:** the risk factors selected for AF within each PHMO risk factor category.
  - *Anthropometric:* height group.
  - *Demographic:* age group, and race or ethnicity.
  - *Comorbidity:* cardiovascular disease, chronic obstructive pulmonary disease, diabetes mellitus, hypertension, kidney disease, and sleep apnoea.
  - *ECG:* prolonged PR interval, PR interval variation, prolonged P-wave, P-wave variation, prolonged RR interval, and RR interval variation.
  - *Lifestyle:* alcohol misuse and smoking status.
- **ECG data:** ECG devices, ECG sensors and their leads, and ECG observations.
- **Medical conditions:** AF and its comorbidities, reused from the Human Disease Ontology.
- **Medical actions:** AF-relevant interventions, such as alcoholism counselling, angiotensin receptor blocker therapy, electrocardiography, and echocardiography, reused from the Medical Action Ontology (MAxO).
- **Example individuals:** monitored persons, clinicians, and caregivers; sensor observations; risk relationships, risk assessments, episode predictions, interventions, and explanations; and the models, datasets, evidence, and publications behind them.

Version 3.0 defines 26 classes, 26 object properties, 1 data property, and 123 individuals in the `afmo` namespace.

## Relationship to the PHMO

The AFMO imports the PHMO and builds on its general concepts, such as monitored persons, observations, risk relationships, models, interventions, evidence, and explanations. For tools that do not follow imports, the AFMO file also contains a copy of the PHMO concepts, so it can be used on its own. General concepts use the `phmo` prefix, and AF-specific concepts use the `afmo` prefix.

## Reused ontologies

In addition to the ontologies reused through the [PHMO](https://github.com/mbithenzomo/phmo#reused-ontologies), the AFMO reuses concepts from the following ontologies:

- Human Disease Ontology (DO)
- Medical Action Ontology (MAxO)

Health domain concepts have been manually cross-referenced to concepts from the Unified Medical Language System (UMLS) metathesaurus.

## Files

- `afmo.rdf`: the latest version of the ontology in RDF/XML.
- `afmo2.2_to_afmo3.0_phmo1.0_renames.csv`: the mapping from AFMO 2.2 terms to their new IRIs in AFMO 3.0 and PHMO 1.0.
- `docs/`: documentation generated with [WIDOCO](https://github.com/dgarijo/Widoco), and versioned copies of the ontology.

## Version history

- **3.0:** general personal health monitoring concepts were moved to the new [PHMO](https://mbithenzomo.github.io/phmo/), which the AFMO now imports. Moved terms changed from the `afmo` namespace to the `phmo` namespace; see `afmo2.2_to_afmo3.0_phmo1.0_renames.csv` for the full mapping. `afmo:ECG_sensor` was renamed `afmo:ECGSensor`.
- **2.2:** the last version of the AFMO as a single application ontology without the PHMO.

## Authorship and attributions

### Author

Mbithe Nzomo

Affiliations:
*University of Cape Town ([UCT](https://uct.ac.za/))*;
*Adaptive and Cognitive Systems Lab at the Centre for Artificial Intelligence Research ([ACS Lab at CAIR](https://www.cair.org.za/group/1))*;
*Artificial Intelligence Research Unit ([AIRU](https://uct.ac.za/))*

## How to cite

If you use find the AFMO useful, please cite it as:

> Nzomo, M. (2026). *Atrial Fibrillation Monitoring Ontology (AFMO)* (Version 3.0). Zenodo. https://doi.org/

```bibtex
@software{nzomo_afmo_2026,
    title = {Atrial Fibrillation Monitoring Ontology ({AFMO})},
    author = {Nzomo, Mbithe},
    version = {3.0},
    year = {2026},
    publisher = {Zenodo},
    doi = {10.5281/zenodo.24157942},
    url = {https://doi.org/10.5281/zenodo.24157942},
}
```

If you use the general concepts, please cite the [PHMO](https://github.com/mbithenzomo/phmo#how-to-cite).
