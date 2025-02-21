# Rags


## Conda setup
Official Quick Install: https://docs.anaconda.com/miniconda/install/

### MacOS
```bash
mkdir -p ~/miniconda3
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
source ~/miniconda3/bin/activate
conda init --all
```

### Linux
```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
source ~/miniconda3/bin/activate
conda init --all
```


## Rags Setup

```bash
pip install uv
uv venv
source .venv/bin/activate
uv pip sync pyproject.toml
playwright install-deps
playwright install
```

## How to run
- run server: `make run`
- run tests: `make test`
- run mypy checks: `make check`
- build wheel: `make build`
