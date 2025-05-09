import setuptools

with open("README.md") as fp:
    long_description = fp.read()

setuptools.setup(
    name="zacks-cdk-library",
    version="0.1.0",
    description="Zack's personal AWS CDK library with reusable constructs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Zack Langford",
    package_dir={"": "zacks_cdk_lib"},
    packages=setuptools.find_packages(where="zacks_cdk_lib"),
    install_requires=[
        "aws-cdk-lib>=2.0.0",
        "constructs>=10.0.0",
    ],
    python_requires=">=3.6",
)