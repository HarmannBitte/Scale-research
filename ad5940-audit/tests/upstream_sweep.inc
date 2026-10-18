/* VERBATIM EXTRACT: ADI copyright/license apply. See source/LICENSE and source/examples/ad5940lib/LICENSE. */
void AD5940_SweepNext(SoftSweepCfg_Type *pSweepCfg, float *pNextFreq)
{
   float frequency;

   if(pSweepCfg->SweepLog)/* Log step */
   {
      if(pSweepCfg->SweepStart<pSweepCfg->SweepStop) /* Normal */
      {
         if(++pSweepCfg->SweepIndex == pSweepCfg->SweepPoints)
            pSweepCfg->SweepIndex = 0;
         frequency = pSweepCfg->SweepStart*pow(10,pSweepCfg->SweepIndex*log10(pSweepCfg->SweepStop/pSweepCfg->SweepStart)/(pSweepCfg->SweepPoints-1));
      }
      else
      {
         pSweepCfg->SweepIndex --;
         if(pSweepCfg->SweepIndex >= pSweepCfg->SweepPoints)
            pSweepCfg->SweepIndex = pSweepCfg->SweepPoints-1;
         frequency = pSweepCfg->SweepStop*pow(10,pSweepCfg->SweepIndex*
                                     (log10(pSweepCfg->SweepStart/pSweepCfg->SweepStop)/(pSweepCfg->SweepPoints-1)));
      }
   }
   else/* Linear step */
   {
      if(pSweepCfg->SweepStart<pSweepCfg->SweepStop) /* Normal */
      {
         if(++pSweepCfg->SweepIndex == pSweepCfg->SweepPoints)
            pSweepCfg->SweepIndex = 0;
         frequency = pSweepCfg->SweepStart + pSweepCfg->SweepIndex*(double)(pSweepCfg->SweepStop-pSweepCfg->SweepStart)/(pSweepCfg->SweepPoints-1);
      }
      else
      {
         pSweepCfg->SweepIndex --;
         if(pSweepCfg->SweepIndex >= pSweepCfg->SweepPoints)
            pSweepCfg->SweepIndex = pSweepCfg->SweepPoints-1;
         frequency = pSweepCfg->SweepStop + pSweepCfg->SweepIndex*(double)(pSweepCfg->SweepStart - pSweepCfg->SweepStop)/(pSweepCfg->SweepPoints-1);
      }
   }
   
   *pNextFreq = frequency;
}
