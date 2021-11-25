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
[⏬ download](https://htp.plantdna.site/download/htp-template-files.zip)

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

> /home/plantdna/htp/dataset/template_genotyping.txt

**Output file**

> /home/plantdna/htp/output/{$genotyping_file_name}_{$timestamp}/all_htps.csv

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

**Output file**

> /home/plantdna/htp/output/hca_compare_result_{$timestamp}.csv

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

**Output file**

> /home/plantdna/htp/output/wghca_compare_result_{$timestamp}.csv

##  Data prediction
---

### HPB 

**Description**
> Heterotic Pattern Building

```bash
(venv) (base) root:~/work/plantdna/htp$ htp-hpb
Please type input genotype files dir: ./
Please type output path: ./
```

### Score

```bash
(venv) (base) root:~/work/plantdna/htp$ htp-score
Please type input group files dir: ./
Please type output path: ./
```

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

### HLP

**Description**
> HTP Loci Predicting

```bash
(venv) (base) root:~/work/plantdna/htp$ htp-hlp
Please type input your sequence: A-T-A---A
Please type HTP code: HTP_0001
```

## Population analysis
---
### ABSS
> Accurate Background Selection Strategy

```bash
(venv) (base) root:~/work/plantdna/htp$ htp-abss
Please type input genotype files dir: ./
Please type input sample file path: ./
Please type output file path: ./
```