----------------------------------------------------------------------------
-- LuaJIT ARM disassembler module.
--
-- Copyright (C) 2005-2015 Mike Pall. All rights reserved.
-- Released under the MIT license. See Copyright Notice in luajit.h
----------------------------------------------------------------------------
-- This is a helper module used by the LuaJIT machine code dumper module.
--
-- It disassembles most user-mode ARMv7 instructions
-- NYI: Advanced SIMD and VFP instructions.
------------------------------------------------------------------------------

local type = type
local sub, byte, format = string.sub, string.byte, string.format
local match, gmatch, gsub = string.match, string.gmatch, string.gsub
local concat = table.concat
local bit = require("bit")
local band, bor, ror, tohex = bit.band, bit.bor, bit.ror, bit.tohex
local lshift, rshift, arshift = bit.lshift, bit.rshift, bit.arshift

------------------------------------------------------------------------------
-- Opcode maps
------------------------------------------------------------------------------

local map_loadc = {
  shift = 8, mask = 15,
  [10] = {
    shift = 20, mask = 1,
    [0] = {
      shift = 23, mask = 3,
      [0] = "vmovFmDN", "vstmFNdr",
      _ = {
	shift = 21, mask = 1,
	[0] = "vstrFdl",
	{ shift = 16, mask = 15, [13] = "vpushFdr", _ = "vstmdbFNdr", }
      },
    },
    {
      shift = 23, mask = 3,
      [0] = "vmovFDNm",
      { shift = 16, mask = 15, [13] = "vpopFdr", _ = "vldmFNdr", },
      _ = {
	shift = 21, mask = 1,
	[0] = "vldrFdl", "vldmdbFNdr",
      },
    },
  },
  [11] = {
    shift = 20, mask = 1,
    [0] = {
      shift = 23, mask = 3,
      [0] = "vmovGmDN", "vstmGNdr",
      _ = {
	shift = 21, mask = 1,
	[0] = "vstrGdl",
	{ shift = 16, mask = 15, [13] = "vpushGdr", _ = "vstmdbGNdr", }
      },
    },
    {
      shift = 23, mask = 3,
      [0] = "vmovGDNm",
      { shift = 16, mask = 15, [13] = "vpopGdr", _ = "vldmGNdr", },
      _ = {
	shift = 21, mask = 1,
	[0] = "vldrGdl", "vldmdbGNdr",
      },
    },
  },
  _ = {
    shift = 0, mask = 0 -- NYI ldc, mcrr, mrrc.
  },
}

local map_vfps = {
  shift = 6, mask = 0x2c001,
  [0] = "vmlaF.dnm", "vmlsF.dnm",
  [0x04000] = "vnmlsF.dnm", [0x04001] = "vnmlaF.dnm",
  [0x08000] = "vmulF.dnm", [0x08001] = "vnmulF.dnm",
  [0x0c000] = "vaddF.dnm", [0x0c001] = "vsubF.dnm",
  [0x20000] = "vdivF.dnm",
  [0x24000] = "vfnmsF.dnm", [0x24001] = "vfnmaF.dnm",
  [0x28000] = "vfmaF.dnm", [0x28001] = "vfmsF.dnm",
  [0x2c000] = "vmovF.dY",
  [0x2c001] = {
    shift = 7, mask = 0x1e01,
    [0] = "vmovF.dm", "vabsF.dm",
    [0x0200] = "vnegF.dm", [0x0201] = "vsqrtF.dm",
    [0x0800] = "vcmpF.dm", [0x0801] = "vcmpeF.dm",
    [0x0a00] = "vcmpzF.d", [0x0a01] = "vcmpzeF.d",
    [0x0e01] = "vcvtG.dF.m",
    [0x1000] = "vcvt.f32.u32Fdm", [0x1001] = "vcvt.f32.s32Fdm",
    [0x1800] = "vcvtr.u32F.dm", [0x1801] = "vcvt.u32F.dm",
    [0x1a00] = "vcvtr.s32F.dm", [0x1a01] = "vcvt.s32F.dm",
  },
}

