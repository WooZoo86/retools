"""
The pseudocode of ARMv7 uses several functions / constants that
offer type information so we can generate better code.
"""
# Set the types for implicit things in the pseudocode.
known_types = []

# Set the types for known expressions.
known_types.append({"name" : "APSR.C",                           "type" : ("int",  1)})
known_types.append({"name" : "APSR.GE",                          "type" : ("int",  1)})
known_types.append({"name" : "APSR.N",                           "type" : ("int",  1)})
known_types.append({"name" : "APSR.Q",                           "type" : ("int",  1)})
known_types.append({"name" : "APSR.V",                           "type" : ("int",  1)})
known_types.append({"name" : "APSR.Z",                           "type" : ("int",  1)})
known_types.append({"name" : "ARMExpandImm",                     "type" : ("int", 32)})
known_types.append({"name" : "ARMExpandImm_C",                   "type" : ("list", 2)})
known_types.append({"name" : "AddWithCarry",                     "type" : ("list", 3)})
known_types.append({"name" : "AdvSIMDExpandImm",                 "type" : ("int", 64)})
known_types.append({"name" : "Align",                            "type" : ("int", 32)})
known_types.append({"name" : "BigEndian",                        "type" : ("int",  1)})
known_types.append({"name" : "BitCount",                         "type" : ("int", 32)})
known_types.append({"name" : "CPSR",                             "type" : ("int", 32)})
known_types.append({"name" : "CPSR.M",                           "type" : ("int",  1)})
known_types.append({"name" : "ConditionPassed",                  "type" : ("int",  1)})
known_types.append({"name" : "Coproc_Accepted",                  "type" : ("int",  1)})
known_types.append({"name" : "Coproc_DoneLoading",               "type" : ("int",  1)})
known_types.append({"name" : "Coproc_DoneStoring",               "type" : ("int",  1)})
known_types.append({"name" : "Coproc_GetOneWord",                "type" : ("int",  1)})
known_types.append({"name" : "Coproc_GetTwoWords",               "type" : ("list", 2)})
known_types.append({"name" : "Coproc_GetTwoWords",               "type" : ("list", 2)})
known_types.append({"name" : "Coproc_GetWordToStore",            "type" : ("int", 32)})
known_types.append({"name" : "CurrentCond",                      "type" : ("int",  4)})
known_types.append({"name" : "CurrentModeIsHyp",                 "type" : ("int",  1)})
known_types.append({"name" : "CurrentModeIsNotUser",             "type" : ("int",  1)})
known_types.append({"name" : "CurrentModeIsUserOrSystem",        "type" : ("int",  1)})
known_types.append({"name" : "DecodeImmShift",                   "type" : ("list", 2)})
known_types.append({"name" : "DecodeRegShift",                   "type" : ("int", 32)})
known_types.append({"name" : "ELR_hyp",                          "type" : ("int", 32)})
known_types.append({"name" : "FPCompare",                        "type" : ("list", 4)})
known_types.append({"name" : "FPCompareEQ",                      "type" : ("int",  1)})
known_types.append({"name" : "FPCompareGE",                      "type" : ("int",  1)})
known_types.append({"name" : "FPCompareGT",                      "type" : ("int",  1)})
known_types.append({"name" : "FPDoubleToSingle",                 "type" : ("int", 32)})
known_types.append({"name" : "FPHalfToSingle",                   "type" : ("int", 32)})
known_types.append({"name" : "FPRSqrtEstimate",                  "type" : ("int", 32)})
known_types.append({"name" : "FPRSqrtStep",                      "type" : ("int", 32)})
known_types.append({"name" : "FPRecipEstimate",                  "type" : ("int", 32)})
known_types.append({"name" : "FPRecipStep",                      "type" : ("int", 32)})
known_types.append({"name" : "FPSCR.C",                          "type" : ("int",  1)})
known_types.append({"name" : "FPSCR.N",                          "type" : ("int",  1)})
known_types.append({"name" : "FPSCR.V",                          "type" : ("int",  1)})
known_types.append({"name" : "FPSCR.Z",                          "type" : ("int",  1)})
known_types.append({"name" : "FPSingleToDouble",                 "type" : ("int", 64)})
known_types.append({"name" : "FPSingleToHalf",                   "type" : ("int", 16)})
known_types.append({"name" : "HasVirtExt",                       "type" : ("int",  1)})
known_types.append({"name" : "HaveLPAE",                         "type" : ("int",  1)})
known_types.append({"name" : "HaveMPExt",                        "type" : ("int",  1)})
known_types.append({"name" : "HaveVirtExt",                      "type" : ("int",  1)})
known_types.append({"name" : "ITSTATE.IT",                       "type" : ("int",  1)})
known_types.append({"name" : "InITBlock",                        "type" : ("int",  1)})
known_types.append({"name" : "InstrSet_ARM",                     "type" : ("int", 32)})
known_types.append({"name" : "InstrSet_Thumb",                   "type" : ("int", 32)})
known_types.append({"name" : "IntegerZeroDivideTrappingEnabled", "type" : ("int",  1)})
known_types.append({"name" : "IsAlignmentFault",                 "type" : ("int",  1)})
known_types.append({"name" : "IsExternalAbort",                  "type" : ("int",  1)})
known_types.append({"name" : "IsExternalAbort",                  "type" : ("int",  1)})
known_types.append({"name" : "IsSecure",                         "type" : ("int",  1)})
known_types.append({"name" : "IsZero",                           "type" : ("int",  1)})
known_types.append({"name" : "IsZeroBit",                        "type" : ("int",  1)})
known_types.append({"name" : "JazelleAcceptsExecution",          "type" : ("int",  1)})
known_types.append({"name" : "LR",                               "type" : ("int", 32)})
known_types.append({"name" : "LSInstructionSyndrome",            "type" : ("int",  9)})
known_types.append({"name" : "LastInITBlock",                    "type" : ("int",  1)})
known_types.append({"name" : "MBReqDomain_FullSystem",           "type" : ("int", 32)})
known_types.append({"name" : "MBReqDomain_InnerShareable",       "type" : ("int", 32)})
known_types.append({"name" : "MBReqDomain_Nonshareable",         "type" : ("int", 32)})
known_types.append({"name" : "MBReqDomain_OuterShareable",       "type" : ("int", 32)})
known_types.append({"name" : "MBReqTypes_All",                   "type" : ("int", 32)})
known_types.append({"name" : "MBReqTypes_Writes",                "type" : ("int", 32)})
known_types.append({"name" : "PC",                               "type" : ("int", 32)})
known_types.append({"name" : "PCStoreValue",                     "type" : ("int", 32)})
known_types.append({"name" : "RemapRegsHaveResetValues",         "type" : ("int",  1)})
known_types.append({"name" : "SP",                               "type" : ("int", 32)})
known_types.append({"name" : "SatQ",                             "type" : ("list", 2)})
known_types.append({"name" : "Shift",                            "type" : ("int", 32)})
known_types.append({"name" : "Shift_C",                          "type" : ("list", 2)})
known_types.append({"name" : "SignedSatQ",                       "type" : ("list", 2)})
known_types.append({"name" : "StandardFPSCRValue",               "type" : ("int", 32)})
known_types.append({"name" : "ThisInstr",                        "type" : ("int", 32)})
known_types.append({"name" : "ThumbExpandImm",                   "type" : ("int", 32)})
known_types.append({"name" : "ThumbExpandImm_C",                 "type" : ("list", 2)})
known_types.append({"name" : "UInt",                             "type" : ("int", 32)})
known_types.append({"name" : "UnalignedSupport",                 "type" : ("int",  1)})
known_types.append({"name" : "UnsignedRSqrtEstimate",            "type" : ("int", 32)})
known_types.append({"name" : "UnsignedRecipEstimate",            "type" : ("int", 32)})
known_types.append({"name" : "UnsignedSatQ",                     "type" : ("list", 2)})
known_types.append({"name" : "VBitOps_VBIF",                     "type" : ("int", 32)})
known_types.append({"name" : "VBitOps_VBIT",                     "type" : ("int", 32)})
known_types.append({"name" : "VBitOps_VBSL",                     "type" : ("int", 32)})
known_types.append({"name" : "VBitOps_VBSL",                     "type" : ("int", 32)})
known_types.append({"name" : "VCGEtype_fp",                      "type" : ("int", 32)})
known_types.append({"name" : "VCGEtype_signed",                  "type" : ("int", 32)})
known_types.append({"name" : "VCGEtype_unsigned",                "type" : ("int", 32)})
known_types.append({"name" : "VCGTtype_fp",                      "type" : ("int", 32)})
known_types.append({"name" : "VCGTtype_signed",                  "type" : ("int", 32)})
known_types.append({"name" : "VCGTtype_unsigned",                "type" : ("int", 32)})
known_types.append({"name" : "VFPNegMul_VNMLA",                  "type" : ("int", 32)})
known_types.append({"name" : "VFPNegMul_VNMLS",                  "type" : ("int", 32)})
known_types.append({"name" : "VFPNegMul_VNMUL",                  "type" : ("int", 32)})
known_types.append({"name" : "write_g",                          "type" : ("int",  1)})
known_types.append({"name" : "write_nzcvq",                      "type" : ("int",  1)})