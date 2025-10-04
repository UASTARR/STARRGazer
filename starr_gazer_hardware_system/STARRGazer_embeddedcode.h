//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
//
// File: STARRGazer_embeddedcode.h
//
// Code generated for Simulink model 'STARRGazer_embeddedcode'.
//
// Model version                  : 1.10
// Simulink Coder version         : 25.1 (R2025a) 21-Nov-2024
// C/C++ source code generated on : Fri Oct  3 22:42:05 2025
//
// Target selection: ert.tlc
// Embedded hardware selection: Intel->x86-64 (Windows64)
// Code generation objectives:
//    1. Execution efficiency
//    2. RAM efficiency
// Validation result: Not run
//
#ifndef STARRGazer_embeddedcode_h_
#define STARRGazer_embeddedcode_h_
#include <cmath>
#include "rtwtypes.h"

// Class declaration for model STARRGazer_embeddedcode
class ustarr_sim final
{
  // public data and function members
 public:
  // Block signals and states (default storage) for system '<Root>'
  struct DW {
    real_T UnitDelay_DSTATE;           // '<Root>/Unit Delay'
    real_T UD_DSTATE;                  // '<S32>/UD'
    real_T Integrator_DSTATE;          // '<S39>/Integrator'
    real_T UnitDelay1_DSTATE;          // '<Root>/Unit Delay1'
    real_T Filter_DSTATE;              // '<S86>/Filter'
    real_T Integrator_DSTATE_p;        // '<S91>/Integrator'
  };

  // External inputs (root inport signals with default storage)
  struct ExtU {
    real_T PitchInput;                 // '<Root>/In1'
    real_T YawInput;                   // '<Root>/In2'
  };

  // External outputs (root outports fed by signals with default storage)
  struct ExtY {
    real_T Out1;                       // '<Root>/Out1'
    real_T Out2;                       // '<Root>/Out2'
  };

  // Parameters (default storage)
  struct P {
    real_T PIDController_D;            // Mask Parameter: PIDController_D
                                          //  Referenced by: '<S30>/Derivative Gain'

    real_T PIDController1_D;           // Mask Parameter: PIDController1_D
                                          //  Referenced by: '<S84>/Derivative Gain'

    real_T PIDController_DifferentiatorICP;
                              // Mask Parameter: PIDController_DifferentiatorICP
                                 //  Referenced by: '<S32>/UD'

    real_T PIDController_I;            // Mask Parameter: PIDController_I
                                          //  Referenced by: '<S36>/Integral Gain'

    real_T PIDController1_I;           // Mask Parameter: PIDController1_I
                                          //  Referenced by: '<S88>/Integral Gain'

    real_T PIDController1_InitialCondition;
                              // Mask Parameter: PIDController1_InitialCondition
                                 //  Referenced by: '<S86>/Filter'

    real_T PIDController_InitialConditionF;
                              // Mask Parameter: PIDController_InitialConditionF
                                 //  Referenced by: '<S39>/Integrator'

    real_T PIDController1_InitialConditi_k;
                              // Mask Parameter: PIDController1_InitialConditi_k
                                 //  Referenced by: '<S91>/Integrator'

    real_T PIDController1_N;           // Mask Parameter: PIDController1_N
                                          //  Referenced by: '<S94>/Filter Coefficient'

    real_T PIDController_P;            // Mask Parameter: PIDController_P
                                          //  Referenced by: '<S44>/Proportional Gain'

    real_T PIDController1_P;           // Mask Parameter: PIDController1_P
                                          //  Referenced by: '<S96>/Proportional Gain'

    real_T UnitDelay_InitialCondition; // Expression: 0
                                          //  Referenced by: '<Root>/Unit Delay'

    real_T Gain_Gain;                  // Expression: 0.125
                                          //  Referenced by: '<Root>/Gain'

    real_T Tsamp_WtEt;                 // Computed Parameter: Tsamp_WtEt
                                          //  Referenced by: '<S34>/Tsamp'

    real_T Integrator_gainval;         // Computed Parameter: Integrator_gainval
                                          //  Referenced by: '<S39>/Integrator'

    real_T UnitDelay1_InitialCondition;// Expression: 0
                                          //  Referenced by: '<Root>/Unit Delay1'

    real_T Gain1_Gain;                 // Expression: 0.1
                                          //  Referenced by: '<Root>/Gain1'

    real_T Filter_gainval;             // Computed Parameter: Filter_gainval
                                          //  Referenced by: '<S86>/Filter'

