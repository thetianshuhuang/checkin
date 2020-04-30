import uuid
import time
from client import Program

from test_strings import LOREM_IPSUM, SAMPLE_ERROR


USER_TOKEN = "UMq5zGrrYO2A6Mml_-9xcZe_cYTIwiMwEQzhJ4SmFzSKxzApT_l_9UjeBkWrXQhH"

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

# input()
st1.done()
# input()
qt.start()

for i in range(10):
    print(i)
    time.sleep(1)
    err = qt.error(
        name="Test Error {}".format(i + 1),
        desc="Error traceback\n" + SAMPLE_ERROR)

# input()
qt.done()
p.done()
