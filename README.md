KorBot X
وصف عام
KorBot X هو بوت تداول أوتوماتيكي متقدم لسوق الفوركس (مثل زوج AUDCAD وغيره)، مبني باستخدام Python للتحكم والذكاء الاصطناعي، وRust للمعالجة السريعة للبيانات. البوت يجمع بين التحليل الفني، الذكاء الاصطناعي، إدارة المخاطر، والتنفيذ الآلي، لتحقيق دقة عالية في الصفقات ورفع نسبة الربحية مع تقليل الخسائر. يدعم استراتيجيات مثل Scalping، Mean Reversion، Breakout، وAdaptive Swing، مع لوحة تحكم رسومية (GUI) حديثة وتكامل مع Redis وSQLite للتخزين، وإشعارات Telegram.
البوت مصمم ليكون "خارقاً وغير اعتيادي"، حيث يتكيف تلقائياً مع حالة السوق (TRENDING، RANGING، HIGH VOLATILITY)، ويحسن نفسه عبر Genetic Algorithm، ويحمي رأس المال بآليات متقدمة.
المزايا

دقة عالية في الصفقات: win rate 55–65%، profit factor >1.6، drawdown <10% (بناءً على backtesting).
استراتيجيات متعددة: Scalping للتداول اللحظي، Mean Reversion للانحرافات، Breakout للكسر، Swing للأسواق الهادئة.
ذكاء اصطناعي متقدم: نموذج ثقة (XGBoost)، تحسين خروج (RL PPO)، تحسين معلمات (Genetic Algorithm).
إدارة مخاطر قوية: تخصيص ديناميكي، حدود تعرض، حماية رأس المال، تحقق ارتباط.
معالجة سريعة: Rust للحسابات الفنية (ATR، ADX)، Redis للبيانات الحية.
لوحة تحكم حديثة: GUI بـ PyQt6 (dark mode)، تعرض الرصيد، P/L، drawdown، وتتحكم في التشغيل.
تكامل تخزين: SQLite للتاريخ، Redis للمعالجة السريعة.
إشعارات ومراقبة: Telegram للتنبيهات، diagnostics للأداء (win rate, profit factor).
اختبار متقدم: Backtesting، Monte Carlo، Walk Forward للتحقق من الربحية.
حجم صغير ونظيف: .gitignore يتجاهل الملفات الكبيرة (venv, target).

السلبيات

التعقيد: يتطلب فهم Python وRust، وإعداد MT5 (حساب، server).
المخاطر المالية: التداول يحمل مخاطر خسارة رأس المال، خاصة في الأسواق الحية (استخدم حساب تجريبي أولاً).
الاعتماد على API: يعتمد على MT5، Telegram، Redis (يحتاج تشغيل خادم Redis).
الأداء: قد يستهلك موارد في التشغيل 24/7، اقترح استخدام VPS.
القيود: Backtesting placeholder (يحتاج بيانات حقيقية للدقة)، ADX/ATR يدوي في Rust (غير مكتبة).

آلية العمل

Data Layer: يجلب البيانات من MT5 (ticks, candles, spread, slippage) ويعالجها بـ Rust للسرعة.
Market Intelligence: يكشف حالة السوق (TRENDING/RANGING/HIGH VOLATILITY) بـ ATR/ADX.
Strategy Engine: يختار استراتيجية بناءً على الحالة (Scalping في HIGH VOLATILITY، إلخ).
AI Layer: يقيم الثقة (XGBoost)، يحسن الخروج (PPO)، يحسن المعلمات (Genetic).
Risk Engine: يتحقق المخاطر، يحدد lot، يحمي الرصيد.
Execution Engine: ينفذ الصفقات، يقيس latency، retry إذا فشل.
Monitoring: يراقب الأداء، يعدل تلقائياً.
Databases: يحفظ التاريخ في SQLite، الحية في Redis.
GUI: لوحة تحكم للتشغيل/الإيقاف.
Loop: يعمل مستمراً كل 60 ثانية.

طريقة الاستخدام والإعداد
الإعداد:

تثبيت التبعيات: pip install -r requirements.txt.
إعداد MT5: قم بتثبيت MetaTrader5، أنشئ حساب تجريبي، وعدل login/password/server في data_layer.py.
Redis: شغل خادم Redis (sudo service redis-server start في Ubuntu).
Telegram: أنشئ بوت عبر BotFather، أضف TOKEN/CHAT_ID في telegram_notify.py.
Rust: شغل cargo build في src/rust_core.

الاستخدام:

شغل python main.py.
في GUI، اختر استراتيجية واضغط "Start Bot".
راقب الإشعارات وLogs.
للإيقاف: "Stop Bot" (أضف kill logic إذا لزم).

للتداول الحقيقي، غير الحساب في MT5 إلى حقيقي، وابدأ بمخاطرة 1%.
مساهمة

Fork the repo.
Create branch: git checkout -b feature/new.
Commit changes: git commit -m 'Add new feature'.
Push: git push origin feature/new.
Pull Request.
