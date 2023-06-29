from setuptools import setup

setup(
   name='cross_exchange_rate_fallback',
   version='1.0.0',
   description='Cross Exchange Rate Fallback Service',
   author='Aypahyo',
   author_email='Aypahyo@github.com',
   url='https://github.com/aypahyo/cross-exchange-rate-fallback',
   packages=['cross_exchange_rate_fallback_core'],
   py_modules=['cross_exchange_rate_fallback'],
   entry_points={
    'console_scripts' : [
      'cross_exchange_rate_fallback = cross_exchange_rate_fallback:main'
    ],
   }
)


















