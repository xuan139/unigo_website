PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE user_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            password TEXT NOT NULL
        );
INSERT INTO user_info VALUES(1,'User1','user1@example.com','555-0101','scrypt:32768:8:1$Ahyqz4BXXL7Eezk2$273a6e160682688fc0362c2b7b30ae213cb6e8ae6cc49275e6ce02d66979a2d5ad38dd01490133fdf2af40f08b3e3aea46296fa378034b27c6d1f257a00b901a');
INSERT INTO user_info VALUES(2,'User2','user2@example.com','555-0102','scrypt:32768:8:1$P46FuPCxiyMEKIHG$f13f53c325f7083216f379e68bb026463454dfc5a830bc0a81e150c0940e71459de24dbc8ef7e218cebdcc486bdb22552e2967ca440b1cf0f4609203df05ef95');
INSERT INTO user_info VALUES(3,'User3','user3@example.com','555-0103','scrypt:32768:8:1$N7ydG0luQ6WgyNEk$dcbf6fb0e4336dfa3d196c714c22faeccd4d21aefc5ccfa8428542b082e2fa6343c80623736583430e28cc009a0966961f54575265a8b0ff6b5c3ba542e76695');
CREATE TABLE history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            details TEXT,
            FOREIGN KEY (user_id) REFERENCES user_info(id)
        );
INSERT INTO history VALUES(1,1,'Upload File','2025-07-28 20:57:54','Uploaded MyApp_v1.0.app to server');
CREATE TABLE app_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_name TEXT NOT NULL,
            version TEXT NOT NULL,
            build_version TEXT NOT NULL,
            patch TEXT,
            release_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            notes TEXT
        );
INSERT INTO app_versions VALUES(32,'OStation-2.2-2.3.delta','1.0.0','100','macOS','2025-09-13 02:53:59',replace('Initial release.\n\n[File Size: 0.11 MB]','\n',char(10)));
INSERT INTO app_versions VALUES(33,'OStation-2.3.app.zip','1.0.0','100','macOS','2025-09-13 02:54:13',replace('Initial release.\n\n[File Size: 0.17 MB]','\n',char(10)));
INSERT INTO app_versions VALUES(34,'OStation.json','1.0.0','100','macOS','2025-09-13 02:54:23',replace('Initial release.\n\n[File Size: 0.00 MB]','\n',char(10)));
INSERT INTO app_versions VALUES(36,'steam.json','1.0.0','100','macOS','2025-09-13 17:02:06',replace('Initial release.\n\n[File Size: 0.00 MB]','\n',char(10)));
INSERT INTO app_versions VALUES(37,'steampc.json','1.0.0','100','macOS','2025-09-13 17:08:46',replace('Initial release.\n\n[File Size: 0.00 MB]','\n',char(10)));
CREATE TABLE qa_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
INSERT INTO qa_list VALUES(7,'什么是 NVMe SSD？','NVMe 是一种为固态硬盘设计的高速传输协议，相比 SATA SSD 拥有更高的读写速度，特别适合需要快速加载的游戏应用。','2025-08-06 14:43:04');
INSERT INTO qa_list VALUES(8,'如何将 Steam 游戏安装到外部 SSD？','在 Steam 客户端设置中添加外部 SSD 为新的库文件夹，然后在安装游戏时选择该路径即可。','2025-08-06 14:43:04');
INSERT INTO qa_list VALUES(9,'Steam Deck 支持更换 SSD 吗？','是的，Steam Deck 使用 M.2 2230 NVMe 接口的 SSD，可以更换，但需要注意尺寸兼容和数据备份。','2025-08-06 14:43:04');
INSERT INTO qa_list VALUES(10,'SSD 对游戏加载速度有多大提升？','相比传统机械硬盘，SSD 能将游戏加载时间减少一半以上，尤其在大型开放世界游戏中效果显著。','2025-08-06 14:43:04');
INSERT INTO qa_list VALUES(11,'如何迁移 Steam 游戏到新的 SSD？','复制 Steam 库文件夹到新 SSD 后，在 Steam 设置中添加该库路径，然后可以移动或重新识别游戏。','2025-08-06 14:43:04');
INSERT INTO qa_list VALUES(12,'我可以在多个硬盘之间共享 Steam 游戏吗？','可以，Steam 支持多个库位置，只需在设置中添加多个安装目录即可按需选择。','2025-08-06 14:43:04');
INSERT INTO qa_list VALUES(13,'SSD 会影响游戏帧率吗？','不会直接影响帧率，但可以显著提升加载速度和减少卡顿，尤其在读取大量资源时。','2025-08-06 14:43:04');
INSERT INTO qa_list VALUES(14,'如何检查我的 SSD 是否支持 PCIe 4.0？','可通过主板说明书或系统信息工具（如 CrystalDiskInfo）查看接口类型和协议支持情况。','2025-08-06 14:43:04');
INSERT INTO qa_list VALUES(15,'Steam 游戏能否安装到移动硬盘？','可以，但推荐使用 SSD 移动硬盘，否则加载速度和游戏体验可能受到影响。','2025-08-06 14:43:04');
INSERT INTO qa_list VALUES(16,'购买游戏前如何确认是否支持我的 SSD？','一般无需特别担心兼容性，Steam 游戏对硬盘要求较低，只需确保有足够的存储空间即可。','2025-08-06 14:43:04');
CREATE TABLE translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lang_code TEXT NOT NULL,
            trans_key TEXT NOT NULL,
            trans_value TEXT NOT NULL,
            UNIQUE(lang_code, trans_key)
        );