local map_vfpd = {
  shift = 6, mask = 0x2c001,
  [0] = "vmlaG.dnm", "vmlsG.dnm",
  [0x04000] = "vnmlsG.dnm", [0x04001] = "vnmlaG.dnm",
  [0x08000] = "vmulG.dnm", [0x08001] = "vnmulG.dnm",
  [0x0c000] = "vaddG.dnm", [0x0c001] = "vsubG.dnm",
  [0x20000] = "vdivG.dnm",
  [0x24000] = "vfnmsG.dnm", [0x24001] = "vfnmaG.dnm",
  [0x28000] = "vfmaG.dnm", [0x28001] = "vfmsG.dnm",
  [0x2c000] = "vmovG.dY",
  [0x2c001] = {
    shift = 7, mask = 0x1e01,
    [0] = "vmovG.dm", "vabsG.dm",
    [0x0200] = "vnegG.dm", [0x0201] = "vsqrtG.dm",
    [0x0800] = "vcmpG.dm", [0x0801] = "vcmpeG.dm",
    [0x0a00] = "vcmpzG.d", [0x0a01] = "vcmpzeG.d",
    [0x0e01] = "vcvtF.dG.m",
    [0x1000] = "vcvt.f64.u32GdFm", [0x1001] = "vcvt.f64.s32GdFm",
    [0x1800] = "vcvtr.u32FdG.m", [0x1801] = "vcvt.u32FdG.m",
    [0x1a00] = "vcvtr.s32FdG.m", [0x1a01] = "vcvt.s32FdG.m",
  },
}

local map_datac = {
  shift = 24, mask = 1,
  [0] = {
    shift = 4, mask = 1,
    [0] = {
      shift = 8, mask = 15,
      [10] = map_vfps,
      [11] = map_vfpd,
      -- NYI cdp, mcr, mrc.
    },
    {
      shift = 8, mask = 15,
      [10] = {
	shift = 20, mask = 15,
	[0] = "vmovFnD", "vmovFDn",
	[14] = "vmsrD",
	[15] = { shift = 12, mask = 15, [15] = "vmrs", _ = "vmrsD", },
      },
    },
  },
  "svcT",
}

local map_loadcu = {
  shift = 0, mask = 0, -- NYI unconditional CP load/store.
}

local map_datacu = {
  shift = 0, mask = 0, -- NYI unconditional CP data.
}

local map_simddata = {
  shift = 0, mask = 0, -- NYI SIMD data.
}

local map_simdload = {
  shift = 0, mask = 0, -- NYI SIMD load/store, preload.
}

local map_preload = {
  shift = 0, mask = 0, -- NYI preload.
}

