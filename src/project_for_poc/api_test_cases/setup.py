from setuptools import setup
setup(name='PythonBDDPOC',
      version='1.0',
      description='Python BDD POC',
      author='Artur Gh',
      author_email='artur.ghonyan@carrier.com',
      package_dir={'': 'features'},
      packages=[
            'APICommon',
            'APICommon.APICommonFuncs',
            'APICommon.APICommonSteps'
      ],
     )