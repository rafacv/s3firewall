from setuptools import setup

setup(name='s3firewall',
      version='0.1',
      description='Protect your S3 bucket behind WWW Basic Auth and or IP address check.',
      author='Rafael Valverde',
      author_email='rafacvo@gmail.com',
      url='http://www.github.com/rafacv/s3firewall',
      packages=['s3firewall'],
      install_requires='boto>=2.10.0'
)
