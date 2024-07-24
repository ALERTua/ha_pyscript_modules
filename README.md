[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg)](https://stand-with-ukraine.pp.ua)
[![Made in Ukraine](https://img.shields.io/badge/made_in-Ukraine-ffd700.svg?labelColor=0057b7)](https://stand-with-ukraine.pp.ua)
[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraine.svg)](https://stand-with-ukraine.pp.ua)
[![Russian Warship Go Fuck Yourself](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/RussianWarship.svg)](https://stand-with-ukraine.pp.ua)

# ha_pyscript_modules

![image](https://github.com/ALERTua/ha_pyscript_modules/assets/8375129/5adc7464-d47b-4bc4-93b3-f33897a456d2)

```
from entities.entity import entity
from entities.ha import HA
# or
from imports import *

ha = HA()
ha_external_url = ha.external_url()

ent = entity(constants.OFFICE_LIGHTS)  # resolves to entities.light.Light instance
ent.turn_off()
```
