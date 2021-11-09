import pandas as pd
import numpy as np
import json
import os
import math
import matplotlib.pyplot as plt

from .base import append_write_csv_by_df

def fitting_rp_genotype(genotypes, default_allele) -> str:
    '''
    根据位点的全部基因型拟合受体基因型
    '''
    alleles = []
    for genotype in genotypes:
        if genotype != '---':
            alleles+=genotype.split('/')

    alleles_counts = pd.value_counts(alleles).to_dict()
    alleles_counts_rate = {}
    for allele in alleles_counts:
        allele_rate = round(alleles_counts[allele]/len(alleles), 3)
        alleles_counts_rate[allele] = allele_rate

    allele_items = list(alleles_counts_rate.keys())
    allele = allele_items[0] if len(allele_items) > 0 else default_allele

    return '{}/{}'.format(allele, allele)



def filter_snp(chr_snp_rates):
    # 筛选标记
    selected = {}
    for probeset, rates in chr_snp_rates.items():
        # 过滤单态标记
        if rates['rp_rate'] >= 0.8 or rates['dp_rate'] >= 0.8 or rates['nc_rate'] >= 0.8 or rates['hy_rate'] >= 0.8:
            pass
        # 过滤混杂标记
        elif rates['dp_rate']+rates['nc_rate']+rates['hy_rate'] >= 0.8 or rates['nc_rate']+rates['dp_rate'] >= 0.2:
            pass
        else:
            selected[probeset] = rates['rp_rate']

    return selected



def fitting(chr_dir, rp_codes, dp_codes, probeset_info_df, is_filter_marker, tracke_probeset_file_path, image_dir):
    '''
    拟合供体受体数据
    '''
    snp_rates = {}
    target_probeset = {}

    fig, axs = plt.subplots(ncols=2, nrows=5, figsize=(24, 20))

    for chr_id in range(1, 11):
        snp_rates['chr{}'.format(chr_id)] = {}

        chr_fitting_data = {
            'call_code': ['simulate_fitting_rp_by_rps', 'simulate_fitting_rp_by_group', 'simulate_fitting_dp_by_group'],
        }

        chr_df = pd.read_csv('{}/chr{}.csv'.format(chr_dir, chr_id))
        chr_probesets = chr_df.columns.tolist()[1:]
        chr_group_df = chr_df[~chr_df['call_code'].isin(rp_codes+dp_codes)]
        chr_rp_df = chr_df[chr_df['call_code'].isin(rp_codes)]
        target_probeset['chr{}'.format(chr_id)] = chr_probesets

        # 按位点遍历
        for probeset in chr_probesets:
            # 理论AA BB基因型
            probeset_AA = '/'.join(probeset_info_df.loc[probeset]['Allele A']*2)
            probeset_BB = '/'.join(probeset_info_df.loc[probeset]['Allele B']*2)

            chr_rp_probeset_values = chr_rp_df[probeset].tolist()
            chr_group_probeset_values = chr_group_df[probeset].tolist()
            # 拟合受体基因型
            probeset_rp_genotype_fitting_by_rp = fitting_rp_genotype(chr_rp_probeset_values, probeset_info_df.loc[probeset]['Allele A'])
            probeset_rp_genotype_fitting_by_group = fitting_rp_genotype(chr_group_probeset_values, probeset_info_df.loc[probeset]['Allele A'])
            # 拟合供体基因型
            probeset_dp_genotype_fitting_by_group = ''
            if probeset_rp_genotype_fitting_by_group == probeset_AA:
                probeset_dp_genotype_fitting_by_group = probeset_BB
            else:
                probeset_dp_genotype_fitting_by_group = probeset_AA

            chr_fitting_data[probeset] = [
                probeset_rp_genotype_fitting_by_rp,
                probeset_rp_genotype_fitting_by_group,
                probeset_dp_genotype_fitting_by_group
            ]
            
            rp_rate = round(chr_group_probeset_values.count(probeset_rp_genotype_fitting_by_rp)/len(chr_group_probeset_values), 3)
            dp_rate = round(chr_group_probeset_values.count(probeset_dp_genotype_fitting_by_group)/len(chr_group_probeset_values), 3)
            nc_rate = round(chr_group_probeset_values.count('---')/len(chr_group_probeset_values), 3)
            hy_rate = round(1-(rp_rate+dp_rate+nc_rate), 3)
            
            snp_rates['chr{}'.format(chr_id)][probeset] = {
                'rp_rate': rp_rate,
                'dp_rate': dp_rate,
                'nc_rate': nc_rate,
                'hy_rate': hy_rate,
            }

        fitting_df = pd.DataFrame(chr_fitting_data)

        # 将拟合数据写入数据集
        append_write_csv_by_df(fitting_df, chr_dir, 'chr{}'.format(chr_id))

        axs_x = math.ceil(chr_id/2)-1
        axs_y = (chr_id-1)%2
        axs[axs_x, axs_y].tick_params(labelsize=15)
        axs[axs_x, axs_y].set_ylim(0, 1)
        axs[axs_x, axs_y].set_title('Chr{}'.format(chr_id), fontsize=15)
        
        # 绘制全部标记
        axs[axs_x, axs_y].scatter(
            np.array([probeset_info_df.loc[key]['Position'] for key in list(snp_rates['chr{}'.format(chr_id)])]),
            [item['rp_rate'] for item in list(snp_rates['chr{}'.format(chr_id)].values())],
            zorder=0,
            color='gray'
        )

        if not os.path.exists(tracke_probeset_file_path) and is_filter_marker:
            # 过滤异常值标记
            s1data = filter_snp(snp_rates['chr{}'.format(chr_id)])
            s1_probesets = list(s1data.keys())
            xdata = np.array([probeset_info_df.loc[key]['Position'] for key in s1_probesets])
            ydata = np.array(list(s1data.values()))
            # 拟合曲线
            z_fit = np.polyfit(xdata, ydata, 3)
            curve_equation = np.poly1d(z_fit)

            s2data = {}

            y_list = []
            y1_list = []
            y2_list = []
            for i in range(len(xdata)):
                x = xdata[i]
                y = ydata[i]
                y1 = curve_equation(x) + 0.1
                y2 = curve_equation(x) - 0.1
                if y2 <= y <= y1:
                    s2data[s1_probesets[i]] = y

                y_list.append(curve_equation(x))
                y1_list.append(y1)
                y2_list.append(y2)
            
            # 绘制拟合曲线
            axs[axs_x, axs_y].plot(xdata, y_list, color='red', zorder=2)
            axs[axs_x, axs_y].plot(xdata, y1_list, color='red', zorder=2)
            axs[axs_x, axs_y].plot(xdata, y2_list, color='red', zorder=2)
            # 绘制选中标记
            axs[axs_x, axs_y].scatter(
                np.array([probeset_info_df.loc[key]['Position'] for key in list(s2data.keys())]),
                list(s2data.values()),
                zorder=1,
            )

            target_probeset['chr{}'.format(chr_id)] = list(s2data.keys())

    plt.subplots_adjust(hspace=0.4)
    if not os.path.exists(tracke_probeset_file_path):
        with open(tracke_probeset_file_path, 'w', )as f:
            json.dump(target_probeset, f)
        f.close()

        plt.savefig('{}/selected_snps.jpg'.format(image_dir, chr_id), format='jpg', dpi=300)

    plt.close()
