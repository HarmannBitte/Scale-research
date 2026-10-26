#!/bin/bash
for r in Shah-Dom/SmartScale PavelDemyanov/qn-scale etlami/opentara uniextra/Yunmai-dashboard robzarry/healthtrack zibous/ha-miscale2 zibous/hc_scale dkuku/bodymiscale dckiller51/bodymiscale dkuku/bodymeasurements lolouk44/xiaomi_mi_scale lswiderski/MiScaleBodyComposition syoo15/AD5933_ARDUINO_Biomass justiceamoh/autoimpedance mjmeli/arduino-ad5933 ashtonchase/ad5933_analyzer kasonhaimen/AD5933_STM32_Platform analogdevicesinc/MAX32655_MAX30009 oscaroflores/UPRM-Multi_Frq-BioZ-Research; do
  curl -sSL "https://api.github.com/repos/$r" -o "meta_$(echo $r | tr '/' '_').json"
  sleep 0.3
done
