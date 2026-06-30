<h1 align="center">富士通 CELSIUS J5012 黑苹果引导 (macOS 15/26)</h1>

<p align="center">
  <strong>基于 Intel 13代 Core i5-13500 + 双 AMD 独显的完美“白苹果级”黑苹果工作站</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/macOS-Tahoe%2026-red.svg" alt="macOS 26">
  <img src="https://img.shields.io/badge/macOS-Sequoia%2015-orange.svg" alt="macOS 15">
  <img src="https://img.shields.io/badge/macOS-Ventura%2013-blue.svg" alt="macOS 13">
  <img src="https://img.shields.io/badge/OpenCore-1.0.x-green.svg" alt="OpenCore Version">
  <img src="https://img.shields.io/badge/Fujitsu-Celsius%20J5012-orange.svg" alt="Celsius">
  <img src="https://img.shields.io/badge/SMBIOS-MacPro7,1-success.svg" alt="SMBIOS">
</p>

<p align="center">
  <a href="README.md">🇨🇳 中文</a> | <a href="README_en.md">🇺🇸 English</a>
</p>

---

## � 项目简介

本项目提供富士通 CELSIUS J5012 工作站运行 macOS 的完整 OpenCore 引导配置（当前底层使用的核心引导版本为 **OpenCore v1.0.x**）。
针对这台**5盘位、双显卡、多网卡**的极客级硬件堆料，我们进行了最底层的驱动重构与优化。目前已完美支持最新的 **macOS 26 (Tahoe)** 和 **macOS 15 (Sequoia)**，同时向下兼容 macOS 13 (Ventura)。系统运行极度稳定，不仅实现了双显卡满血渲染，还攻克了 13代主板在原生 macOS 15+ 上的 SATA 死锁难题。

## �💻 硬件配置 (Hardware Specifications)

| 硬件组件 | 详细型号信息 | 状态 / 备注 |
| :--- | :--- | :--- |
| **处理器 (CPU)** | 13th Gen Intel Core i5-13500 (14核 6P+8E) | ✅ XCPM 睿频完美，已屏蔽无解的 UHD 770 核显 |
| **内存 (RAM)** | 64 GB DDR4 3200 MHz | ✅ 正常识别并全速运行 |
| **主显卡 (GPU 1)** | AMD Radeon RX 5700 XT (8GB) | ✅ Slot-2 满血 x16，Metal 3 支持，硬件编解码全开 |
| **副显卡 (GPU 2)** | AMD Radeon RX 550 (4GB) 蓝宝石 | ✅ Slot-1 x8 带宽，Metal 2 支持，双卡共存无冲突 |
| **有线网络** | Intel I219-V + 扩展 Intel 82576 NS | ✅ 双千兆/多网口原生驱动 |
| **无线/蓝牙** | 博通 BCM43xx (DW1820A / 类似型号) | ✅ AirDrop、接力、通用剪贴板完美 (依赖 OCLP) |
| **固态 (NVMe)** | Samsung 970 EVO Plus 1TB & 500GB | ✅ x4 满速，双盘双系统，建议打入 `NVMeFix.kext` |
| **固态/光驱 (SATA)**| 512GB SSD + 860 EVO 250G + HL-DT-ST 光驱 | ✅ **原生 SATA 通道满血复活**，无 PCI/USB 死锁 |
| **声卡** | 主板自带 + AMD HDMI Audio | ✅ `alcid=69`，各通道输出完美，主副卡音频分离 |

> **💡 双显卡特别说明：** 本机的两张独立显卡中，一张为机箱内置，另一张则是通过主板 PCIe 槽转接 Oculink 接口接入的外接显卡坞（eGPU）实现的，双卡在 macOS 下完美协同工作。

## 🌟 功能兼容性与核心优化

本 EFI 绝非简单的“拼凑版”，在底层驱动和逻辑上进行了“去黑苹果化”的深度调优：

### 工作正常 (Working Perfectly)
- ✅ **双显卡协同架构**：主卡(RX5700XT)负责高负载渲染，副卡(RX550)负责多屏亮机，各自拥有独立的音频通道标签 (`onboard-1` & `onboard-2`)。
- ✅ **无核显完美硬件解码**：机型绑定 `MacPro7,1`，成功将所有视频硬件解码/编码任务（UVD/VCE）强制分配给 AMD 独立显卡，彻底解决核显无解导致的视频软件闪退问题。
- ✅ **SATA 接口满血复活 (macOS 15/26)**：解锁了 `CtlnaAHCIPort` 的内核版本限制，并安全移除了对 `AppleAHCIPort` 的 Block 拦截，完美挂载双 SATA 固态及光驱。
- ✅ **Intel vPro 技术完美兼容**：黑苹果系统的运行与本机支持的 Intel vPro 硬件级管理技术完全不冲突，vPro 的远程管理、KVM 等功能均可正常使用。
- ✅ **睡眠与电源策略**：已通过终端底层切断 `tcpkeepalive`、`powernap`、`womp`、`proximitywake`，休眠极其稳定，告别半夜惊醒或睡死。
- ✅ **冷启动防卡码优化**：将 APFS 的 `SetApfsTrimTimeout` 修改为 `-1`，彻底根除 macOS 15/26 在加载 `libignition` 时因 NVMe 初始化慢引发的死锁卡码难题。
- ✅ **苹果生态**：iCloud、App Store、隔空投送、随航等全部正常。