local map_media = {
  shift = 20, mask = 31,
  [0] = false,
  { --01
    shift = 5, mask = 7,
    [0] = "sadd16DNM", "sasxDNM", "ssaxDNM", "ssub16DNM",
    "sadd8DNM", false, false, "ssub8DNM",
  },
  { --02
    shift = 5, mask = 7,
    [0] = "qadd16DNM", "qasxDNM", "qsaxDNM", "qsub16DNM",
    "qadd8DNM", false, false, "qsub8DNM",
  },
  { --03
    shift = 5, mask = 7,
    [0] = "shadd16DNM", "shasxDNM", "shsaxDNM", "shsub16DNM",
    "shadd8DNM", false, false, "shsub8DNM",
  },
  false,
  { --05
    shift = 5, mask = 7,
    [0] = "uadd16DNM", "uasxDNM", "usaxDNM", "usub16DNM",
    "uadd8DNM", false, false, "usub8DNM",
  },
  { --06
    shift = 5, mask = 7,
    [0] = "uqadd16DNM", "uqasxDNM", "uqsaxDNM", "uqsub16DNM",
    "uqadd8DNM", false, false, "uqsub8DNM",
  },
  { --07
    shift = 5, mask = 7,
    [0] = "uhadd16DNM", "uhasxDNM", "uhsaxDNM", "uhsub16DNM",
    "uhadd8DNM", false, false, "uhsub8DNM",
  },
  { --08
    shift = 5, mask = 7,
    [0] = "pkhbtDNMU", false, "pkhtbDNMU",
    { shift = 16, mask = 15, [15] = "sxtb16DMU", _ = "sxtab16DNMU", },
    "pkhbtDNMU", "selDNM", "pkhtbDNMU",
  },
  false,
  { --0a
    shift = 5, mask = 7,
    [0] = "ssatDxMu", "ssat16DxM", "ssatDxMu",
    { shift = 16, mask = 15, [15] = "sxtbDMU", _ = "sxtabDNMU", },
    "ssatDxMu", false, "ssatDxMu",
  },
  { --0b
    shift = 5, mask = 7,
    [0] = "ssatDxMu", "revDM", "ssatDxMu",
    { shift = 16, mask = 15, [15] = "sxthDMU", _ = "sxtahDNMU", },
    "ssatDxMu", "rev16DM", "ssatDxMu",
  },
  { --0c
    shift = 5, mask = 7,
    [3] = { shift = 16, mask = 15, [15] = "uxtb16DMU", _ = "uxtab16DNMU", },
  },
  false,
  { --0e
    shift = 5, mask = 7,
    [0] = "usatDwMu", "usat16DwM", "usatDwMu",
    { shift = 16, mask = 15, [15] = "uxtbDMU", _ = "uxtabDNMU", },
    "usatDwMu", false, "usatDwMu",
  },
  { --0f
    shift = 5, mask = 7,
    [0] = "usatDwMu", "rbitDM", "usatDwMu",
    { shift = 16, mask = 15, [15] = "uxthDMU", _ = "uxtahDNMU", },
    "usatDwMu", "revshDM", "usatDwMu",
  },
  { --10
    shift = 12, mask = 15,
    [15] = {
      shift = 5, mask = 7,
      "smuadNMS", "smuadxNMS", "smusdNMS", "smusdxNMS",
    },
    _ = {
      shift = 5, mask = 7,
      [0] = "smladNMSD", "smladxNMSD", "smlsdNMSD", "smlsdxNMSD",
    },
  },
  false, false, false,
  { --14
    shift = 5, mask = 7,
    [0] = "smlaldDNMS", "smlaldxDNMS", "smlsldDNMS", "smlsldxDNMS",
  },
  { --15
    shift = 5, mask = 7,
    [0] = { shift = 12, mask = 15, [15] = "smmulNMS", _ = "smmlaNMSD", },
    { shift = 12, mask = 15, [15] = "smmulrNMS", _ = "smmlarNMSD", },
    false, false, false, false,
    "smmlsNMSD", "smmlsrNMSD",
  },
  false, false,
  { --18
    shift = 5, mask = 7,
    [0] = { shift = 12, mask = 15, [15] = "usad8NMS", _ = "usada8NMSD", },
  },
  false,
  { --1a
    shift = 5, mask = 3, [2] = "sbfxDMvw",
  },
  { --1b
    shift = 5, mask = 3, [2] = "sbfxDMvw",
  },
  { --1c
    shift = 5, mask = 3,
    [0] = { shift = 0, mask = 15, [15] = "bfcDvX", _ = "bfiDMvX", },
  },
  { --1d
    shift = 5, mask = 3,
    [0] = { shift = 0, mask = 15, [15] = "bfcDvX", _ = "bfiDMvX", },
  },
  { --1e
    shift = 5, mask = 3, [2] = "ubfxDMvw",
  },
  { --1f
    shift = 5, mask = 3, [2] = "ubfxDMvw",
  },
}

local map_load = {
  shift = 21, mask = 9,
  {
    shift = 20, mask = 5,
    [0] = "strtDL", "ldrtDL", [4] = "strbtDL", [5] = "ldrbtDL",
  },
  _ = {
    shift = 20, mask = 5,
    [0] = "strDL", "ldrDL", [4] = "strbDL", [5] = "ldrbDL",
  }
}

local map_load1 = {
  shift = 4, mask = 1,
  [0] = map_load, map_media,
}

local map_loadm = {
  shift = 20, mask = 1,
  [0] = {
    shift = 23, mask = 3,
    [0] = "stmdaNR", "stmNR",
    { shift = 16, mask = 63, [45] = "pushR", _ = "stmdbNR", }, "stmibNR",
  },
  {
    shift = 23, mask = 3,
    [0] = "ldmdaNR", { shift = 16, mask = 63, [61] = "popR", _ = "ldmNR", },
    "ldmdbNR", "ldmibNR",
  },
}

local map_data = {
  shift = 21, mask = 15,
  [0] = "andDNPs", "eorDNPs", "subDNPs", "rsbDNPs",
  "addDNPs", "adcDNPs", "sbcDNPs", "rscDNPs",
  "tstNP", "teqNP", "cmpNP", "cmnNP",
  "orrDNPs", "movDPs", "bicDNPs", "mvnDPs",
}

local map_mul = {
  shift = 21, mask = 7,
  [0] = "mulNMSs", "mlaNMSDs", "umaalDNMS", "mlsDNMS",
  "umullDNMSs", "umlalDNMSs", "smullDNMSs", "smlalDNMSs",
}

local map_sync = {
  shift = 20, mask = 15, -- NYI: brackets around N. R(D+1) for ldrexd/strexd.
  [0] = "swpDMN", false, false, false,
  "swpbDMN", false, false, false,
  "strexDMN", "ldrexDN", "strexdDN", "ldrexdDN",
  "strexbDMN", "ldrexbDN", "strexhDN", "ldrexhDN",
}
