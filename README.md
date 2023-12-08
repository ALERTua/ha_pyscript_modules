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
