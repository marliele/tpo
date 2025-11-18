Запуск qemu:
sudo qemu-system-arm -m 256 -M romulus-bmc -nographic -drive file=/home/foxxoret/Загрузки/romulus/obmc-phosphor-image-romulus-20250922125238.static.mtd,format=raw,if=mtd -net nic -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:623-:623,hostname=qemu

Запуск тестов Selenium:
python3 lab4/openbmc_auth_tests.py

Запуск нагрузочного тестирования locust:
locust -f lab6/locustfile.py --host=httsp://localhost:2443 -u 10 -r 2 OpenBmcUser
locust -f lab6/locustfile.py --host=https://localhost:2443 -u 10 -r 2 PublicApiUser


