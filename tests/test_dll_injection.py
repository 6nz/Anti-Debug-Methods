import importlib.machinery
import importlib.util
import sys
import types
import ctypes
from unittest import TestCase, mock

class TestSetProcessMitigationPolicy(TestCase):
    """Tests for Anti-DLL-Injection ``set_process_mitigation_policy`` function.

    Run ``python -m unittest`` from the repository root to execute these tests.
    """

    MODULE_PATH = 'dll-related/Anti-DLL-Injection.py'
    MODULE_NAME = 'anti_dll_module'

    def _load_module(self, setproc_return, last_error):
        """Load the target module with patched ctypes."""
        dummy_kernelbase = types.SimpleNamespace(
            SetProcessMitigationPolicy=lambda *args: setproc_return
        )
        patches = [
            mock.patch('ctypes.windll', new=types.SimpleNamespace(kernelbase=dummy_kernelbase), create=True),
            mock.patch('ctypes.GetLastError', return_value=last_error, create=True),
            mock.patch('ctypes.WinError', side_effect=lambda code: Exception(f'WinError {code}'), create=True),
        ]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)
        loader = importlib.machinery.SourceFileLoader(self.MODULE_NAME, self.MODULE_PATH)
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        sys.modules[self.MODULE_NAME] = module
        loader.exec_module(module)
        return module

    def test_success(self):
        module = self._load_module(setproc_return=1, last_error=0)
        buf = ctypes.c_int(0)
        result = module.set_process_mitigation_policy(1, buf, ctypes.sizeof(buf))
        self.assertEqual(result, (True, None))

    def test_failure(self):
        module = self._load_module(setproc_return=0, last_error=5)
        buf = ctypes.c_int(0)
        success, err = module.set_process_mitigation_policy(1, buf, ctypes.sizeof(buf))
        self.assertFalse(success)
        self.assertIsInstance(err, Exception)
        self.assertIn('WinError 5', str(err))
