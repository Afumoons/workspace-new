from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from autonomous_trading_ai.scheduler import main as sched

sched.MANAGED_SYMBOLS = ['BTCUSDc', 'XAGUSDc']
sched.job_research_strategies()
print('rerun_btc_xag done')
