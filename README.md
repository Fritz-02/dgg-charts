# DGG Charts

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

## About

This a project that collects and displays various data from [Destiny's](https://www.youtube.com/user/destiny) 
livestreams onto a chart. Data used is from destiny.gg (livestream information), and "Last Month on Destiny" (LWOD, timestamps of things that occur during streams) 
spreadsheets by cantclosevim.

## Usage

Run this is collect data:
```sh
python collect_data.py
```

Run this to display chart for the specified date (in YY-MM-DD format, optional, defaults to date in config.json):
```sh
python chart.py 22-09-09
```

Run this to clean up a csv file (so far only works on chat.csv, and removes data from offline chat)
```sh
python clean_csv.py ./data/22-09-09/chat.csv
```

## Example Charts

![Chart, 8 Sept 2022](https://i.imgur.com/T8z6YCE.png)

## License

Distributed under the MIT License. See `LICENSE` for more information.

## More Stuff

### LWOD Links

Links to LWOD spreadsheets created by cantclosevim since September 2022.

- [September 2022](https://docs.google.com/spreadsheets/d/1vkx2vxMiNkoqRXRfWrZJms_k7-toLWXxHIE2MJJPv5Y/edit?usp=sharing)
- [October 2022](https://docs.google.com/spreadsheets/d/1BY2ICnELKlwXE5qbsaDtMyu0HMHPHEWdvz2c1GculYQ)



[contributors-shield]: https://img.shields.io/github/contributors/Fritz-02/dgg-charts.svg?style=for-the-badge
[contributors-url]: https://github.com/Fritz-02/dgg-charts/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Fritz-02/dgg-charts.svg?style=for-the-badge
[forks-url]: https://github.com/Fritz-02/dgg-charts/network/members
[stars-shield]: https://img.shields.io/github/stars/Fritz-02/dgg-charts.svg?style=for-the-badge
[stars-url]: https://github.com/Fritz-02/dgg-charts/stargazers
[issues-shield]: https://img.shields.io/github/issues/Fritz-02/dgg-charts.svg?style=for-the-badge
[issues-url]: https://github.com/Fritz-02/dgg-charts/issues
[license-shield]: https://img.shields.io/github/license/Fritz-02/dgg-charts.svg?style=for-the-badge
[license-url]: https://github.com/Fritz-02/dgg-charts/blob/master/LICENSE
