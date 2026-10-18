/* NEW 2026-10-17: included in BodyImpedance.c to avoid extra IDE entries.
   Original modified ADI unit's licensing applies. Not a clinical logger. */
static char BenchRunId[49];
static BoolFlag BenchLogReady=bFALSE;
uint32_t BenchLogCrc32(const unsigned char *p,size_t n) {
 uint32_t crc=0xffffffffu;size_t i;unsigned bit;
 for(i=0;i<n;i++){crc^=p[i];for(bit=0;bit<8;bit++)crc=(crc>>1)^((crc&1)?0xedb88320u:0);}
 return crc^0xffffffffu;
}
AD5940Err BenchLogEmitJson(const char *json) {
 char header[64];size_t n;int h;
 if(!BenchLogReady||!json)return AD5940ERR_PARA;
 n=strlen(json);if(!n||n>BIA_BENCH_PAYLOAD_MAX||strchr(json,'\n')||strchr(json,'\r'))return AD5940ERR_BUFF;
 h=snprintf(header,sizeof(header),"BIA1 %lu %08lx ",(unsigned long)n,
            (unsigned long)BenchLogCrc32((const unsigned char*)json,n));
 if(h<0||(size_t)h>=sizeof(header))return AD5940ERR_BUFF;
 if(fwrite(header,1,(size_t)h,stdout)!=(size_t)h||fwrite(json,1,n,stdout)!=n||fputc('\n',stdout)==EOF||fflush(stdout)!=0) {
  BenchLogReady=bFALSE;return AD5940ERR_ERROR;
 }
 return AD5940ERR_OK;
}
AD5940Err BenchLogBegin(const char *id) {
 size_t i,n;char payload[256];BenchLogReady=bFALSE;
 if(!id)return AD5940ERR_NULLP;n=strlen(id);
 if(!n||n>48||!strcmp(id,"UNSET"))return AD5940ERR_PARA;
 for(i=0;i<n;i++)if(!((id[i]>='A'&&id[i]<='Z')||(id[i]>='a'&&id[i]<='z')||
                     (id[i]>='0'&&id[i]<='9')||id[i]=='-'||id[i]=='_'))return AD5940ERR_PARA;
 if(strcmp(BIA_BENCH_SOURCE_KIND,"hardware")&&strcmp(BIA_BENCH_SOURCE_KIND,"synthetic"))return AD5940ERR_PARA;
 memcpy(BenchRunId,id,n+1);BenchLogReady=bTRUE;
 snprintf(payload,sizeof(payload),"{\"type\":\"session\",\"schema\":1,\"run_id\":\"%s\",\"source_kind\":\"%s\",\"device_qualified\":false,\"acquisition_time_available\":false}",BenchRunId,BIA_BENCH_SOURCE_KIND);
 return BenchLogEmitJson(payload);
}
AD5940Err AppBIABenchExportConfig(void) {
 char p[BIA_BENCH_PAYLOAD_MAX+1];int n;uint32_t chip,fcw;double estimate;AD5940Err e;
 if(!AppBIABenchCalibrationValid()||!ConfigId||!CalId||!BenchLogReady)return AD5940ERR_CALOR;
 chip=AD5940_ReadReg(REG_AFECON_CHIPID);fcw=AD5940_ReadReg(REG_AFE_WGFCW);
 if(AD5940_BenchIoFault)return AD5940ERR_TIMEOUT;
 if(chip!=0x5500&&chip!=0x5501&&chip!=0x5502)return AD5940ERR_APPERROR;
 if(fcw!=(uint32_t)((double)AppBIACfg.SinFreq*(chip==0x5500?67108864.0:1073741824.0)/AppBIACfg.SysClkFreq+0.5))return AD5940ERR_APPERROR;
 estimate=(double)fcw*AppBIACfg.SysClkFreq/(chip==0x5500?67108864.0:1073741824.0);
 n=snprintf(p,sizeof(p),"{\"type\":\"configuration\",\"run_id\":\"%s\",\"config_id\":%lu,\"calibration_id\":%lu,\"chip_id\":%lu,\"frequency_word\":%lu,\"frequency_requested_hz\":%.9g,\"frequency_estimate_hz\":%.12g,\"frequency_measured_hz\":null,\"clock_assumed_hz\":%.9g,\"adc_clock_assumed_hz\":%.9g,\"wake_clock_assumed_hz\":%.9g,\"effective_odr_hz\":%.9g,\"dac_parameter_mvpp\":%.9g,\"min_current_dft_counts\":%.9g,\"settings\":{\"power\":%lu,\"rtia\":%lu,\"ctia\":%lu,\"excitation_gain\":%lu,\"dac_gain\":%lu,\"dac_update\":%lu,\"pga\":%lu,\"osr3\":%lu,\"osr2\":%lu,\"dft\":%lu,\"dft_source\":%lu,\"hanning\":%lu,\"fifo_threshold_words\":%lu},\"full_register_dump_available\":false,\"sweep_enabled\":false}",
 BenchRunId,(unsigned long)ConfigId,(unsigned long)CalId,(unsigned long)chip,(unsigned long)fcw,
 AppBIACfg.SinFreq,estimate,AppBIACfg.SysClkFreq,AppBIACfg.AdcClkFreq,AppBIACfg.WuptClkFreq,
 AppBIACfg.BiaODR,AppBIACfg.DacVoltPP,AppBIACfg.MinCurrentDftMagnitude,
 (unsigned long)AppBIACfg.PwrMod,(unsigned long)AppBIACfg.HstiaRtiaSel,(unsigned long)AppBIACfg.CtiaSel,
 (unsigned long)AppBIACfg.ExcitBufGain,(unsigned long)AppBIACfg.HsDacGain,(unsigned long)AppBIACfg.HsDacUpdateRate,
 (unsigned long)AppBIACfg.ADCPgaGain,(unsigned long)AppBIACfg.ADCSinc3Osr,(unsigned long)AppBIACfg.ADCSinc2Osr,
 (unsigned long)AppBIACfg.DftNum,(unsigned long)AppBIACfg.DftSrc,(unsigned long)AppBIACfg.HanWinEn,(unsigned long)AppBIACfg.FifoThresh);
 if(n<0||(size_t)n>=sizeof(p))return AD5940ERR_BUFF;
 e=BenchLogEmitJson(p);if(e)return e;
 n=snprintf(p,sizeof(p),"{\"type\":\"calibration\",\"run_id\":\"%s\",\"config_id\":%lu,\"calibration_id\":%lu,\"status\":0,\"rcal_configured_ohm\":%.9g,\"reference_certificate\":null,\"rtia_magnitude_ohm\":%.9g,\"rtia_phase_rad\":%.9g,\"raw_dft_available\":%s,\"raw_rcal_rtia_dft\":[%lu,%lu,%lu,%lu]}",
 BenchRunId,(unsigned long)ConfigId,(unsigned long)CalId,AppBIACfg.RcalVal,AppBIACfg.RtiaCurrValue[0],AppBIACfg.RtiaCurrValue[1],AD5940_BenchCalTrace.available?"true":"false",
 (unsigned long)AD5940_BenchCalTrace.raw[0],(unsigned long)AD5940_BenchCalTrace.raw[1],(unsigned long)AD5940_BenchCalTrace.raw[2],(unsigned long)AD5940_BenchCalTrace.raw[3]);
 if(n<0||(size_t)n>=sizeof(p))return AD5940ERR_BUFF;return BenchLogEmitJson(p);
}
AD5940Err AppBIABenchExportFrames(void) {
 uint32_t i;char p[BIA_BENCH_PAYLOAD_MAX+1],values[256];int n;AD5940Err e;
 for(i=0;i<FrameCount;i++) {
  const BIABenchFrame *f=&Frames[i];
  if(f->status==0)snprintf(values,sizeof(values),"[%.9g,%.9g,%.9g,%.9g]",f->r,f->x,f->magnitude,f->phase_rad);
  else strcpy(values,"null");
  n=snprintf(p,sizeof(p),"{\"type\":\"measurement\",\"run_id\":\"%s\",\"sequence\":%lu,\"config_id\":%lu,\"calibration_id\":%lu,\"frequency_requested_hz\":%.9g,\"acquisition_time_ns\":null,\"raw\":[%lu,%lu,%lu,%lu],\"dft_counts\":[%ld,%ld,%ld,%ld],\"derived_r_x_mag_ohm_phase_rad\":%s,\"status\":%ld,\"numerical_valid\":%s,\"interrupt_flags\":%lu,\"clipping\":null,\"compliance_fault\":null,\"lead_off\":null,\"transport_loss\":null,\"qualification_eligible\":false}",
  BenchRunId,(unsigned long)f->sequence,(unsigned long)f->config_id,(unsigned long)f->calibration_id,f->frequency_requested_hz,
  (unsigned long)f->raw[0],(unsigned long)f->raw[1],(unsigned long)f->raw[2],(unsigned long)f->raw[3],
  (long)f->dft[0],(long)f->dft[1],(long)f->dft[2],(long)f->dft[3],values,(long)f->status,
  f->status==0?"true":"false",(unsigned long)f->interrupt_flags);
  if(n<0||(size_t)n>=sizeof(p))return AD5940ERR_BUFF;
  e=BenchLogEmitJson(p);if(e)return e;
 }
 return AD5940ERR_OK;
}
AD5940Err AppBIABenchExportFault(int32_t status) {
 char p[640];
 snprintf(p,sizeof(p),"{\"type\":\"fault\",\"run_id\":\"%s\",\"status\":%ld,\"config_id\":%lu,\"calibration_id\":%lu,\"io_fault\":%ld,\"interrupt_flags\":%lu,\"fifo_words\":%lu,\"advertised_capacity_words\":%lu,\"loss_extent\":\"unknown\",\"calibration_raw_available\":%s,\"calibration_raw\":[%lu,%lu,%lu,%lu],\"qualification_eligible\":false}",
 BenchRunId,(long)status,(unsigned long)ConfigId,(unsigned long)CalId,(long)AD5940_BenchIoFault,
 (unsigned long)LastInterruptFlags,(unsigned long)LastFifoWords,(unsigned long)LastCapacity,
 AD5940_BenchCalTrace.available?"true":"false",
 (unsigned long)AD5940_BenchCalTrace.raw[0],(unsigned long)AD5940_BenchCalTrace.raw[1],(unsigned long)AD5940_BenchCalTrace.raw[2],(unsigned long)AD5940_BenchCalTrace.raw[3]);
 return BenchLogEmitJson(p);
}

AD5940Err AppBIABenchExportEnd(void) {
 char p[256];snprintf(p,sizeof(p),"{\"type\":\"end\",\"run_id\":\"%s\",\"frames_decoded\":%lu,\"loss_extent\":\"unknown\",\"qualification_eligible\":false}",BenchRunId,(unsigned long)FrameSequence);
 return BenchLogEmitJson(p);
}