INSERT INTO translations VALUES(1,'en','page_title','OStation - Plug-and-Play Gaming SSD Platform');
INSERT INTO translations VALUES(2,'en','nav_brand','OStation');
INSERT INTO translations VALUES(3,'en','nav_home','Home');
INSERT INTO translations VALUES(4,'en','nav_product','Product');
INSERT INTO translations VALUES(5,'en','nav_updates','Updates');
INSERT INTO translations VALUES(6,'en','nav_guide','Guide');
INSERT INTO translations VALUES(7,'en','nav_faq','FAQ');
INSERT INTO translations VALUES(8,'en','nav_download','Downloads');
INSERT INTO translations VALUES(9,'en','nav_support','Support');
INSERT INTO translations VALUES(10,'en','hero_title','Plug and Play. The Ultimate Gaming SSD Solution.');
INSERT INTO translations VALUES(11,'en','hero_sub','Pre-installed with Steam, Epic, VM Windows11 , drivers, and a full gaming environment. Power up and play instantly.');
INSERT INTO translations VALUES(12,'en','get_started','Get Started');
INSERT INTO translations VALUES(13,'en','features_title','Top 3 Features');
INSERT INTO translations VALUES(14,'en','feature1_title','Plug & Play');
INSERT INTO translations VALUES(15,'en','feature1_desc','Connect the SSD to your Mac and launch without any setup or installation.');
INSERT INTO translations VALUES(16,'en','feature2_title','Gaming Ready');
INSERT INTO translations VALUES(17,'en','feature2_desc','Preloaded with Steam, Epic, runtime libraries, and for most AAA titles.');
INSERT INTO translations VALUES(18,'en','feature3_title','VM Support');
INSERT INTO translations VALUES(19,'en','feature3_desc','Comes with VMware virtual machines so you can launch Windows 11 instantly or DIY Ubuntu or others.');
INSERT INTO translations VALUES(20,'en','product_support_title','Support for Mac');
INSERT INTO translations VALUES(21,'en','product_support_desc','OStation is optimized for MacOS, offering seamless performance across systems so you can play anywhere.');
INSERT INTO translations VALUES(22,'en','product_support_li1','Supports USB-C and Thunderbolt');
INSERT INTO translations VALUES(23,'en','product_support_li2','Compatible with macOS Catalina to Sonoma');
INSERT INTO translations VALUES(24,'en','product_support_li3','Works with M1/M2/M3');
INSERT INTO translations VALUES(25,'en','updates_title','Software Updates');
INSERT INTO translations VALUES(26,'en','update1_version','Version 1.2.3 ');
INSERT INTO translations VALUES(27,'en','update1_desc',replace('• Improved compatibility with macOS Sonoma\n• Fixed virtual machine display bug\n• Added auto-launch tool','\n',char(10)));
INSERT INTO translations VALUES(28,'en','update2_version','Version 1.2.2 ');
INSERT INTO translations VALUES(29,'en','update2_desc',replace('• Added DXVK installer\n• Updated preloaded game libraries','\n',char(10)));
INSERT INTO translations VALUES(30,'en','guide_title','Installation Guide');
INSERT INTO translations VALUES(31,'en','guide_step1_title','Step 1: Plug in the SSD');
INSERT INTO translations VALUES(32,'en','guide_step1_desc','Connect the SSD to your Mac device via USB-C or Thunderbolt.');
INSERT INTO translations VALUES(33,'en','guide_step2_title','Step 2: Launch Toolkit');
INSERT INTO translations VALUES(34,'en','guide_step2_desc','Open the OStation app to initialize game or virtual machine launch.');
INSERT INTO translations VALUES(35,'en','guide_step3_title','Step 3: Start Gaming');
INSERT INTO translations VALUES(36,'en','guide_step3_desc','Enjoy Steam, Epic, or pre-configured games instantly. No setup needed.');
INSERT INTO translations VALUES(37,'en','faq_title','Frequently Asked Questions');
INSERT INTO translations VALUES(38,'en','faq_q1','Why isn''t the SSD recognized on my Mac?');
INSERT INTO translations VALUES(39,'en','faq_a1','Please ensure your system allows external drives in Security & Privacy. Try switching USB ports.');
INSERT INTO translations VALUES(40,'en','faq_q2','Steam doesn''t launch or update properly?');
INSERT INTO translations VALUES(41,'en','faq_a2','Make sure the internet is connected and permissions are granted. Try using our Steam Repair Tool in the Download Center.');
INSERT INTO translations VALUES(42,'en','faq_q3','How do I restore the original SSD environment?');
INSERT INTO translations VALUES(43,'en','faq_a3','Visit the Download Center and get the official restoration image. You may need your SSD serial number.');
INSERT INTO translations VALUES(44,'en','download_title','Download or Purchase Now');
INSERT INTO translations VALUES(45,'en','download_desc','Get the latest toolkit or order the pre-configured SSD package.');
INSERT INTO translations VALUES(46,'en','download_button','Visit Download Center');
INSERT INTO translations VALUES(47,'en','support_title','Product Verification');
INSERT INTO translations VALUES(48,'en','support_label','Enter Your Product Serial Numbers');
INSERT INTO translations VALUES(49,'en','support_button','Verify');
INSERT INTO translations VALUES(50,'en','footer_text','© 2025 OStation | Contact: support@gamessd.com | All rights reserved.');
INSERT INTO translations VALUES(51,'zh','page_title','OStation - 即插即用游戏SSD平台');
INSERT INTO translations VALUES(52,'zh','nav_brand','OStation');
INSERT INTO translations VALUES(53,'zh','nav_home','首页');
INSERT INTO translations VALUES(54,'zh','nav_product','产品');
INSERT INTO translations VALUES(55,'zh','nav_updates','更新');
INSERT INTO translations VALUES(56,'zh','nav_guide','指南');
INSERT INTO translations VALUES(57,'zh','nav_faq','常见问题');
INSERT INTO translations VALUES(58,'zh','nav_download','下载');
INSERT INTO translations VALUES(59,'zh','nav_support','支持');
INSERT INTO translations VALUES(60,'zh','hero_title','即插即玩。终极游戏SSD解决方案。');
INSERT INTO translations VALUES(61,'zh','hero_sub','预装 Steam、Epic、Windows11 虚拟机、驱动程序和完整游戏环境。即开即玩。');
INSERT INTO translations VALUES(62,'zh','get_started','开始使用');
INSERT INTO translations VALUES(63,'zh','features_title','三大核心功能');
INSERT INTO translations VALUES(64,'zh','feature1_title','即插即用');
INSERT INTO translations VALUES(65,'zh','feature1_desc','连接 SSD 到 Mac，无需设置或安装即可启动。');
INSERT INTO translations VALUES(66,'zh','feature2_title','游戏就绪');
INSERT INTO translations VALUES(67,'zh','feature2_desc','预装 Steam、Epic、运行库，支持多数大型游戏。');
INSERT INTO translations VALUES(68,'zh','feature3_title','虚拟机支持');
INSERT INTO translations VALUES(69,'zh','feature3_desc','内置 VMware 虚拟机，支持即时启动 Windows 11 或自定义 Ubuntu 等。');
INSERT INTO translations VALUES(70,'zh','product_support_title','Mac 支持');
INSERT INTO translations VALUES(71,'zh','product_support_desc','OStation 针对 MacOS 优化，提供流畅性能，随时随地游戏。');
INSERT INTO translations VALUES(72,'zh','product_support_li1','支持 USB-C 和 Thunderbolt');
INSERT INTO translations VALUES(73,'zh','product_support_li2','兼容 macOS Catalina 到 Sonoma');
INSERT INTO translations VALUES(74,'zh','product_support_li3','支持 M1/M2/M3 芯片');
INSERT INTO translations VALUES(75,'zh','updates_title','软件更新');
INSERT INTO translations VALUES(76,'zh','update1_version','版本 1.2.3 ');
INSERT INTO translations VALUES(77,'zh','update1_desc',replace('• 改进对 macOS Sonoma 的兼容性\n• 修复虚拟机显示问题\n• 增加自动启动工具','\n',char(10)));
INSERT INTO translations VALUES(78,'zh','update2_version','版本 1.2.2 ');
INSERT INTO translations VALUES(79,'zh','update2_desc',replace('• 新增 DXVK 安装器\n• 更新预装游戏库','\n',char(10)));
INSERT INTO translations VALUES(80,'zh','guide_title','安装指南');
INSERT INTO translations VALUES(81,'zh','guide_step1_title','步骤 1：插入 SSD');
INSERT INTO translations VALUES(82,'zh','guide_step1_desc','通过 USB-C 或 Thunderbolt 连接 SSD 到 Mac。');
INSERT INTO translations VALUES(83,'zh','guide_step2_title','步骤 2：启动工具包');
INSERT INTO translations VALUES(84,'zh','guide_step2_desc','打开 OStation 应用，初始化游戏或虚拟机启动。');
INSERT INTO translations VALUES(85,'zh','guide_step3_title','步骤 3：开始游戏');
INSERT INTO translations VALUES(86,'zh','guide_step3_desc','立即享用 Steam、Epic 或预配置游戏，无需设置。');
INSERT INTO translations VALUES(87,'zh','faq_title','常见问题');
INSERT INTO translations VALUES(88,'zh','faq_q1','为什么我的 Mac 识别不了 SSD？');
INSERT INTO translations VALUES(89,'zh','faq_a1','请确保系统安全与隐私设置允许外接硬盘。尝试更换 USB 端口。');
INSERT INTO translations VALUES(90,'zh','faq_q2','Steam 无法正常启动或更新？');
INSERT INTO translations VALUES(91,'zh','faq_a2','确保网络连接正常并已授予权限。尝试使用下载中心的 Steam 修复工具。');
INSERT INTO translations VALUES(92,'zh','faq_q3','如何恢复 SSD 的原始环境？');
INSERT INTO translations VALUES(93,'zh','faq_a3','访问下载中心获取官方恢复镜像，可能需要 SSD 序列号。');
INSERT INTO translations VALUES(94,'zh','download_title','立即下载或购买');
INSERT INTO translations VALUES(95,'zh','download_desc','获取最新工具包或订购预配置 SSD 套装。');
INSERT INTO translations VALUES(96,'zh','download_button','访问下载中心');
INSERT INTO translations VALUES(97,'zh','support_title','产品验证');
INSERT INTO translations VALUES(98,'zh','support_label','请输入您的产品 Serial Numbers');
INSERT INTO translations VALUES(99,'zh','support_button','验证');
INSERT INTO translations VALUES(100,'zh','footer_text','© 2025 OStation | 联系: support@gamessd.com | 保留所有权利。');
INSERT INTO translations VALUES(101,'zh_tw','page_title','OStation - 即插即用遊戲SSD平台');
INSERT INTO translations VALUES(102,'zh_tw','nav_brand','OStation');
INSERT INTO translations VALUES(103,'zh_tw','nav_home','首頁');
INSERT INTO translations VALUES(104,'zh_tw','nav_product','產品');
INSERT INTO translations VALUES(105,'zh_tw','nav_updates','更新');
INSERT INTO translations VALUES(106,'zh_tw','nav_guide','指南');
INSERT INTO translations VALUES(107,'zh_tw','nav_faq','常見問題');
INSERT INTO translations VALUES(108,'zh_tw','nav_download','下載');
INSERT INTO translations VALUES(109,'zh_tw','nav_support','支援');
INSERT INTO translations VALUES(110,'zh_tw','hero_title','即插即玩。終極遊戲SSD解決方案。');
INSERT INTO translations VALUES(111,'zh_tw','hero_sub','預裝 Steam、Epic、Windows11 虛擬機、驅動程式和完整遊戲環境。即開即玩。');
INSERT INTO translations VALUES(112,'zh_tw','get_started','開始使用');
INSERT INTO translations VALUES(113,'zh_tw','features_title','三大核心功能');
INSERT INTO translations VALUES(114,'zh_tw','feature1_title','即插即用');
INSERT INTO translations VALUES(115,'zh_tw','feature1_desc','連接 SSD 到 Mac，無需設置或安裝即可啟動。');
INSERT INTO translations VALUES(116,'zh_tw','feature2_title','遊戲就緒');
INSERT INTO translations VALUES(117,'zh_tw','feature2_desc','預裝 Steam、Epic、運行庫，支持多數大型遊戲。');
INSERT INTO translations VALUES(118,'zh_tw','feature3_title','虛擬機支持');
INSERT INTO translations VALUES(119,'zh_tw','feature3_desc','內置 VMware 虛擬機，支持即時啟動 Windows 11 或自訂 Ubuntu 等。');
INSERT INTO translations VALUES(120,'zh_tw','product_support_title','Mac 支持');
INSERT INTO translations VALUES(121,'zh_tw','product_support_desc','OStation 針對 MacOS 優化，提供流暢性能，隨時隨地遊戲。');
INSERT INTO translations VALUES(122,'zh_tw','product_support_li1','支持 USB-C 和 Thunderbolt');
INSERT INTO translations VALUES(123,'zh_tw','product_support_li2','相容 macOS Catalina 到 Sonoma');
INSERT INTO translations VALUES(124,'zh_tw','product_support_li3','支持 M1/M2/M3 晶片');
INSERT INTO translations VALUES(125,'zh_tw','updates_title','軟體更新');
INSERT INTO translations VALUES(126,'zh_tw','update1_version','版本 1.2.3 ');
INSERT INTO translations VALUES(127,'zh_tw','update1_desc',replace('• 改善對 macOS Sonoma 的相容性\n• 修復虛擬機顯示問題\n• 新增自動啟動工具','\n',char(10)));
INSERT INTO translations VALUES(128,'zh_tw','update2_version','版本 1.2.2 ');
INSERT INTO translations VALUES(129,'zh_tw','update2_desc',replace('• 新增 DXVK 安裝器\n• 更新預裝遊戲庫','\n',char(10)));
INSERT INTO translations VALUES(130,'zh_tw','guide_title','安裝指南');
INSERT INTO translations VALUES(131,'zh_tw','guide_step1_title','步驟 1：插入 SSD');
INSERT INTO translations VALUES(132,'zh_tw','guide_step1_desc','透過 USB-C 或 Thunderbolt 連接 SSD 到 Mac。');
INSERT INTO translations VALUES(133,'zh_tw','guide_step2_title','步驟 2：啟動工具包');
INSERT INTO translations VALUES(134,'zh_tw','guide_step2_desc','開啟 OStation 應用，初始化遊戲或虛擬機啟動。');
INSERT INTO translations VALUES(135,'zh_tw','guide_step3_title','步驟 3：開始遊戲');
INSERT INTO translations VALUES(136,'zh_tw','guide_step3_desc','立即享用 Steam、Epic 或預配置遊戲，無需設置。');
INSERT INTO translations VALUES(137,'zh_tw','faq_title','常見問題');
INSERT INTO translations VALUES(138,'zh_tw','faq_q1','為什麼我的 Mac 識別不了 SSD？');
INSERT INTO translations VALUES(139,'zh_tw','faq_a1','請確保系統安全與隱私設定允許外接硬碟。嘗試更換 USB 埠。');
INSERT INTO translations VALUES(140,'zh_tw','faq_q2','Steam 無法正常啟動或更新？');
INSERT INTO translations VALUES(141,'zh_tw','faq_a2','確保網路連線正常並已授予權限。嘗試使用下載中心的 Steam 修復工具。');
INSERT INTO translations VALUES(142,'zh_tw','faq_q3','如何恢復 SSD 的原始環境？');
INSERT INTO translations VALUES(143,'zh_tw','faq_a3','訪問下載中心取得官方恢復映像，可能需要 SSD 序號。');
INSERT INTO translations VALUES(144,'zh_tw','download_title','立即下載或購買');
INSERT INTO translations VALUES(145,'zh_tw','download_desc','取得最新工具包或訂購預配置 SSD 套裝。');
INSERT INTO translations VALUES(146,'zh_tw','download_button','訪問下載中心');
INSERT INTO translations VALUES(147,'zh_tw','support_title','產品驗證');
INSERT INTO translations VALUES(148,'zh_tw','support_label','請輸入您的產品 Serial Numbers');
INSERT INTO translations VALUES(149,'zh_tw','support_button','驗證');
INSERT INTO translations VALUES(150,'zh_tw','footer_text','© 2025 OStation | 聯絡: support@gamessd.com | 保留所有權利。');
INSERT INTO translations VALUES(151,'ja','page_title','OStation - プラグアンドプレイのゲームSSDプラットフォーム');
INSERT INTO translations VALUES(152,'ja','nav_brand','OStation');
INSERT INTO translations VALUES(153,'ja','nav_home','ホーム');
INSERT INTO translations VALUES(154,'ja','nav_product','製品');
INSERT INTO translations VALUES(155,'ja','nav_updates','アップデート');
INSERT INTO translations VALUES(156,'ja','nav_guide','ガイド');
INSERT INTO translations VALUES(157,'ja','nav_faq','よくある質問');
INSERT INTO translations VALUES(158,'ja','nav_download','ダウンロード');
INSERT INTO translations VALUES(159,'ja','nav_support','サポート');
INSERT INTO translations VALUES(160,'ja','hero_title','プラグアンドプレイ。究極のゲームSSDソリューション。');
INSERT INTO translations VALUES(161,'ja','hero_sub','Steam、Epic、Windows11仮想マシン、ドライバ、完全なゲーム環境をプリインストール。すぐにプレイ開始。');
INSERT INTO translations VALUES(162,'ja','get_started','始める');
INSERT INTO translations VALUES(163,'ja','features_title','主な3つの機能');
INSERT INTO translations VALUES(164,'ja','feature1_title','プラグアンドプレイ');
INSERT INTO translations VALUES(165,'ja','feature1_desc','SSDをMacに接続し、セットアップ不要で起動。');
INSERT INTO translations VALUES(166,'ja','feature2_title','ゲーム準備完了');
INSERT INTO translations VALUES(167,'ja','feature2_desc','Steam、Epic、ランタイムライブラリ、多くのAAAタイトルをプリロード。');
INSERT INTO translations VALUES(168,'ja','feature3_title','VMサポート');
INSERT INTO translations VALUES(169,'ja','feature3_desc','VMware仮想マシンを搭載し、Windows 11やUbuntuなどを即起動可能。');
INSERT INTO translations VALUES(170,'ja','product_support_title','Mac対応');
INSERT INTO translations VALUES(171,'ja','product_support_desc','OStationはMacOSに最適化されており、どこでもスムーズなパフォーマンスを提供します。');
INSERT INTO translations VALUES(172,'ja','product_support_li1','USB-CおよびThunderbolt対応');
INSERT INTO translations VALUES(173,'ja','product_support_li2','macOS CatalinaからSonomaまで対応');
INSERT INTO translations VALUES(174,'ja','product_support_li3','M1/M2/M3チップ対応');
INSERT INTO translations VALUES(175,'ja','updates_title','ソフトウェアアップデート');
INSERT INTO translations VALUES(176,'ja','update1_version','バージョン 1.2.3 ');
INSERT INTO translations VALUES(177,'ja','update1_desc',replace('• macOS Sonomaとの互換性を改善\n• 仮想マシン表示バグを修正\n• 自動起動ツールを追加','\n',char(10)));
INSERT INTO translations VALUES(178,'ja','update2_version','バージョン 1.2.2 ');
INSERT INTO translations VALUES(179,'ja','update2_desc',replace('• DXVKインストーラーを追加\n• プリロードゲームライブラリを更新','\n',char(10)));
INSERT INTO translations VALUES(180,'ja','guide_title','インストールガイド');
INSERT INTO translations VALUES(181,'ja','guide_step1_title','ステップ1：SSDを接続');
INSERT INTO translations VALUES(182,'ja','guide_step1_desc','USB-CまたはThunderbolt経由でSSDをMacに接続。');
INSERT INTO translations VALUES(183,'ja','guide_step2_title','ステップ2：ツールキットを起動');
INSERT INTO translations VALUES(184,'ja','guide_step2_desc','OStationアプリを開き、ゲームまたは仮想マシンの起動を初期化。');
INSERT INTO translations VALUES(185,'ja','guide_step3_title','ステップ3：ゲーム開始');
INSERT INTO translations VALUES(186,'ja','guide_step3_desc','Steam、Epic、または事前設定済みゲームを即座に楽しめます。設定不要。');
INSERT INTO translations VALUES(187,'ja','faq_title','よくある質問');
INSERT INTO translations VALUES(188,'ja','faq_q1','MacでSSDが認識されないのはなぜですか？');
INSERT INTO translations VALUES(189,'ja','faq_a1','システムのセキュリティとプライバシーで外部ドライブを許可していることを確認してください。USBポートを変更してみてください。');
INSERT INTO translations VALUES(190,'ja','faq_q2','Steamが正しく起動しない、または更新できませんか？');
INSERT INTO translations VALUES(191,'ja','faq_a2','インターネット接続と権限が付与されていることを確認してください。ダウンロードセンターのSteam修復ツールを試してください。');
INSERT INTO translations VALUES(192,'ja','faq_q3','元のSSD環境に戻すには？');
INSERT INTO translations VALUES(193,'ja','faq_a3','ダウンロードセンターにアクセスして公式の復元イメージを入手してください。SSDのシリアル番号が必要な場合があります。');
INSERT INTO translations VALUES(194,'ja','download_title','今すぐダウンロードまたは購入');
INSERT INTO translations VALUES(195,'ja','download_desc','最新のツールキットを取得するか、事前構成済みのSSDパッケージを注文してください。');
INSERT INTO translations VALUES(196,'ja','download_button','ダウンロードセンターにアクセス');
INSERT INTO translations VALUES(197,'ja','support_title','製品認証');
INSERT INTO translations VALUES(198,'ja','support_label','製品Serial Numbersを入力してください');
INSERT INTO translations VALUES(199,'ja','support_button','認証');
INSERT INTO translations VALUES(200,'ja','footer_text','© 2025 OStation | 連絡先: support@gamessd.com | 全著作権所有。');
INSERT INTO translations VALUES(201,'ko','page_title','OStation - 플러그 앤 플레이 게임 SSD 플랫폼');
INSERT INTO translations VALUES(202,'ko','nav_brand','OStation');
INSERT INTO translations VALUES(203,'ko','nav_home','홈');
INSERT INTO translations VALUES(204,'ko','nav_product','제품');
INSERT INTO translations VALUES(205,'ko','nav_updates','업데이트');
INSERT INTO translations VALUES(206,'ko','nav_guide','가이드');
INSERT INTO translations VALUES(207,'ko','nav_faq','자주 묻는 질문');
INSERT INTO translations VALUES(208,'ko','nav_download','다운로드');
INSERT INTO translations VALUES(209,'ko','nav_support','지원');
INSERT INTO translations VALUES(210,'ko','hero_title','플러그 앤 플레이. 궁극의 게임 SSD 솔루션.');
INSERT INTO translations VALUES(211,'ko','hero_sub','Steam, Epic, Windows11 가상 머신, 드라이버, 완전한 게임 환경이 사전 설치되어 있습니다. 즉시 실행 가능.');
INSERT INTO translations VALUES(212,'ko','get_started','시작하기');
INSERT INTO translations VALUES(213,'ko','features_title','주요 3가지 기능');
INSERT INTO translations VALUES(214,'ko','feature1_title','플러그 앤 플레이');
INSERT INTO translations VALUES(215,'ko','feature1_desc','SSD를 Mac에 연결하면 별도 설정 없이 바로 실행됩니다.');
INSERT INTO translations VALUES(216,'ko','feature2_title','게임 준비 완료');
INSERT INTO translations VALUES(217,'ko','feature2_desc','Steam, Epic, 런타임 라이브러리, 대부분 AAA 타이틀 사전 로드.');
INSERT INTO translations VALUES(218,'ko','feature3_title','VM 지원');
INSERT INTO translations VALUES(219,'ko','feature3_desc','VMware 가상 머신 포함, Windows 11 즉시 실행 또는 Ubuntu 등 DIY 가능.');
INSERT INTO translations VALUES(220,'ko','product_support_title','Mac 지원');
INSERT INTO translations VALUES(221,'ko','product_support_desc','OStation은 MacOS에 최적화되어 시스템 전반에 걸쳐 원활한 성능을 제공합니다.');
INSERT INTO translations VALUES(222,'ko','product_support_li1','USB-C 및 Thunderbolt 지원');
INSERT INTO translations VALUES(223,'ko','product_support_li2','macOS Catalina부터 Sonoma까지 호환');
INSERT INTO translations VALUES(224,'ko','product_support_li3','M1/M2/M3 칩과 호환');
INSERT INTO translations VALUES(225,'ko','updates_title','소프트웨어 업데이트');
INSERT INTO translations VALUES(226,'ko','update1_version','버전 1.2.3 ');
INSERT INTO translations VALUES(227,'ko','update1_desc',replace('• macOS Sonoma와 호환성 개선\n• 가상 머신 표시 버그 수정\n• 자동 실행 도구 추가','\n',char(10)));
INSERT INTO translations VALUES(228,'ko','update2_version','버전 1.2.2 ');
INSERT INTO translations VALUES(229,'ko','update2_desc',replace('• DXVK 설치 프로그램 추가\n• 사전 로드 게임 라이브러리 업데이트','\n',char(10)));
INSERT INTO translations VALUES(230,'ko','guide_title','설치 가이드');
INSERT INTO translations VALUES(231,'ko','guide_step1_title','1단계: SSD 연결');
INSERT INTO translations VALUES(232,'ko','guide_step1_desc','USB-C 또는 Thunderbolt를 통해 Mac에 SSD 연결.');
INSERT INTO translations VALUES(233,'ko','guide_step2_title','2단계: 툴킷 실행');
INSERT INTO translations VALUES(234,'ko','guide_step2_desc','OStation 앱을 열어 게임 또는 가상 머신 실행 초기화.');
INSERT INTO translations VALUES(235,'ko','guide_step3_title','3단계: 게임 시작');
INSERT INTO translations VALUES(236,'ko','guide_step3_desc','즉시 Steam, Epic 또는 사전 구성된 게임 즐기기. 설정 불필요.');
INSERT INTO translations VALUES(237,'ko','faq_title','자주 묻는 질문');
INSERT INTO translations VALUES(238,'ko','faq_q1','Mac에서 SSD가 인식되지 않는 이유는 무엇인가요?');
INSERT INTO translations VALUES(239,'ko','faq_a1','시스템 보안 및 개인 정보 보호 설정에서 외장 드라이브를 허용했는지 확인하세요. USB 포트를 변경해 보세요.');
INSERT INTO translations VALUES(240,'ko','faq_q2','Steam이 제대로 실행되거나 업데이트되지 않나요?');
INSERT INTO translations VALUES(241,'ko','faq_a2','인터넷 연결과 권한 부여를 확인하세요. 다운로드 센터의 Steam 복구 도구를 사용해 보세요.');
INSERT INTO translations VALUES(242,'ko','faq_q3','원래 SSD 환경으로 복원하려면 어떻게 하나요?');
INSERT INTO translations VALUES(243,'ko','faq_a3','다운로드 센터를 방문하여 공식 복원 이미지를 받아보세요. SSD 시리얼 번호가 필요할 수 있습니다。');
INSERT INTO translations VALUES(244,'ko','download_title','지금 다운로드 또는 구매');
INSERT INTO translations VALUES(245,'ko','download_desc','최신 툴킷을 받거나 사전 구성된 SSD 패키지를 주문하세요。');
INSERT INTO translations VALUES(246,'ko','download_button','다운로드 센터 방문');
INSERT INTO translations VALUES(247,'ko','support_title','제품 검증');
INSERT INTO translations VALUES(248,'ko','support_label','제품 Serial Numbers를 입력하세요');
INSERT INTO translations VALUES(249,'ko','support_button','검증');
INSERT INTO translations VALUES(250,'ko','footer_text','© 2025 OStation | 문의: support@gamessd.com | 모든 권리 보유。');
INSERT INTO translations VALUES(251,'th','page_title','OStation - แพลตฟอร์ม SSD เกมแบบ Plug-and-Play');
INSERT INTO translations VALUES(252,'th','nav_brand','OStation');
INSERT INTO translations VALUES(253,'th','nav_home','หน้าหลัก');
INSERT INTO translations VALUES(254,'th','nav_product','สินค้า');
INSERT INTO translations VALUES(255,'th','nav_updates','อัปเดต');
INSERT INTO translations VALUES(256,'th','nav_guide','คู่มือ');
INSERT INTO translations VALUES(257,'th','nav_faq','คำถามที่พบบ่อย');
INSERT INTO translations VALUES(258,'th','nav_download','ดาวน์โหลด');
INSERT INTO translations VALUES(259,'th','nav_support','สนับสนุน');
INSERT INTO translations VALUES(260,'th','hero_title','Plug and Play. โซลูชัน SSD เกมที่ดีที่สุด');
INSERT INTO translations VALUES(261,'th','hero_sub','ติดตั้งล่วงหน้าด้วย Steam, Epic, VM Windows11, ไดรเวอร์ และสภาพแวดล้อมเกมเต็มรูปแบบ เปิดเครื่องแล้วเล่นได้ทันที');
INSERT INTO translations VALUES(262,'th','get_started','เริ่มต้นใช้งาน');
INSERT INTO translations VALUES(263,'th','features_title','คุณสมบัติเด่น 3 ข้อ');
INSERT INTO translations VALUES(264,'th','feature1_title','Plug & Play');
INSERT INTO translations VALUES(265,'th','feature1_desc','เชื่อมต่อ SSD เข้ากับ Mac ของคุณแล้วใช้งานได้ทันทีโดยไม่ต้องติดตั้ง');
INSERT INTO translations VALUES(266,'th','feature2_title','พร้อมเล่นเกม');
INSERT INTO translations VALUES(267,'th','feature2_desc','ติดตั้ง Steam, Epic, ไลบรารีรันไทม์ และเกม AAA ส่วนใหญ่ล่วงหน้าแล้ว');
INSERT INTO translations VALUES(268,'th','feature3_title','รองรับ VM');
INSERT INTO translations VALUES(269,'th','feature3_desc','มาพร้อม VMware virtual machines เพื่อให้คุณเปิด Windows 11 ได้ทันที หรือเลือกติดตั้ง Ubuntu หรืออื่น ๆ ได้เอง');
INSERT INTO translations VALUES(270,'th','product_support_title','รองรับสำหรับ Mac');
INSERT INTO translations VALUES(271,'th','product_support_desc','OStation ได้รับการปรับแต่งสำหรับ macOS มอบประสิทธิภาพราบรื่นทุกระบบ ให้คุณเล่นได้ทุกที่');
INSERT INTO translations VALUES(272,'th','product_support_li1','รองรับ USB-C และ Thunderbolt');
INSERT INTO translations VALUES(273,'th','product_support_li2','รองรับ macOS Catalina ถึง Sonoma');
INSERT INTO translations VALUES(274,'th','product_support_li3','ทำงานกับ M1/M2/M3');
INSERT INTO translations VALUES(275,'th','updates_title','อัปเดตซอฟต์แวร์');
INSERT INTO translations VALUES(276,'th','update1_version','เวอร์ชัน 1.2.3');
INSERT INTO translations VALUES(277,'th','update1_desc',replace('• ปรับปรุงความเข้ากันได้กับ macOS Sonoma\n• แก้ไขบั๊กการแสดงผล VM\n• เพิ่มเครื่องมือเปิดอัตโนมัติ','\n',char(10)));
INSERT INTO translations VALUES(278,'th','update2_version','เวอร์ชัน 1.2.2');
INSERT INTO translations VALUES(279,'th','update2_desc',replace('• เพิ่มตัวติดตั้ง DXVK\n• อัปเดตไลบรารีเกมที่ติดตั้งล่วงหน้า','\n',char(10)));
INSERT INTO translations VALUES(280,'th','guide_title','คู่มือติดตั้ง');
INSERT INTO translations VALUES(281,'th','guide_step1_title','ขั้นตอนที่ 1: เสียบ SSD');
INSERT INTO translations VALUES(282,'th','guide_step1_desc','เชื่อมต่อ SSD เข้ากับ Mac ของคุณผ่าน USB-C หรือ Thunderbolt');
INSERT INTO translations VALUES(283,'th','guide_step2_title','ขั้นตอนที่ 2: เปิด Toolkit');
INSERT INTO translations VALUES(284,'th','guide_step2_desc','เปิดแอป OStation เพื่อเริ่มต้นการเล่นเกมหรือ VM');
INSERT INTO translations VALUES(285,'th','guide_step3_title','ขั้นตอนที่ 3: เริ่มเล่นเกม');
INSERT INTO translations VALUES(286,'th','guide_step3_desc','เพลิดเพลินกับ Steam, Epic หรือเกมที่ตั้งค่าล่วงหน้าได้ทันที ไม่ต้องติดตั้ง');
INSERT INTO translations VALUES(287,'th','faq_title','คำถามที่พบบ่อย');
INSERT INTO translations VALUES(288,'th','faq_q1','ทำไม Mac ของฉันไม่ตรวจพบ SSD?');
INSERT INTO translations VALUES(289,'th','faq_a1','โปรดตรวจสอบว่าระบบอนุญาตไดรฟ์ภายนอกใน ความปลอดภัยและความเป็นส่วนตัว แล้วลองเปลี่ยนพอร์ต USB');
INSERT INTO translations VALUES(290,'th','faq_q2','Steam ไม่เปิดหรืออัปเดตอย่างถูกต้อง?');
INSERT INTO translations VALUES(291,'th','faq_a2','ตรวจสอบให้แน่ใจว่าเชื่อมต่ออินเทอร์เน็ตและให้สิทธิ์แล้ว ลองใช้ Steam Repair Tool ที่ศูนย์ดาวน์โหลด');
INSERT INTO translations VALUES(292,'th','faq_q3','ฉันจะกู้คืนสภาพแวดล้อม SSD ดั้งเดิมได้อย่างไร?');
INSERT INTO translations VALUES(293,'th','faq_a3','ไปที่ศูนย์ดาวน์โหลดและรับอิมเมจการกู้คืนอย่างเป็นทางการ คุณอาจต้องใช้หมายเลขประจำเครื่อง SSD ของคุณ');
INSERT INTO translations VALUES(294,'th','download_title','ดาวน์โหลดหรือสั่งซื้อทันที');
INSERT INTO translations VALUES(295,'th','download_desc','รับเครื่องมือเวอร์ชันล่าสุดหรือสั่งซื้อแพ็คเกจ SSD ที่ตั้งค่าล่วงหน้า');
INSERT INTO translations VALUES(296,'th','download_button','เยี่ยมชมศูนย์ดาวน์โหลด');
INSERT INTO translations VALUES(297,'th','support_title','การตรวจสอบผลิตภัณฑ์');
INSERT INTO translations VALUES(298,'th','support_label','กรอกหมายเลขประจำเครื่องผลิตภัณฑ์ของคุณ');
INSERT INTO translations VALUES(299,'th','support_button','ตรวจสอบ');
INSERT INTO translations VALUES(300,'th','footer_text','© 2025 OStation | ติดต่อ: support@gamessd.com | สงวนลิขสิทธิ์ทั้งหมด');
CREATE TABLE forum_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_info(id)
        );
