from setuptools import setup

setup(
    name="minipay",
    version="0.1.4",
    keywords=["wechat", "minipay", "mini program", "pay", "sdk"],
    description="微信小程序支付SDK",
    author="tanjm",
    long_description=open("README.rst", encoding="utf-8").read(),
    license="MIT",
    url="https://github.com/tanjm/minipay",
    author_email="tjm0510@163.com",
    packages=["minipay"],
    include_package_data=True,
    platforms="any",
    install_requires=["requests", "pycryptodome", "aiohttp"],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent", "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ]
)
