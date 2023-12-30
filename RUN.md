# Commands

## run all labs
python main.py run -a \
--iso_path https://s3.amazonaws.com/s3-us.vyos.io/snapshot/vyos-1.3.0-rc6/vyos-1.3.0-rc6-amd64.iso \
--iso_version 1.3.0-rc6 \
--branch equuleus

## run single lab
python main.py run -l Wireguard \
--iso_path https://s3.amazonaws.com/s3-us.vyos.io/snapshot/vyos-1.3.0-rc6/vyos-1.3.0-rc6-amd64.iso \
--iso_version 1.3.0-rc6 \
--branch equuleus

## run single with upgrade
python main.py run -l Wireguard \
--iso_path https://s3.amazonaws.com/s3-us.vyos.io/snapshot/vyos-1.3.0-rc6/vyos-1.3.0-rc6-amd64.iso \
--iso_version 1.3.0-rc6 \
--branch equuleus

python main.py run -l Wireguard \
--iso_path https://github.com/vyos/vyos-rolling-nightly-builds/releases/download/1.5-rolling-202312301423/vyos-1.5-rolling-202312301423-amd64.iso \
--iso_version 1.5-rolling-202312301423 \
--branch master
