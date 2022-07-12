# Commands

## run all labs
python main.py run \
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
--upgrade_iso_path https://s3.amazonaws.com/s3-us.vyos.io/rolling/current/vyos-1.4-rolling-202203250317-amd64.iso \
--upgrade_iso_version 1.4-rolling-202203250317 \
--branch equuleus

python main.py run -l Wireguard \
--iso_path https://s3.amazonaws.com/s3-us.vyos.io/rolling/current/vyos-1.4-rolling-202203280217-amd64.iso \
--iso_version 1.4-rolling-202203280217 \
--branch master