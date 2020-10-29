#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="tap-sap-cxai-recommendations",
    version="0.1.0",
    description="Singer.io tap for extracting data",
    author="SAP and Stitch",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=[
        "tap_sap_cxai_recommendations",
        "tap_sap_cxai_recommendations.record",
        "tap_sap_cxai_recommendations.record.handler"
    ],
    install_requires=[
	"singer-python==5.6.1",
        "requests==2.20.0"
    ],
    entry_points="""
    [console_scripts]
    tap-sap-cxai-recommendations=tap_sap_cxai_recommendations:main
    """,
    packages=find_packages(),
    package_data = {
        "schemas": ["tap_sap_cxai_recommendations/schemas/*.json"]
    },
    include_package_data=True,
)
