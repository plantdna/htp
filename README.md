# HTP
> Haplotype-tag polymorphisms (HTP) is a high-resolution, high-efficient, and low-cost molecular marker which can serve as a low cost, time, and high-throughput genotyping resources for genetic mapping, germplasm resource analysis and genomics-informed breeding in maize. This platform is an open source web server and free software that fully support HTP mark with comprehensive analysis include crossing pattern in maize heterosis and DNA fingerprint analysis.

## Dependance

This project was developed based on python3. If your operating system does not have Python3 environment installed, Please install the [Python3](https://www.python.org/downloads/) first.

## Quickstart

```bash
git clone https://github.com/plantdna/htp.git

cd htp

python3 -m venv venv

source ./venv/bin/activate

pip install -r requirements.txt

pip install --editable .
```

### SNP2HTP

```bash
(venv) (base) jovyan@b6da7f9716dd:~/work/plantdna/htp$ htp
Please select mode (snp2htp, wghca, hca): snp2htp
Please type input file path: /home/jovyan/work/plantdna/htp/dataset/template_genotyping.txt
Please type output dir path [/home/jovyan/work/plantdna/htp/output]: 
Please type contrast file path [/]: 
Please type similarity threshold [0.8]: 
Please type missing string [---]: 
```

### HCA

> HTP comparison algorithm

```bash
(venv) (base) jovyan@b6da7f9716dd:~/work/plantdna/htp$ htp
Please select mode (snp2htp, wghca, hca): hca
Please type input file path: /home/jovyan/work/plantdna/htp/dataset/hca_template.csv
Please type output dir path [/home/jovyan/work/plantdna/htp/output]: 
Please type contrast file path [/]: /home/jovyan/work/plantdna/htp/dataset/hca_template.csv
Please type similarity threshold [0.8]: 
Please type missing string [---]: 
```

### WGHCA

> Whole genome haplotype comparison algorithm

```bash
(venv) (base) jovyan@b6da7f9716dd:~/work/plantdna/htp$ htp
Please select mode (snp2htp, wghca, hca): wghca
Please type input file path: /home/jovyan/work/plantdna/htp/dataset/wghca_template.csv
Please type output dir path [/home/jovyan/work/plantdna/htp/output]: 
Please type contrast file path [/]: /home/jovyan/work/plantdna/htp/dataset/wghca_template.csv
Please type similarity threshold [0.8]: 
Please type missing string [---]: 
```
### help

```bash
(venv) (base) jovyan@b6da7f9716dd:~/work/plantdna/htp$ htp -h
Usage: htp [OPTIONS]

  Welcome use htp cli

Options:
  -m, --mode [snp2htp|wghca|hca]  mode options.
  -i, --input PATH                input file path.
  -o, --output PATH               output dir path.  [default: /home/jovyan/work/plantdna/htp/output]
  -c, --contrast PATH             contrast file path (This is required when the mode is HCA and WGHCA).  [default: /]
  -st, --similarity_threshold FLOAT
                                  similarity threshold.  [default: 0.8]
  -ms, --missing_string TEXT      missing string.  [default: ---]
  -h, --help                      Show this message and exit.
```