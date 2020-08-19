# Natural Language Passwords

This tool was created for my honours project as a proof-of-concept, utilising a Word2Vec model combined with common password permutations to create a customised wordlist to the password or term given. This project proved that using these custom wordlists in a dictionary attack were more reliable and greatly more efficient than popular wordlists such as RockYou.

As this is a proof-of-concept tool, there will likely be bugs with this tool. While I am not actively maintaining this tool, I am more than happy to accept any community contributions into the main branch of this repo.

## Install
1. Download the NLP model from [here.](https://drive.google.com/file/d/1Ws9m5iHbgN3IHPiGl1iVBMp-wS6cteXF/view?usp=sharing)
2. Install Pip3 if not already installed (See [documentation](https://pip.pypa.io/en/stable/installing/) for further help).
3. Install requirements using:  
```bash
pip3 install -r requirements.txt
```
4. Place downloaded NLP model into "models/w2v" or specify a custom path with the "-model-path=" flag.
5. Run script using:
```bash
./NLPasswords.py
```

## System Requirements
It is recommended to run this script on a system with at least 4GB of RAM to load the model. Using a system with less RAM will result in substantially lower performance and/or crashes.