    real_T Integrator_gainval_a;     // Computed Parameter: Integrator_gainval_a
                                        //  Referenced by: '<S91>/Integrator'

  };

  // Copy Constructor
  ustarr_sim(ustarr_sim const&) = delete;

  // Assignment Operator
  ustarr_sim& operator= (ustarr_sim const&) & = delete;

  // Move Constructor
  ustarr_sim(ustarr_sim &&) = delete;

  // Move Assignment Operator
  ustarr_sim& operator= (ustarr_sim &&) = delete;

  // External inputs
  ExtU rtU;

  // External outputs
  ExtY rtY;

  // model initialize function
  void initialize();

  // model step function
  void step();

  // Constructor
  ustarr_sim();

  // Destructor
  ~ustarr_sim();

  // private data and function members
 private:
  // Block states
  DW rtDW;

  // Tunable parameters
  static P rtP;
};

//-
//  These blocks were eliminated from the model due to optimizations:
//
//  Block '<S32>/DTDup' : Unused code path elimination


//-
//  The generated code includes comments that allow you to trace directly
//  back to the appropriate location in the model.  The basic format
//  is <system>/block_name, where system is the system number (uniquely
//  assigned by Simulink) and block_name is the name of the block.
//
//  Use the MATLAB hilite_system command to trace the generated code back
//  to the model.  For example,
//
//  hilite_system('<S3>')    - opens system 3
//  hilite_system('<S3>/Kp') - opens and selects block Kp which resides in S3
//
//  Here is the system hierarchy for this model
//
//  '<Root>' : 'STARRGazer_embeddedcode'
//  '<S1>'   : 'STARRGazer_embeddedcode/PID Controller'
//  '<S2>'   : 'STARRGazer_embeddedcode/PID Controller1'
//  '<S3>'   : 'STARRGazer_embeddedcode/PID Controller/Anti-windup'
//  '<S4>'   : 'STARRGazer_embeddedcode/PID Controller/D Gain'
//  '<S5>'   : 'STARRGazer_embeddedcode/PID Controller/External Derivative'
//  '<S6>'   : 'STARRGazer_embeddedcode/PID Controller/Filter'
//  '<S7>'   : 'STARRGazer_embeddedcode/PID Controller/Filter ICs'
//  '<S8>'   : 'STARRGazer_embeddedcode/PID Controller/I Gain'
//  '<S9>'   : 'STARRGazer_embeddedcode/PID Controller/Ideal P Gain'
//  '<S10>'  : 'STARRGazer_embeddedcode/PID Controller/Ideal P Gain Fdbk'
//  '<S11>'  : 'STARRGazer_embeddedcode/PID Controller/Integrator'
//  '<S12>'  : 'STARRGazer_embeddedcode/PID Controller/Integrator ICs'
//  '<S13>'  : 'STARRGazer_embeddedcode/PID Controller/N Copy'
//  '<S14>'  : 'STARRGazer_embeddedcode/PID Controller/N Gain'
//  '<S15>'  : 'STARRGazer_embeddedcode/PID Controller/P Copy'
//  '<S16>'  : 'STARRGazer_embeddedcode/PID Controller/Parallel P Gain'
//  '<S17>'  : 'STARRGazer_embeddedcode/PID Controller/Reset Signal'
//  '<S18>'  : 'STARRGazer_embeddedcode/PID Controller/Saturation'
//  '<S19>'  : 'STARRGazer_embeddedcode/PID Controller/Saturation Fdbk'
//  '<S20>'  : 'STARRGazer_embeddedcode/PID Controller/Sum'
//  '<S21>'  : 'STARRGazer_embeddedcode/PID Controller/Sum Fdbk'
//  '<S22>'  : 'STARRGazer_embeddedcode/PID Controller/Tracking Mode'
//  '<S23>'  : 'STARRGazer_embeddedcode/PID Controller/Tracking Mode Sum'
//  '<S24>'  : 'STARRGazer_embeddedcode/PID Controller/Tsamp - Integral'
//  '<S25>'  : 'STARRGazer_embeddedcode/PID Controller/Tsamp - Ngain'
//  '<S26>'  : 'STARRGazer_embeddedcode/PID Controller/postSat Signal'
//  '<S27>'  : 'STARRGazer_embeddedcode/PID Controller/preInt Signal'
//  '<S28>'  : 'STARRGazer_embeddedcode/PID Controller/preSat Signal'
//  '<S29>'  : 'STARRGazer_embeddedcode/PID Controller/Anti-windup/Passthrough'
//  '<S30>'  : 'STARRGazer_embeddedcode/PID Controller/D Gain/Internal Parameters'
//  '<S31>'  : 'STARRGazer_embeddedcode/PID Controller/External Derivative/Error'
//  '<S32>'  : 'STARRGazer_embeddedcode/PID Controller/Filter/Differentiator'
//  '<S33>'  : 'STARRGazer_embeddedcode/PID Controller/Filter/Differentiator/Tsamp'
//  '<S34>'  : 'STARRGazer_embeddedcode/PID Controller/Filter/Differentiator/Tsamp/Internal Ts'
//  '<S35>'  : 'STARRGazer_embeddedcode/PID Controller/Filter ICs/Internal IC - Differentiator'
//  '<S36>'  : 'STARRGazer_embeddedcode/PID Controller/I Gain/Internal Parameters'
//  '<S37>'  : 'STARRGazer_embeddedcode/PID Controller/Ideal P Gain/Passthrough'
//  '<S38>'  : 'STARRGazer_embeddedcode/PID Controller/Ideal P Gain Fdbk/Disabled'
//  '<S39>'  : 'STARRGazer_embeddedcode/PID Controller/Integrator/Discrete'
//  '<S40>'  : 'STARRGazer_embeddedcode/PID Controller/Integrator ICs/Internal IC'
//  '<S41>'  : 'STARRGazer_embeddedcode/PID Controller/N Copy/Disabled wSignal Specification'
//  '<S42>'  : 'STARRGazer_embeddedcode/PID Controller/N Gain/Passthrough'
//  '<S43>'  : 'STARRGazer_embeddedcode/PID Controller/P Copy/Disabled'
//  '<S44>'  : 'STARRGazer_embeddedcode/PID Controller/Parallel P Gain/Internal Parameters'
//  '<S45>'  : 'STARRGazer_embeddedcode/PID Controller/Reset Signal/Disabled'
//  '<S46>'  : 'STARRGazer_embeddedcode/PID Controller/Saturation/Passthrough'
//  '<S47>'  : 'STARRGazer_embeddedcode/PID Controller/Saturation Fdbk/Disabled'
//  '<S48>'  : 'STARRGazer_embeddedcode/PID Controller/Sum/Sum_PID'
//  '<S49>'  : 'STARRGazer_embeddedcode/PID Controller/Sum Fdbk/Disabled'
//  '<S50>'  : 'STARRGazer_embeddedcode/PID Controller/Tracking Mode/Disabled'
//  '<S51>'  : 'STARRGazer_embeddedcode/PID Controller/Tracking Mode Sum/Passthrough'
//  '<S52>'  : 'STARRGazer_embeddedcode/PID Controller/Tsamp - Integral/TsSignalSpecification'
//  '<S53>'  : 'STARRGazer_embeddedcode/PID Controller/Tsamp - Ngain/Passthrough'
//  '<S54>'  : 'STARRGazer_embeddedcode/PID Controller/postSat Signal/Forward_Path'
//  '<S55>'  : 'STARRGazer_embeddedcode/PID Controller/preInt Signal/Internal PreInt'
//  '<S56>'  : 'STARRGazer_embeddedcode/PID Controller/preSat Signal/Forward_Path'
//  '<S57>'  : 'STARRGazer_embeddedcode/PID Controller1/Anti-windup'
//  '<S58>'  : 'STARRGazer_embeddedcode/PID Controller1/D Gain'
//  '<S59>'  : 'STARRGazer_embeddedcode/PID Controller1/External Derivative'
//  '<S60>'  : 'STARRGazer_embeddedcode/PID Controller1/Filter'
//  '<S61>'  : 'STARRGazer_embeddedcode/PID Controller1/Filter ICs'
//  '<S62>'  : 'STARRGazer_embeddedcode/PID Controller1/I Gain'
//  '<S63>'  : 'STARRGazer_embeddedcode/PID Controller1/Ideal P Gain'
//  '<S64>'  : 'STARRGazer_embeddedcode/PID Controller1/Ideal P Gain Fdbk'
//  '<S65>'  : 'STARRGazer_embeddedcode/PID Controller1/Integrator'
//  '<S66>'  : 'STARRGazer_embeddedcode/PID Controller1/Integrator ICs'
//  '<S67>'  : 'STARRGazer_embeddedcode/PID Controller1/N Copy'
//  '<S68>'  : 'STARRGazer_embeddedcode/PID Controller1/N Gain'
//  '<S69>'  : 'STARRGazer_embeddedcode/PID Controller1/P Copy'
//  '<S70>'  : 'STARRGazer_embeddedcode/PID Controller1/Parallel P Gain'
//  '<S71>'  : 'STARRGazer_embeddedcode/PID Controller1/Reset Signal'
//  '<S72>'  : 'STARRGazer_embeddedcode/PID Controller1/Saturation'
//  '<S73>'  : 'STARRGazer_embeddedcode/PID Controller1/Saturation Fdbk'
//  '<S74>'  : 'STARRGazer_embeddedcode/PID Controller1/Sum'
//  '<S75>'  : 'STARRGazer_embeddedcode/PID Controller1/Sum Fdbk'
//  '<S76>'  : 'STARRGazer_embeddedcode/PID Controller1/Tracking Mode'
//  '<S77>'  : 'STARRGazer_embeddedcode/PID Controller1/Tracking Mode Sum'
//  '<S78>'  : 'STARRGazer_embeddedcode/PID Controller1/Tsamp - Integral'
//  '<S79>'  : 'STARRGazer_embeddedcode/PID Controller1/Tsamp - Ngain'
//  '<S80>'  : 'STARRGazer_embeddedcode/PID Controller1/postSat Signal'
//  '<S81>'  : 'STARRGazer_embeddedcode/PID Controller1/preInt Signal'
//  '<S82>'  : 'STARRGazer_embeddedcode/PID Controller1/preSat Signal'
//  '<S83>'  : 'STARRGazer_embeddedcode/PID Controller1/Anti-windup/Passthrough'
//  '<S84>'  : 'STARRGazer_embeddedcode/PID Controller1/D Gain/Internal Parameters'
//  '<S85>'  : 'STARRGazer_embeddedcode/PID Controller1/External Derivative/Error'
//  '<S86>'  : 'STARRGazer_embeddedcode/PID Controller1/Filter/Disc. Forward Euler Filter'
//  '<S87>'  : 'STARRGazer_embeddedcode/PID Controller1/Filter ICs/Internal IC - Filter'
//  '<S88>'  : 'STARRGazer_embeddedcode/PID Controller1/I Gain/Internal Parameters'
//  '<S89>'  : 'STARRGazer_embeddedcode/PID Controller1/Ideal P Gain/Passthrough'
//  '<S90>'  : 'STARRGazer_embeddedcode/PID Controller1/Ideal P Gain Fdbk/Disabled'
//  '<S91>'  : 'STARRGazer_embeddedcode/PID Controller1/Integrator/Discrete'
//  '<S92>'  : 'STARRGazer_embeddedcode/PID Controller1/Integrator ICs/Internal IC'
//  '<S93>'  : 'STARRGazer_embeddedcode/PID Controller1/N Copy/Disabled'
//  '<S94>'  : 'STARRGazer_embeddedcode/PID Controller1/N Gain/Internal Parameters'
//  '<S95>'  : 'STARRGazer_embeddedcode/PID Controller1/P Copy/Disabled'
//  '<S96>'  : 'STARRGazer_embeddedcode/PID Controller1/Parallel P Gain/Internal Parameters'
//  '<S97>'  : 'STARRGazer_embeddedcode/PID Controller1/Reset Signal/Disabled'
//  '<S98>'  : 'STARRGazer_embeddedcode/PID Controller1/Saturation/Passthrough'
//  '<S99>'  : 'STARRGazer_embeddedcode/PID Controller1/Saturation Fdbk/Disabled'
//  '<S100>' : 'STARRGazer_embeddedcode/PID Controller1/Sum/Sum_PID'
//  '<S101>' : 'STARRGazer_embeddedcode/PID Controller1/Sum Fdbk/Disabled'
//  '<S102>' : 'STARRGazer_embeddedcode/PID Controller1/Tracking Mode/Disabled'
//  '<S103>' : 'STARRGazer_embeddedcode/PID Controller1/Tracking Mode Sum/Passthrough'
//  '<S104>' : 'STARRGazer_embeddedcode/PID Controller1/Tsamp - Integral/TsSignalSpecification'
//  '<S105>' : 'STARRGazer_embeddedcode/PID Controller1/Tsamp - Ngain/Passthrough'
//  '<S106>' : 'STARRGazer_embeddedcode/PID Controller1/postSat Signal/Forward_Path'
//  '<S107>' : 'STARRGazer_embeddedcode/PID Controller1/preInt Signal/Internal PreInt'
//  '<S108>' : 'STARRGazer_embeddedcode/PID Controller1/preSat Signal/Forward_Path'

#endif                                 // STARRGazer_embeddedcode_h_

//
// File trailer for generated code.
//
// [EOF]
//
