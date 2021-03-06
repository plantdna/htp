from setuptools import setup, find_packages

setup(
    name='htp',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'htp-hca=scripts.hca_cli:cli',
            'htp-wghca=scripts.wghca_cli:cli',
            'htp-snp2htp=scripts.snp2htp_cli:cli',
            'htp-abss=scripts.abss_cli:cli',
            'htp-hpa=scripts.hpb_cli:cli',
            'htp-hpp=scripts.hpp_cli:cli',
            'htp-predicting=scripts.hlp_cli:cli',
            'htp-ilpa=scripts.ilpa_cli:cli',
            'htp-score=scripts.score_cli:cli',
        ],
    },
)