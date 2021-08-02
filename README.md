Required
- 3GB of free disk space is required for generate data-set.
- python 3.8 version

Generate data
```
git clone https://github.com/wsscc2021/data-generator.git
cd data-generator/
python3 data_generator.py
```

Generate data-set sample
|column|data-type|description|
|---|---|---|
|station|string|Station name in/out per passenger|
|direction|string|
|in_out|string|"in" or "out"|
|passenger_gender|string|"male" or "female"|
|passenger_age|int|
|passenger_class|string|"youth","college_student","adult","senior_citizen"|
|passenger_price|int|
|datetime|datetime|
|year|string|
|month|string|
|day|string|
|hour|string|