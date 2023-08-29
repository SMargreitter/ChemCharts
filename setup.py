from setuptools import setup, find_namespace_packages

setup(
    name="chemcharts",
    maintainer="Sophie Margreitter, Christian Margreitter",
    version="0.9.0",
    url="https://github.com/SMargreitter/ChemCharts",
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    description="ChemCharts: Chemical Space Visualizer",
    python_requires=">=3.8",
    install_requires=[
        "dill",
        "plotly>=5.1.0",
        "rdkit>=2022.9.5",
        "seaborn>=0.11",
        "molplotly",
        "ffmpeg-python>=0.2.0",
        "scikit-learn>=0.24",
        "umap-learn",
        "kaleido"
    ],
    entry_points={"console_scripts": ["chemcharts_cli = chemcharts.scripts.chemcharts_cli:main",
                                      "chemcharts = chemcharts.scripts.chemcharts_json:main"]},
)
