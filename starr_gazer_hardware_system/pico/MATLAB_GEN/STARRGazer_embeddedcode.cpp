//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
//
// File: STARRGazer_embeddedcode.cpp
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
#include "rtwtypes.h"

// Model step function
void ustarr_sim::step()
{
  real_T rtb_FilterCoefficient;
  real_T rtb_IntegralGain;
  real_T rtb_ProportionalGain;
  real_T rtb_Tsamp;
  real_T rtb_Yaw_error;

  // Gain: '<Root>/Gain' incorporates:
  //   UnitDelay: '<Root>/Unit Delay'

  rtb_Yaw_error = rtP.Gain_Gain * rtDW.UnitDelay_DSTATE;

  // Outport: '<Root>/Out1'
  rtY.Out1 = rtb_Yaw_error;

  // Sum: '<Root>/Subtract' incorporates:
  //   Inport: '<Root>/In1'

  rtb_Yaw_error = rtU.PitchInput - rtb_Yaw_error;

  // SampleTimeMath: '<S34>/Tsamp' incorporates:
  //   Gain: '<S30>/Derivative Gain'
  //
  //  About '<S34>/Tsamp':
  //   y = u * K where K = 1 / ( w * Ts )
  //
  rtb_Tsamp = rtP.PIDController_D * rtb_Yaw_error * rtP.Tsamp_WtEt;

  // Gain: '<S44>/Proportional Gain'
  rtb_ProportionalGain = rtP.PIDController_P * rtb_Yaw_error;

  // Gain: '<S36>/Integral Gain'
  rtb_IntegralGain = rtP.PIDController_I * rtb_Yaw_error;

  // Gain: '<Root>/Gain1' incorporates:
  //   UnitDelay: '<Root>/Unit Delay1'

  rtb_Yaw_error = rtP.Gain1_Gain * rtDW.UnitDelay1_DSTATE;

  // Outport: '<Root>/Out2'
  rtY.Out2 = rtb_Yaw_error;

  // Sum: '<Root>/Subtract1' incorporates:
  //   Inport: '<Root>/In2'

  rtb_Yaw_error = rtU.YawInput - rtb_Yaw_error;

  // Gain: '<S94>/Filter Coefficient' incorporates:
  //   DiscreteIntegrator: '<S86>/Filter'
  //   Gain: '<S84>/Derivative Gain'
  //   Sum: '<S86>/SumD'

  rtb_FilterCoefficient = (rtP.PIDController1_D * rtb_Yaw_error -
    rtDW.Filter_DSTATE) * rtP.PIDController1_N;

  // Update for UnitDelay: '<Root>/Unit Delay' incorporates:
  //   Delay: '<S32>/UD'
  //   DiscreteIntegrator: '<S39>/Integrator'
  //   Sum: '<S32>/Diff'
  //   Sum: '<S48>/Sum'

  rtDW.UnitDelay_DSTATE = (rtb_ProportionalGain + rtDW.Integrator_DSTATE) +
    (rtb_Tsamp - rtDW.UD_DSTATE);

  // Update for Delay: '<S32>/UD'
  rtDW.UD_DSTATE = rtb_Tsamp;

  // Update for DiscreteIntegrator: '<S39>/Integrator'
  rtDW.Integrator_DSTATE += rtP.Integrator_gainval * rtb_IntegralGain;

  // Update for UnitDelay: '<Root>/Unit Delay1' incorporates:
  //   DiscreteIntegrator: '<S91>/Integrator'
  //   Gain: '<S96>/Proportional Gain'
  //   Sum: '<S100>/Sum'

  rtDW.UnitDelay1_DSTATE = (rtP.PIDController1_P * rtb_Yaw_error +
    rtDW.Integrator_DSTATE_p) + rtb_FilterCoefficient;

  // Update for DiscreteIntegrator: '<S86>/Filter'
  rtDW.Filter_DSTATE += rtP.Filter_gainval * rtb_FilterCoefficient;

  // Update for DiscreteIntegrator: '<S91>/Integrator' incorporates:
  //   Gain: '<S88>/Integral Gain'

  rtDW.Integrator_DSTATE_p += rtP.PIDController1_I * rtb_Yaw_error *
    rtP.Integrator_gainval_a;
}

// Model initialize function
void ustarr_sim::initialize()
{
  // InitializeConditions for UnitDelay: '<Root>/Unit Delay'
  rtDW.UnitDelay_DSTATE = rtP.UnitDelay_InitialCondition;

  // InitializeConditions for Delay: '<S32>/UD'
  rtDW.UD_DSTATE = rtP.PIDController_DifferentiatorICP;

  // InitializeConditions for DiscreteIntegrator: '<S39>/Integrator'
  rtDW.Integrator_DSTATE = rtP.PIDController_InitialConditionF;

  // InitializeConditions for UnitDelay: '<Root>/Unit Delay1'
  rtDW.UnitDelay1_DSTATE = rtP.UnitDelay1_InitialCondition;

  // InitializeConditions for DiscreteIntegrator: '<S86>/Filter'
  rtDW.Filter_DSTATE = rtP.PIDController1_InitialCondition;

  // InitializeConditions for DiscreteIntegrator: '<S91>/Integrator'
  rtDW.Integrator_DSTATE_p = rtP.PIDController1_InitialConditi_k;
}

// Constructor
ustarr_sim::ustarr_sim():
  rtU(),
  rtY(),
  rtDW()
{
  // Currently there is no constructor body generated.
}

// Destructor
// Currently there is no destructor body generated.
ustarr_sim::~ustarr_sim() = default;

//
// File trailer for generated code.
//
// [EOF]
//
