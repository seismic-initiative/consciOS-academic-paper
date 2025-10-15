import os


class TraceLogger:
	def __init__(self, path: str, header: list[str]):
		os.makedirs(os.path.dirname(path), exist_ok=True)
		self._fh = open(path, "w", encoding="utf-8")
		self._fh.write(",".join(map(str, header)) + "\n")

	def log_row(self, row: list):
		self._fh.write(",".join(map(str, row)) + "\n")
		self._fh.flush()

	def close(self):
		try:
			self._fh.close()
		except Exception:
			pass


