from setuptools import setup


setup(
    name="minipay-sdk",
    version="1.0",

    author="MagicalGoldOx",
    author_email="dkodoc.udlrbaba@gmail.com",

    keywords=("mini programs", "wechat", "python", "sdk", "pay"),
    description="minipy python sdk",
    license="Apache Licence",
    packages=['minipay'],
    platform="any",
    install_requires=[
        'pycryptodome',
        'requests'
    ],
    zip_safe=False
)