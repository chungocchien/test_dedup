## AI Project Template

### Requirements
'pandas', 'simhash'

### Installation
Note: Activate your environment (if necessary)

cd <path_to_root_project> (folder containing setup.py)
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

### Demo simhash
```bash
python simhash_dedup.py
```

### Demo minhash
```bash
python minhash_dedup.py
```

