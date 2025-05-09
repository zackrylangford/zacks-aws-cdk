import setuptools

with open("README.md") as fp:
    long_description = fp.read()

setuptools.setup(
    name="my-cdk-lib",
    version="0.1.0",
    description="Personal AWS CDK library with reusable constructs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    package_dir={"": "my_cdk_lib"},
    packages=setuptools.find_packages(where="my_cdk_lib"),
    install_requires=[
        "aws-cdk-lib>=2.0.0",
        "constructs>=10.0.0",
    ],
    python_requires=">=3.6",
)