### 不工作 / 存在缺陷 (Not Working / Flaws)
- ❌ **长时间睡眠死机 (Sleep Death)**：受限于特定硬件架构，短时间休眠可以唤醒，但长时间睡眠必然会导致睡死（唤醒黑屏或直接重启）。建议在系统设置中**完全关闭系统休眠**，此问题大概率无法解决。
- ❌ Intel UHD Graphics 770 核显（自 Intel 11代起，macOS 彻底失去对核显的支持，必须搭配免驱独显）。

## 📸 屏幕截图 (Screenshots)

![Image 1](images/jietu-1782827213067.jpg)
![Image 2](images/jietu-1782827259060.jpg)
![Image 3](images/jietu-1782827282059.jpg)
![Image 4](images/jietu-1782827289975.jpg)
![Image 5](images/jietu-1782827298817.jpg)
![Image 6](images/jietu-1782827309112.jpg)
![Image 7](images/jietu-1782827316836.jpg)
![Image 8](images/jietu-1782827327129.jpg)
![Image 9](images/jietu-1782827340046.jpg)
![Image 10](images/jietu-1782827355515.jpg)
![Image 11](images/jietu-1782827380829.jpg)

## ⚙️ 富士通 BIOS 设置指南 (BIOS Settings)

> **💡 说明：** 富士通作为品牌整机，其 BIOS 开放给用户修改的选项极少。以下仅为您在有限的选项中能修改的**参考建议**。如果您的 BIOS 中找不到某些选项，保持默认即可。

在使用此 EFI 引导之前，请务必开机按 **F2** 进入 BIOS 进行如下配置：

**必须关闭 (Disable / Disabled)：**
- Security -> **Secure Boot** (安全启动)
- Security -> **Intel SGX**
- Advanced -> System Agent (SA) Configuration -> **VT-d** (如果未启用 DisableIoMapper)
- Boot -> **Legacy Boot** (必须纯 UEFI)
- Fast Boot / CSM

**必须开启 (Enable / Enabled)：**
- Advanced -> CPU Configuration -> **Intel Virtualization Technology (VT-x)**
- Advanced -> Devices -> **USB Configuration (所有端口)**
- Advanced -> Devices -> **XHCI Hand-off**
- OS type: Windows 8.1/10 UEFI Mode
- SATA Mode: **AHCI** (极度重要)
- Above 4G decoding (大于4G地址空间解码)

## ⚠️ 故障排除与注意事项 (Troubleshooting & Notes)

1. **OCLP 补丁与冷启动：** 
   为了在 macOS 15/26 上驱动被淘汰的博通网卡，系统禁用了苹果密钥库 (`-applekeystore=disabled`) 并降低了安全等级。偶发的冷启动跑码卡死属于此类补丁的正常副作用，通常**强制热重启一次**即可秒进系统。
2. **隔空投送 (AirDrop) 搜不到：** 
   若“仅限联系人”模式下搜不到设备，请在控制中心切换为“所有人”。或在终端执行以下命令重置哈希池：
   ```bash
   defaults delete com.apple.sharingd AirDropRandomHashUUIDKey1
   defaults delete com.apple.sharingd AirDropRandomHashUUIDKey2
   defaults delete com.apple.sharingd "HashManager-LastDeviceIDHashKey"
   killall sharingd
   ```
3. **NVRAM 重置 (至关重要)：** 
   每次更新 EFI（尤其是修改了 config.plist 中的底层 SATA 或核心驱动逻辑后），**首次引导时务必在 OC 菜单按空格键选择 `Reset NVRAM` 并回车执行**，否则新的驱动策略可能无法生效甚至导致内核崩溃。
4. **三星 NVMe 固态硬盘：**
   当前使用了两根三星 970 EVO Plus。由于其原厂主控与苹果原生驱动的兼容性问题，建议在后期配置中加入并启用 `NVMeFix.kext` 以防止高负载下的 Kernel Panic。

## 🔄 更新日志 (Changelog)

### v2.0 (2026年6月30日)
- **SATA 修复**: 解锁原生 SATA 驱动限制，在 macOS 26 (Tahoe) 下完美识别双 SATA 固态及光驱。
- **冷启动优化**: 将 APFS Trim 超时 (`SetApfsTrimTimeout`) 强制设为 `-1`，优化冷启动速度与稳定性。
- **架构升级**: 确认 RX 5700 XT + RX 550 双显卡混合渲染阵列稳定运行。

### v1.x (2026年6月28日及之前)
- **系统适配**: macOS 26 (Tahoe) / macOS 15 (Sequoia) 初步适配支持。
- **网络修复**: 加入 `IOSkywalkFamily` 与 `AMFIPass` 组合，复活博通网卡。
- **基础框架**: 基于 OpenCore 提供 Ventura 13.x 到最新版 macOS 的兼容方案。

## 👏 致谢 (Credits)

- [Acidanthera](https://github.com/acidanthera) 团队提供卓越的 OpenCore 引导器与各类核心 Kexts。
- 黑苹果社区（Dortania 等）提供的详尽安装指南与排错思路。

---

*免责声明：本项目仅用于技术研究和学习目的。因硬件体质差异，任何人直接套用本配置所导致的数据丢失或硬件损坏，请自行承担后果。请确保您的 macOS 使用符合 Apple 的许可协议。*