INSERT INTO forum_posts VALUES(1,1,'测试','测试','2025-08-28 15:00:19');
INSERT INTO forum_posts VALUES(2,0,'test','test','2025-08-28 15:08:13');
INSERT INTO forum_posts VALUES(3,0,'Dx12結論',replace(replace('透過 symlink 方式實現最佳，複製整個資料夾會導致使用的容量加倍，而使用symlink 則僅有數kb的設定需要執行。\r\n还是需要完整的steam能运行dx9-dx12的，目前还没完成\r\n','\r',char(13)),'\n',char(10)),'2025-08-28 15:13:27');
INSERT INTO forum_posts VALUES(4,0,'目前乙方已提交甲方內容物',replace(replace('Steam dx10-11-12 (遊戲捷徑已改)\r\nBattle net  – Mac Version\r\nBlue stack\r\nVm Ware win11 （還在修改ui）\r\nOStation','\r',char(13)),'\n',char(10)),'2025-08-28 15:16:00');
INSERT INTO forum_posts VALUES(5,0,'directx12 可玩游戏汇总',replace(replace('Details\r\n劍星體驗版dx12\r\n可以下載\r\n改成dx12 玩起來有點卡\r\nm1 mac air 可以下載，無法玩\r\n33遠征隊\r\n可以下載\r\n藍色steam 改成dx12 \r\n打開就是黑的 過了一會就自己關了\r\nanimal well dx12 (mac air m1)\r\n可以下載\r\n藍色steam 改成dx12 後可以遊戲且順暢\r\n黑悟空\r\n白色 steam wine 可以下載\r\n藍色steam 改成dx12 後可以遊戲且順暢\r\n\r\nmonster hunter wilds\r\n白色 steam wine 可以下載\r\n藍色steam 改成dx12 \r\n打開就是黑的 有報錯過了一會就自己關了\r\nstreet fighter 6 demo\r\n可以下載\r\n藍色steam 改成dx12 可以順暢玩\r\n\r\n    cyberpunk 2077\r\n可以下載\r\n可以玩但沒聲音\r\nhttps://chatgpt.com/share/68ae723c-8adc-800c-bc4e-33a49d498db0\r\n\r\nred dead 2  \r\n可以下載\r\n使用d3dmetal可以打開(一開始是用DXMT但不行）\r\n可以順玩\r\n\r\n       the witcher 3  \r\nd3dmetal\r\n可以下載\r\n可以順玩\r\n\r\n    艾爾登法環  （mac air m4 16gb）\r\nd3dmetal\r\n可以下載\r\n可以順玩\r\n\r\n    gta5 legacy \r\nd3dmetal\r\n可以下載\r\n可以順玩\r\n\r\ngta5 enhanced\r\n可以下載\r\n不能玩 顯示以下\r\n\r\n\r\n\r\nresident evil 4 \r\nd3dmetal\r\n可以下載\r\n可以順玩\r\n\r\nmarvel rivals dx12\r\n可以下載\r\n不能玩，顯示系統過舊，但明明用的是d3dmetal （dx12）\r\n\r\n','\r',char(13)),'\n',char(10)),'2025-08-28 15:16:52');
INSERT INTO forum_posts VALUES(6,0,'劍星體驗版dx12',replace(replace('可以下載\r\n改成dx12 玩起來有點卡\r\nm1 mac air 可以下載，無法玩\r\n','\r',char(13)),'\n',char(10)),'2025-08-28 20:19:24');
CREATE TABLE forum_comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER,
            user_id INTEGER,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES forum_posts(id),
            FOREIGN KEY (user_id) REFERENCES user_info(id)
        );
