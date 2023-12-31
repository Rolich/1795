/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * Copyright (c) 2010 TELEMATICS LAB, DEE - Politecnico di Bari
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 * Author: Giuseppe Piro  <g.piro@poliba.it>
 * Modified by: NIST
 * Modified by: <luca.lusvarghi5@unimore.it>
 */

#ifndef NR_V2X_SPECTRUM_VALUE_HELPER_H
#define NR_V2X_SPECTRUM_VALUE_HELPER_H


#include <ns3/spectrum-value.h>
#include <vector>

namespace ns3 {


/**
 * \ingroup lte
 *
 * \brief This class defines all functions to create spectrum model for lte
 */
class NrV2XSpectrumValueHelper
{
public:

  /**
   * Calculates the carrier frequency from the E-UTRA Absolute
   * Radio Frequency Channel Number (EARFCN) according to 3GPP TS
   * 36.101 section 5.7.3 "Carrier frequency and EARFCN".
   *
   * \param earfcn the EARFCN
   *
   * \return the carrier frequency in Hz
   */
  static double GetCarrierFrequency (uint16_t earfcn);

  /**
   * Calculates the dowlink carrier frequency from the E-UTRA Absolute
   * Radio Frequency Channel Number (EARFCN) using the formula in 3GPP TS
   * 36.101 section 5.7.3 "Carrier frequency and EARFCN".
   *
   * \param earfcn the EARFCN
   *
   * \return the dowlink carrier frequency in Hz
   */
  static double GetDownlinkCarrierFrequency (uint16_t earfcn);

  /**
   * Calculates the uplink carrier frequency from the E-UTRA Absolute
   * Radio Frequency Channel Number (EARFCN) using the formula in 3GPP TS
   * 36.101 section 5.7.3 "Carrier frequency and EARFCN".
   *
   * \param earfcn the EARFCN
   *
   * \return the uplink carrier frequency in Hz
   */
  static double GetUplinkCarrierFrequency (uint16_t earfcn);

  /**
   *
   *
   * \param txBandwidthConf the tranmission bandwidth
   * configuration in number of resource blocks
   *
   * \return the nominal channel bandwidth in Hz as per 3GPP TS 36.101
   */
  static double GetChannelBandwidth (uint16_t txBandwidthConf);

  /**
   *
   * \param earfcn the carrier frequency (EARFCN) at which reception
   * is made
   * \param bandwidth the Transmission Bandwidth Configuration in
   * number of resource blocks
   *
   * \return the static SpectrumModel instance corresponding to the
   * given carrier frequency and transmission bandwidth
   * configuration. If such SpectrumModel does not exist, it is
   * created.
   */
  static Ptr<SpectrumModel> GetSpectrumModel (uint16_t earfcn, uint16_t bandwidth);


  /**
   * create a spectrum value representing the power spectral
   * density of a signal to be transmitted. See 3GPP TS 36.101 for
   * a definition of most of the parameters described here.
   *
   * \param earfcn the carrier frequency (EARFCN) of the transmission
   * \param bandwidth the Transmission Bandwidth Configuration in
   * number of resource blocks
   * \param powerTx the total power in dBm over the whole bandwidth
   * \param activeRbs the list of Active Resource Blocks (PRBs)
   *
   * \return a pointer to a newly allocated SpectrumValue representing the TX Power Spectral Density in W/Hz for each Resource Block
   */
  static Ptr<SpectrumValue> CreateTxPowerSpectralDensity (uint16_t earfcn,
                                                          uint16_t bandwidth,
                                                          double powerTx,
                                                          std::vector <int> activeRbs);

  /**
   * create a spectrum value representing the power spectral
   * density of a signal to be transmitted. See 3GPP TS 36.101 for
   * a definition of most of the parameters described here.
   * This function splits the power over the active RBs instead of the entire bandwidth
   * \param earfcn the carrier frequency (EARFCN) of the transmission
   * \param powerTx the total power in dBm over the whole bandwidth
   * \param activeRbs the list of Active Resource Blocks (PRBs)
   *
   * \return a pointer to a newly allocated SpectrumValue representing the TX Power Spectral Density in W/Hz for each Resource Block
   */
  static Ptr<SpectrumValue> CreateUlTxPowerSpectralDensity (uint16_t earfcn,
                                                          uint16_t bandwidth,
                                                          double powerTx,
                                                          std::vector <int> activeRbs, 
                                                          double slotDuration,
                                                          uint16_t SCS,
                                                          uint16_t mcsIndex,
                                                          bool IBE);
  /**
   * create a spectrum value representing the power spectral
   * density of a signal to be transmitted. See 3GPP TS 36.101 for
   * a definition of most of the parameters described here.
   *
   * \param earfcn the carrier frequency (EARFCN) of the transmission
   * \param bandwidth the Transmission Bandwidth Configuration in
   * number of resource blocks
   * \param powerTx the total power in dBm over the whole bandwidth
   * \param powerTxMap the map of power in dBm for each RB,
   * if map contain power for RB, powerTx is not used for this RB,
   * otherwise powerTx is set for this RB
   * \param activeRbs the list of Active Resource Blocks (PRBs)
   *
   * \return a pointer to a newly allocated SpectrumValue representing the TX Power Spectral Density in W/Hz for each Resource Block
   */
  static Ptr<SpectrumValue> CreateTxPowerSpectralDensity (uint16_t earfcn,
                                                          uint16_t bandwidth,
                                                          double powerTx,
                                                          std::map<int, double> powerTxMap,
                                                          std::vector <int> activeRbs);

  /**
   * create a SpectrumValue that models the power spectral density of AWGN
   *
   * \param earfcn the carrier frequency (EARFCN) at which reception
   * is made
   * \param bandwidth the Transmission Bandwidth Configuration in
   * number of resource blocks
   * \param noiseFigure the noise figure in dB w.r.t. a reference temperature of 290K
   *
   * \return a pointer to a newly allocated SpectrumValue representing the noise Power Spectral Density in W/Hz for each Resource Block
   */
  static Ptr<SpectrumValue> CreateNoisePowerSpectralDensity (uint16_t earfcn, uint16_t bandwidth, double noiseFigure);

  /**
   *  create a SpectrumValue that models the power spectral density of AWGN
   *
   * \param noiseFigure  the noise figure in dB  w.r.t. a reference temperature of 290K
   * \param spectrumModel the SpectrumModel instance to be used
   *
   * \return a pointer to a newly allocated SpectrumValue representing the noise Power Spectral Density in W/Hz for each Resource Block
   */
  static Ptr<SpectrumValue> CreateNoisePowerSpectralDensity (double noiseFigure, Ptr<SpectrumModel> spectrumModel);


};


} // namespace ns3



#endif /*  NR_V2X_SPECTRUM_VALUE_HELPER_H */
