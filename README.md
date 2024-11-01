## Text dataset deduplication

### Requirements
'pandas', 'simhash', 'datasketch'

### Installation
Active environment (if necessary)
```bash
python3 -m venv venv
source ./venv/bin/activate
```

Install requirements
```bash
pip install -r requirements.txt
```

### Instruction
Set input data
```python
texts = pd.read_csv('data_duplicate.csv')['text']
```
Set output data
```python
output = pd.DataFrame({'text': output_texts})
output.to_csv('new_data_simhash.csv')
```

Run simhash
```bash
python simhash_dedup.py
```

Run minhash
```bash
python minhash_dedup.py
```

