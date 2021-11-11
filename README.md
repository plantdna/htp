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

pip3 install -r requirements.txt

pip3 install --editable .
```

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
Please type input file path: /home/plantdna/htp/dataset/hca_template.csv
Please type contrast file path [/]: /home/plantdna/htp/dataset/hca_template.csv
Please type output dir path [/home/plantdna/htp/output]: 
Please type missing string [---]: 
Please type number of process [1]: 
```

- mode two

```bash
htp-hca -i /home/plantdna/htp/dataset/hca_template.csv -c /home/plantdna/htp/dataset/hca_template.csv -o /home/plantdna/htp/output -ms --- -p 1
```
**Input file**

- compare file path: /home/plantdna/htp/dataset/hca_template.csv
- contrast file path: /home/plantdna/htp/dataset/hca_template.csv

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


### HPB 
> heterotic pattern building

### HPP
# Accurate Background Selection Strategy