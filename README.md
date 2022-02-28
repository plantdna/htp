# HTP

[Website](https://htp.plantdna.site/)

> Haplotype-tag polymorphisms (HTP) is a high-resolution, high-efficient, and low-cost molecular marker which can serve as a low cost, time, and high-throughput genotyping resources for genetic mapping, germplasm resource analysis and genomics-informed breeding in maize.

## Dependance

This project was based on python3 environment. If your operating system does not have Python3 environment installed, Please install the [Python3](https://www.python.org/downloads/) first.

## Quickstart

```bash
git clone https://github.com/plantdna/htp.git

cd htp

python3 -m venv venv

source ./venv/bin/activate

pip install -r requirements.txt

pip install --editable .
```

## Dataset Download

[⏬ Download](https://htp.plantdna.site/download/htp-template-files.zip)

## Tips

Since the paper has not been published yet, only part of the haplotype_database.csv was disclosed here. We hope to get your understanding. Thanks so much.

## Project Structure

```
.
├── LICENSE
├── README.md
├── dataset
│   ├── haplotype_database.csv
│   ├── hca_template.csv
│   ├── htp-template-files
│   ├── htp-template-files.zip
│   ├── marker_info.csv
│   ├── template_genotyping.txt
│   └── wghca_template.csv
├── requirements.txt
├── scripts
│   ├── abss
│   ├── abss_cli.py
│   ├── base_class.py
│   ├── hca
│   ├── hca_cli.py
│   ├── hlp
│   ├── hlp_cli.py
│   ├── hpb
│   ├── hpb_cli.py
│   ├── hpp
│   ├── hpp_cli.py
│   ├── ilpa
│   ├── ilpa_cli.py
│   ├── score
│   ├── score_cli.py
│   ├── snp2htp
│   ├── snp2htp_cli.py
│   ├── wghca
│   └── wghca_cli.py
└── setup.py
```

## Command Set

- Data comparison
  - [htp-snp2htp](https://github.com/plantdna/htp#snp2htp)
  - [htp-hca](https://github.com/plantdna/htp#hca)
  - [htp-wghca](https://github.com/plantdna/htp#wghca)
- Data prediction
  - [htp-hpb](https://github.com/plantdna/htp#hpb)
  - [htp-score](https://github.com/plantdna/htp#score)
  - [htp-hpp](https://github.com/plantdna/htp#hpp)
  - [htp-ilpa](https://github.com/plantdna/htp#ilpa)
  - [htp-hlp](https://github.com/plantdna/htp#hlp)
- Group analysis
  - [abss](https://github.com/plantdna/htp#abss)

## Data comparison

---

### SNP2HTP

**Description**

> Convert SNP data into HTP data

**Usage**

- mode one

```bash
(venv) (base) root:~/home/plantdna/htp$ htp-snp2htp
Please type input file path: /home/plantdna/htp/dataset/template_genotyping.txt
Please type output dir path [/home/plantdna/htp/output]:
```

- mode two

```bash
htp-snp2htp -i /home/plantdna/htp/dataset/template_genotyping.txt -o /home/plantdna/htp/output
```

**Input file**

> Maize6H-60K array data

**Output file**

> /home/plantdna/htp/output/{$genotyping_file_name}_{$timestamp}/all_htps.csv

_Output Example_
| Index | HTP_0001 | ... |
|--------------|-----------|------------|
| call_code1 | 5/5 | ... |
| call_code2 | 1/1 | ... |

### HCA

**Description**

> HTP comparison algorithm

**Usage**

- mode one

```bash
(venv) (base) root:~/home/plantdna/htp$ htp-hca
Please type input file path: /home/plantdna/htp/dataset/Data-comparison-Hybrid-1-compared-sample.csv
Please type contrast file path: /home/plantdna/htp/dataset/Data-comparison-Hybrids-200-referenced-samples.csv
Please type output dir path [/home/plantdna/htp/output]:
Please type missing string [---]:
Please type number of process [1]: 3
```

- mode two

```bash
htp-hca -i /home/plantdna/htp/dataset/Data-comparison-Hybrid-1-compared-sample.csv -c /home/plantdna/htp/dataset/Data-comparison-Hybrids-200-referenced-samples.csv -o /home/plantdna/htp/output -ms --- -p 3
```

**Input file**

- compare file path: /home/plantdna/htp/dataset/Data-comparison-Hybrid-1-compared-sample.csv
- contrast file path: /home/plantdna/htp/dataset/Data-comparison-Hybrids-200-referenced-samples.csv

_Input Example_
| Index | HTP_0001 | ... |
|--------------|-----------|------------|
| call_code1 | 5/5 | ... |
| call_code2 | 1/1 | ... |

**Output file**

> /home/plantdna/htp/output/hca*compare_result*{$timestamp}.csv

_Output Example_
| Sam1 | Sam1 | Diff_Num | Similar_Rate |
|--------------|-----------|------------|------------|
| call_code1 | call_code2 | 5 | 0.54 |

### WGHCA

**Description**

> Whole genome haplotype comparison algorithm

**Usage**

- mode one

```bash
(venv) (base) root:~/work/plantdna/htp$ htp-wghca
Please type input file path: /home/plantdna/htp/dataset/wghca_template.csv
Please type contrast file path [/]: /home/plantdna/htp/dataset/wghca_template.csv
Please type output dir path [/home/plantdna/htp/output]:
Please type similarity threshold [0.8]:
Please type missing string [---]:
Please type number of process [1]:
```

- mode two

```bash
htp-wghca -i /home/plantdna/htp/dataset/wghca_template.csv -o /home/plantdna/htp/output -c /home/plantdna/htp/dataset/wghca_template.csv -st 0.8 -ms --- -p 2
```

**Input file**

- compare file path: /home/plantdna/htp/dataset/wghca_template.csv
- contrast file path: /home/plantdna/htp/dataset/wghca_template.csv

_Input Example_
| Index | HTP_0001 | ... |
|--------------|-----------|------------|
| call_code1 | ATC/GGA | ... |
| call_code2 | ATC/GGA | ... |

**Output file**

> /home/plantdna/htp/output/wghca*compare_result*{$timestamp}.csv

_Output Example_
| Sam1 | Sam1 | Diff_Num | Similar_Rate |
|--------------|-----------|------------|------------|
| call_code1 | call_code2 | 5 | 1 |

## Data prediction

---

### HPB

**Description**

> Heterotic Pattern Building

```bash
(venv) (base) root:~/work/plantdna/htp$ htp-hpb
Please type input genotype files dir: ./
Please type output path: ./
```

**Input file**

_Input genotype files dir_

```
├── group1
├── group1
├── ...
└── groupn
```

_Input group data_
| Index | HTP_0001 | ... |
|--------------|-----------|------------|
| call_code1 | 5 | ... |
| call_code2 | 1 | ... |

**Output file**

_Output data_
| Index | HTP_0001 | ... |
|--------------|-----------|------------|
| call_code1/call_code2 | 5/1 | ... |

### Score

```bash
(venv) (base) root:~/work/plantdna/htp$ htp-score
Please type input group files dir: ./
Please type output path: ./
```

**Input file**

> HPB output dir path

### HPP

**Description**

> Heterotic Pattern Prediction

```bash
(venv) (base) root:~/work/plantdna/htp$ htp-hpp
Please type hybrid file path: ./
Please type group dataset dir: ./
Please type output path: ./
```

### ILPA

**Description**

> Inbred Line Pedigree Analysis

```bash
(venv) (base) root:~/work/plantdna/htp$ htp-ilpa
Please type input genotype files dir: /home/plantdna/htp/dataset/Jing2416-inbredX.csv
Please type output file path [/home/plantdna/htp/output]:
```

**Input file**

_Input Example_
| Index | HTP_0001 | ... |
|--------------|-----------|------------|
| children | 5 | ... |
| parent1 | 1 | ... |
| parent2 | 1 | ... |

### HLP

**Description**

> HTP Loci Predicting

```bash
(venv) (base) root:~/work/plantdna/htp$ htp-hlp
Please type input your sequence: A-T-A---A
Please type HTP code: HTP_0001
```

## Group analysis

When the analyzed data is available, use BCPlot to drawing images to visualize background information on the backcross population

---

### ABSS

> Accurate Background Selection Strategy

```bash
(venv) (base) root:~/work/plantdna/htp$ htp-abss
Please type input genotype files dir: ./
Please type input sample file path: ./
Please type output file path: ./
```
