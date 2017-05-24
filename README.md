# MDSGA
Tool for chromatin 3D structure reconstruction from 3C experimental data. Improvement of ShRec3D.

# CLI

```
usage: sample_generator.py [-h] [-r RADIUS] [-pog PERCENT_OF_GAPS]
                           [-p POINTS_AMOUNT]

Generates sample Hi-C experimental data

optional arguments:
  -h, --help            show this help message and exit
  -r RADIUS, --radius RADIUS
                        radius between each point (+/- radius divaded by 4)
  -pog PERCENT_OF_GAPS, --percent-of-gaps PERCENT_OF_GAPS
                        percent of gaps introduced to distance matrix (0..1)
  -p POINTS_AMOUNT, --points POINTS_AMOUNT
                        amount of points in sample model
```

```
usage: ga_main.py [-h] [-p POPULATION_SIZE] [-g GENERATIONS]
                  [-m MUTATION_RATE]
                  [--cg [CHECK_GENERATIONS [CHECK_GENERATIONS ...]]]
                  PATH

Generates sample Hi-C experimental data

positional arguments:
  PATH                  path to sample folder

optional arguments:
  -h, --help            show this help message and exit
  -p POPULATION_SIZE, --population POPULATION_SIZE
                        size of population for GA
  -g GENERATIONS, --generations GENERATIONS
                        number of generations for GA
  -m MUTATION_RATE, --mutation-rate MUTATION_RATE
                        mutation rate (0..1
  --cg [CHECK_GENERATIONS [CHECK_GENERATIONS ...]]
                        generations on which FULL error is calculated
```

### Docker command

```
docker build -t skkap/mdsga:latest .
```

```
sudo docker run --name m1 -d -e SAMPLE_PATH='../samples/200_0.95_10_1/' -e TRIES='3' -v /raidz/skkap/docker/result:/app/result skkap/mdsga /app/docker-entry.sh
sudo docker run --name m2 -d -e SAMPLE_PATH='../samples/200_0.95_10_2/' -e TRIES='3' -v /raidz/skkap/docker/result:/app/result skkap/mdsga /app/docker-entry.sh
sudo docker run --name m3 -d -e SAMPLE_PATH='../samples/200_0.95_10_3/' -e TRIES='3' -v /raidz/skkap/docker/result:/app/result skkap/mdsga /app/docker-entry.sh
```
