import logging
from websocket_server import WebsocketServer
from PIL import Image, ImageOps
import io

from trans_interior import TransInterior

PORT = 5000
HOST = '127.0.0.1'
# logger_setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(' %(module)s -  %(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


def new_client(client, server):
    logger.info('New client {}:{} has joined.'.format(client['address'][0], client['address'][1]))


def client_left(client, server):
    logger.info('Client {}:{} has left.'.format(client['address'][0], client['address'][1]))


def message_received(client, server, message):
    """
    :param client:
    :param server:
    :param message: byte array
    :return:
    """
    global is_processing
    logger.info('Message has been received from {}:{}'.format(client['address'][0], client['address'][1]))

    if is_processing:
        print("NOW PROCESS")
        return

    is_processing = True

    header = message[:6]    # 始め 6byte は data の種類を記述しておく
    d_header = header.decode("ascii")
    print(header)
    contents = message[6:]  # 6byte より後ろは data の内容

    # labels = [黒床, 赤レンガ壁, 白床, 白壁, 木床, 木壁, 海面, 空]
    # /label のときは labels の index を空白で区切って送られてくる(ex. 黒床、白壁の場合は "0 3" が送られてくる)
    if d_header == "/label":
        target_labels = contents.decode("ascii")
        print(target_labels)
        target_labels = target_labels.split(" ")
        target_labels = target_labels[:len(target_labels) - 1]
        translation.set_target_labels(target_labels)
    # cmr00 は左カメラ cmr01は右カメラ
    elif d_header == "/cmr00" or d_header == "/cmr01":
        image = Image.open(io.BytesIO(contents))

        # 処理
        image = ImageOps.flip(image)
        # image = translation.test_translation(image)
        image = translation.trans_interior(image)
        image = ImageOps.flip(image)

        buf = io.BytesIO()
        image.save(buf, "JPEG")
        message[6:] = buf.getvalue()

        server.send_message(client, message)

    is_processing = False
    logger.info('Message has been sent to {}:{}'.format(client['address'][0], client['address'][1]))


# main
if __name__ == "__main__":
    is_processing = False
    translation = TransInterior()

    server = WebsocketServer(port=PORT, host=HOST)
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    server.run_forever()
