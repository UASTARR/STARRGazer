//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
//
// File: STARRGazer_embeddedcode_data.cpp
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
#include "STARRGazer_embeddedcode.h"

// Block parameters (default storage)
ustarr_sim::P ustarr_sim::rtP{
  // Mask Parameter: PIDController_D
  //  Referenced by: '<S30>/Derivative Gain'

  -0.00062160966127948838,

  // Mask Parameter: PIDController1_D
  //  Referenced by: '<S84>/Derivative Gain'

  -0.0126517123405476,

  // Mask Parameter: PIDController_DifferentiatorICP
  //  Referenced by: '<S32>/UD'

  0.0,

  // Mask Parameter: PIDController_I
  //  Referenced by: '<S36>/Integral Gain'

  0.087802518404973592,

  // Mask Parameter: PIDController1_I
  //  Referenced by: '<S88>/Integral Gain'

  0.00750088180468963,

  // Mask Parameter: PIDController1_InitialCondition
  //  Referenced by: '<S86>/Filter'

  0.0,

  // Mask Parameter: PIDController_InitialConditionF
  //  Referenced by: '<S39>/Integrator'

  0.0,

  // Mask Parameter: PIDController1_InitialConditi_k
  //  Referenced by: '<S91>/Integrator'

  0.0,

  // Mask Parameter: PIDController1_N
  //  Referenced by: '<S94>/Filter Coefficient'

  3.5978185978083,

  // Mask Parameter: PIDController_P
  //  Referenced by: '<S44>/Proportional Gain'

  2.2255876033347297,

  // Mask Parameter: PIDController1_P
  //  Referenced by: '<S96>/Proportional Gain'

  0.0524976391518717,

  // Expression: 0
  //  Referenced by: '<Root>/Unit Delay'

  0.0,

  // Expression: 0.125
  //  Referenced by: '<Root>/Gain'

  0.125,

  // Computed Parameter: Tsamp_WtEt
  //  Referenced by: '<S34>/Tsamp'

  14.0,

  // Computed Parameter: Integrator_gainval
  //  Referenced by: '<S39>/Integrator'

  0.071428571428571425,

  // Expression: 0
  //  Referenced by: '<Root>/Unit Delay1'

  0.0,

  // Expression: 0.1
  //  Referenced by: '<Root>/Gain1'

  0.1,

  // Computed Parameter: Filter_gainval
  //  Referenced by: '<S86>/Filter'

  0.071428571428571425,

  // Computed Parameter: Integrator_gainval_a
  //  Referenced by: '<S91>/Integrator'

  0.071428571428571425
};

//
// File trailer for generated code.
//
// [EOF]
//
