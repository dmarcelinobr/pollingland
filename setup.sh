cd /Users/marcelino/Documents/pollingland

conda env create --prefix ./env --file pollingland.yml  --force

conda activate /Users/marcelino/Documents/pollingland/env

conda env export --name pollingland

conda env export --name pollingland --from-history --file environment.yml
