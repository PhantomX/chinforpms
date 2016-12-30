/*
 * Intel ACPI Component Architecture
 * AML Disassembler version 20090625
 *
 * Disassembly of dsdt.dat, Fri Oct  9 02:23:40 2009
 *
 *
 * Original Table Header:
 *     Signature        "DSDT"
 *     Length           0x00006E13 (28179)
 *     Revision         0x01 **** ACPI 1.0, no 64-bit math support
 *     Checksum         0xC5
 *     OEM ID           "AMD770"
 *     OEM Table ID     "AWRDACPI"
 *     OEM Revision     0x00001000 (4096)
 *     Compiler ID      "MSFT"
 *     Compiler Version 0x03000000 (50331648)
 */
DefinitionBlock ("dsdt.aml", "DSDT", 1, "AMD770", "AWRDACPI", 0x00001001)
{
    External (LNKB)
    External (LNKA)
    External (LNKD)
    External (LNKC)
    External (\_PR.C000)
    External (\_PR.C001)
    External (\_PR.C002)
    External (\_PR.C003)

    Scope (\_PR)
    {
        Processor (\_PR.C000, 0x00, 0x00004010, 0x06) {}
        Processor (\_PR.C001, 0x01, 0x00004010, 0x06) {}
        Processor (\_PR.C002, 0x02, 0x00004010, 0x06) {}
        Processor (\_PR.C003, 0x03, 0x00004010, 0x06) {}
    }

    Name (\_S0, Package (0x04)
    {
        0x00, 
        0x00, 
        0x00, 
        0x00
    })
    Name (\_S3, Package (0x04)
    {
        0x03, 
        0x01, 
        0x01, 
        0x01
    })
    Name (\_S4, Package (0x04)
    {
        0x04, 
        0x04, 
        0x04, 
        0x04
    })
    Name (\_S5, Package (0x04)
    {
        0x05, 
        0x05, 
        0x05, 
        0x05
    })
    OperationRegion (\DEBG, SystemIO, 0x80, 0x01)
    Field (\DEBG, ByteAcc, NoLock, Preserve)
    {
        DBG1,   8
    }

    Name (OSTY, Ones)
    OperationRegion (ACMS, SystemIO, 0x72, 0x02)
    Field (ACMS, ByteAcc, NoLock, Preserve)
    {
        ICMS,   8, 
        DCMS,   8
    }

    IndexField (ICMS, DCMS, ByteAcc, NoLock, Preserve)
    {
                Offset (0x01), 
                Offset (0x04), 
                Offset (0x08), 
        BS_A,   32, 
        REV0,   8, 
        REV1,   8
    }

    OperationRegion (ACAF, SystemMemory, BS_A, 0x20)
    Field (ACAF, AnyAcc, NoLock, Preserve)
    {
        OCC0,   1, 
        OCC1,   1, 
        OCC2,   1, 
        OCC3,   1, 
        OCC4,   1, 
        OCC5,   1, 
        OCC6,   1, 
        OCC7,   1, 
        OCC8,   1, 
        OCC9,   1, 
                Offset (0x02), 
        TPMF,   1, 
        STHP,   1, 
        SHPG,   1, 
        OSCF,   1, 
                Offset (0x04), 
        PCIE,   32, 
        HPBS,   32, 
        OCM0,   4, 
        OCM1,   4, 
        OCM2,   4, 
        OCM3,   4, 
        OCM4,   4, 
        OCM5,   4, 
        OCM6,   4, 
        OCM7,   4, 
        OCM8,   4, 
        OCM9,   4, 
                Offset (0x14), 
        P92T,   8
    }

    OperationRegion (CMPT, SystemIO, 0x0C50, 0x03)
    Field (CMPT, ByteAcc, NoLock, Preserve)
    {
        CMID,   8, 
            ,   6, 
        GPCT,   2, 
        GP0I,   1, 
        GP1I,   1, 
        GP2I,   1, 
        GP3I,   1, 
        GP4I,   1, 
        GP5I,   1, 
        GP6I,   1, 
        GP7I,   1
    }

    OperationRegion (PCFG, SystemMemory, PCIE, 0x02000000)
    Field (PCFG, AnyAcc, NoLock, Preserve)
    {
                Offset (0x90024), 
        STB5,   32, 
                Offset (0x98042), 
        PT0D,   1, 
        PT1D,   1, 
        PT2D,   1, 
        PT3D,   1, 
        PT4D,   1, 
        PT5D,   1, 
        PT6D,   1, 
        PT7D,   1, 
        PT8D,   1, 
        PT9D,   1, 
                Offset (0xA0004), 
        SMIE,   1, 
        SMME,   1, 
                Offset (0xA0008), 
        RVID,   8, 
                Offset (0xA0014), 
        SMB1,   32, 
                Offset (0xA0078), 
            ,   14, 
        P92E,   1
    }

    OperationRegion (BAR, SystemMemory, STB5, 0x1000)
    Field (BAR, AnyAcc, NoLock, Preserve)
    {
                Offset (0x120), 
            ,   7, 
        PMBY,   1, 
                Offset (0x128), 
        PMS0,   4, 
                Offset (0x129), 
        PMS1,   4, 
                Offset (0x12C), 
        DET0,   4, 
                Offset (0x130), 
                Offset (0x132), 
        PRC0,   1, 
                Offset (0x1A0), 
            ,   7, 
        SMBY,   1, 
                Offset (0x1A8), 
        SMS0,   4, 
                Offset (0x1A9), 
        SMS1,   4, 
                Offset (0x1AC), 
        DET1,   4, 
                Offset (0x1B0), 
                Offset (0x1B2), 
        PRC1,   1, 
                Offset (0x220), 
            ,   7, 
        PSBY,   1, 
                Offset (0x228), 
        PSS0,   4, 
                Offset (0x229), 
        PSS1,   4, 
                Offset (0x22C), 
        DET2,   4, 
                Offset (0x230), 
                Offset (0x232), 
        PRC2,   1, 
                Offset (0x2A0), 
            ,   7, 
        SSBY,   1, 
                Offset (0x2A8), 
        SSS0,   4, 
                Offset (0x2A9), 
        SSS1,   4, 
                Offset (0x2AC), 
        DET3,   4, 
                Offset (0x2B0), 
                Offset (0x2B2), 
        PRC3,   1
    }

    OperationRegion (PMIO, SystemIO, 0x0CD6, 0x02)
    Field (PMIO, ByteAcc, NoLock, Preserve)
    {
        INPM,   8, 
        DAPM,   8
    }

    IndexField (INPM, DAPM, ByteAcc, NoLock, Preserve)
    {
            ,   1, 
        TM1E,   1, 
        TM2E,   1, 
                Offset (0x01), 
            ,   1, 
        TM1S,   1, 
        TM2S,   1, 
                Offset (0x04), 
            ,   7, 
        SLPS,   1, 
                Offset (0x07), 
            ,   7, 
        CLPS,   1, 
                Offset (0x10), 
            ,   6, 
        PWDE,   1, 
                Offset (0x1C), 
            ,   3, 
        MKME,   1, 
        PI3E,   1, 
        PI2E,   1, 
        PI1E,   1, 
        PI0E,   1, 
            ,   3, 
        MKMS,   1, 
        PI3S,   1, 
        PI2S,   1, 
        PI1S,   1, 
        PI0S,   1, 
                Offset (0x20), 
        P1EB,   16, 
                Offset (0x36), 
            ,   6, 
        GV6P,   1, 
        GV7P,   1, 
            ,   3, 
        GM0P,   1, 
        GM1P,   1, 
        GM2P,   1, 
        GM3P,   1, 
        GM8P,   1, 
            ,   1, 
        GM4P,   1, 
        GM5P,   1, 
            ,   1, 
        GM6P,   1, 
        GM7P,   1, 
                Offset (0x3B), 
        GPX0,   1, 
        GPX4,   1, 
        GPX5,   1, 
        GPX1,   1, 
        GPX6,   1, 
        GPX7,   1, 
        GPX2,   1, 
        GPX3,   1, 
                Offset (0x55), 
        SPRE,   1, 
            ,   1, 
            ,   1, 
        EPNM,   1, 
        DPPF,   1, 
        FNGS,   1, 
                Offset (0x61), 
            ,   7, 
        R617,   1, 
                Offset (0x65), 
            ,   4, 
        RSTU,   1, 
                Offset (0x68), 
            ,   3, 
        TPDE,   1, 
            ,   1, 
                Offset (0x92), 
            ,   7, 
        GV7S,   1, 
                Offset (0x96), 
        GP8I,   1, 
        GP9I,   1, 
                Offset (0x9A), 
            ,   7, 
        HECO,   1, 
                Offset (0xA8), 
        PI4E,   1, 
        PI5E,   1, 
        PI6E,   1, 
        PI7E,   1, 
                Offset (0xA9), 
        PI4S,   1, 
        PI5S,   1, 
        PI6S,   1, 
        PI7S,   1
    }

    OperationRegion (P1E0, SystemIO, P1EB, 0x04)
    Field (P1E0, ByteAcc, NoLock, Preserve)
    {
            ,   14, 
        PEWS,   1, 
        WSTA,   1, 
            ,   14, 
        PEWD,   1
    }

    Method (C_OC, 0, NotSerialized)
    {
        Sleep (0x14)
        Store (0x13, CMID)
        Store (Zero, GPCT)
    }

    Method (U_OC, 2, NotSerialized)
    {
        If (LEqual (OCM0, Arg0))
        {
            Store (Arg1, PT0D)
        }

        If (LEqual (OCM1, Arg0))
        {
            Store (Arg1, PT1D)
        }

        If (LEqual (OCM2, Arg0))
        {
            Store (Arg1, PT2D)
        }

        If (LEqual (OCM3, Arg0))
        {
            Store (Arg1, PT3D)
        }

        If (LEqual (OCM4, Arg0))
        {
            Store (Arg1, PT4D)
        }

        If (LEqual (OCM5, Arg0))
        {
            Store (Arg1, PT5D)
        }

        If (LEqual (OCM6, Arg0))
        {
            Store (Arg1, PT6D)
        }

        If (LEqual (OCM7, Arg0))
        {
            Store (Arg1, PT7D)
        }

        If (LEqual (OCM8, Arg0))
        {
            Store (Arg1, PT8D)
        }

        If (LEqual (OCM9, Arg0))
        {
            Store (Arg1, PT9D)
        }
    }

    Method (SPTS, 1, NotSerialized)
    {
        If (LEqual (Arg0, 0x03))
        {
            Store (Zero, RSTU)
        }

        Store (One, CLPS)
        Store (One, SLPS)
        If (LLessEqual (\RVID, 0x13))
        {
            Store (Zero, \PWDE)
        }

        If (LEqual (\P92T, 0x00))
        {
            Store (Zero, \PI0E)
        }

        If (LEqual (\P92T, 0x01))
        {
            Store (Zero, \PI1E)
        }

        If (LEqual (\P92T, 0x02))
        {
            Store (Zero, \PI2E)
        }

        If (LEqual (\P92T, 0x03))
        {
            Store (Zero, \PI3E)
        }

        If (LEqual (\P92T, 0x04))
        {
            Store (Zero, \PI4E)
        }

        If (LEqual (\P92T, 0x05))
        {
            Store (Zero, \PI5E)
        }

        If (LEqual (\P92T, 0x06))
        {
            Store (Zero, \PI6E)
        }

        If (LEqual (\P92T, 0x07))
        {
            Store (Zero, \PI7E)
        }

        If (LLessEqual (\P92T, 0x07))
        {
            Store (One, \P92E)
        }
    }

    Method (SWAK, 1, NotSerialized)
    {
        Store (One, HECO)
        If (LEqual (Arg0, 0x03))
        {
            Store (One, RSTU)
        }

        Store (\PEWS, \PEWS)
        If (LLessEqual (\P92T, 0x07))
        {
            Store (Zero, \P92E)
        }

        If (LEqual (\P92T, 0x00))
        {
            Store (One, \PI0E)
        }

        If (LEqual (\P92T, 0x01))
        {
            Store (One, \PI1E)
        }

        If (LEqual (\P92T, 0x02))
        {
            Store (One, \PI2E)
        }

        If (LEqual (\P92T, 0x03))
        {
            Store (One, \PI3E)
        }

        If (LEqual (\P92T, 0x04))
        {
            Store (One, \PI4E)
        }

        If (LEqual (\P92T, 0x05))
        {
            Store (One, \PI5E)
        }

        If (LEqual (\P92T, 0x06))
        {
            Store (One, \PI6E)
        }

        If (LEqual (\P92T, 0x07))
        {
            Store (One, \PI7E)
        }
    }

    Method (TRMD, 1, NotSerialized)
    {
        Store (Arg0, SPRE)
        Store (Arg0, TPDE)
    }

    If (OCC0)
    {
        Scope (\_GPE)
        {
            Method (_L13, 0, NotSerialized)
            {
                \C_OC ()
                If (LEqual (GP0I, GM0P))
                {
                    Not (GM0P, GM0P)
                    \U_OC (0x00, GM0P)
                }
            }
        }
    }

    If (OCC1)
    {
        Scope (\_GPE)
        {
            Method (_L14, 0, NotSerialized)
            {
                \C_OC ()
                If (LEqual (GP1I, GM1P))
                {
                    Not (GM1P, GM1P)
                    \U_OC (0x01, GM1P)
                }
            }
        }
    }

    If (OCC2)
    {
        Scope (\_GPE)
        {
            Method (_L15, 0, NotSerialized)
            {
                \C_OC ()
                If (LEqual (GP2I, GM2P))
                {
                    Not (GM2P, GM2P)
                    \U_OC (0x02, GM2P)
                }
            }
        }
    }

    If (OCC3)
    {
        Scope (\_GPE)
        {
            Method (_L16, 0, NotSerialized)
            {
                \C_OC ()
                If (LEqual (GP3I, GM3P))
                {
                    Not (GM3P, GM3P)
                    \U_OC (0x03, GM3P)
                }
            }
        }
    }

    If (OCC4)
    {
        Scope (\_GPE)
        {
            Method (_L19, 0, NotSerialized)
            {
                \C_OC ()
                If (LEqual (GP4I, GM4P))
                {
                    Not (GM4P, GM4P)
                    \U_OC (0x04, GM4P)
                }
            }
        }
    }

    If (OCC5)
    {
        Scope (\_GPE)
        {
            Method (_L1A, 0, NotSerialized)
            {
                \C_OC ()
                If (LEqual (GP5I, GM5P))
                {
                    Not (GM5P, GM5P)
                    \U_OC (0x05, GM5P)
                }
            }
        }
    }

    If (OCC6)
    {
        Scope (\_GPE)
        {
            Method (_L1C, 0, NotSerialized)
            {
                \C_OC ()
                If (LEqual (GP6I, GM6P))
                {
                    Not (GV6P, GV6P)
                    \U_OC (0x06, GV6P)
                }
            }
        }
    }

    If (OCC7)
    {
        Scope (\_GPE)
        {
            Method (_L1D, 0, NotSerialized)
            {
                \C_OC ()
                If (LEqual (GP7I, GM7P))
                {
                    Not (GV7P, GV7P)
                    \U_OC (0x07, GV7P)
                }
            }
        }
    }

    If (OCC8)
    {
        Scope (\_GPE)
        {
            Method (_L17, 0, NotSerialized)
            {
                \C_OC ()
                If (LEqual (GP8I, GM8P))
                {
                    Not (GM8P, GM8P)
                    \U_OC (0x08, GM8P)
                }
            }
        }
    }

    If (OCC9)
    {
        Scope (\_GPE)
        {
            Method (_L0E, 0, NotSerialized)
            {
                \C_OC ()
                If (LEqual (GP9I, 0x00))
                {
                    \U_OC (0x09, 0x01)
                }
            }
        }
    }

    Scope (\)
    {
        Name (SBA1, 0x0B00)
        Name (SBA2, 0x0B10)
        Name (SIOP, 0x2E)
        Name (GIOB, 0x0F40)
        OperationRegion (NCLK, SystemMemory, PCIE, 0x02000000)
        Field (NCLK, AnyAcc, NoLock, Preserve)
        {
                    Offset (0x4C), 
            CLKE,   1, 
                    Offset (0x104C), 
            P4EN,   1, 
            P4NM,   12, 
            P4HI,   12, 
            P4IO,   1, 
                    Offset (0x1050), 
            P5EN,   1, 
            P5NM,   12, 
            P5HI,   12, 
            P5IO,   1, 
                    Offset (0x1054), 
            P6EN,   1, 
            P6NM,   12, 
            P6HI,   12, 
            P6IO,   1, 
                    Offset (0x10B0), 
            P1NM,   12, 
            P1HI,   12, 
            P1EN,   1, 
            P1IO,   1, 
                    Offset (0x10B4), 
            P2NM,   12, 
            P2HI,   12, 
            P2EN,   1, 
            P2IO,   1, 
                    Offset (0x10CC), 
            P3EN,   1, 
            P3NM,   12, 
            P3HI,   12, 
            P3IO,   1
        }

        OperationRegion (SOR1, SystemIO, SBA1, 0x10)
        Field (SOR1, ByteAcc, NoLock, Preserve)
        {
            SMR0,   8, 
            SMR1,   8, 
            SMR2,   8, 
            SMR3,   8, 
            SMR4,   8, 
            SMR5,   8, 
            SMR6,   8, 
            SMR7,   8, 
            SMR8,   8, 
            SMR9,   8, 
            SMRA,   16, 
            SMRC,   16, 
            SMRE,   8
        }

        Mutex (MSMB, 0x00)
        Method (RWBK, 4, NotSerialized)
        {
            Acquire (MSMB, 0xFFFF)
            Store (SMR0, Local0)
            Store (0xFF, SMR0)
            Store (Arg1, Local1)
            Store (Arg2, Local2)
            If (LEqual (And (Arg0, 0x01), 0x01))
            {
                Store (Arg0, SMR4)
                Store (Arg1, SMR3)
                Store (0x54, SMR2)
                If (LEqual (WDNE (0xFFFF), 0x00))
                {
                    Store (SMR2, Local0)
                    Store (SMR5, Local0)
                    While (LNotEqual (Local0, 0x00))
                    {
                        Store (SMR7, Local3)
                        If (LNotEqual (Local2, 0x00))
                        {
                            Store (Local3, Index (Arg3, Local1))
                            Increment (Local1)
                            Decrement (Local2)
                        }

                        Decrement (Local0)
                    }
                }
                Else
                {
                    Store (0x01, Local0)
                }

                Store (0xFF, SMR0)
            }
            Else
            {
                Store (Arg0, SMR4)
                Store (Arg1, SMR3)
                Store (0x14, SMR2)
                Store (SMR2, Local0)
                Store (Local2, SMR5)
                While (LNotEqual (Local2, 0x00))
                {
                    Store (DerefOf (Index (Arg3, Local1)), SMR7)
                    Increment (Local1)
                    Decrement (Local2)
                }

                Store (0x1E, SMR0)
                While (LNotEqual (And (SMR0, 0x01), 0x00)) {}
                Store (Or (SMR2, 0x40), SMR2)
                Store (WDNE (0xFFFF), Local0)
                Store (0xFF, SMR0)
            }

            Release (MSMB)
            Return (Local0)
        }

        Method (RWAB, 3, NotSerialized)
        {
            Acquire (MSMB, 0xFFFF)
            Store (SMR0, Local0)
            Store (0xFF, SMR0)
            If (LEqual (And (Arg0, 0x01), 0x01))
            {
                Store (Arg0, SMR4)
                Store (Arg1, SMR3)
                Store (0x48, SMR2)
                If (LEqual (WDNE (0xFFFF), 0x00))
                {
                    Store (SMR5, Local0)
                }
                Else
                {
                    Store (0x00, Local0)
                }

                Store (0xFF, SMR0)
            }
            Else
            {
                Store (Arg2, SMR5)
                Store (Arg0, SMR4)
                Store (Arg1, SMR3)
                Store (0x48, SMR2)
                Store (WDNE (0xFFFF), Local0)
                Store (0xFF, SMR0)
            }

            Release (MSMB)
            Return (Local0)
        }

        Method (WDNE, 1, NotSerialized)
        {
            Store (0x00, Local0)
            While (LNotEqual (Local0, Arg0))
            {
                Store (0x00, Local1)
                While (LNotEqual (Local1, 0x64))
                {
                    Increment (Local1)
                }

                If (LEqual (And (SMR0, 0x02), 0x02))
                {
                    Return (0x00)
                }

                Increment (Local0)
            }

            Return (0x01)
        }

        OperationRegion (IOOR, SystemIO, SIOP, 0x02)
        Field (IOOR, ByteAcc, NoLock, Preserve)
        {
            IOID,   8, 
            IODT,   8
        }

        Name (LDNO, 0x00)
        Method (SIOI, 0, NotSerialized)
        {
            Store (0x87, IOID)
            Store (0x87, IOID)
            Store (RSIO (0x07), IOID)
            Store (IODT, LDNO)
        }

        Method (SIOO, 0, NotSerialized)
        {
            WSIO (0x07, LDNO)
            Store (0xAA, IOID)
        }

        Method (RSIO, 1, NotSerialized)
        {
            Store (Arg0, IOID)
            Return (IODT)
        }

        Method (WSIO, 2, NotSerialized)
        {
            Store (Arg0, IOID)
            Store (Arg1, IODT)
        }

        Device (AOD)
        {
            Name (CVID, 0x00)
            Name (OBID, Package (0x13)
            {
                0x09, 
                0x01010000, 
                0x01020000, 
                0x01030000, 
                0x02010000, 
                0x02020000, 
                0x02030000, 
                0x02040000, 
                0x02050000, 
                0x02060000, 
                "CPU Clock", 
                "PCIE Clock", 
                "South Bridge Clock", 
                "Memory VDDQ", 
                "Memory VTT", 
                "CPU VDDC", 
                "NB Core Voltage", 
                "NB PCIE Voltage", 
                "CPU HT Voltage"
            })
            Method (HM06, 0, NotSerialized)
            {
            }

            Method (HM07, 1, NotSerialized)
            {
                CreateDWordField (Arg0, 0x00, BIF1)
                Store (BIF1, CVID)
                If (LGreaterEqual (CVID, 0x20))
                {
                    Store (Subtract (0x000129DA, Multiply (Subtract (CVID, 0x20), 0x04E2)
                        ), CPUV)
                }
                Else
                {
                    Store (Subtract (0x00025D78, Multiply (CVID, 0x09C4)), CPUV)
                }
            }

            Name (ID01, 0x00)
            Name (ID02, 0x00)
            Method (SOID, 1, NotSerialized)
            {
                ShiftRight (Arg0, 0x18, ID01)
                ShiftRight (And (Arg0, 0x00FF0000), 0x10, ID02)
                Return (0x00)
            }

            Method (ABS, 2, NotSerialized)
            {
                If (LLess (Arg0, Arg1))
                {
                    Return (Subtract (Arg1, Arg0))
                }
                Else
                {
                    Return (Subtract (Arg0, Arg1))
                }
            }

            Name (TSBF, Buffer (0x20)
            {
                /* 0000 */    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                /* 0008 */    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                /* 0010 */    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                /* 0018 */    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
            })
            Name (GBUF, Buffer (0x10)
            {
                /* 0000 */    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                /* 0008 */    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
            })
            CreateDWordField (GBUF, 0x00, BSRC)
            CreateDWordField (GBUF, 0x04, RVCO)
            CreateDWordField (GBUF, 0x08, CPUV)
            CreateWordField (GBUF, 0x0C, NVAL)
            CreateByteField (GBUF, 0x0E, MVAL)
            Name (GVBF, Buffer (0x05)
            {
                0x00, 0x00, 0x00, 0x00, 0x00
            })
            CreateDWordField (GVBF, 0x00, GVB1)
            CreateByteField (GVBF, 0x04, GVB2)
            Method (GETC, 1, Serialized)
            {
                If (LEqual (\RWBK (0xD3, 0x00, 0x20, TSBF), 0x00))
                {
                    Store (0x00, GVB1)
                    Store (0x00, GVB2)
                    Store (GCFV (0x04, 0x37EE), BSRC)
                    While (One)
                    {
                        Name (T_0, 0x00)
                        Store (Add (Arg0, 0x00), T_0)
                        If (LEqual (T_0, 0x01))
                        {
                            Store (GCFV (0x01, Divide (BSRC, 0x02, )), GVB1)
                        }
                        Else
                        {
                            If (LEqual (T_0, 0x02))
                            {
                                Store (GCFV (0x02, 0x37EE), GVB1)
                            }
                            Else
                            {
                                If (LEqual (T_0, 0x03))
                                {
                                    Store (GCFV (0x03, 0x37EE), GVB1)
                                }
                                Else
                                {
                                    Store (BSRC, GVB1)
                                }
                            }
                        }

                        Break
                    }

                    Return (GVBF)
                }

                Store (0x0001D4C0, GVB1)
                Store (0x00, GVB2)
                Return (GVBF)
            }

            Method (SETC, 2, Serialized)
            {
                If (LEqual (\RWBK (0xD3, 0x00, 0x20, TSBF), 0x00))
                {
                    Divide (Arg1, 0x0100, Local0, Local1)
                    Store (Local0, DBG1)
                    Divide (Local1, 0x0100, Local0, Local1)
                    Store (Local0, DBG1)
                    Divide (Local1, 0x0100, Local0, Local1)
                    Store (Local0, DBG1)
                    Store (Local1, DBG1)
                    Store (GCFV (0x04, 0x37EE), BSRC)
                    Multiply (Arg1, GDIV (Arg0), RVCO)
                    While (One)
                    {
                        Name (T_0, 0x00)
                        Store (Add (Arg0, 0x00), T_0)
                        If (LEqual (T_0, 0x01))
                        {
                            Store (GBMV (RVCO, Divide (BSRC, 0x02, )), MVAL)
                            Store (GBNV (RVCO, Divide (BSRC, 0x02, ), MVAL), NVAL)
                            Store (0x10, Local0)
                            Store (0x14, Local1)
                            Or (DerefOf (Index (TSBF, 0x0C)), 0x80, Index (TSBF, 0x0C
                                ))
                        }
                        Else
                        {
                            If (LEqual (T_0, 0x02))
                            {
                                Store (GBMV (RVCO, 0x37EE), MVAL)
                                Store (GBNV (RVCO, 0x37EE, MVAL), NVAL)
                                Store (0xF0, DBG1)
                                Store (DerefOf (Index (TSBF, 0x1A)), DBG1)
                                Store (DerefOf (Index (TSBF, 0x1B)), DBG1)
                                Store (DerefOf (Index (TSBF, 0x1C)), DBG1)
                                Store (0x1A, Local0)
                                Store (0x1C, Local1)
                                Or (DerefOf (Index (TSBF, 0x0C)), 0x20, Index (TSBF, 0x0C
                                    ))
                            }
                            Else
                            {
                                If (LEqual (T_0, 0x03))
                                {
                                    Store (GBMV (RVCO, 0x37EE), MVAL)
                                    Store (GBNV (RVCO, 0x37EE, MVAL), NVAL)
                                    Store (0xF1, DBG1)
                                    Store (DerefOf (Index (TSBF, 0x15)), DBG1)
                                    Store (DerefOf (Index (TSBF, 0x16)), DBG1)
                                    Store (DerefOf (Index (TSBF, 0x19)), DBG1)
                                    Store (0x15, Local0)
                                    Store (0x19, Local1)
                                    Or (DerefOf (Index (TSBF, 0x0C)), 0x40, Index (TSBF, 0x0C
                                        ))
                                }
                                Else
                                {
                                    Store (GBMV (RVCO, 0x37EE), MVAL)
                                    Store (GBNV (RVCO, 0x37EE, MVAL), NVAL)
                                    Store (0xF2, DBG1)
                                    Store (DerefOf (Index (TSBF, 0x1D)), DBG1)
                                    Store (DerefOf (Index (TSBF, 0x1E)), DBG1)
                                    Store (DerefOf (Index (TSBF, 0x1F)), DBG1)
                                    Store (0x1D, Local0)
                                    Store (0x1F, Local1)
                                    Or (DerefOf (Index (TSBF, 0x0C)), 0x10, Index (TSBF, 0x0C
                                        ))
                                }
                            }
                        }

                        Break
                    }

                    If (LAnd (NVAL, 0x01))
                    {
                        Or (ShiftLeft (And (NVAL, 0x07FE), 0x05), MVAL, NVAL)
                        Store (0x80, MVAL)
                    }
                    Else
                    {
                        Or (ShiftLeft (And (NVAL, 0x07FE), 0x05), MVAL, NVAL)
                        Store (0x00, MVAL)
                    }

                    Or (MVAL, And (DerefOf (Index (TSBF, Local1)), 0x7F), 
                        Index (TSBF, Local1))
                    Store (And (NVAL, 0xFF), Index (TSBF, Local0))
                    Store (And (ShiftRight (NVAL, 0x08), 0xFF), Index (TSBF, 
                        Add (Local0, 0x01)))
                    RWBK (0xD2, Local0, Add (Subtract (Local1, Local0), 0x01), 
                        TSBF)
                    RWBK (0xD2, 0x0C, 0x02, TSBF)
                }

                Return (0x00)
            }

            Method (CINI, 0, NotSerialized)
            {
                If (\RWBK (0xD3, 0x00, 0x20, TSBF))
                {
                    If (LNotEqual (DerefOf (Index (TSBF, 0x07)), 0x75))
                    {
                        Return (0x03)
                    }

                    Store (0x20, Index (TSBF, 0x0B))
                    If (\RWBK (0xD2, 0x00, 0x0B, TSBF))
                    {
                        Return (0x01)
                    }

                    Return (0x00)
                }

                Return (0x01)
            }

            Method (GBMV, 2, NotSerialized)
            {
                Store (0x06, Local0)
                Store (Local0, Local1)
                Store (Arg1, Local2)
                While (LLess (Local0, 0x13))
                {
                    Divide (Multiply (Arg0, Local0), Arg1, Local3, Local4)
                    If (LLess (Local4, 0x07F0))
                    {
                        If (LLess (Local3, Local2))
                        {
                            Store (Local3, Local2)
                            Store (Local0, Local1)
                        }
                    }

                    Increment (Local0)
                }

                Return (Local1)
            }

            Method (GBNV, 3, NotSerialized)
            {
                Return (Divide (Multiply (Arg0, Arg2), Arg1, ))
            }

            Method (GCFV, 2, Serialized)
            {
                While (One)
                {
                    Name (T_0, 0x00)
                    Store (Add (Arg0, 0x00), T_0)
                    If (LEqual (T_0, 0x02))
                    {
                        Or (ShiftLeft (DerefOf (Index (TSBF, 0x1B)), 0x08), DerefOf (
                            Index (TSBF, 0x1A)), NVAL)
                        ShiftRight (And (DerefOf (Index (TSBF, 0x1C)), 0x80), 0x07, 
                            Local0)
                    }
                    Else
                    {
                        If (LEqual (T_0, 0x03))
                        {
                            Or (ShiftLeft (DerefOf (Index (TSBF, 0x16)), 0x08), DerefOf (
                                Index (TSBF, 0x15)), NVAL)
                            ShiftRight (And (DerefOf (Index (TSBF, 0x19)), 0x80), 0x07, 
                                Local0)
                        }
                        Else
                        {
                            If (LEqual (T_0, 0x04))
                            {
                                Or (ShiftLeft (DerefOf (Index (TSBF, 0x1E)), 0x08), DerefOf (
                                    Index (TSBF, 0x1D)), NVAL)
                                ShiftRight (And (DerefOf (Index (TSBF, 0x1F)), 0x80), 0x07, 
                                    Local0)
                            }
                            Else
                            {
                                Or (ShiftLeft (DerefOf (Index (TSBF, 0x11)), 0x08), DerefOf (
                                    Index (TSBF, 0x10)), NVAL)
                                ShiftRight (And (DerefOf (Index (TSBF, 0x14)), 0x80), 0x07, 
                                    Local0)
                            }
                        }
                    }

                    Break
                }

                And (NVAL, 0x3F, MVAL)
                Or (Local0, And (ShiftRight (NVAL, 0x05), 0x07FE), NVAL)
                Store (Divide (Multiply (Arg1, NVAL), MVAL, ), RVCO)
                Return (Divide (RVCO, GDIV (Arg0), ))
            }

            Name (DIVA, Buffer (0x10)
            {
                /* 0000 */    0x02, 0x03, 0x05, 0x0F, 0x04, 0x06, 0x0A, 0x1E, 
                /* 0008 */    0x08, 0x0C, 0x14, 0x3C, 0x10, 0x18, 0x28, 0x78
            })
            Name (DIVB, Buffer (0x10)
            {
                /* 0000 */    0x04, 0x03, 0x05, 0x0F, 0x08, 0x06, 0x0A, 0x1E, 
                /* 0008 */    0x10, 0x0C, 0x14, 0x3C, 0x20, 0x18, 0x28, 0x78
            })
            Name (DIVC, Buffer (0x10)
            {
                /* 0000 */    0x02, 0x03, 0x05, 0x07, 0x04, 0x06, 0x0A, 0x0E, 
                /* 0008 */    0x08, 0x0C, 0x14, 0x1C, 0x10, 0x18, 0x28, 0x38
            })
            Name (DIVD, Buffer (0x10)
            {
                /* 0000 */    0x02, 0x03, 0x05, 0x07, 0x04, 0x06, 0x0A, 0x0E, 
                /* 0008 */    0x08, 0x0C, 0x14, 0x1C, 0x10, 0x18, 0x28, 0x38
            })
            Method (GDIV, 1, Serialized)
            {
                While (One)
                {
                    Name (T_0, 0x00)
                    Store (Add (Arg0, 0x00), T_0)
                    If (LEqual (T_0, 0x02))
                    {
                        Return (DerefOf (Index (DIVB, And (DerefOf (Index (TSBF, 0x1C)), 
                            0x0F))))
                    }
                    Else
                    {
                        If (LEqual (T_0, 0x03))
                        {
                            Return (DerefOf (Index (DIVA, And (DerefOf (Index (TSBF, 0x19)), 
                                0x0F))))
                        }
                        Else
                        {
                            If (LEqual (T_0, 0x04))
                            {
                                Return (DerefOf (Index (DIVC, And (DerefOf (Index (TSBF, 0x1F)), 
                                    0x0F))))
                            }
                            Else
                            {
                                Return (DerefOf (Index (DIVD, And (DerefOf (Index (TSBF, 0x14)), 
                                    0x0F))))
                            }
                        }
                    }

                    Break
                }
            }

            Name (VCPU, Package (0x10)
            {
                0x00, 
                0x09C4, 
                0x1388, 
                0x1D4C, 
                0x2710, 
                0x30D4, 
                0x3A98, 
                0x445C, 
                0x4E20, 
                0x57E4, 
                0x61A8, 
                0x6B6C, 
                0x7530, 
                0x7EF4, 
                0x88B8, 
                0x927C
            })
            Name (VDDR, Package (0x10)
            {
                0x0002BF20, 
                0x0002D2A8, 
                0x0002E630, 
                0x0002F9B8, 
                0x00030D40, 
                0x000320C8, 
                0x00033450, 
                0x00035B60, 
                0x00038270, 
                0x0003A980, 
                0x0003D090, 
                0x000445C0, 
                0x000445C0, 
                0x000445C0, 
                0x000445C0, 
                0x000445C0
            })
            Name (VLDT, Package (0x08)
            {
                0x0001D4C0, 
                0x0001E848, 
                0x0001FBD0, 
                0x00020F58, 
                0x000222E0, 
                0x00023668, 
                0x000249F0, 
                0x00027100
            })
            Name (VSB0, Package (0x08)
            {
                0x0001D4C0, 
                0x0001E366, 
                0x0001F20C, 
                0x000200B2, 
                0x00020F58, 
                0x00022CA4, 
                0x000249F0, 
                0x0002673C
            })
            Name (VNB0, Package (0x08)
            {
                0x0002BF20, 
                0x0002D2A8, 
                0x0002E630, 
                0x0002F9B8, 
                0x00030D40, 
                0x00034008, 
                0x00036CF4, 
                0x000395F8
            })
            Name (VNB1, Package (0x10)
            {
                0x0001ADB0, 
                0x0001BB5C, 
                0x0001C908, 
                0x0001D6B4, 
                0x0001E460, 
                0x0001F20C, 
                0x0001FFB8, 
                0x00020D64, 
                0x00021B10, 
                0x00023668, 
                0x000251C0, 
                0x00027100, 
                0x00029810, 
                0x0002BF20, 
                0x0002E630, 
                0x00030D40
            })
            Method (SETV, 2, Serialized)
            {
                Store (0x00, Local0)
                While (One)
                {
                    Name (T_0, 0x00)
                    Store (Add (Arg0, 0x00), T_0)
                    If (LEqual (T_0, 0x01))
                    {
                        Store (GVID (VDDR, 0x0A, Arg1), Local0)
                        Store (RWAB (0x5D, 0x00, 0x00), Local1)
                        Or (And (Local1, 0xF0), And (Local0, 0x0F), Local0)
                        RWAB (0x5C, 0x00, Local0)
                    }
                    Else
                    {
                        If (LEqual (T_0, 0x03))
                        {
                            Store (GVID (VCPU, 0x0F, Subtract (Arg1, CPUV)), Local0)
                            SIOI ()
                            WSIO (0x07, 0x09)
                            Or (And (ShiftLeft (Local0, 0x03), 0x60), And (Local0, 
                                0x03), Local0)
                            Or (And (RSIO (0xF1), 0x9C), Local0, Local0)
                            WSIO (0xF1, Local0)
                            SIOO ()
                        }
                        Else
                        {
                            If (LEqual (T_0, 0x04))
                            {
                                Store (GVID (VNB1, 0x0E, Arg1), Local0)
                                Store (RWAB (0x5D, 0x07, 0x00), Local1)
                                Or (And (Local1, 0xF0), And (Local0, 0x0F), Local0)
                                RWAB (0x5C, 0x07, Local0)
                            }
                            Else
                            {
                                If (LEqual (T_0, 0x05))
                                {
                                    Store (GVID (VNB0, 0x07, Arg1), Local0)
                                    Store (RWAB (0x5D, 0x05, 0x00), Local1)
                                    Or (And (Local1, 0xF8), And (Local0, 0x07), Local0)
                                    RWAB (0x5C, 0x05, Local0)
                                }
                                Else
                                {
                                    If (LEqual (T_0, 0x06))
                                    {
                                        Store (GVID (VLDT, 0x07, Arg1), Local0)
                                        Store (RWAB (0x5D, 0x04, 0x00), Local1)
                                        Or (And (Local1, 0xF8), And (Local0, 0x07), Local0)
                                        RWAB (0x5C, 0x04, Local0)
                                    }
                                    Else
                                    {
                                    }
                                }
                            }
                        }
                    }

                    Break
                }
            }

            Method (GETV, 1, Serialized)
            {
                Store (0x00, GVB1)
                Store (0x00, GVB2)
                While (One)
                {
                    Name (T_0, 0x00)
                    Store (Add (Arg0, 0x00), T_0)
                    If (LEqual (T_0, 0x01))
                    {
                        Store (DerefOf (Index (VDDR, GVDD ())), GVB1)
                    }
                    Else
                    {
                        If (LEqual (T_0, 0x02))
                        {
                            Store (0x00, GVB1)
                        }
                        Else
                        {
                            If (LEqual (T_0, 0x03))
                            {
                                SIOI ()
                                WSIO (0x07, 0x09)
                                Store (RSIO (0xF1), Local0)
                                SIOO ()
                                Or (And (ShiftRight (Local0, 0x03), 0x0C), And (Local0, 
                                    0x03), Local0)
                                Add (CPUV, DerefOf (Index (VCPU, Local0)), GVB1)
                            }
                            Else
                            {
                                If (LEqual (T_0, 0x04))
                                {
                                    Store (DerefOf (Index (VNB1, GNBC ())), GVB1)
                                }
                                Else
                                {
                                    If (LEqual (T_0, 0x05))
                                    {
                                        Store (DerefOf (Index (VNB0, GNBP ())), GVB1)
                                    }
                                    Else
                                    {
                                        If (LEqual (T_0, 0x06))
                                        {
                                            Store (DerefOf (Index (VLDT, GHTV ())), GVB1)
                                        }
                                        Else
                                        {
                                            If (LEqual (T_0, 0x07))
                                            {
                                                Store (0x0001E848, GVB1)
                                            }
                                            Else
                                            {
                                                Store (0x04, GVB2)
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }

                    Break
                }

                Return (GVBF)
            }

            Method (GVDD, 0, NotSerialized)
            {
                Store (RWAB (0x5D, 0x00, 0x00), Local0)
                Return (And (Local0, 0x0F))
            }

            Method (GNBP, 0, NotSerialized)
            {
                Store (RWAB (0x5D, 0x05, 0x00), Local0)
                Return (And (Local0, 0x07))
            }

            Method (GNBC, 0, NotSerialized)
            {
                Store (RWAB (0x5D, 0x07, 0x00), Local0)
                Return (And (Local0, 0x0F))
            }

            Method (GHTV, 0, NotSerialized)
            {
                Store (RWAB (0x5D, 0x04, 0x00), Local0)
                Return (And (Local0, 0x07))
            }

            Method (GVID, 3, NotSerialized)
            {
                Store (0x00, Local0)
                Store (0x00, Local3)
                Store (0x000186A0, Local1)
                While (LLess (Local0, Arg1))
                {
                    Store (ABS (DerefOf (Index (Arg0, Local0)), Arg2), Local2)
                    If (LLess (Local2, Local1))
                    {
                        Store (Local2, Local1)
                        Store (Local0, Local3)
                    }

                    Increment (Local0)
                }

                Return (Local3)
            }

            Name (GF01, 0x00)
            Name (OVFL, 0x01)
            Name (OCFL, 0x01)
            Method (AM01, 0, NotSerialized)
            {
                If (LNot (GF01))
                {
                    Store (0x01, GF01)
                }

                Return (0x00)
            }

            Method (AM02, 0, NotSerialized)
            {
                Return (OBID)
            }

            Method (AM03, 1, NotSerialized)
            {
                SOID (Arg0)
                If (LEqual (ID01, 0x01))
                {
                    Store (GETC (ID02), Local0)
                }
                Else
                {
                    If (LEqual (ID01, 0x02))
                    {
                        Store (GETV (ID02), Local0)
                    }
                    Else
                    {
                        Store (0x00, GVB1)
                        Store (0x04, GVB2)
                        Store (GVBF, Local0)
                    }
                }

                Return (Local0)
            }

            Method (AM04, 2, NotSerialized)
            {
                SOID (Arg0)
                If (LEqual (ID01, 0x01))
                {
                    SETC (ID02, Arg1)
                }
                Else
                {
                    If (LEqual (ID01, 0x02))
                    {
                        SETV (ID02, Arg1)
                    }
                    Else
                    {
                        Return (0x04)
                    }
                }

                Return (0x00)
            }

            Name (IDMM, Package (0x2A)
            {
                0x01010000, 
                0x0002BF20, 
                0x00061A80, 
                0x03E8, 
                0x01020000, 
                0x000186A0, 
                0x00030D40, 
                0x03E8, 
                0x01030000, 
                0x000186A0, 
                0x00030D40, 
                0x03E8, 
                0x02010000, 
                0x0002BF20, 
                0x0003D090, 
                0x1388, 
                0x02020000, 
                0x00, 
                0x00, 
                0x03E8, 
                0x02030000, 
                0x00023AB4, 
                0x00033644, 
                0x09C4, 
                0x02040000, 
                0x0001ADB0, 
                0x0002E630, 
                0x0DAC, 
                0x02050000, 
                0x0002BF20, 
                0x000395F8, 
                0x1388, 
                0x02060000, 
                0x0001D4C0, 
                0x000249F0, 
                0x1388, 
                0x00, 
                0x00, 
                0x00, 
                0x00, 
                0x00, 
                0x00
            })
            Method (AM05, 1, Serialized)
            {
                Name (INFO, Buffer (0x18)
                {
                    /* 0000 */    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                    /* 0008 */    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                    /* 0010 */    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
                })
                CreateDWordField (INFO, 0x00, IFID)
                CreateDWordField (INFO, 0x04, IFMI)
                CreateDWordField (INFO, 0x08, IFMX)
                CreateDWordField (INFO, 0x0C, IFVL)
                CreateDWordField (INFO, 0x10, IFSP)
                CreateField (INFO, 0xA0, 0x03, IFST)
                SOID (Arg0)
                Store (0x00, Local0)
                While (DerefOf (Index (IDMM, Local0)))
                {
                    If (LEqual (Arg0, DerefOf (Index (IDMM, Local0))))
                    {
                        Store (DerefOf (Index (IDMM, Add (Local0, 0x01))), IFMI)
                        Store (DerefOf (Index (IDMM, Add (Local0, 0x02))), IFMX)
                        Store (DerefOf (Index (IDMM, Add (Local0, 0x03))), IFSP)
                        Break
                    }

                    Add (Local0, 0x04, Local0)
                }

                If (LEqual (Arg0, 0x02030000))
                {
                    Store (CPUV, IFMI)
                    Store (Add (CPUV, 0x927C), IFMX)
                }

                If (LEqual (ID01, 0x01))
                {
                    GETC (ID02)
                    Store (GVB1, IFVL)
                    Store (GVB2, IFST)
                }
                Else
                {
                    If (LEqual (ID01, 0x02))
                    {
                        GETV (ID02)
                        Store (GVB1, IFVL)
                        Store (GVB2, IFST)
                    }
                    Else
                    {
                        Store (0x04, IFST)
                    }
                }

                Return (INFO)
            }

            Method (AM06, 0, NotSerialized)
            {
                HM06 ()
                Return (0x00)
            }

            Method (AM07, 1, NotSerialized)
            {
                HM07 (Arg0)
                Return (0x00)
            }

            Name (WQBA, Buffer (0x081B)
            {
                /* 0000 */    0x46, 0x4F, 0x4D, 0x42, 0x01, 0x00, 0x00, 0x00, 
                /* 0008 */    0x0B, 0x08, 0x00, 0x00, 0x50, 0x2F, 0x00, 0x00, 
                /* 0010 */    0x44, 0x53, 0x00, 0x01, 0x1A, 0x7D, 0xDA, 0x54, 
                /* 0018 */    0x28, 0x4D, 0x97, 0x00, 0x01, 0x06, 0x18, 0x42, 
                /* 0020 */    0x10, 0x0F, 0x10, 0x22, 0x21, 0x04, 0x12, 0x01, 
                /* 0028 */    0xA1, 0xC8, 0x2C, 0x0C, 0x86, 0x10, 0x38, 0x2E, 
                /* 0030 */    0x84, 0x1C, 0x40, 0x48, 0x1C, 0x14, 0x4A, 0x08, 
                /* 0038 */    0x84, 0xFA, 0x13, 0xC8, 0xAF, 0x00, 0x84, 0x0E, 
                /* 0040 */    0x05, 0xC8, 0x14, 0x60, 0x50, 0x80, 0x53, 0x04, 
                /* 0048 */    0x11, 0xF4, 0x2A, 0xC0, 0xA6, 0x00, 0x93, 0x02, 
                /* 0050 */    0x2C, 0x0A, 0xD0, 0x2E, 0xC0, 0xB2, 0x00, 0xDD, 
                /* 0058 */    0x02, 0xA4, 0xC3, 0x12, 0x91, 0xE0, 0x28, 0x31, 
                /* 0060 */    0xE0, 0x28, 0x9D, 0xD8, 0xC2, 0x0D, 0x1B, 0xBC, 
                /* 0068 */    0x50, 0x14, 0xCD, 0x20, 0x4A, 0x82, 0xCA, 0x05, 
                /* 0070 */    0xF8, 0x46, 0x10, 0x78, 0xB9, 0x02, 0x24, 0x4F, 
                /* 0078 */    0x40, 0x9A, 0x05, 0x18, 0x16, 0x60, 0x5D, 0x80, 
                /* 0080 */    0xEC, 0x21, 0x50, 0xA9, 0x43, 0x40, 0xC9, 0x19, 
                /* 0088 */    0x02, 0x6A, 0x00, 0xAD, 0x4E, 0x40, 0xF8, 0x95, 
                /* 0090 */    0x4E, 0x09, 0x49, 0x10, 0xCE, 0x58, 0xC5, 0xE3, 
                /* 0098 */    0x6B, 0x16, 0x4D, 0xCF, 0x49, 0xCE, 0x31, 0xE4, 
                /* 00A0 */    0x78, 0x5C, 0xE8, 0x41, 0x70, 0xB1, 0x16, 0x40, 
                /* 00A8 */    0x98, 0xFC, 0x21, 0x4B, 0x1E, 0x0C, 0x4A, 0xC2, 
                /* 00B0 */    0x58, 0xA8, 0x8B, 0x51, 0xA3, 0x46, 0xCA, 0x06, 
                /* 00B8 */    0x64, 0x88, 0xD2, 0x46, 0x8D, 0x1E, 0xD0, 0xF9, 
                /* 00C0 */    0x1D, 0xC9, 0xD9, 0x1D, 0xDD, 0x91, 0x24, 0x30, 
                /* 00C8 */    0xEA, 0x31, 0x1D, 0x63, 0x61, 0x33, 0x12, 0x6A, 
                /* 00D0 */    0x8C, 0xE6, 0xA0, 0x48, 0xB8, 0x41, 0xA3, 0x25, 
                /* 00D8 */    0xC2, 0x6A, 0x5C, 0xB1, 0xCF, 0xCC, 0xC2, 0x87, 
                /* 00E0 */    0x25, 0x8C, 0x23, 0x38, 0xB0, 0x83, 0xB5, 0x68, 
                /* 00E8 */    0x18, 0xA1, 0x15, 0x04, 0xA7, 0x41, 0x1C, 0x45, 
                /* 00F0 */    0x94, 0x30, 0x0C, 0xCF, 0x98, 0x81, 0x8E, 0x92, 
                /* 00F8 */    0x21, 0x85, 0x09, 0x7A, 0x02, 0x41, 0x4E, 0x9E, 
                /* 0100 */    0x61, 0x19, 0xE2, 0x0C, 0x38, 0x56, 0x8C, 0x50, 
                /* 0108 */    0x21, 0x31, 0x03, 0x09, 0xFE, 0xFF, 0x3F, 0x81, 
                /* 0110 */    0xAE, 0x31, 0xE4, 0x19, 0x88, 0xDC, 0x03, 0x4E, 
                /* 0118 */    0x20, 0x48, 0xF4, 0x28, 0xC1, 0x8D, 0x6B, 0x54, 
                /* 0120 */    0x36, 0xA6, 0xB3, 0xC1, 0x0D, 0xCC, 0x04, 0x71, 
                /* 0128 */    0x0E, 0x0F, 0x23, 0x03, 0x42, 0x13, 0x88, 0x1F, 
                /* 0130 */    0x3B, 0x7C, 0x02, 0xBB, 0x3F, 0x0E, 0x48, 0x21, 
                /* 0138 */    0x82, 0x2E, 0x04, 0x67, 0x5A, 0xA3, 0x00, 0x6B, 
                /* 0140 */    0x67, 0x07, 0xD9, 0x82, 0xD0, 0x59, 0x20, 0x56, 
                /* 0148 */    0x63, 0x28, 0x82, 0x88, 0x10, 0x34, 0x8A, 0xF1, 
                /* 0150 */    0x22, 0x84, 0x0A, 0x11, 0x25, 0xEA, 0x39, 0x07, 
                /* 0158 */    0xA9, 0x4D, 0x80, 0x32, 0x10, 0xA1, 0x05, 0x33, 
                /* 0160 */    0x02, 0xB3, 0x3F, 0x08, 0x12, 0xF0, 0x31, 0xA1, 
                /* 0168 */    0x1F, 0x81, 0x25, 0x9C, 0x08, 0x64, 0x64, 0x34, 
                /* 0170 */    0xF4, 0xB0, 0xE0, 0x93, 0x00, 0x3B, 0x20, 0x78, 
                /* 0178 */    0x3E, 0xA7, 0x66, 0x02, 0x07, 0x86, 0x10, 0xAC, 
                /* 0180 */    0x45, 0x1D, 0x2D, 0x28, 0x81, 0xA5, 0x1C, 0x0D, 
                /* 0188 */    0x88, 0xED, 0x81, 0xE9, 0x1E, 0x70, 0x84, 0xE7, 
                /* 0190 */    0xEE, 0xCB, 0xC1, 0xA9, 0xF9, 0xA7, 0xE1, 0x69, 
                /* 0198 */    0x3E, 0x24, 0x60, 0x86, 0xE8, 0xB1, 0x1E, 0x44, 
                /* 01A0 */    0xC0, 0x43, 0x64, 0xA7, 0x04, 0x03, 0xE2, 0xBD, 
                /* 01A8 */    0x5F, 0x0B, 0xC8, 0x08, 0x5E, 0x12, 0x0C, 0xE8, 
                /* 01B0 */    0x49, 0x3C, 0x20, 0x80, 0xE5, 0xA0, 0x71, 0xE0, 
                /* 01B8 */    0x27, 0x54, 0xF1, 0x1D, 0x80, 0x1E, 0x09, 0xD8, 
                /* 01C0 */    0x8C, 0xE2, 0x9B, 0xA0, 0xAC, 0xE3, 0x03, 0x7A, 
                /* 01C8 */    0xCE, 0xD1, 0x9E, 0x1D, 0x5E, 0x16, 0x9A, 0xBD, 
                /* 01D0 */    0x62, 0x10, 0x82, 0xD7, 0x00, 0xDF, 0x14, 0x7C, 
                /* 01D8 */    0x1A, 0xB1, 0xA0, 0xD5, 0xC9, 0xC9, 0xAA, 0x3C, 
                /* 01E0 */    0x62, 0x7A, 0xAA, 0xF0, 0x21, 0xE2, 0x00, 0x04, 
                /* 01E8 */    0x26, 0x0D, 0xC3, 0x05, 0x8D, 0x82, 0xE1, 0xA2, 
                /* 01F0 */    0xFE, 0xFF, 0xC3, 0x05, 0xEF, 0x71, 0xE0, 0x70, 
                /* 01F8 */    0xC1, 0x72, 0x48, 0xA8, 0x6A, 0x78, 0x9A, 0xC3, 
                /* 0200 */    0xE9, 0x36, 0x8F, 0x4F, 0x4E, 0x16, 0x9E, 0x2F, 
                /* 0208 */    0x1B, 0xCB, 0x51, 0xB1, 0x53, 0x08, 0x1B, 0x1D, 
                /* 0210 */    0x1F, 0x85, 0xC7, 0xFB, 0xD6, 0x50, 0x2C, 0x88, 
                /* 0218 */    0x4C, 0x40, 0xE8, 0xC4, 0x70, 0xDC, 0x60, 0x71, 
                /* 0220 */    0x76, 0x7E, 0x10, 0x24, 0x19, 0xB2, 0x44, 0x0C, 
                /* 0228 */    0x1C, 0x3D, 0x9D, 0x04, 0xC3, 0x43, 0x68, 0xE0, 
                /* 0230 */    0xE0, 0x01, 0xF4, 0xC0, 0xC1, 0x2F, 0x6F, 0xE0, 
                /* 0238 */    0x20, 0x9A, 0x42, 0xB0, 0xB7, 0x1A, 0x7E, 0xC4, 
                /* 0240 */    0x78, 0x0E, 0xF1, 0xA0, 0xC1, 0x3D, 0x06, 0x1C, 
                /* 0248 */    0x81, 0x87, 0x84, 0x3B, 0x1A, 0xC1, 0xF9, 0xFF, 
                /* 0250 */    0xDF, 0x7B, 0xEC, 0xF3, 0x4A, 0x41, 0x06, 0xF0, 
                /* 0258 */    0xCE, 0x82, 0x3B, 0x1B, 0x01, 0x97, 0x11, 0x70, 
                /* 0260 */    0x91, 0xAB, 0xA4, 0x67, 0x20, 0xCB, 0x82, 0x41, 
                /* 0268 */    0x1D, 0x83, 0x00, 0xD6, 0xDC, 0x7D, 0x5E, 0x7F, 
                /* 0270 */    0x7C, 0x0C, 0x02, 0x77, 0xB0, 0xF3, 0x80, 0xFE, 
                /* 0278 */    0xFF, 0x3F, 0x02, 0xCB, 0x39, 0xC5, 0x40, 0x3B, 
                /* 0280 */    0x0C, 0xF9, 0xF4, 0x01, 0x9E, 0x33, 0x10, 0x70, 
                /* 0288 */    0x38, 0x4C, 0xE0, 0x4F, 0x07, 0xF0, 0x06, 0xF9, 
                /* 0290 */    0x10, 0x03, 0xD6, 0x31, 0xFA, 0x10, 0x03, 0xBE, 
                /* 0298 */    0x83, 0x12, 0xEE, 0x00, 0x02, 0xCF, 0xE3, 0x90, 
                /* 02A0 */    0x84, 0x7C, 0x08, 0xC1, 0x0F, 0xE9, 0x98, 0x1E, 
                /* 02A8 */    0x41, 0x80, 0xA1, 0x90, 0x87, 0x81, 0xCF, 0x1F, 
                /* 02B0 */    0x34, 0xFA, 0x11, 0x04, 0xF4, 0xFF, 0xFF, 0x23, 
                /* 02B8 */    0x08, 0xC0, 0x81, 0xB3, 0xC2, 0x23, 0x08, 0xD8, 
                /* 02C0 */    0xC5, 0x3F, 0xC2, 0x74, 0x1E, 0x70, 0x70, 0x08, 
                /* 02C8 */    0x39, 0x39, 0xD8, 0xA1, 0x86, 0x63, 0xAD, 0x07, 
                /* 02D0 */    0x01, 0x32, 0x9E, 0x17, 0x01, 0x07, 0x3D, 0xD7, 
                /* 02D8 */    0x01, 0xDD, 0xB3, 0x06, 0xEE, 0x7C, 0x00, 0xEF, 
                /* 02E0 */    0xFF, 0x7F, 0x3E, 0xF0, 0x91, 0x8E, 0x9F, 0x3B, 
                /* 02E8 */    0xC0, 0x17, 0x1D, 0x42, 0x87, 0x42, 0xFC, 0x81, 
                /* 02F0 */    0xCA, 0x43, 0xF4, 0xD9, 0xC0, 0x04, 0x1E, 0x2D, 
                /* 02F8 */    0xB8, 0x8E, 0x75, 0xC0, 0xE1, 0xA4, 0x81, 0x1B, 
                /* 0300 */    0x2D, 0xDC, 0xE3, 0xEA, 0x63, 0x01, 0xE6, 0x40, 
                /* 0308 */    0x08, 0xAE, 0x43, 0x0B, 0x98, 0xAE, 0x0B, 0x98, 
                /* 0310 */    0x4B, 0x0B, 0xFE, 0xD0, 0x02, 0x7C, 0x84, 0x9E, 
                /* 0318 */    0x58, 0x50, 0xD2, 0x0E, 0x2D, 0xA0, 0xFB, 0xFF, 
                /* 0320 */    0x1F, 0x5A, 0x00, 0x4E, 0xCC, 0xF5, 0xA1, 0x05, 
                /* 0328 */    0xEC, 0xE1, 0x8E, 0x61, 0x80, 0xAA, 0xFF, 0xFF, 
                /* 0330 */    0x99, 0x12, 0x3F, 0x8B, 0xF8, 0x71, 0xA2, 0xBD, 
                /* 0338 */    0x05, 0xF8, 0x68, 0x0A, 0xDC, 0x0E, 0xB0, 0xB8, 
                /* 0340 */    0x23, 0x08, 0xBC, 0x4B, 0xC1, 0x69, 0x79, 0x6A, 
                /* 0348 */    0xCF, 0xE8, 0x07, 0xD7, 0xF8, 0x15, 0x84, 0xDC, 
                /* 0350 */    0x63, 0x7C, 0x10, 0x03, 0x86, 0x32, 0x0E, 0x62, 
                /* 0358 */    0xA8, 0xE0, 0x87, 0x10, 0x40, 0xEF, 0xFF, 0xFF, 
                /* 0360 */    0x10, 0x02, 0x1C, 0x2F, 0x0B, 0x0F, 0x21, 0x60, 
                /* 0368 */    0x97, 0x7E, 0x10, 0xA3, 0xB1, 0x0F, 0x62, 0xE8, 
                /* 0370 */    0x01, 0xF9, 0x7C, 0xC5, 0xCF, 0x61, 0x80, 0xD3, 
                /* 0378 */    0x33, 0x1C, 0xDC, 0xA8, 0xC7, 0x30, 0xA0, 0xF1, 
                /* 0380 */    0xFF, 0x3F, 0x86, 0x01, 0xB7, 0xB3, 0x28, 0x70, 
                /* 0388 */    0x82, 0x78, 0x0E, 0x03, 0xB6, 0x52, 0xCC, 0x80, 
                /* 0390 */    0xB0, 0x00, 0xAF, 0x07, 0x89, 0x7A, 0x0A, 0x50, 
                /* 0398 */    0x18, 0x1F, 0x90, 0x7C, 0x66, 0x81, 0x2B, 0x09, 
                /* 03A0 */    0x0E, 0x35, 0x46, 0x8F, 0xF3, 0xE1, 0xF6, 0x58, 
                /* 03A8 */    0x4F, 0xE4, 0xBD, 0xC0, 0x83, 0x7B, 0x0A, 0x80, 
                /* 03B0 */    0x71, 0x3E, 0xF0, 0xB4, 0x4E, 0xCA, 0x17, 0x80, 
                /* 03B8 */    0x47, 0x10, 0xDF, 0x46, 0x4C, 0xE0, 0x43, 0x02, 
                /* 03C0 */    0x43, 0xE3, 0x27, 0x19, 0xB0, 0xDE, 0x14, 0x7C, 
                /* 03C8 */    0x3E, 0x80, 0xF7, 0xFF, 0x3F, 0x1F, 0xE0, 0x66, 
                /* 03D0 */    0xFD, 0x1A, 0x83, 0xC1, 0x0A, 0x15, 0xA3, 0xD1, 
                /* 03D8 */    0x93, 0x00, 0x01, 0x3D, 0xBE, 0xBE, 0xAE, 0x03, 
                /* 03E0 */    0x14, 0x2A, 0x62, 0x88, 0x97, 0x02, 0xBB, 0x3C, 
                /* 03E8 */    0x54, 0x20, 0x0F, 0x2D, 0xE0, 0xC2, 0x7E, 0x68, 
                /* 03F0 */    0x01, 0x7B, 0xA8, 0x33, 0x11, 0x8D, 0x34, 0x1A, 
                /* 03F8 */    0xD4, 0x51, 0xC1, 0x87, 0x02, 0xDF, 0x88, 0x7D, 
                /* 0400 */    0xA2, 0x64, 0x20, 0x27, 0x7A, 0x5A, 0x8F, 0x0B, 
                /* 0408 */    0x4F, 0x03, 0x1E, 0x37, 0xBB, 0x26, 0xF8, 0x58, 
                /* 0410 */    0x46, 0x8E, 0x07, 0xE8, 0xFB, 0x43, 0xC0, 0x13, 
                /* 0418 */    0x7D, 0xE4, 0x80, 0x75, 0xF4, 0xC0, 0x9F, 0x32, 
                /* 0420 */    0xE0, 0x8F, 0xC7, 0xC7, 0x00, 0xCF, 0xE7, 0x84, 
                /* 0428 */    0x1F, 0x9F, 0xC8, 0x20, 0x50, 0x27, 0x4F, 0x3E, 
                /* 0430 */    0xD2, 0xD3, 0x7A, 0x1B, 0xF0, 0x21, 0xE1, 0xB0, 
                /* 0438 */    0xD8, 0x09, 0xCC, 0x27, 0x13, 0x70, 0x8C, 0x07, 
                /* 0440 */    0xFE, 0xA9, 0xFB, 0x21, 0xC3, 0x57, 0x06, 0xCF, 
                /* 0448 */    0xD7, 0x04, 0x0F, 0x97, 0x3E, 0x84, 0xC0, 0xFF, 
                /* 0450 */    0xFF, 0xDF, 0x3A, 0x7C, 0x68, 0x08, 0xF5, 0xD4, 
                /* 0458 */    0xE1, 0x19, 0xBC, 0x5F, 0xF8, 0x04, 0x02, 0x4C, 
                /* 0460 */    0xC2, 0x5A, 0x81, 0xE8, 0xE1, 0x64, 0xE1, 0x75, 
                /* 0468 */    0xCA, 0xC6, 0x91, 0x8F, 0x0E, 0xD3, 0x22, 0x0F, 
                /* 0470 */    0x08, 0x3A, 0x1A, 0xF8, 0x20, 0x63, 0x02, 0xCB, 
                /* 0478 */    0x03, 0xD2, 0xA9, 0xC8, 0x10, 0x16, 0x46, 0x21, 
                /* 0480 */    0x59, 0x10, 0x1A, 0x8D, 0x87, 0x47, 0xE0, 0x28, 
                /* 0488 */    0x88, 0x47, 0xEE, 0x90, 0xA7, 0x59, 0x50, 0x1C, 
                /* 0490 */    0x1B, 0x7C, 0x36, 0x83, 0x33, 0xB4, 0x88, 0x27, 
                /* 0498 */    0xE3, 0x69, 0x78, 0xDC, 0xB8, 0x53, 0x07, 0xDC, 
                /* 04A0 */    0x71, 0xE0, 0x4F, 0x7C, 0xF8, 0x83, 0x12, 0x27, 
                /* 04A8 */    0xF0, 0x11, 0x16, 0x5C, 0x02, 0xCF, 0x05, 0xA0, 
                /* 04B0 */    0x00, 0xF2, 0x55, 0xC0, 0x07, 0xBE, 0xC7, 0x01, 
                /* 04B8 */    0x36, 0x85, 0x10, 0x61, 0xA2, 0x19, 0x1E, 0x73, 
                /* 04C0 */    0x9A, 0xF6, 0x91, 0xC9, 0xE3, 0xF1, 0xB0, 0xF8, 
                /* 04C8 */    0x20, 0x7D, 0x7C, 0x61, 0xD8, 0x4F, 0x27, 0x3E, 
                /* 04D0 */    0xA1, 0x1D, 0xE3, 0x7B, 0xC1, 0xF3, 0x16, 0x06, 
                /* 04D8 */    0xD6, 0xC3, 0xE6, 0xFF, 0x7F, 0x58, 0xA3, 0x85, 
                /* 04E0 */    0x3D, 0xDA, 0xC7, 0x07, 0x5F, 0x3D, 0x3C, 0x31, 
                /* 04E8 */    0xDF, 0xD8, 0x7C, 0xE8, 0x00, 0xCB, 0xF1, 0x09, 
                /* 04F0 */    0xFE, 0x00, 0x1F, 0x05, 0xC0, 0x72, 0xFE, 0x61, 
                /* 04F8 */    0x73, 0x78, 0x81, 0x38, 0xF3, 0xD7, 0x13, 0x9F, 
                /* 0500 */    0xEE, 0x30, 0x27, 0x3C, 0xAE, 0x6B, 0x04, 0x24, 
                /* 0508 */    0xE2, 0x19, 0x02, 0x35, 0x08, 0xC7, 0x59, 0xA4, 
                /* 0510 */    0x0E, 0xC3, 0xCC, 0xE7, 0x81, 0x43, 0xAA, 0x51, 
                /* 0518 */    0x04, 0xEF, 0x5B, 0x01, 0x8B, 0x70, 0x8C, 0x40, 
                /* 0520 */    0x89, 0xA7, 0x90, 0xF4, 0x63, 0x04, 0x4A, 0x2C, 
                /* 0528 */    0x1C, 0x05, 0xF1, 0x31, 0xC2, 0x07, 0x09, 0xDB, 
                /* 0530 */    0x38, 0x8C, 0xA1, 0x0F, 0x7E, 0xFC, 0x28, 0xC0, 
                /* 0538 */    0x4F, 0x11, 0xF0, 0x4F, 0x3C, 0xB8, 0xB1, 0xC2, 
                /* 0540 */    0x1D, 0x1C, 0x5B, 0xE1, 0x4B, 0xCF, 0xA1, 0x9D, 
                /* 0548 */    0xDD, 0x43, 0x42, 0x94, 0x98, 0x67, 0x10, 0x31, 
                /* 0550 */    0xC2, 0xEB, 0xA8, 0xD1, 0x3C, 0x46, 0x1C, 0xCE, 
                /* 0558 */    0x39, 0xFA, 0x52, 0xE4, 0x39, 0xC5, 0x7A, 0x54, 
                /* 0560 */    0xE2, 0x47, 0x0A, 0xB8, 0x47, 0x30, 0xFC, 0x91, 
                /* 0568 */    0x02, 0x3F, 0x93, 0xF3, 0xC0, 0xFC, 0xFF, 0xD5, 
                /* 0570 */    0x8D, 0x45, 0xF0, 0x3E, 0x82, 0xE1, 0x0F, 0x16, 
                /* 0578 */    0xC0, 0x43, 0xCA, 0x31, 0x40, 0x07, 0x0B, 0x70, 
                /* 0580 */    0x9D, 0x09, 0x7C, 0xB0, 0x00, 0xAE, 0xE7, 0x03, 
                /* 0588 */    0x9F, 0x0E, 0xC0, 0x7A, 0xF9, 0xE1, 0xF7, 0x03, 
                /* 0590 */    0x18, 0x27, 0x0C, 0x18, 0xE7, 0x03, 0xCC, 0x0D, 
                /* 0598 */    0xC3, 0x61, 0x96, 0xAC, 0x13, 0x06, 0x3F, 0xAE, 
                /* 05A0 */    0x39, 0xD2, 0x6A, 0x75, 0x7A, 0xC7, 0x13, 0x38, 
                /* 05A8 */    0x08, 0x98, 0x4E, 0x16, 0x1E, 0xB5, 0x23, 0x50, 
                /* 05B0 */    0x48, 0xDA, 0x01, 0x03, 0x25, 0xE6, 0x80, 0x41, 
                /* 05B8 */    0x41, 0x0C, 0xE8, 0xA4, 0x87, 0x47, 0xF4, 0xC1, 
                /* 05C0 */    0xCE, 0xA7, 0x06, 0x76, 0x91, 0xF5, 0xF5, 0xC2, 
                /* 05C8 */    0xF3, 0xF4, 0x94, 0x39, 0x9E, 0x8F, 0x21, 0x26, 
                /* 05D0 */    0xF8, 0xFF, 0x47, 0x7D, 0x31, 0x01, 0xCF, 0x8D, 
                /* 05D8 */    0x82, 0x9D, 0x5C, 0x31, 0x17, 0x37, 0x76, 0xB6, 
                /* 05E0 */    0x63, 0xA7, 0x02, 0xA3, 0x1C, 0xEE, 0x1B, 0x98, 
                /* 05E8 */    0xD5, 0x5C, 0x15, 0x50, 0x33, 0xC2, 0x10, 0x78, 
                /* 05F0 */    0xBC, 0x3E, 0x34, 0x82, 0x49, 0xDF, 0x85, 0x02, 
                /* 05F8 */    0xE4, 0xE8, 0x5C, 0xE6, 0xE8, 0x51, 0xE7, 0x28, 
                /* 0600 */    0x9F, 0xA4, 0xF8, 0xE8, 0x1D, 0x1A, 0x42, 0xA7, 
                /* 0608 */    0x15, 0xB8, 0x67, 0x29, 0x1F, 0xA1, 0x80, 0xEF, 
                /* 0610 */    0xC0, 0x7C, 0x29, 0xC0, 0x1D, 0x50, 0xC0, 0x70, 
                /* 0618 */    0x7D, 0xC0, 0x1F, 0xBC, 0x61, 0x9C, 0x51, 0xE0, 
                /* 0620 */    0xFE, 0xFF, 0xCF, 0x28, 0xE0, 0x0A, 0x7C, 0x96, 
                /* 0628 */    0x02, 0x1D, 0xA4, 0xCF, 0x28, 0xC0, 0x75, 0xA8, 
                /* 0630 */    0xB8, 0x33, 0x0A, 0x38, 0xCE, 0xB6, 0x98, 0x73, 
                /* 0638 */    0x14, 0x8B, 0x73, 0x2C, 0x41, 0x87, 0x7A, 0x39, 
                /* 0640 */    0xE8, 0x30, 0x8B, 0x27, 0x70, 0x94, 0x63, 0x09, 
                /* 0648 */    0x2A, 0x04, 0x85, 0x4E, 0x50, 0x3E, 0x49, 0xF0, 
                /* 0650 */    0x33, 0x1E, 0x07, 0x31, 0xA0, 0xB3, 0x9F, 0x24, 
                /* 0658 */    0xD0, 0x2A, 0x4E, 0x12, 0xC8, 0xB0, 0xE7, 0x12, 
                /* 0660 */    0x40, 0xC0, 0xFF, 0xFF, 0x5C, 0xC2, 0xCF, 0x89, 
                /* 0668 */    0x4F, 0x13, 0xE0, 0xBA, 0x11, 0xC3, 0x3F, 0x9F, 
                /* 0670 */    0x00, 0x8B, 0x23, 0x23, 0xE0, 0xEC, 0x20, 0xC8, 
                /* 0678 */    0x8F, 0x8C, 0xC0, 0xF7, 0x5C, 0x02, 0xBE, 0x61, 
                /* 0680 */    0x1B, 0xD6, 0xFF, 0xFF, 0x73, 0x09, 0xE0, 0xE3, 
                /* 0688 */    0x26, 0xCD, 0xCF, 0x25, 0x70, 0x87, 0xEE, 0x38, 
                /* 0690 */    0xA7, 0x2F, 0xC4, 0x15, 0xD6, 0xF7, 0x8C, 0xF8, 
                /* 0698 */    0x09, 0xC6, 0x38, 0x96, 0xA0, 0x02, 0x1C, 0xBE, 
                /* 06A0 */    0x00, 0x9A, 0xFC, 0xFF, 0x4F, 0x23, 0xF8, 0x73, 
                /* 06A8 */    0xB1, 0x47, 0xCF, 0x0F, 0x24, 0x3E, 0x64, 0x90, 
                /* 06B0 */    0xD1, 0xD3, 0xC8, 0x87, 0x2F, 0xE8, 0x11, 0x0F, 
                /* 06B8 */    0x23, 0x40, 0x7B, 0xA0, 0x0F, 0x5F, 0x60, 0xBC, 
                /* 06C0 */    0x3D, 0xF0, 0xE3, 0x26, 0xF0, 0x8A, 0x7D, 0x28, 
                /* 06C8 */    0x01, 0x1D, 0x2C, 0x3F, 0x94, 0x00, 0xCF, 0xD1, 
                /* 06D0 */    0xF3, 0xFF, 0xFF, 0xD9, 0x0B, 0x3C, 0x57, 0x09, 
                /* 06D8 */    0x0F, 0xDE, 0x80, 0xC7, 0xF4, 0x58, 0x60, 0x40, 
                /* 06E0 */    0x76, 0x2E, 0x61, 0xB2, 0xCF, 0x25, 0xE8, 0xF3, 
                /* 06E8 */    0x88, 0xAD, 0xDE, 0x8E, 0xC9, 0x49, 0x1D, 0x23, 
                /* 06F0 */    0xFC, 0x5C, 0x82, 0x92, 0x7C, 0x2E, 0x01, 0x68, 
                /* 06F8 */    0x73, 0xE8, 0x02, 0x4E, 0xFF, 0xFF, 0x43, 0x17, 
                /* 0700 */    0xE0, 0xF5, 0x1A, 0xE8, 0x03, 0x09, 0xB8, 0xEE, 
                /* 0708 */    0x09, 0x3E, 0x90, 0x00, 0xD7, 0xA3, 0x00, 0x78, 
                /* 0710 */    0x8E, 0x20, 0xF8, 0x23, 0xB3, 0x0F, 0xFC, 0xB8, 
                /* 0718 */    0x93, 0xBE, 0x4F, 0xD5, 0x71, 0x8D, 0x7F, 0xC4, 
                /* 0720 */    0x47, 0xD0, 0xF8, 0xE9, 0x8B, 0xDC, 0x0B, 0x7C, 
                /* 0728 */    0x2C, 0xD1, 0x81, 0x1F, 0x25, 0x98, 0x42, 0x72, 
                /* 0730 */    0x0F, 0x10, 0x28, 0x81, 0x70, 0xF4, 0xFF, 0x0F, 
                /* 0738 */    0xE2, 0x03, 0x84, 0xC3, 0x9F, 0x93, 0xA0, 0x5F, 
                /* 0740 */    0x2D, 0xF9, 0xF9, 0x01, 0x7F, 0x1D, 0x61, 0xA3, 
                /* 0748 */    0x64, 0xC7, 0x79, 0xDC, 0x28, 0xE1, 0x82, 0xBD, 
                /* 0750 */    0x3E, 0x18, 0xE2, 0x0E, 0x4F, 0x84, 0x9F, 0x6D, 
                /* 0758 */    0x31, 0xC7, 0x7C, 0xB8, 0x47, 0x85, 0x47, 0x25, 
                /* 0760 */    0x70, 0xCD, 0x1A, 0xD6, 0x61, 0x09, 0xF0, 0xE0, 
                /* 0768 */    0xE1, 0xB0, 0x04, 0x68, 0xF8, 0xFF, 0x9F, 0x0B, 
                /* 0770 */    0xF0, 0xB3, 0xE7, 0x83, 0x38, 0x11, 0x0F, 0x1F, 
                /* 0778 */    0x03, 0x74, 0x2C, 0x6F, 0x07, 0x0C, 0x52, 0x36, 
                /* 0780 */    0x7D, 0x6A, 0x34, 0x6A, 0xD5, 0xA0, 0x4C, 0x8D, 
                /* 0788 */    0x32, 0x0D, 0x6A, 0xF5, 0xA9, 0xD4, 0x98, 0x31, 
                /* 0790 */    0x43, 0x47, 0x0A, 0xAF, 0x56, 0xC3, 0x75, 0xA0, 
                /* 0798 */    0x97, 0x83, 0x40, 0x1C, 0x6C, 0xCD, 0x02, 0x71, 
                /* 07A0 */    0xF0, 0xD5, 0x08, 0xC4, 0x32, 0x56, 0x25, 0x10, 
                /* 07A8 */    0x4B, 0x78, 0x49, 0x08, 0xC4, 0x22, 0xDF, 0x02, 
                /* 07B0 */    0x02, 0xB1, 0xE8, 0xA7, 0x92, 0x40, 0x2C, 0xF7, 
                /* 07B8 */    0x31, 0x2C, 0x10, 0x0B, 0xF3, 0x02, 0xC2, 0x62, 
                /* 07C0 */    0x81, 0x50, 0x61, 0x66, 0x8E, 0x39, 0x4C, 0x26, 
                /* 07C8 */    0x88, 0x80, 0x1C, 0xCE, 0x0D, 0x10, 0x8B, 0x0A, 
                /* 07D0 */    0x22, 0x20, 0x2B, 0xD5, 0x03, 0xC4, 0x64, 0x83, 
                /* 07D8 */    0x08, 0xC8, 0xE2, 0xFD, 0x00, 0xB1, 0x28, 0x20, 
                /* 07E0 */    0x02, 0x72, 0xEE, 0x75, 0x09, 0xC8, 0x22, 0x14, 
                /* 07E8 */    0x01, 0x31, 0x71, 0x8E, 0x80, 0x98, 0x54, 0x10, 
                /* 07F0 */    0x01, 0x39, 0x81, 0x25, 0x20, 0x16, 0x07, 0x44, 
                /* 07F8 */    0x40, 0x0E, 0xA5, 0x09, 0x88, 0x45, 0x04, 0x11, 
                /* 0800 */    0x90, 0xF5, 0x98, 0x02, 0x62, 0xE2, 0x40, 0x34, 
                /* 0808 */    0x3C, 0xA2, 0x0A, 0x88, 0x49, 0x06, 0x11, 0x90, 
                /* 0810 */    0x83, 0xBC, 0x10, 0x04, 0xE4, 0x58, 0x20, 0x02, 
                /* 0818 */    0xF2, 0xFF, 0x1F
            })
            Name (_HID, EisaId ("PNP0C14"))
            Name (_UID, 0x00)
            Name (_WDG, Buffer (0x28)
            {
                /* 0000 */    0x6A, 0x0F, 0xBC, 0xAB, 0xA1, 0x8E, 0xD1, 0x11, 
                /* 0008 */    0x00, 0xA0, 0xC9, 0x06, 0x29, 0x10, 0x00, 0x00, 
                /* 0010 */    0x41, 0x41, 0x01, 0x02, 0x21, 0x12, 0x90, 0x05, 
                /* 0018 */    0x66, 0xD5, 0xD1, 0x11, 0xB2, 0xF0, 0x00, 0xA0, 
                /* 0020 */    0xC9, 0x06, 0x29, 0x10, 0x42, 0x41, 0x01, 0x00
            })
            Method (WMAA, 3, NotSerialized)
            {
                If (LEqual (Arg0, 0x00))
                {
                    If (LOr (LOr (LNotEqual (Arg1, 0x01), LNotEqual (Arg1, 
                        0x02)), LNotEqual (Arg1, 0x06)))
                    {
                        CreateDWordField (Arg2, 0x00, WIID)
                    }

                    If (LEqual (Arg1, 0x01))
                    {
                        Return (AM01 ())
                    }
                    Else
                    {
                        If (LEqual (Arg1, 0x02))
                        {
                            Return (AM02 ())
                        }
                        Else
                        {
                            If (LEqual (Arg1, 0x03))
                            {
                                Return (AM03 (WIID))
                            }
                            Else
                            {
                                If (LEqual (Arg1, 0x04))
                                {
                                    CreateDWordField (Arg2, 0x04, IVAL)
                                    Return (AM04 (WIID, IVAL))
                                }
                                Else
                                {
                                    If (LEqual (Arg1, 0x05))
                                    {
                                        Return (AM05 (WIID))
                                    }
                                    Else
                                    {
                                        If (LEqual (Arg1, 0x06))
                                        {
                                            Return (AM06 ())
                                        }
                                        Else
                                        {
                                            If (LEqual (Arg1, 0x07))
                                            {
                                                AM07 (Arg2)
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }

                Return (Zero)
            }
        }
    }

    OperationRegion (EXTM, SystemMemory, 0x000FF830, 0x12)
    Field (EXTM, WordAcc, NoLock, Preserve)
    {
        ROM1,   16, 
        RMS1,   16, 
        ROM2,   16, 
        RMS2,   16, 
        ROM3,   16, 
        RMS3,   16, 
        AMEM,   32, 
        AINF,   8
    }

    OperationRegion (ELCR, SystemIO, 0x04D0, 0x02)
    Field (ELCR, ByteAcc, NoLock, Preserve)
    {
        ELC1,   8, 
        ELC2,   8
    }

    OperationRegion (\P01, SystemIO, 0x4001, 0x01)
    Field (\P01, ByteAcc, NoLock, Preserve)
    {
        P1,     8
    }

    OperationRegion (\PR20, SystemIO, 0x4020, 0x04)
    Field (\PR20, DWordAcc, NoLock, Preserve)
    {
        P20,    32
    }

    Name (OSFX, 0x01)
    Name (OSFL, 0x01)
    Method (STRC, 2, Serialized)
    {
        If (LNotEqual (SizeOf (Arg0), SizeOf (Arg1)))
        {
            Return (0x00)
        }

        Add (SizeOf (Arg0), 0x01, Local0)
        Name (BUF0, Buffer (Local0) {})
        Name (BUF1, Buffer (Local0) {})
        Store (Arg0, BUF0)
        Store (Arg1, BUF1)
        While (Local0)
        {
            Decrement (Local0)
            If (LNotEqual (DerefOf (Index (BUF0, Local0)), DerefOf (Index (
                BUF1, Local0))))
            {
                Return (Zero)
            }
        }

        Return (One)
    }

    OperationRegion (RTCM, SystemIO, 0x70, 0x02)
    Field (RTCM, ByteAcc, NoLock, Preserve)
    {
        CMIN,   8, 
        CMDA,   8
    }

    IndexField (CMIN, CMDA, ByteAcc, NoLock, Preserve)
    {
                Offset (0x0F), 
        SHUT,   8
    }

    OperationRegion (INFO, SystemMemory, 0x000FF840, 0x01)
    Field (INFO, ByteAcc, NoLock, Preserve)
    {
        KBDI,   1, 
        RTCW,   1, 
        PS2F,   1, 
        IRFL,   2, 
        DISE,   1, 
        SSHU,   1, 
        AWMD,   1
    }

    OperationRegion (BEEP, SystemIO, 0x61, 0x01)
    Field (BEEP, ByteAcc, NoLock, Preserve)
    {
        S1B,    8
    }

    OperationRegion (CONT, SystemIO, 0x40, 0x04)
    Field (CONT, ByteAcc, NoLock, Preserve)
    {
        CNT0,   8, 
        CNT1,   8, 
        CNT2,   8, 
        CTRL,   8
    }

    Method (SPKR, 1, NotSerialized)
    {
        Store (S1B, Local0)
        Store (0xB6, CTRL)
        Store (0x55, CNT2)
        Store (0x03, CNT2)
        Store (Arg0, Local2)
        While (LGreater (Local2, 0x00))
        {
            Or (S1B, 0x03, S1B)
            Store (0x5FFF, Local3)
            While (LGreater (Local3, 0x00))
            {
                Decrement (Local3)
            }

            And (S1B, 0xFC, S1B)
            Store (0x0EFF, Local3)
            While (LGreater (Local3, 0x00))
            {
                Decrement (Local3)
            }

            Decrement (Local2)
        }

        Store (Local0, S1B)
    }

    Scope (\)
    {
        Name (PICF, 0x00)
        Method (_PIC, 1, NotSerialized)
        {
            Store (Arg0, PICF)
            If (Arg0)
            {
                \_SB.PCI0.LPC0.DSPI ()
            }
        }
    }

    Method (\_PTS, 1, NotSerialized)
    {
        Or (Arg0, 0xF0, Local0)
        Store (Local0, DBG1)
        SALD (Arg0)
        If (LEqual (Arg0, 0x01))
        {
            EWBP ()
        }

        If (LEqual (Arg0, 0x05)) {}
        SPTS (Arg0)
    }

    Method (\_WAK, 1, NotSerialized)
    {
        Store (0xFF, DBG1)
        If (LEqual (Arg0, 0x04))
        {
            If (LEqual (OSFL, 0x00))
            {
                Store (0x58, SMIP)
            }

            If (LEqual (OSFL, 0x02))
            {
                Store (0x57, SMIP)
            }

            If (LEqual (OSFL, 0x01))
            {
                Store (0x56, SMIP)
            }

            If (LEqual (OSFX, 0x03))
            {
                Store (0x59, SMIP)
            }
        }

        SALD (0x00)
        SWAK (Arg0)
        If (LEqual (OSFL, 0x01))
        {
            Notify (\_SB.PWRB, 0x02)
        }
        Else
        {
            If (LEqual (Arg0, 0x01))
            {
                And (P1, 0x04, Local0)
                If (LEqual (Local0, 0x00))
                {
                    Notify (\_SB.PWRB, 0x02)
                }
            }

            If (LEqual (Arg0, 0x03))
            {
                If (LEqual (RTCW, Zero))
                {
                    Notify (\_SB.PWRB, 0x02)
                }
            }
        }

        If (LEqual (Arg0, 0x04))
        {
            Notify (\_SB.PWRB, 0x02)
        }

        Return(Package(0x02){Zero, Zero})
    }

    Scope (\_SI)
    {
    }

    OperationRegion (TEMM, SystemMemory, 0x000FF810, 0x0C)
    Field (TEMM, WordAcc, NoLock, Preserve)
    {
        TP1H,   16, 
        TP1L,   16, 
        TP2H,   16, 
        TP2L,   16, 
        TRPC,   16, 
        SENF,   16
    }

    Name (TVAR, Buffer (0x05)
    {
        0x00, 0x00, 0x00, 0x00, 0x00
    })
    CreateByteField (TVAR, 0x00, PLCY)
    CreateWordField (TVAR, 0x01, CTOS)
    CreateWordField (TVAR, 0x03, CTHY)
    Name (TBUF, Buffer (0x04)
    {
        0x00, 0x00, 0x00, 0x00
    })
    CreateByteField (TBUF, 0x00, DB00)
    CreateByteField (TBUF, 0x01, DB01)
    CreateWordField (TBUF, 0x00, DW00)
    CreateWordField (TBUF, 0x02, DW01)
    CreateDWordField (TBUF, 0x00, DATD)
    OperationRegion (SEN1, SystemIO, 0x0295, 0x02)
    Field (SEN1, ByteAcc, NoLock, Preserve)
    {
        SEI0,   8, 
        SED0,   8
    }

    Method (STOS, 3, NotSerialized)
    {
        Store (RSEN (0x4E), Local0)
        And (Local0, Not (0x07), Local1)
        Or (Local1, 0x01, Local1)
        WSEN (0x4E, Local1)
        WSEN (0x55, Arg1)
        WSEN (0x56, Arg0)
        WSEN (0x4E, Local0)
    }

    Method (STHY, 3, NotSerialized)
    {
        Store (RSEN (0x4E), Local0)
        And (Local0, Not (0x07), Local1)
        Or (Local1, 0x01, Local1)
        WSEN (0x4E, Local1)
        WSEN (0x53, Arg1)
        WSEN (0x54, Arg0)
        WSEN (0x4E, Local0)
    }

    Method (RTMP, 0, NotSerialized)
    {
        Store (RSEN (0x4E), Local0)
        And (Local0, Not (0x07), Local1)
        Or (Local1, 0x01, Local1)
        WSEN (0x4E, Local1)
        Store (RSEN (0x50), Local3)
        WSEN (0x4E, Local0)
        If (LLess (Local3, 0x80))
        {
            Multiply (Local3, 0x0A, Local3)
            Add (Local3, 0x0AAC, Local3)
        }
        Else
        {
            Subtract (Local3, 0x80, Local3)
            Multiply (Local3, 0x0A, Local3)
            Subtract (0x0AAC, Local3, Local3)
        }

        If (LGreater (Local3, 0x0E8A))
        {
            Store (0x0AAC, Local3)
        }

        If (LEqual (SSHU, 0x01))
        {
            Store (0x0C3C, Local3)
        }

        If (LNotEqual (RFAN (), 0x00))
        {
            Store (0x02, DBG1)
            Store (0x0F66, Local3)
        }

        Return (Local3)
    }

    Method (RFAN, 0, NotSerialized)
    {
        And (RSMI (), RSTS (), Local1)
        Return (Local1)
    }

    Method (RSMI, 0, NotSerialized)
    {
        Store (RSEN (0x4E), Local0)
        And (Local0, Not (0x07), Local1)
        WSEN (0x4E, Local1)
        And (Not (RSEN (0x43)), 0xC0, Local1)
        And (Not (RSEN (0x44)), 0x08, Local2)
        Or (Local1, Local2, Local1)
        And (Not (RSEN (0x46)), 0x06, Local2)
        Or (Local1, Local2, Local1)
        WSEN (0x4E, Local0)
        Sleep (0x64)
        Return (Local1)
    }

    Method (RSTS, 0, NotSerialized)
    {
        Store (RSEN (0x4E), Local0)
        And (Local0, Not (0x07), Local1)
        Or (Local1, 0x04, Local1)
        WSEN (0x4E, Local1)
        And (RSEN (0x59), 0xC0, Local1)
        And (RSEN (0x5A), 0x08, Local2)
        Or (Local1, Local2, Local1)
        And (RSEN (0x5A), 0x04, Local2)
        ShiftRight (Local2, 0x01, Local2)
        Or (Local1, Local2, Local1)
        And (RSEN (0x5B), 0x80, Local2)
        ShiftRight (Local2, 0x05, Local2)
        Or (Local1, Local2, Local1)
        WSEN (0x4E, Local0)
        Sleep (0x64)
        Return (Local1)
    }

    Method (WSEN, 2, NotSerialized)
    {
        Store (Arg0, SEI0)
        Store (Arg1, SED0)
    }

    Method (RSEN, 1, NotSerialized)
    {
        Store (Arg0, SEI0)
        Store (SED0, Local7)
        Return (Local7)
    }

    Method (SFAN, 1, NotSerialized)
    {
        If (LEqual (Arg0, Zero))
        {
            FOFF ()
        }
        Else
        {
            FON ()
        }
    }

    Method (FON, 0, NotSerialized)
    {
        Store (RSEN (0x4E), Local0)
        And (Local0, Not (0x07), Local1)
        WSEN (0x4E, Local1)
        WSEN (0x01, 0xFF)
        WSEN (0x03, 0xFF)
        WSEN (0x4E, Local0)
    }

    Method (FOFF, 0, NotSerialized)
    {
        Store (RSEN (0x4E), Local0)
        And (Local0, Not (0x07), Local1)
        WSEN (0x4E, Local1)
        WSEN (0x01, 0x00)
        WSEN (0x03, 0x00)
        WSEN (0x4E, Local0)
    }

    OperationRegion (SM00, SystemIO, 0x0B00, 0x08)
    Field (SM00, ByteAcc, NoLock, Preserve)
    {
        HSTS,   8, 
        SLVS,   8, 
        CTLR,   8, 
        CMDR,   8, 
        ADDR,   8, 
        DAT0,   8, 
        DAT1,   8, 
        DAT2,   8
    }

    Method (CSMS, 0, NotSerialized)
    {
        And (HSTS, 0x02, Local0)
        While (LNotEqual (Local0, 0x00))
        {
            Stall (0x01)
            Store (HSTS, HSTS)
            And (HSTS, 0x18, Local0)
        }
    }

    Method (SWFS, 0, NotSerialized)
    {
        And (HSTS, 0x01, Local0)
        While (LEqual (Local0, 0x01))
        {
            Stall (0x01)
            And (HSTS, 0x01, Local0)
        }

        Store (0xFF, HSTS)
    }

    Method (WBYT, 3, NotSerialized)
    {
        CSMS ()
        Store (Arg2, DAT0)
        Store (Arg0, ADDR)
        Store (Arg1, CMDR)
        Store (0x48, CTLR)
        SWFS ()
        CSMS ()
    }

    Method (WWRD, 4, NotSerialized)
    {
        CSMS ()
        Store (Arg2, DAT0)
        Store (Arg3, DAT1)
        Store (Arg0, ADDR)
        Store (Arg1, CMDR)
        Store (0x4C, CTLR)
        SWFS ()
        CSMS ()
    }

    Method (RBYT, 2, NotSerialized)
    {
        CSMS ()
        Store (Arg1, CMDR)
        Or (Arg0, 0x01, ADDR)
        Store (0x48, CTLR)
        SWFS ()
        Return (DAT0)
    }

    Method (RWRD, 2, NotSerialized)
    {
        CSMS ()
        Or (Arg0, 0x01, ADDR)
        Store (Arg1, CMDR)
        Store (0x4C, CTLR)
        SWFS ()
        Store (DAT0, Local0)
        ShiftLeft (DAT1, 0x08, Local1)
        Or (Local0, Local1, Local2)
        Return (Local2)
    }

    Scope (\_TZ)
    {

        Device (FAN)
        {
            Name (_HID, EisaId ("PNP0C0B"))
            Method (_INI, 0, NotSerialized)
            {
                Store (TP1H, CTOS)
                Store (TP1L, CTHY)
            }
        }

        ThermalZone (THRM)
        {
            Name (_AL0, Package (0x01)
            {
                FAN
            })
            Method (_AC0, 0, NotSerialized)
            {
                If (Or (PLCY, PLCY, Local7))
                {
                    Return (TP2L)
                }
                Else
                {
                    Return (TP1L)
                }
            }

            Name (_PSL, Package (0x04)
            {
                \_PR.C000,
                \_PR.C001,
                \_PR.C002,
                \_PR.C003
            })
            Name (_TZD, Package (0x04)
            {
                \_PR.C000,
                \_PR.C001,
                \_PR.C002,
                \_PR.C003
            })

            Name (_TSP, 0x3C)
            Name (_TC1, 0x04)
            Name (_TC2, 0x03)
            Method (_PSV, 0, NotSerialized)
            {
                If (Or (PLCY, PLCY, Local7))
                {
                    Return (TP1H)
                }
                Else
                {
                    Return (TP2H)
                }
            }

            Method (_CRT, 0, NotSerialized)
            {
                Return (TRPC)
            }

            Method (_TMP, 0, NotSerialized)
            {
                And (SENF, 0x01, Local6)
                If (LEqual (Local6, 0x01))
                {
                    Return (RTMP ())
                }
                Else
                {
                    Store ("_TMP Read ERROR", Debug)

                    Return (0x0B86)
                }
            }

            Method (_SCP, 1, NotSerialized)
            {
                If (Arg0)
                {
                    Store (One, PLCY)
                }
                Else
                {
                    Store (Zero, PLCY)
                }

                Notify (\_TZ.THRM, 0x81)
            }

            Method (STMP, 2, NotSerialized)
            {
                Store (Arg1, DW00)
                If (Arg0)
                {
                    STHY (DB00, DB01, DW00)
                }
                Else
                {
                    STOS (DB00, DB01, DW00)
                }
            }
        }
    }

    Scope (\_GPE)
    {
        Method (_L04, 0, NotSerialized)
        {
            Notify (\_SB.PCI0.P2P, 0x02)
        }

        Method (_L18, 0, NotSerialized)
        {
            Notify (\_SB.PCI0.PCE2, 0x02)
            Notify (\_SB.PCI0.PCE3, 0x02)
            Notify (\_SB.PCI0.PCE4, 0x02)
            Notify (\_SB.PCI0.PCE5, 0x02)
            Notify (\_SB.PCI0.PCE6, 0x02)
            Notify (\_SB.PCI0.PCE7, 0x02)
            Notify (\_SB.PCI0.PCE9, 0x02)
            Notify (\_SB.PCI0.PCEA, 0x02)
            Notify (\_SB.PCI0.PCEB, 0x02)
            Notify (\_SB.PCI0.PCEC, 0x02)
        }

        Method (_L09, 0, NotSerialized)
        {
            Notify (\_TZ.THRM, 0x81)
        }

        Method (_L03, 0, NotSerialized)
        {
            Notify (\_SB.PCI0.PS2K, 0x02)
            Notify (\_SB.PCI0.PS2M, 0x02)
        }

        Method (_L0B, 0, NotSerialized)
        {
            Notify (\_SB.PCI0.USB0, 0x02)
            Notify (\_SB.PCI0.USB1, 0x02)
            Notify (\_SB.PCI0.USB2, 0x02)
            Notify (\_SB.PCI0.USB3, 0x02)
            Notify (\_SB.PCI0.USB4, 0x02)
            Notify (\_SB.PCI0.USB5, 0x02)
        }

        Method (_L1B, 0, NotSerialized)
        {
            Notify (\_SB.PCI0.SBAZ, 0x02)
        }
    }

    Scope (\_SB)
    {
        Method (_INI, 0, NotSerialized)
        {
            Store (OSFX, OSTY)
            If (LEqual (OSFX, 0x00))
            {
                Store (0x04, OSTY)
            }

            If (LEqual (OSFX, 0x03))
            {
                Store (0x05, OSTY)
            }

            If (LEqual (OSFX, 0x04))
            {
                Store (0x06, OSTY)
            }
        }

        Device (PWRB)
        {
            Name (_HID, EisaId ("PNP0C0C"))
            Method (_STA, 0, NotSerialized)
            {
                Return (0x0B)
            }
        }

        Device (PCI0)
        {
            Name (_HID, EisaId ("PNP0A03"))
            Name (_ADR, 0x00)
            OperationRegion (BAR1, PCI_Config, 0x14, 0x04)
            Field (BAR1, ByteAcc, NoLock, Preserve)
            {
                MMIO,   32
            }

            Method (_S3D, 0, NotSerialized)
            {
                If (LEqual (OSFL, 0x02))
                {
                    Return (0x02)
                }
                Else
                {
                    Return (0x03)
                }
            }

            Method (_STA, 0, NotSerialized)
            {
                Return (0x0F)
            }

            Method (_CRS, 0, Serialized)
            {
                Name (BUF0, ResourceTemplate ()
                {
                    WordBusNumber (ResourceConsumer, MinNotFixed, MaxNotFixed, PosDecode,
                        0x0000,             // Granularity
                        0x0000,             // Range Minimum
                        0x00FF,             // Range Maximum
                        0x0000,             // Translation Offset
                        0x0100,             // Length
                        ,, )
                    IO (Decode16,
                        0x0CF8,             // Range Minimum
                        0x0CF8,             // Range Maximum
                        0x01,               // Alignment
                        0x08,               // Length
                        )
                    WordIO (ResourceProducer, MinFixed, MaxFixed, PosDecode, EntireRange,
                        0x0000,             // Granularity
                        0x0000,             // Range Minimum
                        0x0CF7,             // Range Maximum
                        0x0000,             // Translation Offset
                        0x0CF8,             // Length
                        ,, , TypeStatic)
                    WordIO (ResourceProducer, MinFixed, MaxFixed, PosDecode, EntireRange,
                        0x0000,             // Granularity
                        0x0D00,             // Range Minimum
                        0xFFFF,             // Range Maximum
                        0x0000,             // Translation Offset
                        0xF300,             // Length
                        ,, , TypeStatic)
                    DWordMemory (ResourceProducer, PosDecode, MinFixed, MaxFixed, Cacheable, ReadWrite,
                        0x00000000,         // Granularity
                        0x000A0000,         // Range Minimum
                        0x000BFFFF,         // Range Maximum
                        0x00000000,         // Translation Offset
                        0x00020000,         // Length
                        ,, , AddressRangeMemory, TypeStatic)
                    DWordMemory (ResourceProducer, PosDecode, MinFixed, MaxFixed, Cacheable, ReadWrite,
                        0x00000000,         // Granularity
                        0x000C0000,         // Range Minimum
                        0x000DFFFF,         // Range Maximum
                        0x00000000,         // Translation Offset
                        0x00020000,         // Length
                        ,, , AddressRangeMemory, TypeStatic)
                    DWordMemory (ResourceProducer, PosDecode, MinFixed, MaxFixed, Cacheable, ReadWrite,
                        0x00000000,         // Granularity
                        0x00100000,         // Range Minimum
                        0xFFFFFFFF,         // Range Maximum
                        0x00000000,         // Translation Offset
                        0xFFF00000,         // Length
                        ,, _Y00, AddressRangeMemory, TypeStatic)
                })
                CreateDWordField (BUF0, \_SB.PCI0._CRS._Y00._MIN, TCMM)
                CreateDWordField (BUF0, \_SB.PCI0._CRS._Y00._LEN, TOMM)
                Add (AMEM, 0x00010000, TCMM)
                Subtract (0xFEC00000, TCMM, TOMM)
                Return (BUF0)
            }

            Name (PICM, Package (0x24)
            {
                Package (0x04)
                {
                    0x0002FFFF, 
                    0x00, 
                    \_SB.PCI0.LPC0.LNKC, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0002FFFF, 
                    0x01, 
                    \_SB.PCI0.LPC0.LNKD, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0002FFFF, 
                    0x02, 
                    \_SB.PCI0.LPC0.LNKA, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0002FFFF, 
                    0x03, 
                    \_SB.PCI0.LPC0.LNKB, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0003FFFF, 
                    0x00, 
                    \_SB.PCI0.LPC0.LNKD, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0003FFFF, 
                    0x01, 
                    \_SB.PCI0.LPC0.LNKA, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0003FFFF, 
                    0x02, 
                    \_SB.PCI0.LPC0.LNKB, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0003FFFF, 
                    0x03, 
                    \_SB.PCI0.LPC0.LNKC, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0004FFFF, 
                    0x00, 
                    \_SB.PCI0.LPC0.LNKA, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0004FFFF, 
                    0x01, 
                    \_SB.PCI0.LPC0.LNKB, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0004FFFF, 
                    0x02, 
                    \_SB.PCI0.LPC0.LNKC, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0004FFFF, 
                    0x03, 
                    \_SB.PCI0.LPC0.LNKD, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0005FFFF, 
                    0x00, 
                    \_SB.PCI0.LPC0.LNKB, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0005FFFF, 
                    0x01, 
                    \_SB.PCI0.LPC0.LNKC, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0005FFFF, 
                    0x02, 
                    \_SB.PCI0.LPC0.LNKD, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0005FFFF, 
                    0x03, 
                    \_SB.PCI0.LPC0.LNKA, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x000BFFFF, 
                    0x00, 
                    \_SB.PCI0.LPC0.LNKD, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x000BFFFF, 
                    0x01, 
                    \_SB.PCI0.LPC0.LNKA, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x000BFFFF, 
                    0x02, 
                    \_SB.PCI0.LPC0.LNKB, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x000BFFFF, 
                    0x03, 
                    \_SB.PCI0.LPC0.LNKC, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x000CFFFF, 
                    0x00, 
                    \_SB.PCI0.LPC0.LNKA, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x000CFFFF, 
                    0x01, 
                    \_SB.PCI0.LPC0.LNKB, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x000CFFFF, 
                    0x02, 
                    \_SB.PCI0.LPC0.LNKC, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x000CFFFF, 
                    0x03, 
                    \_SB.PCI0.LPC0.LNKD, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0014FFFF, 
                    0x00, 
                    \_SB.PCI0.LPC0.LNKA, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0014FFFF, 
                    0x01, 
                    \_SB.PCI0.LPC0.LNKB, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0014FFFF, 
                    0x02, 
                    \_SB.PCI0.LPC0.LNKC, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0014FFFF, 
                    0x03, 
                    \_SB.PCI0.LPC0.LNKD, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0013FFFF, 
                    0x00, 
                    \_SB.PCI0.LPC0.LNKA, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0013FFFF, 
                    0x01, 
                    \_SB.PCI0.LPC0.LNKB, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0013FFFF, 
                    0x02, 
                    \_SB.PCI0.LPC0.LNKC, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0013FFFF, 
                    0x03, 
                    \_SB.PCI0.LPC0.LNKD, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0012FFFF, 
                    0x00, 
                    \_SB.PCI0.LPC0.LNK0, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0012FFFF, 
                    0x01, 
                    \_SB.PCI0.LPC0.LNK0, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0012FFFF, 
                    0x02, 
                    \_SB.PCI0.LPC0.LNK0, 
                    0x00
                }, 

                Package (0x04)
                {
                    0x0012FFFF, 
                    0x03, 
                    \_SB.PCI0.LPC0.LNK0, 
                    0x00
                }
            })
            Name (APIC, Package (0x21)
            {
                Package (0x04)
                {
                    0x0002FFFF, 
                    0x00, 
                    0x00, 
                    0x12
                }, 

                Package (0x04)
                {
                    0x0002FFFF, 
                    0x01, 
                    0x00, 
                    0x13
                }, 

                Package (0x04)
                {
                    0x0002FFFF, 
                    0x02, 
                    0x00, 
                    0x10
                }, 

                Package (0x04)
                {
                    0x0002FFFF, 
                    0x03, 
                    0x00, 
                    0x11
                }, 

                Package (0x04)
                {
                    0x0003FFFF, 
                    0x00, 
                    0x00, 
                    0x13
                }, 

                Package (0x04)
                {
                    0x0003FFFF, 
                    0x01, 
                    0x00, 
                    0x10
                }, 

                Package (0x04)
                {
                    0x0003FFFF, 
                    0x02, 
                    0x00, 
                    0x11
                }, 

                Package (0x04)
                {
                    0x0003FFFF, 
                    0x03, 
                    0x00, 
                    0x12
                }, 

                Package (0x04)
                {
                    0x0004FFFF, 
                    0x00, 
                    0x00, 
                    0x10
                }, 

                Package (0x04)
                {
                    0x0004FFFF, 
                    0x01, 
                    0x00, 
                    0x11
                }, 

                Package (0x04)
                {
                    0x0004FFFF, 
                    0x02, 
                    0x00, 
                    0x12
                }, 

                Package (0x04)
                {
                    0x0004FFFF, 
                    0x03, 
                    0x00, 
                    0x13
                }, 

                Package (0x04)
                {
                    0x0005FFFF, 
                    0x00, 
                    0x00, 
                    0x11
                }, 

                Package (0x04)
                {
                    0x0005FFFF, 
                    0x01, 
                    0x00, 
                    0x12
                }, 

                Package (0x04)
                {
                    0x0005FFFF, 
                    0x02, 
                    0x00, 
                    0x13
                }, 

                Package (0x04)
                {
                    0x0005FFFF, 
                    0x03, 
                    0x00, 
                    0x10
                }, 

                Package (0x04)
                {
                    0x000BFFFF, 
                    0x00, 
                    0x00, 
                    0x13
                }, 

                Package (0x04)
                {
                    0x000BFFFF, 
                    0x01, 
                    0x00, 
                    0x10
                }, 

                Package (0x04)
                {
                    0x000BFFFF, 
                    0x02, 
                    0x00, 
                    0x11
                }, 

                Package (0x04)
                {
                    0x000BFFFF, 
                    0x03, 
                    0x00, 
                    0x12
                }, 

                Package (0x04)
                {
                    0x000CFFFF, 
                    0x00, 
                    0x00, 
                    0x10
                }, 

                Package (0x04)
                {
                    0x000CFFFF, 
                    0x01, 
                    0x00, 
                    0x11
                }, 

                Package (0x04)
                {
                    0x000CFFFF, 
                    0x02, 
                    0x00, 
                    0x12
                }, 

                Package (0x04)
                {
                    0x000CFFFF, 
                    0x03, 
                    0x00, 
                    0x13
                }, 

                Package (0x04)
                {
                    0x0014FFFF, 
                    0x00, 
                    0x00, 
                    0x10
                }, 

                Package (0x04)
                {
                    0x0014FFFF, 
                    0x01, 
                    0x00, 
                    0x11
                }, 

                Package (0x04)
                {
                    0x0014FFFF, 
                    0x02, 
                    0x00, 
                    0x12
                }, 

                Package (0x04)
                {
                    0x0014FFFF, 
                    0x03, 
                    0x00, 
                    0x13
                }, 

                Package (0x04)
                {
                    0x0013FFFF, 
                    0x00, 
                    0x00, 
                    0x10
                }, 

                Package (0x04)
                {
                    0x0013FFFF, 
                    0x01, 
                    0x00, 
                    0x11
                }, 

                Package (0x04)
                {
                    0x0013FFFF, 
                    0x02, 
                    0x00, 
                    0x12
                }, 

                Package (0x04)
                {
                    0x0013FFFF, 
                    0x03, 
                    0x00, 
                    0x13
                }, 

                Package (0x04)
                {
                    0x0012FFFF, 
                    0x00, 
                    0x00, 
                    0x16
                }
            })
            Method (_PRT, 0, NotSerialized)
            {
                If (LNot (PICF))
                {
                    Return (PICM)
                }
                Else
                {
                    Return (APIC)
                }
            }

            Device (SMB0)
            {
                Name (_ADR, 0x00140000)
                Method (_CRS, 0, Serialized)
                {
                    Name (BUF0, ResourceTemplate ()
                    {
                        IO (Decode16,
                            0x0B00,             // Range Minimum
                            0x0B00,             // Range Maximum
                            0x01,               // Alignment
                            0x10,               // Length
                            )
                    })

                    Return (BUF0)
                }

                OperationRegion (SMCF, PCI_Config, 0x90, 0x02)
                Field (SMCF, WordAcc, NoLock, Preserve)
                {
                    SB1,    16
                }

                Method (SMBB, 0, NotSerialized)
                {
                    And (SB1, 0xFFFE, Local0)
                    Return (Local0)
                }

                OperationRegion (\_SB.PCI0.SMB0.HETT, PCI_Config, 0x64, 0x02)
                Scope (\)
                {
                    Field (\_SB.PCI0.SMB0.HETT, ByteAcc, NoLock, Preserve)
                    {
                        HP0,    8, 
                            ,   2, 
                        HPTF,   1, 
                                Offset (0x02)
                    }
                }
            }

            Device (USB0)
            {
                Name (_ADR, 0x00130000)
                Name (_PRW, Package (0x02)
                {
                    0x0B, 
                    0x04
                })
                Method (_S3D, 0, NotSerialized)
                {
                    If (LEqual (OSFL, 0x02))
                    {
                        Return (0x02)
                    }
                    Else
                    {
                        Return (0x03)
                    }
                }
            }

            Device (USB1)
            {
                Name (_ADR, 0x00130001)
                Name (_PRW, Package (0x02)
                {
                    0x0B, 
                    0x04
                })
                Method (_S3D, 0, NotSerialized)
                {
                    If (LEqual (OSFL, 0x02))
                    {
                        Return (0x02)
                    }
                    Else
                    {
                        Return (0x03)
                    }
                }
            }

            Device (USB2)
            {
                Name (_ADR, 0x00130002)
                Name (_PRW, Package (0x02)
                {
                    0x0B, 
                    0x04
                })
                Method (_S3D, 0, NotSerialized)
                {
                    If (LEqual (OSFL, 0x02))
                    {
                        Return (0x02)
                    }
                    Else
                    {
                        Return (0x03)
                    }
                }
            }

            Device (USB3)
            {
                Name (_ADR, 0x00130003)
                Name (_PRW, Package (0x02)
                {
                    0x0B, 
                    0x04
                })
                Method (_S3D, 0, NotSerialized)
                {
                    If (LEqual (OSFL, 0x02))
                    {
                        Return (0x02)
                    }
                    Else
                    {
                        Return (0x03)
                    }
                }
            }

            Device (USB4)
            {
                Name (_ADR, 0x00130004)
                Name (_PRW, Package (0x02)
                {
                    0x0B, 
                    0x04
                })
                Method (_S3D, 0, NotSerialized)
                {
                    If (LEqual (OSFL, 0x02))
                    {
                        Return (0x02)
                    }
                    Else
                    {
                        Return (0x03)
                    }
                }
            }

            Device (USB5)
            {
                Name (_ADR, 0x00130005)
                Name (_PRW, Package (0x02)
                {
                    0x0B, 
                    0x04
                })
                Method (_S3D, 0, NotSerialized)
                {
                    If (LEqual (OSFL, 0x02))
                    {
                        Return (0x02)
                    }
                    Else
                    {
                        Return (0x03)
                    }
                }
            }

            Device (SBAZ)
            {
                Name (_ADR, 0x00140002)
                OperationRegion (PCI, PCI_Config, 0x00, 0x0100)
                Field (PCI, AnyAcc, NoLock, Preserve)
                {
                            Offset (0x42), 
                    DNSP,   1, 
                    DNSO,   1, 
                    ENSR,   1
                }

                Name (_PRW, Package (0x02)
                {
                    0x1B, 
                    0x04
                })
            }

            Device (SATA)
            {
                Name (_ADR, 0x00120000)
                Method (_INI, 0, NotSerialized)
                {
                    \_GPE._L1F ()
                }

                Name (SPTM, Buffer (0x14)
                {
                    /* 0000 */    0x78, 0x00, 0x00, 0x00, 0x0F, 0x00, 0x00, 0x00, 
                    /* 0008 */    0x78, 0x00, 0x00, 0x00, 0x0F, 0x00, 0x00, 0x00, 
                    /* 0010 */    0x1F, 0x00, 0x00, 0x00
                })
                Device (PRID)
                {
                    Name (_ADR, 0x00)
                    Method (_GTM, 0, NotSerialized)
                    {
                        Return (SPTM)
                    }

                    Method (_STM, 3, NotSerialized)
                    {
                    }

                    Name (PRIS, 0x00)
                    Method (_PS0, 0, NotSerialized)
                    {
                        If (LOr (LEqual (OSTY, 0x06), LEqual (OSTY, 0x04)))
                        {
                            If (\PMS1)
                            {
                                Store (0x32, Local0)
                                While (LAnd (LEqual (\PMBY, 0x01), Local0))
                                {
                                    Sleep (0xFA)
                                    Decrement (Local0)
                                }
                            }

                            If (\PSS1)
                            {
                                Store (0x32, Local0)
                                While (LAnd (LEqual (\PSBY, 0x01), Local0))
                                {
                                    Sleep (0xFA)
                                    Decrement (Local0)
                                }
                            }
                        }

                        Store (0x00, PRIS)
                    }

                    Method (_PS3, 0, NotSerialized)
                    {
                        Store (0x03, PRIS)
                    }

                    Method (_PSC, 0, NotSerialized)
                    {
                        Return (PRIS)
                    }

                    Device (P_D0)
                    {
                        Name (_ADR, 0x00)
                        Method (_STA, 0, NotSerialized)
                        {
                            If (Not (LEqual (\PMS1, 0x00)))
                            {
                                Return (0x0F)
                            }
                            Else
                            {
                                Return (0x00)
                            }
                        }

                        Name (S12P, 0x00)
                        Method (_PS0, 0, NotSerialized)
                        {
                            Store (0x32, Local0)
                            While (LAnd (LEqual (\PMBY, 0x01), Local0))
                            {
                                Sleep (0xFA)
                                Decrement (Local0)
                            }

                            Store (0x00, S12P)
                        }

                        Method (_PS3, 0, NotSerialized)
                        {
                            Store (0x03, S12P)
                        }

                        Method (_PSC, 0, NotSerialized)
                        {
                            Return (S12P)
                        }
                    }

                    Device (P_D1)
                    {
                        Name (_ADR, 0x01)
                        Method (_STA, 0, NotSerialized)
                        {
                            If (Not (LEqual (\PSS1, 0x00)))
                            {
                                Return (0x0F)
                            }
                            Else
                            {
                                Return (0x00)
                            }
                        }

                        Name (S12P, 0x00)
                        Method (_PS0, 0, NotSerialized)
                        {
                            Store (0x32, Local0)
                            While (LAnd (LEqual (\PSBY, 0x01), Local0))
                            {
                                Sleep (0xFA)
                                Decrement (Local0)
                            }

                            Store (0x00, S12P)
                        }

                        Method (_PS3, 0, NotSerialized)
                        {
                            Store (0x03, S12P)
                        }

                        Method (_PSC, 0, NotSerialized)
                        {
                            Return (S12P)
                        }
                    }
                }

                Device (SECD)
                {
                    Name (_ADR, 0x01)
                    Method (_GTM, 0, NotSerialized)
                    {
                        Return (SPTM)
                    }

                    Method (_STM, 3, NotSerialized)
                    {
                    }

                    Name (SECS, 0x00)
                    Method (_PS0, 0, NotSerialized)
                    {
                        If (LOr (LEqual (OSTY, 0x06), LEqual (OSTY, 0x04)))
                        {
                            If (\SMS1)
                            {
                                Store (0x32, Local0)
                                While (LAnd (LEqual (\SMBY, 0x01), Local0))
                                {
                                    Sleep (0xFA)
                                    Decrement (Local0)
                                }
                            }

                            If (\SSS1)
                            {
                                Store (0x32, Local0)
                                While (LAnd (LEqual (\SSBY, 0x01), Local0))
                                {
                                    Sleep (0xFA)
                                    Decrement (Local0)
                                }
                            }
                        }

                        Store (0x00, SECS)
                    }

                    Method (_PS3, 0, NotSerialized)
                    {
                        Store (0x03, SECS)
                    }

                    Method (_PSC, 0, NotSerialized)
                    {
                        Return (SECS)
                    }

                    Device (S_D0)
                    {
                        Name (_ADR, 0x00)
                        Method (_STA, 0, NotSerialized)
                        {
                            If (Not (LEqual (\SMS1, 0x00)))
                            {
                                Return (0x0F)
                            }
                            Else
                            {
                                Return (0x00)
                            }
                        }

                        Name (S12P, 0x00)
                        Method (_PS0, 0, NotSerialized)
                        {
                            Store (0x32, Local0)
                            While (LAnd (LEqual (\SMBY, 0x01), Local0))
                            {
                                Sleep (0xFA)
                                Decrement (Local0)
                            }

                            Store (0x00, S12P)
                        }

                        Method (_PS3, 0, NotSerialized)
                        {
                            Store (0x03, S12P)
                        }

                        Method (_PSC, 0, NotSerialized)
                        {
                            Return (S12P)
                        }
                    }

                    Device (S_D1)
                    {
                        Name (_ADR, 0x01)
                        Method (_STA, 0, NotSerialized)
                        {
                            If (Not (LEqual (\SSS1, 0x00)))
                            {
                                Return (0x0F)
                            }
                            Else
                            {
                                Return (0x00)
                            }
                        }

                        Name (S12P, 0x00)
                        Method (_PS0, 0, NotSerialized)
                        {
                            Store (0x32, Local0)
                            While (LAnd (LEqual (\SSBY, 0x01), Local0))
                            {
                                Sleep (0xFA)
                                Decrement (Local0)
                            }

                            Store (0x00, S12P)
                        }

                        Method (_PS3, 0, NotSerialized)
                        {
                            Store (0x03, S12P)
                        }

                        Method (_PSC, 0, NotSerialized)
                        {
                            Return (S12P)
                        }
                    }
                }

                Scope (\_GPE)
                {
                    Method (_L1F, 0, NotSerialized)
                    {
                        If (\PRC0)
                        {
                            If (Not (LEqual (\PMS1, 0x00)))
                            {
                                Sleep (0x1E)
                            }

                            Notify (\_SB.PCI0.SATA.PRID.P_D0, 0x01)
                            Store (One, \PRC0)
                        }

                        If (\PRC1)
                        {
                            If (Not (LEqual (\SMS1, 0x00)))
                            {
                                Sleep (0x1E)
                            }

                            Notify (\_SB.PCI0.SATA.SECD.S_D0, 0x01)
                            Store (One, \PRC1)
                        }

                        If (\PRC2)
                        {
                            If (Not (LEqual (\PSS1, 0x00)))
                            {
                                Sleep (0x1E)
                            }

                            Notify (\_SB.PCI0.SATA.PRID.P_D1, 0x01)
                            Store (One, \PRC2)
                        }

                        If (\PRC3)
                        {
                            If (Not (LEqual (\SSS1, 0x00)))
                            {
                                Sleep (0x1E)
                            }

                            Notify (\_SB.PCI0.SATA.SECD.S_D1, 0x01)
                            Store (One, \PRC3)
                        }
                    }
                }
            }

            Device (LPC0)
            {
                Name (_ADR, 0x00140003)
                Device (PMIO)
                {
                    Name (_HID, EisaId ("PNP0C02"))
                    Name (_UID, 0x03)
                    Method (_CRS, 0, Serialized)
                    {
                        Name (BUF0, ResourceTemplate ()
                        {
                            IO (Decode16,
                                0x4100,             // Range Minimum
                                0x4100,             // Range Maximum
                                0x01,               // Alignment
                                0x20,               // Length
                                )
                            IO (Decode16,
                                0x0228,             // Range Minimum
                                0x0228,             // Range Maximum
                                0x01,               // Alignment
                                0x08,               // Length
                                )
                            IO (Decode16,
                                0x040B,             // Range Minimum
                                0x040B,             // Range Maximum
                                0x01,               // Alignment
                                0x01,               // Length
                                )
                            IO (Decode16,
                                0x04D6,             // Range Minimum
                                0x04D6,             // Range Maximum
                                0x01,               // Alignment
                                0x01,               // Length
                                )
                            IO (Decode16,
                                0x0C00,             // Range Minimum
                                0x0C00,             // Range Maximum
                                0x01,               // Alignment
                                0x02,               // Length
                                )
                            IO (Decode16,
                                0x0C14,             // Range Minimum
                                0x0C14,             // Range Maximum
                                0x01,               // Alignment
                                0x01,               // Length
                                )
                            IO (Decode16,
                                0x0C50,             // Range Minimum
                                0x0C50,             // Range Maximum
                                0x01,               // Alignment
                                0x03,               // Length
                                )
                            IO (Decode16,
                                0x0C6C,             // Range Minimum
                                0x0C6C,             // Range Maximum
                                0x01,               // Alignment
                                0x02,               // Length
                                )
                            IO (Decode16,
                                0x0C6F,             // Range Minimum
                                0x0C6F,             // Range Maximum
                                0x01,               // Alignment
                                0x01,               // Length
                                )
                            IO (Decode16,
                                0x0CD0,             // Range Minimum
                                0x0CD0,             // Range Maximum
                                0x01,               // Alignment
                                0x02,               // Length
                                )
                            IO (Decode16,
                                0x0CD2,             // Range Minimum
                                0x0CD2,             // Range Maximum
                                0x01,               // Alignment
                                0x02,               // Length
                                )
                            IO (Decode16,
                                0x0CD4,             // Range Minimum
                                0x0CD4,             // Range Maximum
                                0x01,               // Alignment
                                0x0C,               // Length
                                )
                            IO (Decode16,
                                0x4000,             // Range Minimum
                                0x4000,             // Range Maximum
                                0x01,               // Alignment
                                0xFF,               // Length
                                )
                            IO (Decode16,
                                0x4210,             // Range Minimum
                                0x4210,             // Range Maximum
                                0x01,               // Alignment
                                0x08,               // Length
                                )
                            IO (Decode16,
                                0x0B10,             // Range Minimum
                                0x0B10,             // Range Maximum
                                0x01,               // Alignment
                                0x10,               // Length
                                )
                            DWordMemory (ResourceProducer, PosDecode, MinFixed, MaxFixed, Cacheable, ReadWrite,
                                0x00000000,         // Granularity
                                0xE0000000,         // Range Minimum
                                0xE0000000,         // Range Maximum
                                0x00000000,         // Translation Offset
                                0x00000001,         // Length
                                ,, _Y01, AddressRangeMemory, TypeStatic)
                            DWordMemory (ResourceProducer, PosDecode, MinFixed, MaxFixed, Cacheable, ReadWrite,
                                0x00000000,         // Granularity
                                0xFEE00400,         // Range Minimum
                                0xFEE00FFF,         // Range Maximum
                                0x00000000,         // Translation Offset
                                0x00000C00,         // Length
                                ,, , AddressRangeMemory, TypeStatic)
                        })
                        CreateDWordField (BUF0, \_SB.PCI0.LPC0.PMIO._CRS._Y01._MIN, BARX)
                        CreateDWordField (BUF0, \_SB.PCI0.LPC0.PMIO._CRS._Y01._LEN, GALN)
                        CreateDWordField (BUF0, \_SB.PCI0.LPC0.PMIO._CRS._Y01._MAX, GAMX)
                        Store (0x1000, GALN)
                        Store (\_SB.PCI0.MMIO, Local0)
                        And (Local0, 0xFFFFFFF0, BARX)
                        Add (Local0, GALN, GAMX)
                        Subtract (GAMX, 0x01, GAMX)
                        Return (BUF0)
                    }
                }

                OperationRegion (PIRQ, SystemIO, 0x0C00, 0x02)
                Field (PIRQ, ByteAcc, NoLock, Preserve)
                {
                    PIID,   8, 
                    PIDA,   8
                }

                Name (IPRS, ResourceTemplate ()
                {
                    IRQ (Level, ActiveLow, Shared, )
                        {3,4,5,6,7,10,11}
                })
                IndexField (PIID, PIDA, ByteAcc, NoLock, Preserve)
                {
                    PIRA,   8, 
                    PIRB,   8, 
                    PIRC,   8, 
                    PIRD,   8, 
                    PIRS,   8, 
                            Offset (0x09), 
                    PIRE,   8, 
                    PIRF,   8, 
                    PIR0,   8, 
                    PIR1,   8
                }

                Method (DSPI, 0, NotSerialized)
                {
                    Store (0x00, PIRA)
                    Store (0x00, PIRB)
                    Store (0x00, PIRC)
                    Store (0x00, PIRD)
                    Store (0x00, PIRE)
                    Store (0x00, PIRF)
                    Store (0x00, PIR0)
                    Store (0x00, PIR1)
                }

                Device (LNKA)
                {
                    Name (_HID, EisaId ("PNP0C0F"))
                    Name (_UID, 0x01)
                    Method (_STA, 0, NotSerialized)
                    {
                        If (PIRA)
                        {
                            Return (0x0B)
                        }
                        Else
                        {
                            Return (0x09)
                        }
                    }

                    Method (_PRS, 0, NotSerialized)
                    {
                        Return (IPRS)
                    }

                    Method (_DIS, 0, NotSerialized)
                    {
                        Store (0x00, PIRA)
                    }

                    Method (_CRS, 0, NotSerialized)
                    {
                        Store (IPRS, Local0)
                        CreateWordField (Local0, 0x01, IRQ0)
                        ShiftLeft (0x01, PIRA, IRQ0)
                        Return (Local0)
                    }

                    Method (_SRS, 1, NotSerialized)
                    {
                        CreateWordField (Arg0, 0x01, IRQ0)
                        FindSetRightBit (IRQ0, Local0)
                        Decrement (Local0)
                        Store (Local0, PIRA)
                    }
                }

                Device (LNKB)
                {
                    Name (_HID, EisaId ("PNP0C0F"))
                    Name (_UID, 0x02)
                    Method (_STA, 0, NotSerialized)
                    {
                        If (PIRB)
                        {
                            Return (0x0B)
                        }
                        Else
                        {
                            Return (0x09)
                        }
                    }

                    Method (_PRS, 0, NotSerialized)
                    {
                        Return (IPRS)
                    }

                    Method (_DIS, 0, NotSerialized)
                    {
                        Store (0x00, PIRB)
                    }

                    Method (_CRS, 0, NotSerialized)
                    {
                        Store (IPRS, Local0)
                        CreateWordField (Local0, 0x01, IRQ0)
                        ShiftLeft (0x01, PIRB, IRQ0)
                        Return (Local0)
                    }

                    Method (_SRS, 1, NotSerialized)
                    {
                        CreateWordField (Arg0, 0x01, IRQ0)
                        FindSetRightBit (IRQ0, Local0)
                        Decrement (Local0)
                        Store (Local0, PIRB)
                    }
                }

                Device (LNKC)
                {
                    Name (_HID, EisaId ("PNP0C0F"))
                    Name (_UID, 0x03)
                    Method (_STA, 0, NotSerialized)
                    {
                        If (PIRC)
                        {
                            Return (0x0B)
                        }
                        Else
                        {
                            Return (0x09)
                        }
                    }

                    Method (_PRS, 0, NotSerialized)
                    {
                        Return (IPRS)
                    }

                    Method (_DIS, 0, NotSerialized)
                    {
                        Store (0x00, PIRC)
                    }

                    Method (_CRS, 0, NotSerialized)
                    {
                        Store (IPRS, Local0)
                        CreateWordField (Local0, 0x01, IRQ0)
                        ShiftLeft (0x01, PIRC, IRQ0)
                        Return (Local0)
                    }

                    Method (_SRS, 1, NotSerialized)
                    {
                        CreateWordField (Arg0, 0x01, IRQ0)
                        FindSetRightBit (IRQ0, Local0)
                        Decrement (Local0)
                        Store (Local0, PIRC)
                    }
                }

                Device (LNKD)
                {
                    Name (_HID, EisaId ("PNP0C0F"))
                    Name (_UID, 0x04)
                    Method (_STA, 0, NotSerialized)
                    {
                        If (PIRD)
                        {
                            Return (0x0B)
                        }
                        Else
                        {
                            Return (0x09)
                        }
                    }

                    Method (_PRS, 0, NotSerialized)
                    {
                        Return (IPRS)
                    }

                    Method (_DIS, 0, NotSerialized)
                    {
                        Store (0x00, PIRD)
                    }

                    Method (_CRS, 0, NotSerialized)
                    {
                        Store (IPRS, Local0)
                        CreateWordField (Local0, 0x01, IRQ0)
                        ShiftLeft (0x01, PIRD, IRQ0)
                        Return (Local0)
                    }

                    Method (_SRS, 1, NotSerialized)
                    {
                        CreateWordField (Arg0, 0x01, IRQ0)
                        FindSetRightBit (IRQ0, Local0)
                        Decrement (Local0)
                        Store (Local0, PIRD)
                    }
                }

                Device (LNKE)
                {
                    Name (_HID, EisaId ("PNP0C0F"))
                    Name (_UID, 0x05)
                    Method (_STA, 0, NotSerialized)
                    {
                        If (PIRE)
                        {
                            Return (0x0B)
                        }
                        Else
                        {
                            Return (0x09)
                        }
                    }

                    Method (_PRS, 0, NotSerialized)
                    {
                        Return (IPRS)
                    }

                    Method (_DIS, 0, NotSerialized)
                    {
                        Store (0x00, PIRE)
                    }

                    Method (_CRS, 0, NotSerialized)
                    {
                        Store (IPRS, Local0)
                        CreateWordField (Local0, 0x01, IRQ0)
                        ShiftLeft (0x01, PIRE, IRQ0)
                        Return (Local0)
                    }

                    Method (_SRS, 1, NotSerialized)
                    {
                        CreateWordField (Arg0, 0x01, IRQ0)
                        FindSetRightBit (IRQ0, Local0)
                        Decrement (Local0)
                        Store (Local0, PIRE)
                    }
                }

                Device (LNKF)
                {
                    Name (_HID, EisaId ("PNP0C0F"))
                    Name (_UID, 0x06)
                    Method (_STA, 0, NotSerialized)
                    {
                        If (PIRF)
                        {
                            Return (0x0B)
                        }
                        Else
                        {
                            Return (0x09)
                        }
                    }

                    Method (_PRS, 0, NotSerialized)
                    {
                        Return (IPRS)
                    }

                    Method (_DIS, 0, NotSerialized)
                    {
                        Store (0x00, PIRF)
                    }

                    Method (_CRS, 0, NotSerialized)
                    {
                        Store (IPRS, Local0)
                        CreateWordField (Local0, 0x01, IRQ0)
                        ShiftLeft (0x01, PIRF, IRQ0)
                        Return (Local0)
                    }

                    Method (_SRS, 1, NotSerialized)
                    {
                        CreateWordField (Arg0, 0x01, IRQ0)
                        FindSetRightBit (IRQ0, Local0)
                        Decrement (Local0)
                        Store (Local0, PIRF)
                    }
                }

                Device (LNK0)
                {
                    Name (_HID, EisaId ("PNP0C0F"))
                    Name (_UID, 0x07)
                    Method (_STA, 0, NotSerialized)
                    {
                        If (PIR0)
                        {
                            Return (0x0B)
                        }
                        Else
                        {
                            Return (0x09)
                        }
                    }

                    Method (_PRS, 0, NotSerialized)
                    {
                        Return (IPRS)
                    }

                    Method (_DIS, 0, NotSerialized)
                    {
                        Store (0x00, PIR0)
                    }

                    Method (_CRS, 0, NotSerialized)
                    {
                        Store (IPRS, Local0)
                        CreateWordField (Local0, 0x01, IRQ0)
                        ShiftLeft (0x01, PIR0, IRQ0)
                        Return (Local0)
                    }

                    Method (_SRS, 1, NotSerialized)
                    {
                        CreateWordField (Arg0, 0x01, IRQ0)
                        FindSetRightBit (IRQ0, Local0)
                        Decrement (Local0)
                        Store (Local0, PIR0)
                    }
                }

                Device (LNK1)
                {
                    Name (_HID, EisaId ("PNP0C0F"))
                    Name (_UID, 0x08)
                    Method (_STA, 0, NotSerialized)
                    {
                        If (PIR1)
                        {
                            Return (0x0B)
                        }
                        Else
                        {
                            Return (0x09)
                        }
                    }

                    Method (_PRS, 0, NotSerialized)
                    {
                        Return (IPRS)
                    }

                    Method (_DIS, 0, NotSerialized)
                    {
                        Store (0x00, PIR1)
                    }

                    Method (_CRS, 0, NotSerialized)
                    {
                        Store (IPRS, Local0)
                        CreateWordField (Local0, 0x01, IRQ0)
                        ShiftLeft (0x01, PIR1, IRQ0)
                        Return (Local0)
                    }

                    Method (_SRS, 1, NotSerialized)
                    {
                        CreateWordField (Arg0, 0x01, IRQ0)
                        FindSetRightBit (IRQ0, Local0)
                        Decrement (Local0)
                        Store (Local0, PIR1)
                    }
                }

                Device (PIC)
                {
                    Name (_HID, EisaId ("PNP0000"))
                    Name (_CRS, ResourceTemplate ()
                    {
                        IO (Decode16,
                            0x0020,             // Range Minimum
                            0x0020,             // Range Maximum
                            0x01,               // Alignment
                            0x02,               // Length
                            )
                        IO (Decode16,
                            0x00A0,             // Range Minimum
                            0x00A0,             // Range Maximum
                            0x01,               // Alignment
                            0x02,               // Length
                            )
                        IRQNoFlags ()
                            {2}
                    })
                }

                Device (DMA1)
                {
                    Name (_HID, EisaId ("PNP0200"))
                    Name (_CRS, ResourceTemplate ()
                    {
                        DMA (Compatibility, BusMaster, Transfer8, )
                            {4}
                        IO (Decode16,
                            0x0000,             // Range Minimum
                            0x0000,             // Range Maximum
                            0x01,               // Alignment
                            0x10,               // Length
                            )
                        IO (Decode16,
                            0x0080,             // Range Minimum
                            0x0080,             // Range Maximum
                            0x01,               // Alignment
                            0x11,               // Length
                            )
                        IO (Decode16,
                            0x0094,             // Range Minimum
                            0x0094,             // Range Maximum
                            0x01,               // Alignment
                            0x0C,               // Length
                            )
                        IO (Decode16,
                            0x00C0,             // Range Minimum
                            0x00C0,             // Range Maximum
                            0x01,               // Alignment
                            0x20,               // Length
                            )
                    })
                }

                Device (TMR)
                {
                    Name (_HID, EisaId ("PNP0100"))
                    Name (ATT5, ResourceTemplate ()
                    {
                        IO (Decode16,
                            0x0040,             // Range Minimum
                            0x0040,             // Range Maximum
                            0x00,               // Alignment
                            0x04,               // Length
                            )
                        IRQNoFlags ()
                            {0}
                    })
                    Name (ATT6, ResourceTemplate ()
                    {
                        IO (Decode16,
                            0x0040,             // Range Minimum
                            0x0040,             // Range Maximum
                            0x00,               // Alignment
                            0x04,               // Length
                            )
                    })
                    Method (_CRS, 0, NotSerialized)
                    {
                        If (LGreaterEqual (OSFX, 0x03))
                        {
                            If (HPTF)
                            {
                                Return (ATT6)
                            }
                            Else
                            {
                                Return (ATT5)
                            }
                        }
                        Else
                        {
                            Return (ATT5)
                        }
                    }
                }

                Device (HPET)
                {
                    Name (_HID, EisaId ("PNP0103"))
                    Name (ATT3, ResourceTemplate ()
                    {
                        IRQNoFlags ()
                            {0}
                        IRQNoFlags ()
                            {8}
                        Memory32Fixed (ReadWrite,
                            0xFED00000,         // Address Base
                            0x00000400,         // Address Length
                            )
                    })
                    Name (ATT4, ResourceTemplate ()
                    {
                    })
                    Method (_STA, 0, NotSerialized)
                    {
                        If (LGreaterEqual (OSFX, 0x03))
                        {
                            If (HPTF)
                            {
                                Return (0x0F)
                            }
                            Else
                            {
                                Return (0x00)
                            }
                        }
                        Else
                        {
                            Return (0x00)
                        }
                    }

                    Method (_CRS, 0, NotSerialized)
                    {
                        If (LGreaterEqual (OSFX, 0x03))
                        {
                            If (HPTF)
                            {
                                Return (ATT3)
                            }
                            Else
                            {
                                Return (ATT4)
                            }
                        }
                        Else
                        {
                            Return (ATT4)
                        }
                    }
                }

                Device (RTC)
                {
                    Name (_HID, EisaId ("PNP0B00"))
                    Name (ATT0, ResourceTemplate ()
                    {
                        IO (Decode16,
                            0x0070,             // Range Minimum
                            0x0070,             // Range Maximum
                            0x00,               // Alignment
                            0x04,               // Length
                            )
                        IRQNoFlags ()
                            {8}
                    })
                    Name (ATT1, ResourceTemplate ()
                    {
                        IO (Decode16,
                            0x0070,             // Range Minimum
                            0x0070,             // Range Maximum
                            0x00,               // Alignment
                            0x04,               // Length
                            )
                    })
                    Method (_CRS, 0, NotSerialized)
                    {
                        If (LGreaterEqual (OSFX, 0x03))
                        {
                            If (HPTF)
                            {
                                Return (ATT1)
                            }
                            Else
                            {
                                Return (ATT0)
                            }
                        }
                        Else
                        {
                            Return (ATT0)
                        }
                    }
                }

                Device (SPKR)
                {
                    Name (_HID, EisaId ("PNP0800"))
                    Name (_CRS, ResourceTemplate ()
                    {
                        IO (Decode16,
                            0x0061,             // Range Minimum
                            0x0061,             // Range Maximum
                            0x01,               // Alignment
                            0x01,               // Length
                            )
                    })
                }

                Device (COPR)
                {
                    Name (_HID, EisaId ("PNP0C04"))
                    Name (_CRS, ResourceTemplate ()
                    {
                        IO (Decode16,
                            0x00F0,             // Range Minimum
                            0x00F0,             // Range Maximum
                            0x01,               // Alignment
                            0x10,               // Length
                            )
                        IRQNoFlags ()
                            {13}
                    })
                }
            }

            Device (P2P)
            {
                Name (_ADR, 0x00140004)
                Method (_S3D, 0, NotSerialized)
                {
                    If (LEqual (OSFL, 0x02))
                    {
                        Return (0x02)
                    }
                    Else
                    {
                        Return (0x03)
                    }
                }

                Method (_PRW, 0, NotSerialized)
                {
                    Return (Package (0x02)
                    {
                        0x04, 
                        0x05
                    })
                }

                Name (PICM, Package (0x0C)
                {
                    Package (0x04)
                    {
                        0x0006FFFF, 
                        0x00, 
                        \_SB.PCI0.LPC0.LNK1, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0x0006FFFF, 
                        0x01, 
                        \_SB.PCI0.LPC0.LNKE, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0x0006FFFF, 
                        0x02, 
                        \_SB.PCI0.LPC0.LNKF, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0x0006FFFF, 
                        0x03, 
                        \_SB.PCI0.LPC0.LNK0, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0x0005FFFF, 
                        0x00, 
                        \_SB.PCI0.LPC0.LNK0, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0x0005FFFF, 
                        0x01, 
                        \_SB.PCI0.LPC0.LNK1, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0x0005FFFF, 
                        0x02, 
                        \_SB.PCI0.LPC0.LNKE, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0x0005FFFF, 
                        0x03, 
                        \_SB.PCI0.LPC0.LNKF, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0x0004FFFF, 
                        0x00, 
                        \_SB.PCI0.LPC0.LNKF, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0x0004FFFF, 
                        0x01, 
                        \_SB.PCI0.LPC0.LNK0, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0x0004FFFF, 
                        0x02, 
                        \_SB.PCI0.LPC0.LNK1, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0x0004FFFF, 
                        0x03, 
                        \_SB.PCI0.LPC0.LNKE, 
                        0x00
                    }
                })
                Name (APIC, Package (0x0C)
                {
                    Package (0x04)
                    {
                        0x0006FFFF, 
                        0x00, 
                        0x00, 
                        0x17
                    }, 

                    Package (0x04)
                    {
                        0x0006FFFF, 
                        0x01, 
                        0x00, 
                        0x14
                    }, 

                    Package (0x04)
                    {
                        0x0006FFFF, 
                        0x02, 
                        0x00, 
                        0x15
                    }, 

                    Package (0x04)
                    {
                        0x0006FFFF, 
                        0x03, 
                        0x00, 
                        0x16
                    }, 

                    Package (0x04)
                    {
                        0x0005FFFF, 
                        0x00, 
                        0x00, 
                        0x16
                    }, 

                    Package (0x04)
                    {
                        0x0005FFFF, 
                        0x01, 
                        0x00, 
                        0x17
                    }, 

                    Package (0x04)
                    {
                        0x0005FFFF, 
                        0x02, 
                        0x00, 
                        0x14
                    }, 

                    Package (0x04)
                    {
                        0x0005FFFF, 
                        0x03, 
                        0x00, 
                        0x15
                    }, 

                    Package (0x04)
                    {
                        0x0004FFFF, 
                        0x00, 
                        0x00, 
                        0x15
                    }, 

                    Package (0x04)
                    {
                        0x0004FFFF, 
                        0x01, 
                        0x00, 
                        0x16
                    }, 

                    Package (0x04)
                    {
                        0x0004FFFF, 
                        0x02, 
                        0x00, 
                        0x17
                    }, 

                    Package (0x04)
                    {
                        0x0004FFFF, 
                        0x03, 
                        0x00, 
                        0x14
                    }
                })
                Method (_PRT, 0, NotSerialized)
                {
                    If (LNot (PICF))
                    {
                        Return (PICM)
                    }
                    Else
                    {
                        Return (APIC)
                    }
                }
            }

            Device (IDE)
            {
                Name (_ADR, 0x00140001)
                Name (UDMT, Package (0x08)
                {
                    0x78, 
                    0x5A, 
                    0x3C, 
                    0x2D, 
                    0x1E, 
                    0x14, 
                    0x0F, 
                    0x00
                })
                Name (PIOT, Package (0x06)
                {
                    0x0258, 
                    0x0186, 
                    0x010E, 
                    0xB4, 
                    0x78, 
                    0x00
                })
                Name (PITR, Package (0x06)
                {
                    0x99, 
                    0x47, 
                    0x34, 
                    0x22, 
                    0x20, 
                    0x99
                })
                Name (MDMT, Package (0x04)
                {
                    0x01E0, 
                    0x96, 
                    0x78, 
                    0x00
                })
                Name (MDTR, Package (0x04)
                {
                    0x77, 
                    0x21, 
                    0x20, 
                    0xFF
                })
                OperationRegion (IDE, PCI_Config, 0x40, 0x20)
                Field (IDE, AnyAcc, NoLock, Preserve)
                {
                    PPIT,   16, 
                    SPIT,   16, 
                    PMDT,   16, 
                    SMDT,   16, 
                    PPIC,   8, 
                    SPIC,   8, 
                    PPIM,   8, 
                    SPIM,   8, 
                            Offset (0x14), 
                    PUDC,   2, 
                    SUDC,   2, 
                            Offset (0x16), 
                    PUDM,   8, 
                    SUDM,   8
                }

                Method (GETT, 1, NotSerialized)
                {
                    Store (And (Arg0, 0x0F), Local0)
                    Store (ShiftRight (Arg0, 0x04), Local1)
                    Return (Multiply (0x1E, Add (Add (Local0, 0x01), Add (Local1, 
                        0x01))))
                }

                Method (GTM, 1, Serialized)
                {
                    CreateByteField (Arg0, 0x00, PIT1)
                    CreateByteField (Arg0, 0x01, PIT0)
                    CreateByteField (Arg0, 0x02, MDT1)
                    CreateByteField (Arg0, 0x03, MDT0)
                    CreateByteField (Arg0, 0x04, PICX)
                    CreateByteField (Arg0, 0x05, UDCX)
                    CreateByteField (Arg0, 0x06, UDMX)
                    Name (BUF, Buffer (0x14)
                    {
                        /* 0000 */    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
                        /* 0008 */    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
                        /* 0010 */    0x00, 0x00, 0x00, 0x00
                    })
                    CreateDWordField (BUF, 0x00, PIO0)
                    CreateDWordField (BUF, 0x04, DMA0)
                    CreateDWordField (BUF, 0x08, PIO1)
                    CreateDWordField (BUF, 0x0C, DMA1)
                    CreateDWordField (BUF, 0x10, FLAG)
                    If (And (PICX, 0x01))
                    {
                        Return (BUF)
                    }

                    Store (GETT (PIT0), PIO0)
                    Store (GETT (PIT1), PIO1)
                    If (And (UDCX, 0x01))
                    {
                        Or (FLAG, 0x01, FLAG)
                        Store (DerefOf (Index (^UDMT, And (UDMX, 0x0F))), DMA0)
                    }
                    Else
                    {
                        Store (GETT (MDT0), DMA0)
                    }

                    If (And (UDCX, 0x02))
                    {
                        Or (FLAG, 0x04, FLAG)
                        Store (DerefOf (Index (^UDMT, ShiftRight (UDMX, 0x04))), DMA1)
                    }
                    Else
                    {
                        Store (GETT (MDT1), DMA1)
                    }

                    Or (FLAG, 0x1A, FLAG)
                    Return (BUF)
                }

                Method (STM, 3, Serialized)
                {
                    CreateDWordField (Arg0, 0x00, PIO0)
                    CreateDWordField (Arg0, 0x04, DMA0)
                    CreateDWordField (Arg0, 0x08, PIO1)
                    CreateDWordField (Arg0, 0x0C, DMA1)
                    CreateDWordField (Arg0, 0x10, FLAG)
                    Name (BUF, Buffer (0x07)
                    {
                        0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0x00
                    })
                    CreateByteField (BUF, 0x00, PIT1)
                    CreateByteField (BUF, 0x01, PIT0)
                    CreateByteField (BUF, 0x02, MDT1)
                    CreateByteField (BUF, 0x03, MDT0)
                    CreateByteField (BUF, 0x04, PIMX)
                    CreateByteField (BUF, 0x05, UDCX)
                    CreateByteField (BUF, 0x06, UDMX)
                    Store (Match (^PIOT, MLE, PIO0, MTR, 0x00, 0x00), Local0)
                    Divide (Local0, 0x05, Local0)
                    Store (Match (^PIOT, MLE, PIO1, MTR, 0x00, 0x00), Local1)
                    Divide (Local1, 0x05, Local1)
                    Store (Or (ShiftLeft (Local1, 0x04), Local0), PIMX)
                    Store (DerefOf (Index (^PITR, Local0)), PIT0)
                    Store (DerefOf (Index (^PITR, Local1)), PIT1)
                    If (And (FLAG, 0x01))
                    {
                        Store (Match (^UDMT, MLE, DMA0, MTR, 0x00, 0x00), Local0)
                        Divide (Local0, 0x07, Local0)
                        Or (UDMX, Local0, UDMX)
                        Or (UDCX, 0x01, UDCX)
                    }
                    Else
                    {
                        If (LNotEqual (DMA0, 0xFFFFFFFF))
                        {
                            Store (Match (^MDMT, MLE, DMA0, MTR, 0x00, 0x00), Local0)
                            Store (DerefOf (Index (^MDTR, Local0)), MDT0)
                        }
                    }

                    If (And (FLAG, 0x04))
                    {
                        Store (Match (^UDMT, MLE, DMA1, MTR, 0x00, 0x00), Local0)
                        Divide (Local0, 0x07, Local0)
                        Or (UDMX, ShiftLeft (Local0, 0x04), UDMX)
                        Or (UDCX, 0x02, UDCX)
                    }
                    Else
                    {
                        If (LNotEqual (DMA1, 0xFFFFFFFF))
                        {
                            Store (Match (^MDMT, MLE, DMA1, MTR, 0x00, 0x00), Local0)
                            Store (DerefOf (Index (^MDTR, Local0)), MDT1)
                        }
                    }

                    Return (BUF)
                }

                Method (GTF, 2, Serialized)
                {
                    CreateByteField (Arg1, 0x00, MDT1)
                    CreateByteField (Arg1, 0x01, MDT0)
                    CreateByteField (Arg1, 0x02, PIMX)
                    CreateByteField (Arg1, 0x03, UDCX)
                    CreateByteField (Arg1, 0x04, UDMX)
                    If (LEqual (Arg0, 0xA0))
                    {
                        Store (And (PIMX, 0x0F), Local0)
                        Store (MDT0, Local1)
                        And (UDCX, 0x01, Local2)
                        Store (And (UDMX, 0x0F), Local3)
                    }
                    Else
                    {
                        Store (ShiftRight (PIMX, 0x04), Local0)
                        Store (MDT1, Local1)
                        And (UDCX, 0x02, Local2)
                        Store (ShiftRight (UDMX, 0x04), Local3)
                    }

                    Name (BUF, Buffer (0x0E)
                    {
                        /* 0000 */    0x03, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xEF, 0x03, 
                        /* 0008 */    0x00, 0x00, 0x00, 0x00, 0xFF, 0xEF
                    })
                    CreateByteField (BUF, 0x01, PMOD)
                    CreateByteField (BUF, 0x08, DMOD)
                    CreateByteField (BUF, 0x05, CMDA)
                    CreateByteField (BUF, 0x0C, CMDB)
                    Store (Arg0, CMDA)
                    Store (Arg0, CMDB)
                    Or (Local0, 0x08, PMOD)
                    If (Local2)
                    {
                        Or (Local3, 0x40, DMOD)
                    }
                    Else
                    {
                        Store (Match (^MDMT, MLE, GETT (Local1), MTR, 0x00, 0x00), Local4)
                        If (LLess (Local4, 0x03))
                        {
                            Or (0x20, Local4, DMOD)
                        }
                    }

                    Return (BUF)
                }

                Device (PRID)
                {
                    Name (_ADR, 0x00)
                    Method (_GTM, 0, Serialized)
                    {
                        Name (BUF, Buffer (0x07)
                        {
                            0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0x00
                        })
                        CreateWordField (BUF, 0x00, VPIT)
                        CreateWordField (BUF, 0x02, VMDT)
                        CreateByteField (BUF, 0x04, VPIC)
                        CreateByteField (BUF, 0x05, VUDC)
                        CreateByteField (BUF, 0x06, VUDM)
                        Store (^^PPIT, VPIT)
                        Store (^^PMDT, VMDT)
                        Store (^^PPIC, VPIC)
                        Store (^^PUDC, VUDC)
                        Store (^^PUDM, VUDM)
                        Return (GTM (BUF))
                    }

                    Method (_STM, 3, Serialized)
                    {
                        Name (BUF, Buffer (0x07)
                        {
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
                        })
                        CreateWordField (BUF, 0x00, VPIT)
                        CreateWordField (BUF, 0x02, VMDT)
                        CreateByteField (BUF, 0x04, VPIM)
                        CreateByteField (BUF, 0x05, VUDC)
                        CreateByteField (BUF, 0x06, VUDM)
                        Store (STM (Arg0, Arg1, Arg2), BUF)
                        Store (VPIT, ^^PPIT)
                        Store (VMDT, ^^PMDT)
                        Store (VPIM, ^^PPIM)
                        Store (VUDC, ^^PUDC)
                        Store (VUDM, ^^PUDM)
                    }

                    Device (P_D0)
                    {
                        Name (_ADR, 0x00)
                        Method (_GTF, 0, Serialized)
                        {
                            Name (BUF, Buffer (0x05)
                            {
                                0x00, 0x00, 0x00, 0x00, 0x00
                            })
                            CreateWordField (BUF, 0x00, VMDT)
                            CreateByteField (BUF, 0x02, VPIM)
                            CreateByteField (BUF, 0x03, VUDC)
                            CreateByteField (BUF, 0x04, VUDM)
                            Store (^^^PMDT, VMDT)
                            Store (^^^PPIM, VPIM)
                            Store (^^^PUDC, VUDC)
                            Store (^^^PUDM, VUDM)
                            Return (GTF (0xA0, BUF))
                        }
                    }

                    Device (P_D1)
                    {
                        Name (_ADR, 0x01)
                        Method (_GTF, 0, Serialized)
                        {
                            Name (BUF, Buffer (0x05)
                            {
                                0x00, 0x00, 0x00, 0x00, 0x00
                            })
                            CreateWordField (BUF, 0x00, VMDT)
                            CreateByteField (BUF, 0x02, VPIM)
                            CreateByteField (BUF, 0x03, VUDC)
                            CreateByteField (BUF, 0x04, VUDM)
                            Store (^^^PMDT, VMDT)
                            Store (^^^PPIM, VPIM)
                            Store (^^^PUDC, VUDC)
                            Store (^^^PUDM, VUDM)
                            Return (GTF (0xB0, BUF))
                        }
                    }
                }

                Device (SECD)
                {
                    Name (_ADR, 0x01)
                    Method (_GTM, 0, Serialized)
                    {
                        Name (BUF, Buffer (0x07)
                        {
                            0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0x00
                        })
                        CreateWordField (BUF, 0x00, VPIT)
                        CreateWordField (BUF, 0x02, VMDT)
                        CreateByteField (BUF, 0x04, VPIC)
                        CreateByteField (BUF, 0x05, VUDC)
                        CreateByteField (BUF, 0x06, VUDM)
                        Store (^^SPIT, VPIT)
                        Store (^^SMDT, VMDT)
                        Store (^^SPIC, VPIC)
                        Store (^^SUDC, VUDC)
                        Store (^^SUDM, VUDM)
                        Return (GTM (BUF))
                    }

                    Method (_STM, 3, Serialized)
                    {
                        Name (BUF, Buffer (0x07)
                        {
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
                        })
                        CreateWordField (BUF, 0x00, VPIT)
                        CreateWordField (BUF, 0x02, VMDT)
                        CreateByteField (BUF, 0x04, VPIM)
                        CreateByteField (BUF, 0x05, VUDC)
                        CreateByteField (BUF, 0x06, VUDM)
                        Store (STM (Arg0, Arg1, Arg2), BUF)
                        Store (VPIT, ^^SPIT)
                        Store (VMDT, ^^SMDT)
                        Store (VPIM, ^^SPIM)
                        Store (VUDC, ^^SUDC)
                        Store (VUDM, ^^SUDM)
                    }

                    Device (S_D0)
                    {
                        Name (_ADR, 0x00)
                        Method (_GTF, 0, Serialized)
                        {
                            Name (BUF, Buffer (0x05)
                            {
                                0x00, 0x00, 0x00, 0x00, 0x00
                            })
                            CreateWordField (BUF, 0x00, VMDT)
                            CreateByteField (BUF, 0x02, VPIM)
                            CreateByteField (BUF, 0x03, VUDC)
                            CreateByteField (BUF, 0x04, VUDM)
                            Store (^^^SMDT, VMDT)
                            Store (^^^SPIM, VPIM)
                            Store (^^^SUDC, VUDC)
                            Store (^^^SUDM, VUDM)
                            Return (GTF (0xA0, BUF))
                        }
                    }

                    Device (S_D1)
                    {
                        Name (_ADR, 0x01)
                        Method (_GTF, 0, Serialized)
                        {
                            Name (BUF, Buffer (0x05)
                            {
                                0x00, 0x00, 0x00, 0x00, 0x00
                            })
                            CreateWordField (BUF, 0x00, VMDT)
                            CreateByteField (BUF, 0x02, VPIM)
                            CreateByteField (BUF, 0x03, VUDC)
                            CreateByteField (BUF, 0x04, VUDM)
                            Store (^^^SMDT, VMDT)
                            Store (^^^SPIM, VPIM)
                            Store (^^^SUDC, VUDC)
                            Store (^^^SUDM, VUDM)
                            Return (GTF (0xB0, BUF))
                        }
                    }
                }
            }

            Device (PCE2)
            {
                Name (_ADR, 0x00020000)
                Method (_PRW, 0, NotSerialized)
                {
                    Return (Package (0x02)
                    {
                        0x18, 
                        0x04
                    })
                }

                Name (PICM, Package (0x04)
                {
                    Package (0x04)
                    {
                        0xFFFF, 
                        0x00, 
                        LNKC, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x01, 
                        LNKD, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x02, 
                        LNKA, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x03, 
                        LNKB, 
                        0x00
                    }
                })
                Name (APIC, Package (0x04)
                {
                    Package (0x04)
                    {
                        0xFFFF, 
                        0x00, 
                        0x00, 
                        0x12
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x01, 
                        0x00, 
                        0x13
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x02, 
                        0x00, 
                        0x10
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x03, 
                        0x00, 
                        0x11
                    }
                })
                Method (_PRT, 0, NotSerialized)
                {
                    If (LNot (PICF))
                    {
                        Return (PICM)
                    }
                    Else
                    {
                        Return (APIC)
                    }
                }
            }

            Device (PCE3)
            {
                Name (_ADR, 0x00030000)
                Method (_PRW, 0, NotSerialized)
                {
                    Return (Package (0x02)
                    {
                        0x18, 
                        0x04
                    })
                }

                Name (PICM, Package (0x04)
                {
                    Package (0x04)
                    {
                        0xFFFF, 
                        0x00, 
                        LNKD, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x01, 
                        LNKA, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x02, 
                        LNKB, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x03, 
                        LNKC, 
                        0x00
                    }
                })
                Name (APIC, Package (0x04)
                {
                    Package (0x04)
                    {
                        0xFFFF, 
                        0x00, 
                        0x00, 
                        0x13
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x01, 
                        0x00, 
                        0x10
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x02, 
                        0x00, 
                        0x11
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x03, 
                        0x00, 
                        0x12
                    }
                })
                Method (_PRT, 0, NotSerialized)
                {
                    If (LNot (PICF))
                    {
                        Return (PICM)
                    }
                    Else
                    {
                        Return (APIC)
                    }
                }
            }

            Device (PCE4)
            {
                Name (_ADR, 0x00040000)
                Method (_PRW, 0, NotSerialized)
                {
                    Return (Package (0x02)
                    {
                        0x18, 
                        0x04
                    })
                }

                Name (PICM, Package (0x04)
                {
                    Package (0x04)
                    {
                        0xFFFF, 
                        0x00, 
                        LNKA, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x01, 
                        LNKB, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x02, 
                        LNKC, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x03, 
                        LNKD, 
                        0x00
                    }
                })
                Name (APIC, Package (0x04)
                {
                    Package (0x04)
                    {
                        0xFFFF, 
                        0x00, 
                        0x00, 
                        0x10
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x01, 
                        0x00, 
                        0x11
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x02, 
                        0x00, 
                        0x12
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x03, 
                        0x00, 
                        0x13
                    }
                })
                Method (_PRT, 0, NotSerialized)
                {
                    If (LNot (PICF))
                    {
                        Return (PICM)
                    }
                    Else
                    {
                        Return (APIC)
                    }
                }
            }

            Device (PCE5)
            {
                Name (_ADR, 0x00050000)
                Method (_PRW, 0, NotSerialized)
                {
                    Return (Package (0x02)
                    {
                        0x18, 
                        0x04
                    })
                }

                Name (PICM, Package (0x04)
                {
                    Package (0x04)
                    {
                        0xFFFF, 
                        0x00, 
                        LNKB, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x01, 
                        LNKC, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x02, 
                        LNKD, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x03, 
                        LNKA, 
                        0x00
                    }
                })
                Name (APIC, Package (0x04)
                {
                    Package (0x04)
                    {
                        0xFFFF, 
                        0x00, 
                        0x00, 
                        0x11
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x01, 
                        0x00, 
                        0x12
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x02, 
                        0x00, 
                        0x13
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x03, 
                        0x00, 
                        0x10
                    }
                })
                Method (_PRT, 0, NotSerialized)
                {
                    If (LNot (PICF))
                    {
                        Return (PICM)
                    }
                    Else
                    {
                        Return (APIC)
                    }
                }
            }

            Device (PCE6)
            {
                Name (_ADR, 0x00060000)
                Method (_PRW, 0, NotSerialized)
                {
                    Return (Package (0x02)
                    {
                        0x18, 
                        0x04
                    })
                }

                Name (PICM, Package (0x04)
                {
                    Package (0x04)
                    {
                        0xFFFF, 
                        0x00, 
                        LNKC, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x01, 
                        LNKD, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x02, 
                        LNKA, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x03, 
                        LNKB, 
                        0x00
                    }
                })
                Name (APIC, Package (0x04)
                {
                    Package (0x04)
                    {
                        0xFFFF, 
                        0x00, 
                        0x00, 
                        0x12
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x01, 
                        0x00, 
                        0x13
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x02, 
                        0x00, 
                        0x10
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x03, 
                        0x00, 
                        0x11
                    }
                })
                Method (_PRT, 0, NotSerialized)
                {
                    If (LNot (PICF))
                    {
                        Return (PICM)
                    }
                    Else
                    {
                        Return (APIC)
                    }
                }
            }

            Device (PCE7)
            {
                Name (_ADR, 0x00070000)
                Method (_PRW, 0, NotSerialized)
                {
                    Return (Package (0x02)
                    {
                        0x18, 
                        0x04
                    })
                }

                Name (PICM, Package (0x04)
                {
                    Package (0x04)
                    {
                        0xFFFF, 
                        0x00, 
                        LNKD, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x01, 
                        LNKA, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x02, 
                        LNKB, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x03, 
                        LNKC, 
                        0x00
                    }
                })
                Name (APIC, Package (0x04)
                {
                    Package (0x04)
                    {
                        0xFFFF, 
                        0x00, 
                        0x00, 
                        0x13
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x01, 
                        0x00, 
                        0x10
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x02, 
                        0x00, 
                        0x11
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x03, 
                        0x00, 
                        0x12
                    }
                })
                Method (_PRT, 0, NotSerialized)
                {
                    If (LNot (PICF))
                    {
                        Return (PICM)
                    }
                    Else
                    {
                        Return (APIC)
                    }
                }
            }

            Device (PCE9)
            {
                Name (_ADR, 0x00090000)
                Method (_PRW, 0, NotSerialized)
                {
                    Return (Package (0x02)
                    {
                        0x18, 
                        0x04
                    })
                }

                Name (PICM, Package (0x04)
                {
                    Package (0x04)
                    {
                        0xFFFF, 
                        0x00, 
                        LNKB, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x01, 
                        LNKC, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x02, 
                        LNKD, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x03, 
                        LNKA, 
                        0x00
                    }
                })
                Name (APIC, Package (0x04)
                {
                    Package (0x04)
                    {
                        0xFFFF, 
                        0x00, 
                        0x00, 
                        0x11
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x01, 
                        0x00, 
                        0x12
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x02, 
                        0x00, 
                        0x13
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x03, 
                        0x00, 
                        0x10
                    }
                })
                Method (_PRT, 0, NotSerialized)
                {
                    If (LNot (PICF))
                    {
                        Return (PICM)
                    }
                    Else
                    {
                        Return (APIC)
                    }
                }
            }

            Device (PCEA)
            {
                Name (_ADR, 0x000A0000)
                Method (_PRW, 0, NotSerialized)
                {
                    Return (Package (0x02)
                    {
                        0x18, 
                        0x04
                    })
                }

                Name (PICM, Package (0x04)
                {
                    Package (0x04)
                    {
                        0xFFFF, 
                        0x00, 
                        LNKC, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x01, 
                        LNKD, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x02, 
                        LNKA, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x03, 
                        LNKB, 
                        0x00
                    }
                })
                Name (APIC, Package (0x04)
                {
                    Package (0x04)
                    {
                        0xFFFF, 
                        0x00, 
                        0x00, 
                        0x12
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x01, 
                        0x00, 
                        0x13
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x02, 
                        0x00, 
                        0x10
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x03, 
                        0x00, 
                        0x11
                    }
                })
                Method (_PRT, 0, NotSerialized)
                {
                    If (LNot (PICF))
                    {
                        Return (PICM)
                    }
                    Else
                    {
                        Return (APIC)
                    }
                }
            }

            Device (PCEB)
            {
                Name (_ADR, 0x000B0000)
                Method (_PRW, 0, NotSerialized)
                {
                    Return (Package (0x02)
                    {
                        0x18, 
                        0x04
                    })
                }

                Name (PICM, Package (0x04)
                {
                    Package (0x04)
                    {
                        0xFFFF, 
                        0x00, 
                        LNKD, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x01, 
                        LNKA, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x02, 
                        LNKB, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x03, 
                        LNKC, 
                        0x00
                    }
                })
                Name (APIC, Package (0x04)
                {
                    Package (0x04)
                    {
                        0xFFFF, 
                        0x00, 
                        0x00, 
                        0x13
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x01, 
                        0x00, 
                        0x10
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x02, 
                        0x00, 
                        0x11
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x03, 
                        0x00, 
                        0x12
                    }
                })
                Method (_PRT, 0, NotSerialized)
                {
                    If (LNot (PICF))
                    {
                        Return (PICM)
                    }
                    Else
                    {
                        Return (APIC)
                    }
                }
            }

            Device (PCEC)
            {
                Name (_ADR, 0x000C0000)
                Method (_PRW, 0, NotSerialized)
                {
                    Return (Package (0x02)
                    {
                        0x18, 
                        0x04
                    })
                }

                Name (PICM, Package (0x04)
                {
                    Package (0x04)
                    {
                        0xFFFF, 
                        0x00, 
                        LNKA, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x01, 
                        LNKB, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x02, 
                        LNKC, 
                        0x00
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x03, 
                        LNKD, 
                        0x00
                    }
                })
                Name (APIC, Package (0x04)
                {
                    Package (0x04)
                    {
                        0xFFFF, 
                        0x00, 
                        0x00, 
                        0x10
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x01, 
                        0x00, 
                        0x11
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x02, 
                        0x00, 
                        0x12
                    }, 

                    Package (0x04)
                    {
                        0xFFFF, 
                        0x03, 
                        0x00, 
                        0x13
                    }
                })
                Method (_PRT, 0, NotSerialized)
                {
                    If (LNot (PICF))
                    {
                        Return (PICM)
                    }
                    Else
                    {
                        Return (APIC)
                    }
                }
            }

            Scope (\)
            {
                Method (DISD, 1, NotSerialized)
                {
                }

                Method (CKIO, 2, NotSerialized)
                {
                }

                Method (SLDM, 2, NotSerialized)
                {
                }
            }

            Scope (\)
            {
                OperationRegion (\SCPP, SystemIO, 0xB0, 0x01)
                Field (\SCPP, ByteAcc, NoLock, Preserve)
                {
                    SMIP,   8
                }
            }

            Method (\_SB.PCI0._INI, 0, NotSerialized)
            {
                If (STRC (_OS_, "Microsoft Windows"))
                {
                    Store (0x56, SMIP)
                }
                Else
                {
                    If (STRC (_OS_, "Microsoft Windows NT"))
                    {
                        If (CondRefOf (\_OSI, Local0))
                        {
                            If (\_OSI ("Windows 2001"))
                            {
                                Store (0x59, SMIP)
                                Store (0x00, OSFL)
                                Store (0x03, OSFX)
                            }

                            If (\_OSI ("Windows 2006"))
                            {
                                Store (0x59, SMIP)
                                Store (0x00, OSFL)
                                Store (0x04, OSFX)
                            }
                        }
                        Else
                        {
                            Store (0x58, SMIP)
                            Store (0x00, OSFX)
                            Store (0x00, OSFL)
                        }
                    }
                    Else
                    {
                        Store (0x57, SMIP)
                        Store (0x02, OSFX)
                        Store (0x02, OSFL)
                    }
                }

                Store (OSFX, OSTY)
                If (LEqual (OSFX, 0x00))
                {
                    Store (0x04, OSTY)
                }

                If (LEqual (OSFX, 0x03))
                {
                    Store (0x05, OSTY)
                }

                If (LEqual (OSFX, 0x04))
                {
                    Store (0x06, OSTY)
                }
            }

            Scope (\)
            {
                Method (OSTP, 0, NotSerialized)
                {
                    If (LEqual (OSFX, 0x01))
                    {
                        Store (0x56, SMIP)
                    }

                    If (LEqual (OSFX, 0x02))
                    {
                        Store (0x57, SMIP)
                    }

                    If (LEqual (OSFX, 0x00))
                    {
                        Store (0x58, SMIP)
                    }

                    If (LEqual (OSFX, 0x03))
                    {
                        Store (0x59, SMIP)
                    }

                    If (LEqual (OSFX, 0x04))
                    {
                        Store (0x59, SMIP)
                    }
                }
            }

            Device (SYSR)
            {
                Name (_HID, EisaId ("PNP0C02"))
                Name (_UID, 0x01)
                Name (_CRS, ResourceTemplate ()
                {
                    IO (Decode16,
                        0x0010,             // Range Minimum
                        0x0010,             // Range Maximum
                        0x01,               // Alignment
                        0x10,               // Length
                        )
                    IO (Decode16,
                        0x0022,             // Range Minimum
                        0x0022,             // Range Maximum
                        0x01,               // Alignment
                        0x1E,               // Length
                        )
                    IO (Decode16,
                        0x0044,             // Range Minimum
                        0x0044,             // Range Maximum
                        0x01,               // Alignment
                        0x1C,               // Length
                        )
                    IO (Decode16,
                        0x0062,             // Range Minimum
                        0x0062,             // Range Maximum
                        0x01,               // Alignment
                        0x02,               // Length
                        )
                    IO (Decode16,
                        0x0065,             // Range Minimum
                        0x0065,             // Range Maximum
                        0x01,               // Alignment
                        0x0B,               // Length
                        )
                    IO (Decode16,
                        0x0074,             // Range Minimum
                        0x0074,             // Range Maximum
                        0x01,               // Alignment
                        0x0C,               // Length
                        )
                    IO (Decode16,
                        0x0091,             // Range Minimum
                        0x0091,             // Range Maximum
                        0x01,               // Alignment
                        0x03,               // Length
                        )
                    IO (Decode16,
                        0x00A2,             // Range Minimum
                        0x00A2,             // Range Maximum
                        0x01,               // Alignment
                        0x1E,               // Length
                        )
                    IO (Decode16,
                        0x00E0,             // Range Minimum
                        0x00E0,             // Range Maximum
                        0x01,               // Alignment
                        0x10,               // Length
                        )
                    IO (Decode16,
                        0x04D0,             // Range Minimum
                        0x04D0,             // Range Maximum
                        0x01,               // Alignment
                        0x02,               // Length
                        )
                })
            }

            Scope (\)
            {
                OperationRegion (WIN1, SystemIO, 0x2E, 0x02)
                Field (WIN1, ByteAcc, NoLock, Preserve)
                {
                    INDP,   8, 
                    DATA,   8
                }

                IndexField (INDP, DATA, ByteAcc, NoLock, Preserve)
                {
                            Offset (0x02), 
                    CFG,    8, 
                            Offset (0x07), 
                    LDN,    8, 
                            Offset (0x20), 
                    IDHI,   8, 
                    IDLO,   8, 
                    POWC,   8, 
                            Offset (0x30), 
                    ACTR,   8, 
                            Offset (0x60), 
                    IOAH,   8, 
                    IOAL,   8, 
                    IO2H,   8, 
                    IO2L,   8, 
                            Offset (0x70), 
                    INTR,   8, 
                            Offset (0x72), 
                    INT1,   8, 
                            Offset (0x74), 
                    DMCH,   8, 
                            Offset (0xE0), 
                    CRE0,   8, 
                    CRE1,   8, 
                    CRE2,   8, 
                    CRE3,   8, 
                    CRE4,   8, 
                            Offset (0xF0), 
                    OPT1,   8, 
                    OPT2,   8, 
                    OPT3,   8, 
                    OPT4,   8, 
                    OPT5,   8, 
                    OPT6,   8, 
                    OPT7,   8, 
                    OPT8,   8, 
                    OPT9,   8, 
                    OPTA,   8
                }

                Method (ENFG, 0, NotSerialized)
                {
                    Store (0x87, INDP)
                    Store (0x87, INDP)
                }

                Method (EXFG, 0, NotSerialized)
                {
                    Store (0xAA, INDP)
                }

                Method (EWBP, 0, NotSerialized)
                {
                    ENFG ()
                    Store (0x0A, LDN)
                    Store (0x00, OPTA)
                    Store (0x00, OPT7)
                    Store (0xFF, OPT4)
                    Store (0xFF, OPT5)
                    Store (CRE0, Local0)
                    Or (Local0, 0x63, Local0)
                    Store (Local0, CRE0)
                    Store (CRE4, Local0)
                    Or (Local0, 0x8C, Local0)
                    Store (Local0, CRE4)
                    Store (ACTR, Local0)
                    Or (Local0, 0x01, Local0)
                    Store (Local0, ACTR)
                    EXFG ()
                }

                Method (DWBP, 0, NotSerialized)
                {
                    ENFG ()
                    Store (0x0A, LDN)
                    Store (0x00, OPTA)
                    Store (0x00, OPT7)
                    Store (0x00, OPT8)
                    Store (0xFF, OPT4)
                    Store (0xFF, OPT5)
                    Store (CRE0, Local0)
                    And (Local0, 0x9C, Local0)
                    Store (Local0, CRE0)
                    Store (CRE4, Local0)
                    And (Local0, 0x73, Local0)
                    Store (Local0, CRE4)
                    Store (ACTR, Local0)
                    And (Local0, 0xFE, Local0)
                    Store (Local0, ACTR)
                    EXFG ()
                }
            }

            OperationRegion (COM1, SystemIO, 0x03F8, 0x08)
            Field (COM1, ByteAcc, NoLock, Preserve)
            {
                P3F8,   8, 
                P3F9,   8, 
                P3FA,   8, 
                P3FB,   8, 
                P3FC,   8, 
                P3FD,   8, 
                P3FE,   8, 
                P3FF,   8
            }

            OperationRegion (COM2, SystemIO, 0x02F8, 0x08)
            Field (COM2, ByteAcc, NoLock, Preserve)
            {
                P2F8,   8, 
                P2F9,   8, 
                P2FA,   8, 
                P2FB,   8, 
                P2FC,   8, 
                P2FD,   8, 
                P2FE,   8, 
                P2FF,   8
            }

            OperationRegion (COM3, SystemIO, 0x03E8, 0x08)
            Field (COM3, ByteAcc, NoLock, Preserve)
            {
                P3E8,   8, 
                P3E9,   8, 
                P3EA,   8, 
                P3EB,   8, 
                P3EC,   8, 
                P3ED,   8, 
                P3EE,   8, 
                P3EF,   8
            }

            OperationRegion (COM4, SystemIO, 0x02E8, 0x08)
            Field (COM4, ByteAcc, NoLock, Preserve)
            {
                P2E8,   8, 
                P2E9,   8, 
                P2EA,   8, 
                P2EB,   8, 
                P2EC,   8, 
                P2ED,   8, 
                P2EE,   8, 
                P2EF,   8
            }

            Method (ICOM, 1, NotSerialized)
            {
                Store (Arg0, Local0)
                If (LEqual (Local0, 0x03F8))
                {
                    Store (P3FD, Local0)
                    Store (P3FD, Local0)
                    Store (0xC3, P3FA)
                    While (LNotEqual (P3FA, 0xC1))
                    {
                        Store (P3FE, Local0)
                    }
                }
                Else
                {
                    If (LEqual (Local0, 0x02F8))
                    {
                        Store (P2FD, Local0)
                        Store (P2FD, Local0)
                        Store (0xC3, P2FA)
                        While (LNotEqual (P2FA, 0xC1))
                        {
                            Store (P2FE, Local0)
                        }
                    }
                    Else
                    {
                        If (LEqual (Local0, 0x03E8))
                        {
                            Store (P3ED, Local0)
                            Store (P3ED, Local0)
                            Store (0xC3, P3EA)
                            While (LNotEqual (P3EA, 0xC1))
                            {
                                Store (P3EE, Local0)
                            }
                        }
                        Else
                        {
                            If (LEqual (Local0, 0x02E8))
                            {
                                Store (P2ED, Local0)
                                Store (P2ED, Local0)
                                Store (0xC3, P2EA)
                                While (LNotEqual (P2EA, 0xC1))
                                {
                                    Store (P2EE, Local0)
                                }
                            }
                        }
                    }
                }
            }

            Device (FDC0)
            {
                Name (_HID, EisaId ("PNP0700"))
                Method (_STA, 0, NotSerialized)
                {
                    ENFG ()
                    Store (Zero, LDN)
                    If (ACTR)
                    {
                        EXFG ()
                        Return (0x0F)
                    }
                    Else
                    {
                        If (LOr (IOAH, IOAL))
                        {
                            EXFG ()
                            Return (0x0D)
                        }
                        Else
                        {
                            EXFG ()
                            Return (0x00)
                        }
                    }
                }

                Method (_DIS, 0, NotSerialized)
                {
                    ENFG ()
                    Store (0x00, LDN)
                    Store (Zero, ACTR)
                    SLDM (DMCH, 0x04)
                    EXFG ()
                    DISD (0x03)
                }

                Method (_CRS, 0, Serialized)
                {
                    Name (BUF0, ResourceTemplate ()
                    {
                        IO (Decode16,
                            0x03F0,             // Range Minimum
                            0x03F0,             // Range Maximum
                            0x01,               // Alignment
                            0x06,               // Length
                            _Y02)
                        IO (Decode16,
                            0x03F7,             // Range Minimum
                            0x03F7,             // Range Maximum
                            0x01,               // Alignment
                            0x01,               // Length
                            )
                        IRQNoFlags ()
                            {6}
                        DMA (Compatibility, NotBusMaster, Transfer8, )
                            {2}
                    })
                    CreateWordField (BUF0, \_SB.PCI0.FDC0._CRS._Y02._MIN, IOLO)
                    CreateByteField (BUF0, 0x03, IOHI)
                    CreateWordField (BUF0, \_SB.PCI0.FDC0._CRS._Y02._MAX, IORL)
                    CreateByteField (BUF0, 0x05, IORH)
                    ENFG ()
                    EXFG ()
                    Return (BUF0)
                }

                Name (_PRS, ResourceTemplate ()
                {
                    StartDependentFnNoPri ()
                    {
                        IO (Decode16,
                            0x03F0,             // Range Minimum
                            0x03F0,             // Range Maximum
                            0x01,               // Alignment
                            0x06,               // Length
                            )
                        IO (Decode16,
                            0x03F7,             // Range Minimum
                            0x03F7,             // Range Maximum
                            0x01,               // Alignment
                            0x01,               // Length
                            )
                        IRQNoFlags ()
                            {6}
                        DMA (Compatibility, NotBusMaster, Transfer8, )
                            {2}
                    }
                    EndDependentFn ()
                })
                Method (_SRS, 1, NotSerialized)
                {
                    CreateByteField (Arg0, 0x02, IOLO)
                    CreateByteField (Arg0, 0x03, IOHI)
                    CreateWordField (Arg0, 0x02, IOAD)
                    CreateWordField (Arg0, 0x19, IRQL)
                    CreateByteField (Arg0, 0x1C, DMAV)
                    ENFG ()
                    Store (Zero, LDN)
                    Store (One, ACTR)
                    SLDM (DMCH, DMCH)
                    EXFG ()
                    CKIO (IOAD, 0x03)
                }
            }

            Device (UAR1)
            {
                Name (_HID, EisaId ("PNP0501"))
                Name (_UID, 0x01)
                Method (_STA, 0, NotSerialized)
                {
                    ENFG ()
                    Store (0x02, LDN)
                    If (ACTR)
                    {
                        EXFG ()
                        Return (0x0F)
                    }
                    Else
                    {
                        If (LOr (IOAH, IOAL))
                        {
                            EXFG ()
                            Return (0x0D)
                        }
                        Else
                        {
                            EXFG ()
                            Return (0x00)
                        }
                    }

                    EXFG ()
                }

                Method (_DIS, 0, NotSerialized)
                {
                    ENFG ()
                    Store (0x02, LDN)
                    Store (Zero, ACTR)
                    EXFG ()
                    DISD (0x00)
                }

                Method (_CRS, 0, Serialized)
                {
                    Name (BUF1, ResourceTemplate ()
                    {
                        IO (Decode16,
                            0x0000,             // Range Minimum
                            0x0000,             // Range Maximum
                            0x01,               // Alignment
                            0x08,               // Length
                            _Y03)
                        IRQNoFlags (_Y04)
                            {}
                    })
                    CreateWordField (BUF1, \_SB.PCI0.UAR1._CRS._Y03._MIN, IOLO)
                    CreateByteField (BUF1, 0x03, IOHI)
                    CreateWordField (BUF1, \_SB.PCI0.UAR1._CRS._Y03._MAX, IORL)
                    CreateByteField (BUF1, 0x05, IORH)
                    CreateWordField (BUF1, \_SB.PCI0.UAR1._CRS._Y04._INT, IRQW)
                    ENFG ()
                    Store (0x02, LDN)
                    Store (IOAL, IOLO)
                    Store (IOAL, IORL)
                    Store (IOAH, IOHI)
                    Store (IOAH, IORH)
                    Store (One, Local0)
                    ShiftLeft (Local0, INTR, IRQW)
                    EXFG ()
                    Return (BUF1)
                }

                Name (_PRS, ResourceTemplate ()
                {
                    StartDependentFnNoPri ()
                    {
                        IO (Decode16,
                            0x03F8,             // Range Minimum
                            0x03F8,             // Range Maximum
                            0x01,               // Alignment
                            0x08,               // Length
                            )
                        IRQNoFlags ()
                            {3,4,5,7,9,10,11,12}
                    }
                    StartDependentFnNoPri ()
                    {
                        IO (Decode16,
                            0x02F8,             // Range Minimum
                            0x02F8,             // Range Maximum
                            0x01,               // Alignment
                            0x08,               // Length
                            )
                        IRQNoFlags ()
                            {3,4,5,7,9,10,11,12}
                    }
                    StartDependentFnNoPri ()
                    {
                        IO (Decode16,
                            0x03E8,             // Range Minimum
                            0x03E8,             // Range Maximum
                            0x01,               // Alignment
                            0x08,               // Length
                            )
                        IRQNoFlags ()
                            {3,4,5,7,9,10,11,12}
                    }
                    StartDependentFnNoPri ()
                    {
                        IO (Decode16,
                            0x02E8,             // Range Minimum
                            0x02E8,             // Range Maximum
                            0x01,               // Alignment
                            0x08,               // Length
                            )
                        IRQNoFlags ()
                            {3,4,5,7,9,10,11,12}
                    }
                    EndDependentFn ()
                })
                Method (_SRS, 1, NotSerialized)
                {
                    CreateByteField (Arg0, 0x02, IOLO)
                    CreateByteField (Arg0, 0x03, IOHI)
                    CreateWordField (Arg0, 0x02, IOAD)
                    CreateWordField (Arg0, 0x09, IRQW)
                    ENFG ()
                    Store (0x02, LDN)
                    Store (One, ACTR)
                    Store (IOLO, IOAL)
                    Store (IOHI, IOAH)
                    FindSetRightBit (IRQW, Local0)
                    Subtract (Local0, 0x01, INTR)
                    EXFG ()
                    CKIO (IOAD, 0x00)
                }
            }

            Device (UAR2)
            {
                Name (_HID, EisaId ("PNP0501"))
                Name (_UID, 0x02)
                Method (_STA, 0, NotSerialized)
                {
                    ENFG ()
                    Store (0x03, LDN)
                    And (OPT2, 0x30, Local0)
                    If (LNotEqual (Local0, 0x10))
                    {
                        If (ACTR)
                        {
                            EXFG ()
                            Return (0x0F)
                        }
                        Else
                        {
                            If (LOr (IOAH, IOAL))
                            {
                                EXFG ()
                                Return (0x0D)
                            }
                            Else
                            {
                                EXFG ()
                                Return (0x00)
                            }
                        }
                    }
                    Else
                    {
                        EXFG ()
                        Return (0x00)
                    }
                }

                Method (_DIS, 0, NotSerialized)
                {
                    ENFG ()
                    Store (0x03, LDN)
                    And (OPT2, 0x38, Local0)
                    If (LEqual (Local0, 0x00))
                    {
                        Store (Zero, ACTR)
                    }

                    EXFG ()
                    DISD (0x01)
                }

                Method (_CRS, 0, Serialized)
                {
                    Name (BUF2, ResourceTemplate ()
                    {
                        IO (Decode16,
                            0x0000,             // Range Minimum
                            0x0000,             // Range Maximum
                            0x01,               // Alignment
                            0x08,               // Length
                            _Y05)
                        IRQNoFlags (_Y06)
                            {4}
                    })
                    CreateWordField (BUF2, \_SB.PCI0.UAR2._CRS._Y05._MIN, IOLO)
                    CreateByteField (BUF2, 0x03, IOHI)
                    CreateWordField (BUF2, \_SB.PCI0.UAR2._CRS._Y05._MAX, IORL)
                    CreateByteField (BUF2, 0x05, IORH)
                    CreateWordField (BUF2, \_SB.PCI0.UAR2._CRS._Y06._INT, IRQW)
                    ENFG ()
                    Store (0x03, LDN)
                    Store (IOAL, IOLO)
                    Store (IOAL, IORL)
                    Store (IOAH, IOHI)
                    Store (IOAH, IORH)
                    Store (One, Local0)
                    ShiftLeft (Local0, INTR, IRQW)
                    EXFG ()
                    Return (BUF2)
                }

                Name (_PRS, ResourceTemplate ()
                {
                    StartDependentFnNoPri ()
                    {
                        IO (Decode16,
                            0x03F8,             // Range Minimum
                            0x03F8,             // Range Maximum
                            0x01,               // Alignment
                            0x08,               // Length
                            )
                        IRQNoFlags ()
                            {3,4,5,7,9,10,11,12}
                    }
                    StartDependentFnNoPri ()
                    {
                        IO (Decode16,
                            0x02F8,             // Range Minimum
                            0x02F8,             // Range Maximum
                            0x01,               // Alignment
                            0x08,               // Length
                            )
                        IRQNoFlags ()
                            {3,4,5,7,9,10,11,12}
                    }
                    StartDependentFnNoPri ()
                    {
                        IO (Decode16,
                            0x03E8,             // Range Minimum
                            0x03E8,             // Range Maximum
                            0x01,               // Alignment
                            0x08,               // Length
                            )
                        IRQNoFlags ()
                            {3,4,5,7,9,10,11,12}
                    }
                    StartDependentFnNoPri ()
                    {
                        IO (Decode16,
                            0x02E8,             // Range Minimum
                            0x02E8,             // Range Maximum
                            0x01,               // Alignment
                            0x08,               // Length
                            )
                        IRQNoFlags ()
                            {3,4,5,7,9,10,11,12}
                    }
                    EndDependentFn ()
                })
                Method (_SRS, 1, NotSerialized)
                {
                    CreateByteField (Arg0, 0x02, IOLO)
                    CreateByteField (Arg0, 0x03, IOHI)
                    CreateWordField (Arg0, 0x02, IOAD)
                    CreateWordField (Arg0, 0x09, IRQW)
                    ENFG ()
                    Store (0x03, LDN)
                    Store (One, ACTR)
                    Store (IOLO, IOAL)
                    Store (IOHI, IOAH)
                    FindSetRightBit (IRQW, Local0)
                    Subtract (Local0, 0x01, INTR)
                    EXFG ()
                    CKIO (IOAD, 0x01)
                }
            }

            Device (IRDA)
            {
                Name (_HID, EisaId ("PNP0510"))
                Method (_STA, 0, NotSerialized)
                {
                    ENFG ()
                    Store (0x03, LDN)
                    And (OPT2, 0x30, Local0)
                    If (LEqual (Local0, 0x10))
                    {
                        If (ACTR)
                        {
                            EXFG ()
                            Return (0x0F)
                        }
                        Else
                        {
                            If (LOr (IOAH, IOAL))
                            {
                                EXFG ()
                                Return (0x0D)
                            }
                            Else
                            {
                                EXFG ()
                                Return (0x00)
                            }
                        }
                    }
                    Else
                    {
                        EXFG ()
                        Return (0x00)
                    }
                }

                Method (_DIS, 0, NotSerialized)
                {
                    If (LEqual (DISE, 0x01))
                    {
                        ENFG ()
                        Store (0x03, LDN)
                        And (OPT2, 0x38, Local0)
                        If (LNotEqual (Local0, 0x00))
                        {
                            Store (Zero, ACTR)
                        }

                        EXFG ()
                        DISD (0x01)
                    }

                    Store (Local0, Local0)
                }

                Method (_CRS, 0, Serialized)
                {
                    Name (BUF4, ResourceTemplate ()
                    {
                        IO (Decode16,
                            0x0000,             // Range Minimum
                            0x0000,             // Range Maximum
                            0x01,               // Alignment
                            0x08,               // Length
                            _Y07)
                        IRQNoFlags (_Y08)
                            {}
                    })
                    CreateWordField (BUF4, \_SB.PCI0.IRDA._CRS._Y07._MIN, IOLO)
                    CreateByteField (BUF4, 0x03, IOHI)
                    CreateWordField (BUF4, \_SB.PCI0.IRDA._CRS._Y07._MAX, IORL)
                    CreateByteField (BUF4, 0x05, IORH)
                    CreateWordField (BUF4, \_SB.PCI0.IRDA._CRS._Y08._INT, IRQW)
                    ENFG ()
                    Store (0x03, LDN)
                    Store (IOAL, IOLO)
                    Store (IOAL, IORL)
                    Store (IOAH, IOHI)
                    Store (IOAH, IORH)
                    ShiftLeft (0x01, INTR, IRQW)
                    EXFG ()
                    Return (BUF4)
                }

                Name (_PRS, ResourceTemplate ()
                {
                    StartDependentFnNoPri ()
                    {
                        IO (Decode16,
                            0x03F8,             // Range Minimum
                            0x03F8,             // Range Maximum
                            0x01,               // Alignment
                            0x08,               // Length
                            )
                        IRQNoFlags ()
                            {3,4,5,7,9,10,11,12}
                    }
                    StartDependentFnNoPri ()
                    {
                        IO (Decode16,
                            0x02F8,             // Range Minimum
                            0x02F8,             // Range Maximum
                            0x01,               // Alignment
                            0x08,               // Length
                            )
                        IRQNoFlags ()
                            {3,4,5,7,9,10,11,12}
                    }
                    StartDependentFnNoPri ()
                    {
                        IO (Decode16,
                            0x03E8,             // Range Minimum
                            0x03E8,             // Range Maximum
                            0x01,               // Alignment
                            0x08,               // Length
                            )
                        IRQNoFlags ()
                            {3,4,5,7,9,10,11,12}
                    }
                    StartDependentFnNoPri ()
                    {
                        IO (Decode16,
                            0x02E8,             // Range Minimum
                            0x02E8,             // Range Maximum
                            0x01,               // Alignment
                            0x08,               // Length
                            )
                        IRQNoFlags ()
                            {3,4,5,7,9,10,11,12}
                    }
                    EndDependentFn ()
                })
                Method (_SRS, 1, NotSerialized)
                {
                    CreateByteField (Arg0, 0x02, IOLO)
                    CreateByteField (Arg0, 0x03, IOHI)
                    CreateWordField (Arg0, 0x02, IOAD)
                    CreateWordField (Arg0, 0x09, IRQW)
                    ENFG ()
                    Store (0x03, LDN)
                    Store (One, ACTR)
                    Store (IOLO, IOAL)
                    Store (IOHI, IOAH)
                    FindSetRightBit (IRQW, Local0)
                    Subtract (Local0, 0x01, INTR)
                    EXFG ()
                    CKIO (IOAD, 0x01)
                }
            }

            Device (LPT1)
            {
                Name (_HID, EisaId ("PNP0400"))
                Method (_STA, 0, NotSerialized)
                {
                    ENFG ()
                    Store (0x01, LDN)
                    And (OPT1, 0x02, Local0)
                    If (LNotEqual (Local0, 0x02))
                    {
                        If (ACTR)
                        {
                            EXFG ()
                            Return (0x0F)
                        }
                        Else
                        {
                            If (LOr (IOAH, IOAL))
                            {
                                EXFG ()
                                Return (0x0D)
                            }
                            Else
                            {
                                EXFG ()
                                Return (0x00)
                            }
                        }
                    }
                    Else
                    {
                        EXFG ()
                        Return (0x00)
                    }
                }

                Method (_DIS, 0, NotSerialized)
                {
                    ENFG ()
                    Store (0x01, LDN)
                    Store (Zero, ACTR)
                    EXFG ()
                    DISD (0x02)
                }

                Method (_CRS, 0, Serialized)
                {
                    Name (BUF5, ResourceTemplate ()
                    {
                        IO (Decode16,
                            0x0000,             // Range Minimum
                            0x0000,             // Range Maximum
                            0x01,               // Alignment
                            0x08,               // Length
                            _Y09)
                        IO (Decode16,
                            0x0000,             // Range Minimum
                            0x0000,             // Range Maximum
                            0x01,               // Alignment
                            0x04,               // Length
                            _Y0A)
                        IRQNoFlags (_Y0B)
                            {}
                    })
                    CreateWordField (BUF5, \_SB.PCI0.LPT1._CRS._Y09._MIN, IOLO)
                    CreateByteField (BUF5, 0x03, IOHI)
                    CreateWordField (BUF5, \_SB.PCI0.LPT1._CRS._Y09._MAX, IORL)
                    CreateByteField (BUF5, 0x05, IORH)
                    CreateByteField (BUF5, \_SB.PCI0.LPT1._CRS._Y09._LEN, IOLE)
                    CreateWordField (BUF5, \_SB.PCI0.LPT1._CRS._Y0A._MIN, IO21)
                    CreateByteField (BUF5, 0x0B, IO22)
                    CreateWordField (BUF5, \_SB.PCI0.LPT1._CRS._Y0A._MAX, IO23)
                    CreateByteField (BUF5, 0x0D, IO24)
                    CreateWordField (BUF5, \_SB.PCI0.LPT1._CRS._Y0B._INT, IRQW)
                    ENFG ()
                    Store (0x01, LDN)
                    Store (IOAL, IOLO)
                    Store (IOLO, IORL)
                    Store (IOAH, IOHI)
                    Store (IOHI, IORH)
                    Store (IOAL, IO21)
                    Store (IOAL, IO23)
                    Add (IOAH, 0x04, IO22)
                    Add (IOAH, 0x04, IO24)
                    If (LEqual (IOLO, 0xBC))
                    {
                        Store (0x04, IOLE)
                    }
                    Else
                    {
                        Store (0x08, IOLE)
                    }

                    Store (One, Local0)
                    Store (INTR, Local5)
                    ShiftLeft (Local0, Local5, IRQW)
                    Store (One, ACTR)
                    EXFG ()
                    Return (BUF5)
                }

                Name (_PRS, ResourceTemplate ()
                {
                    StartDependentFnNoPri ()
                    {
                        IO (Decode16,
                            0x0378,             // Range Minimum
                            0x0378,             // Range Maximum
                            0x01,               // Alignment
                            0x08,               // Length
                            )
                        IO (Decode16,
                            0x0778,             // Range Minimum
                            0x0778,             // Range Maximum
                            0x01,               // Alignment
                            0x04,               // Length
                            )
                        IRQNoFlags ()
                            {3,4,5,7,9,10,11,12}
                    }
                    StartDependentFnNoPri ()
                    {
                        IO (Decode16,
                            0x0278,             // Range Minimum
                            0x0278,             // Range Maximum
                            0x01,               // Alignment
                            0x08,               // Length
                            )
                        IO (Decode16,
                            0x0678,             // Range Minimum
                            0x0678,             // Range Maximum
                            0x01,               // Alignment
                            0x04,               // Length
                            )
                        IRQNoFlags ()
                            {3,4,5,7,9,10,11,12}
                    }
                    StartDependentFnNoPri ()
                    {
                        IO (Decode16,
                            0x03BC,             // Range Minimum
                            0x03BC,             // Range Maximum
                            0x01,               // Alignment
                            0x04,               // Length
                            )
                        IO (Decode16,
                            0x07BC,             // Range Minimum
                            0x07BC,             // Range Maximum
                            0x01,               // Alignment
                            0x04,               // Length
                            )
                        IRQNoFlags ()
                            {3,4,5,7,9,10,11,12}
                    }
                    EndDependentFn ()
                })
                Method (_SRS, 1, NotSerialized)
                {
                    CreateByteField (Arg0, 0x02, IOLO)
                    CreateByteField (Arg0, 0x03, IOHI)
                    CreateWordField (Arg0, 0x02, IOAD)
                    CreateByteField (Arg0, 0x04, IORL)
                    CreateByteField (Arg0, 0x05, IORH)
                    CreateWordField (Arg0, 0x11, IRQW)
                    ENFG ()
                    Store (0x01, LDN)
                    Store (One, ACTR)
                    Store (IOLO, IOAL)
                    Store (IOHI, IOAH)
                    FindSetLeftBit (IRQW, Local0)
                    Subtract (Local0, 0x01, Local0)
                    Store (Local0, INTR)
                    EXFG ()
                    CKIO (IOAD, 0x02)
                }
            }

            Device (ECP1)
            {
                Name (_HID, EisaId ("PNP0401"))
                Method (_STA, 0, NotSerialized)
                {
                    ENFG ()
                    Store (0x01, LDN)
                    And (OPT1, 0x02, Local0)
                    If (LEqual (Local0, 0x02))
                    {
                        If (ACTR)
                        {
                            EXFG ()
                            Return (0x0F)
                        }
                        Else
                        {
                            If (LOr (IOAH, IOAL))
                            {
                                EXFG ()
                                Return (0x0D)
                            }
                            Else
                            {
                                EXFG ()
                                Return (0x00)
                            }
                        }
                    }
                    Else
                    {
                        EXFG ()
                        Return (0x00)
                    }
                }

                Method (_DIS, 0, NotSerialized)
                {
                    ENFG ()
                    Store (0x01, LDN)
                    Store (Zero, ACTR)
                    SLDM (DMCH, 0x04)
                    EXFG ()
                    DISD (0x02)
                }

                Method (_CRS, 0, Serialized)
                {
                    Name (BUF6, ResourceTemplate ()
                    {
                        IO (Decode16,
                            0x0000,             // Range Minimum
                            0x0000,             // Range Maximum
                            0x01,               // Alignment
                            0x08,               // Length
                            _Y0C)
                        IO (Decode16,
                            0x0000,             // Range Minimum
                            0x0000,             // Range Maximum
                            0x01,               // Alignment
                            0x04,               // Length
                            _Y0D)
                        IRQNoFlags (_Y0E)
                            {}
                        DMA (Compatibility, NotBusMaster, Transfer8, _Y0F)
                            {}
                    })
                    CreateWordField (BUF6, \_SB.PCI0.ECP1._CRS._Y0C._MIN, IOLO)
                    CreateByteField (BUF6, 0x03, IOHI)
                    CreateWordField (BUF6, \_SB.PCI0.ECP1._CRS._Y0C._MAX, IORL)
                    CreateByteField (BUF6, 0x05, IORH)
                    CreateWordField (BUF6, \_SB.PCI0.ECP1._CRS._Y0D._MIN, IOEL)
                    CreateByteField (BUF6, 0x0B, IOEH)
                    CreateWordField (BUF6, \_SB.PCI0.ECP1._CRS._Y0D._MAX, IOML)
                    CreateByteField (BUF6, 0x0D, IOMH)
                    CreateByteField (BUF6, \_SB.PCI0.ECP1._CRS._Y0C._LEN, IOLE)
                    CreateWordField (BUF6, \_SB.PCI0.ECP1._CRS._Y0E._INT, IRQW)
                    CreateByteField (BUF6, \_SB.PCI0.ECP1._CRS._Y0F._DMA, DMAC)
                    ENFG ()
                    Store (0x01, LDN)
                    Store (One, ACTR)
                    Store (IOAL, Local2)
                    Store (Local2, IOLO)
                    Store (IOAH, Local3)
                    Store (Local3, IOHI)
                    Or (Local3, 0x04, Local3)
                    Store (Local3, IOEH)
                    Store (Local3, IOMH)
                    Store (IOLO, IORL)
                    Store (IOLO, IOEL)
                    Store (IOLO, IOML)
                    Store (IOHI, IORH)
                    If (LEqual (IOLO, 0xBC))
                    {
                        Store (0x04, IOLE)
                    }
                    Else
                    {
                        Store (0x08, IOLE)
                    }

                    Store (One, Local0)
                    Store (INTR, Local5)
                    ShiftLeft (Local0, Local5, IRQW)
                    Store (One, Local0)
                    Store (DMCH, Local5)
                    ShiftLeft (Local0, Local5, DMAC)
                    EXFG ()
                    Return (BUF6)
                }

                Name (_PRS, ResourceTemplate ()
                {
                    StartDependentFnNoPri ()
                    {
                        IO (Decode16,
                            0x0378,             // Range Minimum
                            0x0378,             // Range Maximum
                            0x01,               // Alignment
                            0x08,               // Length
                            )
                        IO (Decode16,
                            0x0778,             // Range Minimum
                            0x0778,             // Range Maximum
                            0x01,               // Alignment
                            0x04,               // Length
                            )
                        IRQNoFlags ()
                            {3,4,5,7,9,10,11,12}
                        DMA (Compatibility, NotBusMaster, Transfer8, )
                            {0,1,3}
                    }
                    StartDependentFnNoPri ()
                    {
                        IO (Decode16,
                            0x0278,             // Range Minimum
                            0x0278,             // Range Maximum
                            0x01,               // Alignment
                            0x08,               // Length
                            )
                        IO (Decode16,
                            0x0678,             // Range Minimum
                            0x0678,             // Range Maximum
                            0x01,               // Alignment
                            0x04,               // Length
                            )
                        IRQNoFlags ()
                            {3,4,5,7,9,10,11,12}
                        DMA (Compatibility, NotBusMaster, Transfer8, )
                            {0,1,3}
                    }
                    StartDependentFnNoPri ()
                    {
                        IO (Decode16,
                            0x03BC,             // Range Minimum
                            0x03BC,             // Range Maximum
                            0x01,               // Alignment
                            0x04,               // Length
                            )
                        IO (Decode16,
                            0x07BC,             // Range Minimum
                            0x07BC,             // Range Maximum
                            0x01,               // Alignment
                            0x04,               // Length
                            )
                        IRQNoFlags ()
                            {3,4,5,7,9,10,11,12}
                        DMA (Compatibility, NotBusMaster, Transfer8, )
                            {0,1,3}
                    }
                    EndDependentFn ()
                })
                Method (_SRS, 1, NotSerialized)
                {
                    CreateByteField (Arg0, 0x02, IOLO)
                    CreateByteField (Arg0, 0x03, IOHI)
                    CreateWordField (Arg0, 0x02, IOAD)
                    CreateWordField (Arg0, 0x11, IRQW)
                    CreateByteField (Arg0, 0x14, DMAC)
                    ENFG ()
                    Store (0x01, LDN)
                    Store (One, ACTR)
                    Store (IOLO, IOAL)
                    Store (IOHI, IOAH)
                    FindSetLeftBit (IRQW, Local0)
                    Subtract (Local0, 0x01, Local0)
                    Store (Local0, INTR)
                    FindSetLeftBit (DMAC, Local1)
                    Store (DMCH, Local0)
                    Subtract (Local1, 0x01, DMCH)
                    SLDM (Local0, DMCH)
                    EXFG ()
                    CKIO (IOAD, 0x02)
                }
            }

            OperationRegion (KBCT, SystemIO, 0x60, 0x05)
            Field (KBCT, ByteAcc, NoLock, Preserve)
            {
                P060,   8, 
                        Offset (0x04), 
                P064,   8
            }

            Device (PS2M)
            {
                Name (_HID, EisaId ("PNP0F13"))
                Method (_STA, 0, NotSerialized)
                {
                    If (LEqual (PS2F, 0x00))
                    {
                        Return (0x0F)
                    }
                    Else
                    {
                        Return (0x00)
                    }
                }

                Method (_CRS, 0, Serialized)
                {
                    Name (BUF1, ResourceTemplate ()
                    {
                        IRQNoFlags ()
                            {12}
                    })
                    Name (BUF2, ResourceTemplate ()
                    {
                        IO (Decode16,
                            0x0060,             // Range Minimum
                            0x0060,             // Range Maximum
                            0x01,               // Alignment
                            0x01,               // Length
                            )
                        IO (Decode16,
                            0x0064,             // Range Minimum
                            0x0064,             // Range Maximum
                            0x01,               // Alignment
                            0x01,               // Length
                            )
                        IRQNoFlags ()
                            {12}
                    })
                    If (LEqual (KBDI, 0x01))
                    {
                        If (LEqual (OSFL, 0x02))
                        {
                            Return (BUF1)
                        }

                        If (LEqual (OSFL, 0x01))
                        {
                            Return (BUF1)
                        }
                        Else
                        {
                            Return (BUF2)
                        }
                    }
                    Else
                    {
                        Return (BUF1)
                    }
                }
            }

            Device (PS2K)
            {
                Name (_HID, EisaId ("PNP0303"))
                Name (_CID, EisaId ("PNP030B"))
                Method (_STA, 0, NotSerialized)
                {
                    If (LEqual (KBDI, 0x01))
                    {
                        Return (0x00)
                    }
                    Else
                    {
                        Return (0x0F)
                    }
                }

                Name (_CRS, ResourceTemplate ()
                {
                    IO (Decode16,
                        0x0060,             // Range Minimum
                        0x0060,             // Range Maximum
                        0x01,               // Alignment
                        0x01,               // Length
                        )
                    IO (Decode16,
                        0x0064,             // Range Minimum
                        0x0064,             // Range Maximum
                        0x01,               // Alignment
                        0x01,               // Length
                        )
                    IRQNoFlags ()
                        {1}
                })
            }

            Device (PSMR)
            {
                Name (_HID, EisaId ("PNP0C02"))
                Name (_UID, 0x03)
                Method (_STA, 0, NotSerialized)
                {
                    If (LEqual (KBDI, 0x00))
                    {
                        Return (0x00)
                    }

                    If (LEqual (PS2F, 0x00))
                    {
                        If (LEqual (OSFL, 0x02))
                        {
                            Return (0x0F)
                        }

                        If (LEqual (OSFL, 0x01))
                        {
                            Return (0x0F)
                        }

                        Return (0x00)
                    }

                    Return (0x00)
                }

                Name (_CRS, ResourceTemplate ()
                {
                    IO (Decode16,
                        0x0060,             // Range Minimum
                        0x0060,             // Range Maximum
                        0x01,               // Alignment
                        0x01,               // Length
                        )
                    IO (Decode16,
                        0x0064,             // Range Minimum
                        0x0064,             // Range Maximum
                        0x01,               // Alignment
                        0x01,               // Length
                        )
                })
            }

            Scope (\)
            {
                Method (SALD, 1, NotSerialized)
                {
                    If (LEqual (Arg0, 0x00))
                    {
                        Store (0x00, Local0)
                    }

                    If (LEqual (Arg0, 0x01))
                    {
                        Store (0x80, Local0)
                    }

                    If (LEqual (Arg0, 0x03))
                    {
                        Store (0xC0, Local0)
                    }

                    If (LEqual (Arg0, 0x04))
                    {
                        Store (0x40, Local0)
                    }

                    If (LEqual (Arg0, 0x05))
                    {
                        Store (0x40, Local0)
                    }

                    SLED (Local0)
                }
            }

            Scope (\)
            {
                Method (SLED, 1, NotSerialized)
                {
                    ENFG ()
                    Store (0x09, LDN)
                    And (OPT4, 0x3F, Local0)
                    Or (Local0, Arg0, OPT4)
                    EXFG ()
                }
            }

            Method (\_SB.PCI0.PS2M._PRW, 0, NotSerialized)
            {
                Return (Package (0x02)
                {
                    0x03, 
                    0x05
                })
            }

            Method (\_SB.PCI0.PS2K._PRW, 0, NotSerialized)
            {
                Return (Package (0x02)
                {
                    0x03, 
                    0x05
                })
            }

            Method (_PRW, 0, NotSerialized)
            {
                Return (Package (0x02)
                {
                    0x04, 
                    0x05
                })
            }
        }

        Device (MEM)
        {
            Name (_HID, EisaId ("PNP0C01"))
            Method (_CRS, 0, Serialized)
            {
                Name (BUF0, ResourceTemplate ()
                {
                    Memory32Fixed (ReadOnly,
                        0x000F0000,         // Address Base
                        0x00010000,         // Address Length
                        )
                    Memory32Fixed (ReadWrite,
                        0x00000000,         // Address Base
                        0x00200000,         // Address Length
                        _Y11)
                    Memory32Fixed (ReadWrite,
                        0xFED00000,         // Address Base
                        0x00000100,         // Address Length
                        )
                    Memory32Fixed (ReadWrite,
                        0x00000000,         // Address Base
                        0x00010000,         // Address Length
                        _Y10)
                    Memory32Fixed (ReadWrite,
                        0xFFFF0000,         // Address Base
                        0x00010000,         // Address Length
                        )
                    Memory32Fixed (ReadWrite,
                        0x00000000,         // Address Base
                        0x000A0000,         // Address Length
                        )
                    Memory32Fixed (ReadWrite,
                        0x00100000,         // Address Base
                        0x00000000,         // Address Length
                        _Y12)
                    Memory32Fixed (ReadWrite,
                        0xFEC00000,         // Address Base
                        0x00001000,         // Address Length
                        )
                    Memory32Fixed (ReadWrite,
                        0xFEE00000,         // Address Base
                        0x00001000,         // Address Length
                        )
                    Memory32Fixed (ReadWrite,
                        0xFFF80000,         // Address Base
                        0x00070000,         // Address Length
                        )
                })
                CreateDWordField (BUF0, \_SB.MEM._CRS._Y10._BAS, ACMM)
                CreateDWordField (BUF0, \_SB.MEM._CRS._Y11._BAS, RMA5)
                CreateDWordField (BUF0, \_SB.MEM._CRS._Y11._LEN, RSS5)
                CreateDWordField (BUF0, \_SB.MEM._CRS._Y12._LEN, EXTM)
                Subtract (AMEM, 0x00100000, EXTM)
                Store (AMEM, ACMM)
                Return (BUF0)
            }
        }
    }
}

