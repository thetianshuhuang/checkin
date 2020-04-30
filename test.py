import uuid
from client import Program

from test_strings import LOREM_IPSUM, SAMPLE_ERROR


USER_TOKEN = "Fgv9KVIZjTvJ5F2cZsxoesimkry-vaWcY9bxrf3oPlV9TbK2zVBgt8XK8BDgdlUW"

p = Program(
    server="http://localhost:8000", user_token=USER_TOKEN,
    name="Test Program @ " + str(uuid.uuid1()),
    desc="Program description; this program does:" + LOREM_IPSUM).start()
st1 = p.subtask(
    name="Test Parent",
    desc="Test description").start()
info = st1.info(
    name="Test Info",
    desc="Info description\n" + LOREM_IPSUM)
warning = st1.warning(
    name="Test Warning",
    desc="Warning metadata and information")
qt = p.subtask(
    name="Queued Task",
    desc="This task is not yet running.")
err = qt.error(
    name="Test Error",
    desc="Error traceback\n" + SAMPLE_ERROR)

input()
st1.done()
input()
qt.start()
input()
qt.done()
p.done()
