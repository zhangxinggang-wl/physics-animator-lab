import re, io, sys
sys.path.insert(0, '_build')
import importlib.util
spec = importlib.util.spec_from_file_location("b", "_build/build_2009sd25.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
src = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", m.STEPS)
t = src.replace("\\\\","")
for mo in re.finditer(r"\\(?![\s\\])", t):
    print(repr(t[max(0,mo.start()-40):mo.start()+40]))