INSERT INTO forum_comments VALUES(1,2,0,'comment','2025-08-28 15:08:26');
INSERT INTO forum_comments VALUES(2,3,0,'OK looks fine','2025-08-28 15:13:49');
INSERT INTO forum_comments VALUES(3,2,0,replace(replace('家和继续配合James方测试游戏平台\r\n決定使用crossover 25去凌航演示，販售使用symlink 版本，兩種ui會使用一樣的\r\nxuan 确认软件SOW，游戏平台事宜，官网论坛，AI回复功能\r\n官網Domain，官網以及OStation和游戏如何更新 http://unigobot.com\r\n測試vm ware 安裝和更新需要乾淨未安裝過的Mac\r\n預計富動8/29出貨50個\r\ncheck 外殼顏色 （預計8/25or 26到）\r\n先不打包，Rockstar 需要更新，\r\nBatttlenet 可能直接抓Mac版本（熱門遊戲都能玩）\r\n','\r',char(13)),'\n',char(10)),'2025-08-28 15:14:18');
INSERT INTO forum_comments VALUES(4,2,0,replace(replace('家和\r\n裝載symlink 版本steam  已经测试OK\r\nv rising  可以玩  已经测试可以玩\r\nthe witcher 3 没试过  已经测试可以玩','\r',char(13)),'\n',char(10)),'2025-08-28 15:14:47');
INSERT INTO forum_comments VALUES(5,4,0,'收到','2025-08-28 15:22:37');
INSERT INTO forum_comments VALUES(6,5,0,'收到，dx11 可以运行哪些游戏呢','2025-08-28 16:08:35');
CREATE TABLE serial_numbers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            serial TEXT UNIQUE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
INSERT INTO serial_numbers VALUES(110,'0AC3B7D0-0812-39AB-904C-4EF64288FBE1','2025-09-01 20:26:04');
INSERT INTO serial_numbers VALUES(111,'1B23C4D5-6789-123A-456B-789CDE123451','2025-09-01 20:26:04');
INSERT INTO serial_numbers VALUES(112,'ABCDEF12-3456-7890-ABCD-EF1234567891','2025-09-01 20:26:04');
INSERT INTO serial_numbers VALUES(113,'0AC3B7D0-0812-39AB-904C-4EF64288FBE2','2025-09-01 20:26:04');
INSERT INTO serial_numbers VALUES(114,'1B23C4D5-6789-123A-456B-789CDE123452','2025-09-01 20:26:04');
INSERT INTO serial_numbers VALUES(115,'ABCDEF12-3456-7890-ABCD-EF1234567892','2025-09-01 20:26:04');
INSERT INTO serial_numbers VALUES(116,'0AC3B7D0-0812-39AB-904C-4EF64288FBE3','2025-09-01 20:26:04');
INSERT INTO serial_numbers VALUES(117,'1B23C4D5-6789-123A-456B-789CDE123453','2025-09-01 20:26:04');
INSERT INTO serial_numbers VALUES(118,'ABCDEF12-3456-7890-ABCD-EF1234567894','2025-09-01 20:26:04');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('user_info',3);
INSERT INTO sqlite_sequence VALUES('history',1);
INSERT INTO sqlite_sequence VALUES('app_versions',37);
INSERT INTO sqlite_sequence VALUES('qa_list',16);
INSERT INTO sqlite_sequence VALUES('translations',300);
INSERT INTO sqlite_sequence VALUES('forum_posts',6);
INSERT INTO sqlite_sequence VALUES('forum_comments',6);
INSERT INTO sqlite_sequence VALUES('serial_numbers',118);
COMMIT;
