from setuptools import setup


setup(
    name="minipay",
    version="1.3",
    keywords=("wechat", "minipay"),
    description="微信小程序支付简易SDK",
    author="dkodoc",
    author_email="tjm0510@163.com",
    packages=["minipay"],
    include_package_data=True,
    platforms="any",

    install_requires=["requests", "pycryptodome"],
)
